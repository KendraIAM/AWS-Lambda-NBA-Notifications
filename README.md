# AWS Lambda NBA Game Day Notifications

## 📌 Project Overview
This project is an **AWS Lambda-powered notification system** that sends **daily NBA game scores** from yesterday via **Amazon SNS (Simple Notification Service)**. The function fetches real-time NBA data from the **SportsData.io API**, processes the scores, and automatically delivers them via **email or SMS** notifications.

## 🚀 Features
- 🏀 **Daily NBA Score Updates** → Fetches **yesterday's** game scores.
- ⏰ **Automated Execution** → Runs daily using **AWS EventBridge**.
- 📩 **Real-time Notifications** → Delivers game results via **Amazon SNS (email or SMS)**.
- 🕒 **Time Zone Handling** → Converts all game times to **Eastern Time (EST)**.
- 🔍 **Error Handling & Logging** → Logs API responses & execution details in **AWS CloudWatch**.
- 💰 **Low-Cost Serverless Solution** → Uses **AWS Lambda + SNS**, avoiding expensive infrastructure costs.

## ⚙️ Prerequisites
Before deploying the project, ensure you have the following:
- **AWS Account** → Required to deploy AWS Lambda, SNS, and EventBridge.
- **SportsData.io API Key** → Needed to fetch NBA scores.
- **Python 3.x** → Required for running the Lambda function locally.

## 🔧 Technologies Used
- **AWS Lambda** → Runs the serverless Python function.
- **Amazon SNS** → Sends notifications via email or SMS.
- **AWS EventBridge** → Triggers the function daily.
- **AWS CloudWatch** → Logs execution and errors.
- **SportsData.io API** → Provides real-time NBA game data.
- **Python** → Core language for Lambda function.
- **pytz** → Handles time zone conversions.

## 📜 How It Works
### **Technical Architecture**
Below is a VERY simple diagram of the technical architecture:
'''
             +----------------------+
             |   AWS EventBridge     |
             |  (Daily Trigger)      |
             +---------+------------+
                       |
                       v
             +----------------------+
             |   AWS Lambda         |
             | (Fetch NBA Data)      |
             +----+---------+-------+
                  |         |
                  |         v
                  |   +----------------------+
                  |   | SportsData.io API    |
                  |   | (NBA Scores)         |
                  |   +----------------------+
                  |         |
                  |         v
                  |   +----------------------+
                  |   |  AWS CloudWatch      |
                  |   | (Logging & Monitoring)|
                  |   +----------------------+
                  v
        +----------------------+
        |   Amazon SNS         |
        |  (Notification)      |
        +---------+------------+
                  |
                  v
        +----------------------+
        |  Subscribers         |
        | (Email / SMS)        |
        +----------------------+
'''

1. **AWS EventBridge** triggers the **AWS Lambda function** daily.
2. The function **fetches yesterday’s NBA scores** from **SportsData.io**.
3. Game data is formatted and converted to **Eastern Time (EST)**.
4. The results are **published to an SNS Topic**.
5. **Subscribers receive NBA score notifications** via email or SMS.

## 📂 File Structure
```
📂 aws-lambda-nba-notifications/
├── src/                # Source code folder
│   ├── lambda_function.py  # AWS Lambda function
│   ├── requirements.txt    # Dependencies (if applicable)
├── template.yaml      # AWS SAM Template for deployment
└── README.md          # Project documentation
```

## 📝 Usage & Deployment
1. **Deploy to AWS Lambda**.
2. **Set environment variables**:
   - `NBA_API_KEY` → Your SportsData.io API Key.
   - `SNS_TOPIC_ARN` → Your Amazon SNS Topic ARN.
3. **Schedule execution via AWS EventBridge**.
4. **Subscribe to SNS topic** to receive notifications.

## 📌 Future Enhancements
- 📊 **Add Team-Specific Subscriptions** → Let users pick their favorite teams.
- 📅 **Expand to Other Sports Leagues** → NFL, MLB, etc.
- 📈 **Store Game Data in AWS DynamoDB** → For historical analysis.

## 👨🏾‍💻 Author
Developed as part of the **#DevOpsAllStarsChallenge** to improve cloud and DevOps skills. 🚀

## 📜 License
This project is licensed under the **MIT License**.

---
✅ **Built with AWS, Python & SportsData.io** | 🏀 Stay Updated with NBA Scores!

