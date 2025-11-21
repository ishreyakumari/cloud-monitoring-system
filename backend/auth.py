import functools
from flask import request, jsonify
import os

API_KEY = os.environ.get('API_KEY', 'demo-api-key-change-in-production')

def require_api_key(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'success': False, 'error': 'API key is missing'}), 401
        
        if api_key != API_KEY:
            return jsonify({'success': False, 'error': 'Invalid API key'}), 403
        
        return f(*args, **kwargs)
    return decorated_function
