from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import firestore
from datetime import datetime, timedelta
import os
from auth import require_api_key

app = Flask(__name__)
CORS(app)

db = firestore.Client()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'log-monitoring-api'}), 200

@app.route('/api/logs', methods=['POST'])
@require_api_key
def create_log():
    try:
        data = request.get_json()
        
        log_entry = {
            'severity': data.get('severity', 'INFO'),
            'message': data.get('message', ''),
            'source': data.get('source', 'api'),
            'timestamp': datetime.utcnow().isoformat(),
            'metadata': data.get('metadata', {}),
            'created_at': firestore.SERVER_TIMESTAMP
        }
        
        doc_ref = db.collection('logs').add(log_entry)
        
        return jsonify({
            'success': True,
            'log_id': doc_ref[1].id,
            'message': 'Log created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    try:
        limit = int(request.args.get('limit', 100))
        severity = request.args.get('severity')
        source = request.args.get('source')
        hours = int(request.args.get('hours', 24))
        
        query = db.collection('logs')
        
        if severity:
            query = query.where('severity', '==', severity)
        
        if source:
            query = query.where('source', '==', source)
        
        query = query.order_by('created_at', direction=firestore.Query.DESCENDING).limit(limit)
        
        logs = []
        for doc in query.stream():
            log_data = doc.to_dict()
            log_data['id'] = doc.id
            logs.append(log_data)
        
        return jsonify({
            'success': True,
            'count': len(logs),
            'logs': logs
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/logs/<log_id>', methods=['GET'])
def get_log(log_id):
    try:
        doc_ref = db.collection('logs').document(log_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({'success': False, 'error': 'Log not found'}), 404
        
        log_data = doc.to_dict()
        log_data['id'] = doc.id
        
        return jsonify({
            'success': True,
            'log': log_data
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        hours = int(request.args.get('hours', 24))
        
        logs_ref = db.collection('logs')
        
        total_logs = len(list(logs_ref.stream()))
        
        error_logs = len(list(logs_ref.where('severity', '==', 'ERROR').stream()))
        warning_logs = len(list(logs_ref.where('severity', '==', 'WARNING').stream()))
        info_logs = len(list(logs_ref.where('severity', '==', 'INFO').stream()))
        
        stats = {
            'total_logs': total_logs,
            'error_count': error_logs,
            'warning_count': warning_logs,
            'info_count': info_logs,
            'severity_distribution': {
                'ERROR': error_logs,
                'WARNING': warning_logs,
                'INFO': info_logs
            }
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
