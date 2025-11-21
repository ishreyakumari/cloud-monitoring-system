# REST API - retrieve logs
from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud import firestore

app = Flask(__name__)
CORS(app)
db = firestore.Client()

@app.route('/api/logs', methods=['GET'])
def get_logs():
    limit = int(request.args.get('limit', 100))
    severity = request.args.get('severity')
    
    query = db.collection('logs')
    if severity:
        query = query.where('severity', '==', severity)
    query = query.order_by('created_at', direction=firestore.Query.DESCENDING).limit(limit)
    
    logs = []
    for doc in query.stream():
        data = doc.to_dict()
        data['id'] = doc.id
        logs.append(data)
    
    return jsonify({'logs': logs, 'count': len(logs)})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    all_logs = list(db.collection('logs').stream())
    
    stats = {'ERROR': 0, 'WARNING': 0, 'INFO': 0}
    for doc in all_logs:
        severity = doc.to_dict().get('severity', '')
        if severity in stats:
            stats[severity] += 1
    
    return jsonify({'total': len(all_logs), 'distribution': stats})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
