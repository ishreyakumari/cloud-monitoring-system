# ☁️ Cloud Log Monitoring System

A **cloud-based real-time log monitoring and analysis system** built using **React, Flask, Google Cloud Platform, and Firestore**.

---

## 🏗️ Architecture

```mermaid
flowchart LR
    A[Client Apps] --> B[Cloud Logging]
    B --> C[Pub/Sub]
    C --> D[Cloud Function]
    D --> E[Firestore]
    E --> F[Flask REST API]
    F --> G[React Frontend]
````

**Flow:**
Client Apps → Cloud Logging → Pub/Sub → Cloud Function → Firestore
↓
Frontend (React) ← REST API (Flask)

---

## ✨ Features

✅ **Real-time Log Collection** — Collect logs from multiple sources<br/>
✅ **Cloud Storage** — Firestore for scalable log storage<br/>
✅ **Log Processing** — Serverless Cloud Functions for real-time analysis<br/>
✅ **Email Alerts** — Automatic error notifications (30-min throttling)<br/>
✅ **REST API** — Flask backend for log management<br/>
✅ **Web Dashboard** — React.js interface with live updates<br/>
✅ **Visualization** — Charts & graphs for log metrics<br/>
✅ **Filtering** — Filter by severity, source, and time range<br/>

---

## ⚙️ Tech Stack

### 🖥️ Backend

* Python Flask
* Google Cloud Functions
* Google Cloud Pub/Sub
* Google Firestore
* Google Cloud Logging

### 💻 Frontend

* React.js
* Chart.js
* Axios

### ☁️ Infrastructure

* Google Cloud Platform
* Docker
* Google Cloud Run

---

## 📂 Project Structure

```
Cloud-log-mon-system/
├── app.py                  # Sample logging application
├── .env                    # Environment variables
├── requirements.txt         # Python dependencies
├── backend/
│   ├── app.py              # Flask REST API
│   ├── requirements.txt
│   └── Dockerfile
├── cloud-function/
│   ├── main.py             # Cloud Function for log processing
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.js          # Main React component
    │   ├── App.css         # Styles
    │   └── components/
    │       ├── LogTable.js
    │       ├── StatsChart.js
    │       └── FilterPanel.js
    └── package.json
```

---

## ⚡ Setup Instructions

### 🧩 Prerequisites

* Google Cloud Platform account
* Node.js and npm
* Python 3.10+
* `gcloud` CLI

---

### 1️⃣ Clone and Setup Environment

```bash
git clone <repo-url>
cd Cloud-log-mon-system
cp .env.example .env
# Edit .env with your GCP project details and credentials
```

---

### 2️⃣ Enable Required Google Cloud APIs

```bash
source .env
gcloud config set project $PROJECT_ID

gcloud services enable logging.googleapis.com
gcloud services enable pubsub.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable firestore.googleapis.com
```

---

### 3️⃣ Create Pub/Sub Topic

```bash
gcloud pubsub topics create logs-topic --project=$PROJECT_ID
```

---

### 4️⃣ Create Log Sink

```bash
gcloud logging sinks create log-sink \
  pubsub.googleapis.com/projects/$PROJECT_ID/topics/logs-topic \
  --log-filter='severity>=WARNING' \
  --project=$PROJECT_ID
```

---

### 5️⃣ Grant Permissions

```bash
gcloud pubsub topics add-iam-policy-binding logs-topic \
  --member="serviceAccount:service-$PROJECT_NUMBER@gcp-sa-logging.iam.gserviceaccount.com" \
  --role="roles/pubsub.publisher" \
  --project=$PROJECT_ID
```

---

### 6️⃣ Deploy Cloud Function

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

---

### 7️⃣ Run Backend API Locally

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

---

### 8️⃣ Run Frontend Locally

```bash
cd frontend
npm install
npm start
```

---

## 🔌 API Endpoints

| Method | Endpoint        | Description                         | Query Params                           |
| ------ | --------------- | ----------------------------------- | -------------------------------------- |
| `POST` | `/api/logs`     | Create a new log entry              | —                                      |
| `GET`  | `/api/logs`     | Retrieve logs with optional filters | `severity`, `source`, `limit`, `hours` |
| `GET`  | `/api/logs/:id` | Get a specific log by ID            | —                                      |
| `GET`  | `/api/stats`    | Get log statistics and distribution | —                                      |

---

## 🧪 Usage Example

### Sending Logs from Your Application

```python
import google.cloud.logging
import logging

client = google.cloud.logging.Client()
client.setup_logging()

logging.error("This is an error message")
```

---

### Testing the System

```bash
python app.py
```

> This will generate sample logs that flow through the entire pipeline.

---

## 🚀 Deployment to Google Cloud Run

### Deploy Backend

```bash
cd backend
gcloud run deploy log-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

### Deploy Frontend

```bash
cd frontend
npm run build
# Deploy the build/ folder to Cloud Storage or Firebase Hosting
```

---

## ✅ Features Implemented

* [x] Log Collection (Cloud Logging)
* [x] Log Streaming (Pub/Sub)
* [x] Processing Layer (Cloud Functions)
* [x] Storage (Firestore)
* [x] REST API (Flask)
* [x] Web Dashboard (React)
* [x] Visualization (Chart.js)
* [x] Email Alerts
* [ ] Authentication *(Future)*
* [ ] Advanced Analytics *(Future)*

---

## 🔒 Security

* Environment variables for sensitive credentials
* IAM roles & permissions for access control
* Configured CORS policies
* HTTPS endpoints for secure communication

---

## 🧭 Future Enhancements

* User authentication (OAuth 2.0 / Firebase Auth)
* Advanced analytics & anomaly detection
* Log retention policies
* Role-based dashboards
