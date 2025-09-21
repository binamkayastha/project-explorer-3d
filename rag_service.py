#!/usr/bin/env python3
"""
Simple RAG Service for Project Similarity Search
Step 1: Basic text similarity using TF-IDF and cosine similarity
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import sys
from typing import List, Dict, Any

class ProjectRAGService:
    def __init__(self, csv_path: str = "df_out.csv"):
        """Initialize the RAG service with project data"""
        self.csv_path = csv_path
        self.projects_df = None
        self.vectorizer = None
        self.tfidf_matrix = None
        self.load_data()
        self.prepare_embeddings()
    
    def load_data(self):
        """Load project data from CSV"""
        try:
            self.projects_df = pd.read_csv(self.csv_path)
            print(f"✅ Loaded {len(self.projects_df)} projects from {self.csv_path}")
            
            # Clean the data
            self.projects_df['ai_summary'] = self.projects_df['ai_summary'].fillna('')
            self.projects_df['description'] = self.projects_df['description'].fillna('')
            self.projects_df['name'] = self.projects_df['name'].fillna('Unknown Project')
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            sys.exit(1)
    
    def prepare_embeddings(self):
        """Create TF-IDF embeddings for AI summaries"""
        # Combine AI summary with description for better context
        text_data = []
        for idx, row in self.projects_df.iterrows():
            # Primary: AI summary, Fallback: description, Final fallback: name
            text = row['ai_summary'] if row['ai_summary'].strip() else row['description']
            if not text.strip():
                text = row['name']
            text_data.append(text)
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),  # Include bigrams
            min_df=1,
            max_df=0.95
        )
        
        # Fit and transform the text data
        self.tfidf_matrix = self.vectorizer.fit_transform(text_data)
        print(f"✅ Created embeddings with {self.tfidf_matrix.shape[1]} features")
    
    def find_similar_projects(self, user_idea: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Find similar projects using TF-IDF and cosine similarity"""
        
        # Transform user idea to TF-IDF vector
        user_vector = self.vectorizer.transform([user_idea])
        
        # Calculate cosine similarities
        similarities = cosine_similarity(user_vector, self.tfidf_matrix).flatten()
        
        # Get top similar projects
        top_indices = similarities.argsort()[-limit:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.01:  # Filter very low similarities
                project = self.projects_df.iloc[idx]
                
                # Convert all values to JSON-serializable types
                result = {
                    'id': int(idx),
                    'name': str(project['name']),
                    'description': str(project['description']),
                    'ai_summary': str(project['ai_summary']),
                    'github_url': str(project['github_url']) if pd.notna(project['github_url']) else '',
                    'project_url': str(project['project_url']) if pd.notna(project['project_url']) else '',
                    'demo_url': str(project['demo_url']) if pd.notna(project['demo_url']) else '',
                    'github_stars': int(project['github_stars']) if pd.notna(project['github_stars']) else 0,
                    'similarity_score': float(round(similarities[idx] * 100, 2)),
                    'match_reason': str(self._generate_match_reason(user_idea, project)),
                    'integration_complexity': str(self._determine_complexity(similarities[idx]))
                }
                results.append(result)
        
        return results
    
    def _generate_match_reason(self, user_idea: str, project: pd.Series) -> str:
        """Generate a reason why this project matches the user idea"""
        user_words = set(user_idea.lower().split())
        project_text = f"{project['ai_summary']} {project['description']}".lower()
        project_words = set(project_text.split())
        
        common_words = user_words.intersection(project_words)
        common_words = [word for word in common_words if len(word) > 3]
        
        if common_words:
            return f"Shared concepts: {', '.join(common_words[:3])}"
        else:
            return "Semantic similarity in project context"
    
    def _determine_complexity(self, similarity_score: float) -> str:
        """Determine integration complexity based on similarity score"""
        if similarity_score > 0.7:
            return 'low'
        elif similarity_score > 0.4:
            return 'medium'
        else:
            return 'high'

def main():
    """Test the RAG service"""
    print(" Starting Project RAG Service Test...")
    
    # Initialize service
    rag_service = ProjectRAGService()
    
    # Test query
    test_query = "I want to build a CRM tool for real estate agents with AI-powered lead scoring"
    print(f"\n🔍 Testing query: '{test_query}'")
    
    # Find similar projects
    results = rag_service.find_similar_projects(test_query, limit=3)
    
    # Display results
    print(f"\n📊 Found {len(results)} similar projects:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['name']}")
        print(f"   Similarity: {result['similarity_score']}%")
        print(f"   Reason: {result['match_reason']}")
        print(f"   Complexity: {result['integration_complexity']}")
        print(f"   GitHub Stars: {result['github_stars']}")
        if result['ai_summary']:
            print(f"   AI Summary: {result['ai_summary'][:100]}...")

if __name__ == "__main__":
    main()
