CLOUD LOG MONITORING SYSTEM
===========================
Team: Shreya Kumari (fd6317), Richa Sapre (ee9498)
Project: MS Computer Science - Cloud Computing

PROJECT FILES:
1. app.py - Log generator
2. function.py - Cloud Function (processes logs, sends alerts)
3. api.py - REST API (query logs)
4. dashboard.html - Web dashboard with charts
5. requirements.txt - Python dependencies

ARCHITECTURE:
app.py → Cloud Logging → Pub/Sub → function.py → Firestore
                                         ↓            ↓
                                    Email Alert    api.py
                                                      ↓
                                                 dashboard.html

SETUP:
1. Create Pub/Sub topic:
   gcloud pubsub topics create logs-topic --project=sacred-augury-478923-i9

2. Create log sink:
   gcloud logging sinks create log-sink \
     pubsub.googleapis.com/projects/sacred-augury-478923-i9/topics/logs-topic \
     --log-filter='severity>=WARNING' \
     --project=sacred-augury-478923-i9

3. Grant permissions:
   gcloud pubsub topics add-iam-policy-binding logs-topic \
     --member='serviceAccount:service-941728631592@gcp-sa-logging.iam.gserviceaccount.com' \
     --role='roles/pubsub.publisher' \
     --project=sacred-augury-478923-i9

4. Deploy Cloud Function:
   gcloud functions deploy process-log-function \
     --runtime python310 \
     --trigger-topic logs-topic \
     --entry-point process_log \
     --source . \
     --set-env-vars SENDER_EMAIL=ishreyakumari2022@gmail.com,RECEIVER_EMAIL=ishreyakumari2022@gmail.com,EMAIL_PASSWORD=your_app_password \
     --region=us-central1 \
     --project=sacred-augury-478923-i9

5. Run the system:
   # Terminal 1: Generate logs
   python app.py
   
   # Terminal 2: Start API server
   python api.py
   
   # Terminal 3: Open dashboard
   open dashboard.html
   # Or open http://localhost:8080 in your browser after opening dashboard.html
