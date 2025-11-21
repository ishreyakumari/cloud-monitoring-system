# Cloud Log Monitoring System

A complete cloud-based log monitoring and analysis system built with React, Flask, Google Cloud Platform, and Firestore.

## Team Members
- Shreya Kumari (net id - fd6317)
- Richa Sapre (net id - ee9498)

## Architecture

```
Client Apps → Cloud Logging → Pub/Sub → Cloud Function → Firestore
                                                              ↓
Frontend (React) ← REST API (Flask) ← ← ← ← ← ← ← ← ← ← ← ← ←
```

## Features

✅ **Real-time Log Collection**: Collect logs from multiple sources
✅ **Cloud Storage**: Firestore database for scalable log storage
✅ **Log Processing**: Serverless Cloud Functions for real-time processing
✅ **Email Alerts**: Automatic email notifications for errors (30-min throttling)
✅ **REST API**: Flask backend for log management
✅ **Web Dashboard**: React.js dashboard with real-time updates
✅ **Visualization**: Charts and graphs for log metrics
✅ **Filtering**: Filter logs by severity, source, and time range

## Tech Stack

### Backend
- Python Flask
- Google Cloud Functions
- Google Cloud Pub/Sub
- Google Firestore
- Google Cloud Logging

### Frontend
- React.js
- Chart.js
- Axios

### Infrastructure
- Google Cloud Platform
- Docker
- Google Cloud Run

## Project Structure

```
Cloud-log-mon-system/
├── app.py                  # Sample logging application
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
├── backend/
│   ├── app.py             # Flask REST API
│   ├── requirements.txt
│   └── Dockerfile
├── cloud-function/
│   ├── main.py            # Cloud Function for log processing
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.js         # Main React component
    │   ├── App.css        # Styles
    │   └── components/
    │       ├── LogTable.js
    │       ├── StatsChart.js
    │       └── FilterPanel.js
    └── package.json
```

## Setup Instructions

### Prerequisites
- Google Cloud Platform account
- Node.js and npm
- Python 3.10+
- gcloud CLI

### 1. Clone and Setup Environment

```bash
cd Cloud-log-mon-system
cp .env.example .env
# Edit .env with your credentials
```

### 2. Enable Google Cloud APIs

```bash
source .env
gcloud config set project $PROJECT_ID
gcloud services enable logging.googleapis.com
gcloud services enable pubsub.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable firestore.googleapis.com
```

### 3. Create Pub/Sub Topic

```bash
gcloud pubsub topics create logs-topic --project=$PROJECT_ID
```

### 4. Create Log Sink

```bash
gcloud logging sinks create log-sink \
  pubsub.googleapis.com/projects/$PROJECT_ID/topics/logs-topic \
  --log-filter='severity>=WARNING' \
  --project=$PROJECT_ID
```

### 5. Grant Permissions

```bash
gcloud pubsub topics add-iam-policy-binding logs-topic \
  --member='serviceAccount:service-<PROJECT-NUMBER>@gcp-sa-logging.iam.gserviceaccount.com' \
  --role='roles/pubsub.publisher' \
  --project=$PROJECT_ID
```

### 6. Deploy Cloud Function

```bash
gcloud functions deploy process-log-function \
  --runtime python310 \
  --trigger-topic logs-topic \
  --entry-point process_log \
  --source ./cloud-function \
  --set-env-vars SENDER_EMAIL=$SENDER_EMAIL,RECEIVER_EMAIL=$RECEIVER_EMAIL,EMAIL_PASSWORD=$EMAIL_PASSWORD \
  --region=$REGION \
  --project=$PROJECT_ID
```

### 7. Run Backend API (Local)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### 8. Run Frontend (Local)

```bash
cd frontend
npm install
npm start
```

## API Endpoints

### POST /api/logs
Create a new log entry

### GET /api/logs
Get logs with optional filters
- Query params: `severity`, `source`, `limit`, `hours`

### GET /api/logs/:id
Get a specific log by ID

### GET /api/stats
Get log statistics and distribution

## Usage

### Sending Logs from Your Application

```python
import google.cloud.logging
import logging

client = google.cloud.logging.Client()
client.setup_logging()

logging.error("This is an error message")
```

### Testing the System

```bash
python app.py
```

This will generate sample logs that flow through the entire pipeline.

## Deployment to Google Cloud Run

### Deploy Backend

```bash
cd backend
gcloud run deploy log-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Deploy Frontend

```bash
cd frontend
npm run build
# Deploy build/ folder to Cloud Storage or Firebase Hosting
```

## Features Implemented

- [x] Log Collection (Cloud Logging)
- [x] Log Streaming (Pub/Sub)
- [x] Processing Layer (Cloud Functions)
- [x] Storage (Firestore)
- [x] REST API (Flask)
- [x] Web Dashboard (React)
- [x] Visualization (Chart.js)
- [x] Email Alerts
- [ ] Authentication (Future)
- [ ] Advanced Analytics (Future)

## Security

- Environment variables for sensitive data
- IAM roles and permissions
- CORS configuration
- Secure HTTPS endpoints

## License

MIT License

## Contact

- Shreya Kumari - fd6317@nyu.edu
- Richa Sapre - ee9498@nyu.edu
