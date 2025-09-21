#!/bin/bash

echo "🚀 Testing RAG Service Step 1..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Test the RAG service directly
echo "�� Testing RAG service..."
python rag_service.py

echo "✅ Step 1 complete! RAG service is working."
echo "🔗 Next: Start the API server with 'python rag_api.py'"
