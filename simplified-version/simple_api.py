"""
SIMPLE FLASK API
This is a web server that stores and retrieves logs.
Think of it as a "log storage service"
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import firestore
from datetime import datetime

# Create the Flask app (our web server)
app = Flask(__name__)
CORS(app)  # Allow requests from web browsers

# Connect to Firestore database
db = firestore.Client()

# ============================================
# ENDPOINT 1: Check if server is working
# ============================================
@app.route('/health', methods=['GET'])
def health():
    """
    Simple health check
    Visit: http://localhost:8080/health
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Server is running!'
    })


# ============================================
# ENDPOINT 2: Save a new log
# ============================================
@app.route('/api/logs', methods=['POST'])
def create_log():
    """
    Save a log to database
    
    Example:
    POST /api/logs
    Body: {
        "severity": "ERROR",
        "message": "Something went wrong"
    }
    """
    try:
        # Get the data from request
        data = request.get_json()
        
        # Create a log entry
        log = {
            'severity': data.get('severity', 'INFO'),
            'message': data.get('message', ''),
            'timestamp': datetime.utcnow().isoformat(),
            'source': data.get('source', 'unknown'),
            'created_at': firestore.SERVER_TIMESTAMP
        }
        
        # Save to Firestore
        db.collection('logs').add(log)
        
        return jsonify({
            'success': True,
            'message': 'Log saved!'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================
# ENDPOINT 3: Get all logs
# ============================================
@app.route('/api/logs', methods=['GET'])
def get_logs():
    """
    Get logs from database
    
    Example:
    GET /api/logs?severity=ERROR&limit=10
    """
    try:
        # Get parameters from URL
        limit = int(request.args.get('limit', 100))
        severity = request.args.get('severity')  # Optional filter
        
        # Query Firestore
        query = db.collection('logs')
        
        # Filter by severity if provided
        if severity:
            query = query.where('severity', '==', severity)
        
        # Get most recent logs first
        query = query.order_by('created_at', direction=firestore.Query.DESCENDING)
        query = query.limit(limit)
        
        # Convert to list
        logs = []
        for doc in query.stream():
            log_data = doc.to_dict()
            log_data['id'] = doc.id
            logs.append(log_data)
        
        return jsonify({
            'success': True,
            'count': len(logs),
            'logs': logs
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================
# ENDPOINT 4: Get statistics
# ============================================
@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get log statistics (counts by severity)
    
    Example:
    GET /api/stats
    """
    try:
        # Count all logs
        all_logs = list(db.collection('logs').stream())
        total = len(all_logs)
        
        # Count by severity
        error_count = 0
        warning_count = 0
        info_count = 0
        
        for doc in all_logs:
            data = doc.to_dict()
            severity = data.get('severity', '')
            
            if severity == 'ERROR':
                error_count += 1
            elif severity == 'WARNING':
                warning_count += 1
            elif severity == 'INFO':
                info_count += 1
        
        return jsonify({
            'success': True,
            'stats': {
                'total_logs': total,
                'error_count': error_count,
                'warning_count': warning_count,
                'info_count': info_count,
                'severity_distribution': {
                    'ERROR': error_count,
                    'WARNING': warning_count,
                    'INFO': info_count
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================
# Start the server
# ============================================
if __name__ == '__main__':
    print("Starting server on http://localhost:8080")
    print("Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=8080, debug=True)
