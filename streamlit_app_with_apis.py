"""
Project Explorer Pro - Enhanced with Public APIs
Real Intelligence Platform with Free Public API Integration
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import re
import string
import json
from typing import Dict, List, Any
import sys
import os

# Add the integrations directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'integrations'))

# Enhanced imports with better error handling
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.cluster import KMeans
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    st.warning("⚠️ scikit-learn not available. Advanced AI features will be disabled.")

try:
    import nltk
    from nltk.corpus import stopwords
    NLTK_AVAILABLE = True
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
except ImportError:
    NLTK_AVAILABLE = False

# Import API integrations
try:
    from src.integrations import (
        StartupDataManager,
        add_startup_data_to_sidebar,
        render_startup_data_pages
    )
    API_INTEGRATIONS_AVAILABLE = True
except ImportError:
    API_INTEGRATIONS_AVAILABLE = False
    st.warning("⚠️ API integrations not available. Public API data features will be disabled.")

# Page configuration
st.set_page_config(
    page_title="Project Explorer Pro - Venture Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Professional cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .insight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 1rem;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .success-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border-radius: 1rem;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        border-radius: 1rem;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(250, 112, 154, 0.3);
    }
    
    /* API integration styling */
    .api-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(168, 237, 234, 0.2);
    }
    
    .startup-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(255, 236, 210, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Load data
@st.cache_data
def load_project_data():
    """Load project data from CSV file"""
    try:
        # Try to load the main dataset
        df = pd.read_csv("src/integrations/supabase/projects_dataset/sundai_projects_umap.csv")
        return df
    except FileNotFoundError:
        try:
            # Fallback to sample data
            df = pd.read_csv("sample_projects.csv")
            return df
        except FileNotFoundError:
            # Create sample data if no file exists
            sample_data = {
                'title': ['AI Project 1', 'Fintech Startup', 'HealthTech App', 'EdTech Platform'],
                'description': [
                    'An AI-powered automation tool for manufacturing companies',
                    'A fintech solution for small businesses',
                    'A health monitoring application',
                    'An educational technology platform'
                ],
                'category': ['AI', 'Fintech', 'HealthTech', 'EdTech'],
                'project_url': ['https://example1.com', 'https://example2.com', 'https://example3.com', 'https://example4.com'],
                'github_url': ['https://github.com/example1', 'https://github.com/example2', 'https://github.com/example3', 'https://github.com/example4'],
                'funding_amount': [100000, 50000, 75000, 25000],
                'x': [0.1, 0.2, 0.3, 0.4],
                'y': [0.1, 0.2, 0.3, 0.4],
                'z': [0.1, 0.2, 0.3, 0.4]
            }
            return pd.DataFrame(sample_data)

# Load data
df = load_project_data()

# Define all page rendering functions before they're used
def render_home_page():
    """Render the home page"""
    st.markdown('<h1 class="main-header">Project Explorer Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real Intelligence Platform with Free Public API Integration</p>', unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="success-card">
        <h2>🎯 Welcome to Project Explorer Pro!</h2>
        <p>Discover, analyze, and connect with innovative projects using advanced AI technology and real-time data from GitHub, NPM, and PyPI - all completely free!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-card">
            <h3>🤖 AI-Powered Analysis</h3>
            <ul>
                <li>Real content analysis</li>
                <li>Technology stack detection</li>
                <li>Business model recognition</li>
                <li>Similarity matching</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="api-card">
            <h3>🚀 Free Public API Integration</h3>
            <ul>
                <li>GitHub repository search</li>
                <li>NPM package discovery</li>
                <li>PyPI package analysis</li>
                <li>No registration required!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick stats
    st.markdown("### 📊 Platform Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Projects Analyzed", len(df))
    
    with col2:
        st.metric("Categories", df['category'].nunique())
    
    with col3:
        st.metric("AI Features", "6+")
    
    with col4:
        st.metric("Data Sources", "4+" if API_INTEGRATIONS_AVAILABLE else "1")

def render_ai_matcher_page():
    """Render the AI Idea Matcher page"""
    st.markdown("## 🔍 AI Idea Matcher")
    st.markdown("Enter your project idea and discover similar projects with AI-powered analysis")
    
    # Project idea input
    user_query = st.text_area(
        "Describe your project idea",
        placeholder="e.g., I want to build an AI-powered automation tool for manufacturing companies that helps optimize production processes, reduce waste, and improve quality control.",
        height=150
    )
    
    if st.button("🔍 Find Similar Projects", use_container_width=True):
        if user_query:
            with st.spinner("Analyzing your project idea..."):
                # Perform AI analysis
                similar_projects = analyze_project_similarity(user_query, df)
                display_similar_projects(similar_projects, user_query)
        else:
            st.warning("Please enter a project idea to analyze.")

def render_analytics_page():
    """Render the Analytics Dashboard page"""
    st.markdown("## 📊 Analytics Dashboard")
    st.markdown("Comprehensive analytics and insights about projects and trends")
    
    # Analytics tabs
    tab1, tab2, tab3 = st.tabs(["📈 Project Overview", "🎯 Category Analysis", "🚀 Technology Trends"])
    
    with tab1:
        st.markdown("### Project Overview")
        
        # Basic statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Projects", len(df))
        with col2:
            st.metric("Categories", df['category'].nunique())
        with col3:
            st.metric("Avg. Funding", f"${df['funding_amount'].mean():,.0f}")
        
        # Project distribution chart
        st.markdown("### Project Distribution by Category")
        category_counts = df['category'].value_counts()
        fig = px.bar(x=category_counts.index, y=category_counts.values, 
                    title="Projects by Category")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Category Analysis")
        
        # Category insights
        selected_category = st.selectbox("Select Category", df['category'].unique())
        category_data = df[df['category'] == selected_category]
        
        if not category_data.empty:
            st.markdown(f"#### {selected_category} Insights")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Projects", len(category_data))
                st.metric("Avg. Funding", f"${category_data['funding_amount'].mean():,.0f}")
            
            with col2:
                st.metric("Total Funding", f"${category_data['funding_amount'].sum():,.0f}")
                st.metric("Success Rate", f"{len(category_data[category_data['funding_amount'] > 0]) / len(category_data) * 100:.1f}%")
    
    with tab3:
        st.markdown("### Technology Trends")
        
        if API_INTEGRATIONS_AVAILABLE:
            # Show trending technologies from public APIs
            st.markdown("#### 🔥 Trending Technologies")
            
            tech_query = st.text_input("Search for technology trends", placeholder="e.g., AI, React, Python")
            if st.button("🔍 Analyze Trends"):
                if tech_query:
                    with st.spinner("Analyzing technology trends..."):
                        try:
                            from src.integrations import StartupDataManager
                            manager = StartupDataManager()
                            insights = manager.get_market_insights(tech_query)
                            
                            st.markdown(f"#### {tech_query} Market Insights")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Total Projects", insights.get('total_projects_found', 0))
                            with col2:
                                st.metric("GitHub Stars", f"{insights.get('total_stars', 0):,}")
                            with col3:
                                st.metric("Downloads", f"{insights.get('total_downloads', 0):,}")
                            
                            # Show language distribution
                            if insights.get('language_distribution'):
                                st.markdown("#### Programming Language Distribution")
                                lang_data = pd.DataFrame(list(insights['language_distribution'].items()), 
                                                       columns=['Language', 'Count'])
                                fig = px.pie(lang_data, values='Count', names='Language', 
                                           title=f"Languages used in {tech_query} projects")
                                st.plotly_chart(fig, use_container_width=True)
                                
                        except Exception as e:
                            st.error(f"Error analyzing trends: {str(e)}")
                else:
                    st.warning("Please enter a technology to analyze.")
        else:
            st.info("Enable API integrations to view real-time technology trends.")

def render_settings_page():
    """Render the Settings page"""
    st.markdown("## ⚙️ Settings")
    st.markdown("Configure your Project Explorer Pro experience")
    
    # API Settings
    st.markdown("### 🔑 API Configuration")
    
    if API_INTEGRATIONS_AVAILABLE:
        st.success("✅ Public API integrations are enabled and working!")
        st.markdown("""
        **Available APIs:**
        - GitHub API (Free, no registration required)
        - NPM API (Free, no registration required)  
        - PyPI API (Free, no registration required)
        """)
        
        # Show API usage stats
        try:
            from src.integrations import StartupDataManager
            manager = StartupDataManager()
            usage_stats = manager.get_api_usage_stats()
            
            st.markdown("### 📊 API Usage Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Requests Made", usage_stats.get('total_requests', 0))
            with col2:
                st.metric("Remaining Requests", usage_stats.get('public_apis', {}).get('remaining_requests', 100))
            with col3:
                st.metric("APIs Used", len(usage_stats.get('public_apis', {}).get('apis_used', [])))
                
        except Exception as e:
            st.error(f"Error fetching API stats: {str(e)}")
    else:
        st.warning("⚠️ API integrations are not available.")
        st.markdown("""
        To enable API integrations:
        1. Check that all required packages are installed
        2. Verify the integrations directory structure
        3. Restart the application
        """)
    
    # Application Settings
    st.markdown("### 🎛️ Application Settings")
    
    # Theme selection
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    st.info(f"Selected theme: {theme}")
    
    # Data refresh interval
    refresh_interval = st.slider("Data Refresh Interval (minutes)", 1, 60, 15)
    st.info(f"Data will refresh every {refresh_interval} minutes")
    
    # Export settings
    st.markdown("### 📤 Export Settings")
    
    if st.button("📥 Export Current Data"):
        # Create a download link for the current data
        csv = df.to_csv(index=False)
        st.download_button(
            label="📄 Download as CSV",
            data=csv,
            file_name="project_explorer_data.csv",
            mime="text/csv"
        )

def analyze_project_similarity(user_query: str, df: pd.DataFrame) -> List[Dict]:
    """Analyze project similarity using AI techniques"""
    if not SKLEARN_AVAILABLE:
        # Fallback to simple keyword matching
        return simple_keyword_matching(user_query, df)
    
    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english' if NLTK_AVAILABLE else None,
        ngram_range=(1, 2)
    )
    
    # Combine user query with project descriptions
    all_texts = [user_query] + df['description'].tolist()
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Calculate similarity
    user_vector = tfidf_matrix[0:1]
    project_vectors = tfidf_matrix[1:]
    similarities = cosine_similarity(user_vector, project_vectors).flatten()
    
    # Get top similar projects
    top_indices = similarities.argsort()[-5:][::-1]
    
    similar_projects = []
    for idx in top_indices:
        project = df.iloc[idx].to_dict()
        project['similarity_score'] = float(similarities[idx])
        similar_projects.append(project)
    
    return similar_projects

def simple_keyword_matching(user_query: str, df: pd.DataFrame) -> List[Dict]:
    """Simple keyword matching fallback"""
    query_words = set(user_query.lower().split())
    
    similarities = []
    for idx, row in df.iterrows():
        project_words = set(row['description'].lower().split())
        intersection = len(query_words.intersection(project_words))
        union = len(query_words.union(project_words))
        similarity = intersection / union if union > 0 else 0
        similarities.append(similarity)
    
    # Get top similar projects
    top_indices = np.argsort(similarities)[-5:][::-1]
    
    similar_projects = []
    for idx in top_indices:
        project = df.iloc[idx].to_dict()
        project['similarity_score'] = similarities[idx]
        similar_projects.append(project)
    
    return similar_projects

def display_similar_projects(projects: List[Dict], user_query: str):
    """Display similar projects with detailed analysis"""
    st.markdown(f"### 🎯 Found {len(projects)} Similar Projects")
    
    for i, project in enumerate(projects):
        similarity_percent = int(project['similarity_score'] * 100)
        
        with st.expander(f"📋 {project['title']} (Similarity: {similarity_percent}%)", expanded=i==0):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {project['description']}")
                st.markdown(f"**Category:** {project['category']}")
                
                if project['project_url']:
                    st.markdown(f"**Website:** [{project['project_url']}]({project['project_url']})")
                
                if project['github_url']:
                    st.markdown(f"**GitHub:** [{project['github_url']}]({project['github_url']})")
            
            with col2:
                st.metric("Similarity Score", f"{similarity_percent}%")
                
                # Technology analysis
                tech_analysis = analyze_technology_stack(project['description'])
                st.markdown("**Technology Stack:**")
                for tech, confidence in tech_analysis.items():
                    st.markdown(f"- {tech}: {confidence}%")
            
            # Engagement strategy
            engagement = generate_engagement_strategy(project, user_query, project['similarity_score'])
            st.markdown("**🤝 Engagement Strategy:**")
            for strategy in engagement:
                st.markdown(f"- {strategy}")

def analyze_technology_stack(description: str) -> Dict[str, int]:
    """Analyze technology stack from project description"""
    tech_keywords = {
        'Frontend': ['react', 'vue', 'angular', 'javascript', 'html', 'css'],
        'Backend': ['python', 'node.js', 'java', 'php', 'ruby', 'django', 'flask'],
        'Database': ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite'],
        'Cloud': ['aws', 'azure', 'gcp', 'heroku', 'digitalocean'],
        'AI/ML': ['tensorflow', 'pytorch', 'scikit-learn', 'openai', 'gpt'],
        'Mobile': ['react native', 'flutter', 'ios', 'android', 'swift'],
        'DevOps': ['docker', 'kubernetes', 'jenkins', 'git', 'ci/cd'],
        'Blockchain': ['ethereum', 'bitcoin', 'solidity', 'web3', 'defi']
    }
    
    description_lower = description.lower()
    tech_analysis = {}
    
    for tech_category, keywords in tech_keywords.items():
        matches = sum(1 for keyword in keywords if keyword in description_lower)
        confidence = min(100, matches * 25)  # 25% per keyword match
        if confidence > 0:
            tech_analysis[tech_category] = confidence
    
    return tech_analysis

def generate_engagement_strategy(project: Dict, user_query: str, similarity_score: float) -> List[str]:
    """Generate engagement strategy for a project"""
    strategies = []
    
    if similarity_score > 0.8:
        strategies.append("🤝 High similarity suggests direct collaboration potential")
    elif similarity_score > 0.6:
        strategies.append("📚 Good learning opportunity - study their approach")
    else:
        strategies.append("💡 Different approach - explore complementary opportunities")
    
    if 'AI' in project['description'] or 'AI' in user_query:
        strategies.append("🤖 AI/ML focus - consider technical collaboration")
    
    if 'fintech' in project['description'].lower() or 'fintech' in user_query.lower():
        strategies.append("💰 Fintech domain - explore regulatory compliance insights")
    
    strategies.append("📧 Reach out via their website or GitHub")
    strategies.append("🔗 Connect on professional networks")
    
    return strategies

# Sidebar navigation
st.sidebar.markdown("## 🧭 Navigation")
page = st.sidebar.selectbox(
    "Choose a page",
    ["🏠 Home", "🔍 AI Idea Matcher", "📊 Analytics Dashboard", "🚀 Public API Data", "⚙️ Settings"]
)

# Add API integrations to sidebar if available
if API_INTEGRATIONS_AVAILABLE:
    add_startup_data_to_sidebar()

# Page routing
if page == "🏠 Home":
    render_home_page()
elif page == "🔍 AI Idea Matcher":
    render_ai_matcher_page()
elif page == "📊 Analytics Dashboard":
    render_analytics_page()
elif page == "🚀 Public API Data":
    if API_INTEGRATIONS_AVAILABLE:
        render_startup_data_pages()
    else:
        st.error("API integrations are not available. Please check your installation.")
elif page == "⚙️ Settings":
    render_settings_page()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🚀 Project Explorer Pro - Real Intelligence Platform</p>
    <p>Powered by AI and free public APIs from GitHub, NPM & PyPI</p>
</div>
""", unsafe_allow_html=True)
