#!/usr/bin/env python3
"""
Simple Flask API for RAG Service
Step 1: Basic API endpoint to connect Python RAG with TypeScript frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_service import ProjectRAGService
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for TypeScript frontend

# Initialize RAG service
rag_service = ProjectRAGService()

@app.route('/api/similar-projects', methods=['POST'])
def find_similar_projects():
    """API endpoint to find similar projects"""
    try:
        data = request.get_json()
        user_idea = data.get('idea', '')
        limit = data.get('limit', 5)
        
        if not user_idea.strip():
            return jsonify({'error': 'Please provide an idea'}), 400
        
        # Find similar projects
        results = rag_service.find_similar_projects(user_idea, limit)
        
        return jsonify({
            'success': True,
            'matches': results,
            'total_found': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Project RAG Service',
        'total_projects': len(rag_service.projects_df)
    })

if __name__ == '__main__':
    print("🚀 Starting RAG API Server...")
    print("📡 API will be available at: http://localhost:5001")
    print("🔍 Test endpoint: POST /api/similar-projects")
    print("❤️  Health check: GET /api/health")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
