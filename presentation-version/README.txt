CLOUD LOG MONITORING SYSTEM
===========================

FILES:
1. app.py - Generates sample logs
2. function.py - Cloud Function (processes logs, sends email)
3. api.py - REST API (retrieve logs)
4. requirements.txt - Dependencies

HOW IT WORKS:
app.py → Cloud Logging → Pub/Sub → function.py → Firestore
                                                      ↓
                                                   api.py

SETUP COMMANDS:
1. Create Pub/Sub topic:
   gcloud pubsub topics create logs-topic

2. Create log sink:
   gcloud logging sinks create log-sink \
     pubsub.googleapis.com/projects/PROJECT_ID/topics/logs-topic \
     --log-filter='severity>=WARNING'

3. Deploy Cloud Function:
   gcloud functions deploy process-log-function \
     --runtime python310 \
     --trigger-topic logs-topic \
     --entry-point process_log \
     --source . \
     --set-env-vars SENDER_EMAIL=your@gmail.com,RECEIVER_EMAIL=your@gmail.com,EMAIL_PASSWORD=your_app_password

4. Run log generator:
   python app.py

5. Run API:
   python api.py
