import os
import json
import urllib.request
import boto3
from datetime import datetime, timedelta, timezone
import pytz  # Handling time zones

def format_game_data(game):
    status = game.get("Status", "Unknown")
    away_team = game.get("AwayTeam", "Unknown")
    home_team = game.get("HomeTeam", "Unknown")
    final_score = f"{game.get('AwayTeamScore', 'N/A')}-{game.get('HomeTeamScore', 'N/A')}"
    start_time_utc = game.get("DateTime", "Unknown")
    channel = game.get("Channel", "Unknown")

    # Convert Start Time to EST
    if start_time_utc != "Unknown":
        try:
            utc_dt = datetime.strptime(start_time_utc, "%Y-%m-%dT%H:%M:%S")
            utc_dt = utc_dt.replace(tzinfo=timezone.utc)
            est_dt = utc_dt.astimezone(pytz.timezone("America/New_York"))
            start_time_est = est_dt.strftime("%Y-%m-%d %I:%M %p EST")
        except ValueError:
            start_time_est = "Invalid Time Format"
    else:
        start_time_est = "Unknown"

    # Format quarter scores
    quarters = game.get("Quarters", [])
    quarter_scores = ', '.join([f"Q{q['Number']}: {q.get('AwayScore', 'N/A')}-{q.get('HomeScore', 'N/A')}" for q in quarters])

    if status == "Final":
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Final Score: {final_score}\n"
            f"Start Time (EST): {start_time_est}\n"
            f"Channel: {channel}\n"
            f"Quarter Scores: {quarter_scores}\n"
        )
    elif status == "InProgress":
        last_play = game.get("LastPlay", "N/A")
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Current Score: {final_score}\n"
            f"Last Play: {last_play}\n"
            f"Channel: {channel}\n"
        )
    elif status == "Scheduled":
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Start Time (EST): {start_time_est}\n"
            f"Channel: {channel}\n"
        )
    else:
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Details are unavailable at the moment.\n"
        )

def lambda_handler(event, context):
    api_key = os.getenv("NBA_API_KEY")
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")
    sns_client = boto3.client("sns")

    if not api_key:
        print("Error: NBA_API_KEY is missing from environment variables.")
        return {"statusCode": 400, "body": "Error: Missing NBA_API_KEY"}

    # Get the current date in Eastern Time (EST) and subtract one day
    est_now = datetime.now(pytz.timezone("America/New_York"))
    yesterday_date = (est_now - timedelta(days=1)).strftime("%Y-%m-%d")  # Always fetch yesterday's games

    print(f"Fetching games for date (EST): {yesterday_date}")  # Debugging log

    # Corrected API URL with yesterday's date
    api_url = f"https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/{yesterday_date}?key={api_key}"
    
    try:
        with urllib.request.urlopen(api_url, timeout=5) as response:  # Added 5-second timeout
            if response.status != 200:
                print(f"API Error: Received HTTP {response.status}")
                return {"statusCode": response.status, "body": f"API Error: HTTP {response.status}"}

            data = json.loads(response.read().decode())
            print(json.dumps(data, indent=4))  # Debugging: log the raw data
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        return {"statusCode": e.code, "body": f"HTTP Error: {e.reason}"}
    except urllib.error.URLError as e:
        print(f"Network Error: {e.reason}")
        return {"statusCode": 500, "body": f"Network Error: {e.reason}"}
    except json.JSONDecodeError:
        print("Error: Invalid JSON response from API")
        return {"statusCode": 500, "body": "Error: Invalid JSON response from API"}

    if not data or not isinstance(data, list):
        print("Warning: No game data received from API.")
        return {"statusCode": 200, "body": "No games available for today."}

    messages = [format_game_data(game) for game in data]
    final_message = "\n---\n".join(messages) if messages else "No games available for today."

    try:
        sns_response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=final_message,
            Subject="NBA Game Updates"
        )
        print(f"SNS Publish Response: {sns_response}")  # Log SNS response
    except Exception as e:
        print(f"Error publishing to SNS: {e}")
        return {"statusCode": 500, "body": f"Error publishing to SNS: {str(e)}"}

    return {"statusCode": 200, "body": "Data processed and sent to SNS"}
