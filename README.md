# 🏢 Smart Visitor Log System

A serverless, cloud-native visitor management system that automates registration, generates QR codes, stores records securely, and sends real-time email alerts — built entirely on AWS.

![AWS](https://img.shields.io/badge/AWS-Serverless-orange) 
![Lambda](https://img.shields.io/badge/Lambda-Python3.12-yellow) 
![DynamoDB](https://img.shields.io/badge/DynamoDB-NoSQL-blue) 
![API Gateway](https://img.shields.io/badge/API-Gateway-green) 
![SNS](https://img.shields.io/badge/SNS-Alerts-red)

---

## 📌 Problem Statement

Traditional visitor management systems are:
- Paper-based, inefficient, and insecure
- Unable to provide real-time tracking
- Lacking duplicate detection and validation
- Not scalable for modern organizations

---

## ✅ Solution

A fully serverless visitor management system that:
1. **Registers** visitors via a smart web form with real-time validation
2. **Generates** a unique QR code and visitor ID instantly
3. **Stores** records securely in DynamoDB with timestamps
4. **Detects** duplicate check-ins on the same day
5. **Alerts** staff via email on every new visitor check-in
6. **Monitors** system health with CloudWatch alarms

---

## 🏗️ Architecture

```
Visitor opens web form (S3 hosted)
        ↓
Fills form + clicks Check In
        ↓
API Gateway (POST /visitor)
        ↓
Lambda Function
  ├── Validates input
  ├── Checks duplicate (DynamoDB query)
  ├── Saves record to DynamoDB
  └── Sends SNS email alert
        ↓
Response → QR Code generated on screen
        ↓
CloudWatch Alarm watches for Lambda errors
```

---

## 🛠️ AWS Services Used

- **Amazon S3**: Hosts the frontend as a static website  
- **API Gateway**: Exposes secure REST endpoint for form submission  
- **AWS Lambda**: Serverless backend — handles all business logic  
- **Amazon DynamoDB**: NoSQL database — stores all visitor records  
- **Amazon SNS**: Sends real-time email alerts on check-in  
- **CloudWatch Alarm**: Monitors Lambda errors and notifies team  
- **IAM**: Least privilege custom policy 

---

## 🌟 Key Features

- **Smart Validation** — Name, email, phone, purpose all validated before submission
- **Duplicate Detection** — Same visitor can't check in twice on the same day
- **QR Code Generation** — Unique QR code per visitor for quick verification
- **Unique Visitor ID** — Auto-generated ID in format `VIS-YYYYMMDD-XXXX`
- **Real-time Alerts** — Staff notified instantly via email on every check-in
- **Error Monitoring** — CloudWatch alarm triggers if system encounters errors
- **Least Privilege IAM** — Custom policy with only required permissions

---

## 📧 Sample Alert Email

```
Subject: 🏢 New Visitor Check-in!

New visitor has checked in!

Visitor ID: VIS-20260512-4821
Name: Prateek Kumar Singh
Email: prateek@example.com
Phone: 9999999999
Purpose: Meeting
Visiting: Engineering Team
Time: 12/05/2026, 02:30:00 PM
```

---

## 📁 Project Structure

```
smart-visitor-log-system/
├── frontend/
│   └── index.html            # Complete frontend — form, QR, summary
├── lambda/
│   └── visitor_log_handler.py  # Backend logic
└── README.md
```

---

## ⚙️ Setup Instructions

### Prerequisites
- AWS Account
- GitHub account
- Basic understanding of AWS Console

### Step 1 — DynamoDB Table
1. Go to DynamoDB → Create table
2. Table name: `VisitorLogs`
3. Partition key: `visitorId` (String)
4. Create GSI: `email-date-index` with `email` (partition) + `date` (sort)

### Step 2 — SNS Topic
1. SNS → Create topic → Standard → Name: `visitor-alerts`
2. Create subscription → Email → your email
3. Confirm from inbox

### Step 3 — Lambda Function
1. Create function → Name: `visitor-log-handler` → Python 3.12
2. Upload `lambda/visitor_log_handler.py`
3. Update `SNS_TOPIC_ARN` with your ARN
4. Attach custom IAM policy with DynamoDB + SNS permissions
5. Deploy

### Step 4 — API Gateway
1. Create HTTP API → Name: `visitor-log-api`
2. Add route: `POST /visitor` → Lambda integration
3. Enable CORS
4. Deploy to `$default` stage

### Step 5 — Frontend on S3
1. Create S3 bucket → enable static website hosting
2. Update `API_URL` in `index.html` with your API Gateway URL
3. Upload `index.html` → make public
4. Open S3 website URL in browser

### Step 6 — CloudWatch Alarm
1. CloudWatch → Create alarm → Lambda → Errors metric
2. Threshold: >= 1 error in 5 minutes
3. Notification: `visitor-alerts` SNS topic
4. Name: `visitor-log-errors`

---

## 💰 Cost

- **S3 static hosting**: Free tier  
- **API Gateway**: Free tier — 1M calls/month  
- **Lambda**: Free tier — 1M requests/month  
- **DynamoDB**: Free tier — 25GB storage  
- **SNS**: Free tier — 1000 emails/month  
- **CloudWatch**: Free tier  

**Total estimated cost: $0 within free tier limits**

---

## 🔒 Security Features

- API Gateway with CORS protection
- Lambda input sanitization
- IAM least privilege — no wildcard permissions
- DynamoDB duplicate check prevents spam entries

---

## 👤 Author

**Prateek Kumar Singh**
- GitHub: [@Prat-1234](https://github.com/Prat-1234)
- Project: Smart Visitor Log System
