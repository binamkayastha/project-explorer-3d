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
    
    /* Professional buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Professional tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        border-radius: 0.5rem 0.5rem 0 0;
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Professional charts */
    .stPlotlyChart {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 1rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Professional sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    /* Professional text areas */
    .stTextArea textarea {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 0.5rem;
        color: white;
    }
    
    /* Professional selectboxes */
    .stSelectbox select {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 0.5rem;
        color: white;
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Professional badges */
    .badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .badge-success {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    /* Professional progress bars */
    .progress-container {
        background: rgba(255,255,255,0.1);
        border-radius: 1rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        height: 0.5rem;
        border-radius: 0.25rem;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'user_idea' not in st.session_state:
    st.session_state.user_idea = ""

# Enhanced data loading function
@st.cache_data
def load_enhanced_data():
    """Load and enhance project data from the specific path"""
    try:
        # Load data from the specific path
        csv_path = r"C:\Users\excalibur\Desktop\Company\Sundai\project-explorer-3d\src\integrations\supabase\projects_dataset\sundai_projects_umap.csv"
        df = pd.read_csv(csv_path)
        
        # Handle duplicate columns
        duplicate_cols = df.columns[df.columns.duplicated()].tolist()
        if duplicate_cols:
            for col in duplicate_cols:
                new_col = f"{col}_1"
                df = df.rename(columns={col: new_col})
        
        # Standardize column names
        column_mapping = {
            'name': 'title',
            'umap_dim_1': 'x',
            'umap_dim_2': 'y', 
            'umap_dim_3': 'z',
            'description': 'description',
            'category': 'category',
            'subcategory_1': 'subcategory_1',
            'project_url': 'project_url',
            'github_url': 'github_url'
        }
        
        # Apply mapping for existing columns
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df = df.rename(columns={old_col: new_col})
        
        # Ensure required columns exist
        required_cols = ['title', 'x', 'y', 'z', 'description', 'category']
        for col in required_cols:
            if col not in df.columns:
                if col in ['x', 'y', 'z']:
                    # Generate synthetic UMAP coordinates
                    np.random.seed(42)
                    df[col] = np.random.normal(0, 5, len(df))
                else:
                    df[col] = f"Default {col}"
        
        # Clean and enhance data
        df['description'] = df['description'].fillna('No description available')
        df['category'] = df['category'].fillna('Uncategorized')
        df['subcategory_1'] = df['subcategory_1'].fillna('General')
        
        # Ensure optional columns exist
        if 'project_url' not in df.columns:
            df['project_url'] = None
        if 'github_url' not in df.columns:
            df['github_url'] = None
        
        # Add UMAP coordinates as tuple
        df['umap_coords'] = list(zip(df['x'], df['y'], df['z']))
        
        return df
        
    except FileNotFoundError:
        st.error(f"❌ CSV file not found at: {csv_path}")
        st.info("Please ensure the file exists at the specified path.")
        return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Enhanced AI matching functions
def preprocess_text_enhanced(text):
    """Enhanced text preprocessing"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def extract_github_url_enhanced(text):
    """Enhanced GitHub URL extraction"""
    if not text:
        return None
    
    # Multiple patterns for GitHub URLs
    patterns = [
        r'https?://github\.com/[a-zA-Z0-9-]+/[a-zA-Z0-9-_.]+',
        r'github\.com/[a-zA-Z0-9-]+/[a-zA-Z0-9-_.]+',
        r'@([a-zA-Z0-9-]+/[a-zA-Z0-9-_.]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            url = match.group(0)
            if not url.startswith('http'):
                url = 'https://' + url
            return url
    
    return None

def find_similar_projects_enhanced(user_query, df, top_k=5):
    """Enhanced project matching with multiple algorithms"""
    if not SKLEARN_AVAILABLE or df.empty:
        return []
    
    try:
        # Preprocess user query
        processed_query = preprocess_text_enhanced(user_query)
        
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Combine all text fields for better matching
        project_texts = []
        for _, row in df.iterrows():
            text_parts = [
                str(row.get('title', '')),
                str(row.get('description', '')),
                str(row.get('category', 'Uncategorized')),
                str(row.get('subcategory_1', 'General'))
            ]
            project_texts.append(' '.join(text_parts))
        
        # Fit and transform
        tfidf_matrix = vectorizer.fit_transform(project_texts)
        query_vector = vectorizer.transform([processed_query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
        
        # Get top matches
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        similar_projects = []
        for idx in top_indices:
            if similarities[idx] > 0.01:  # Minimum similarity threshold
                project = df.iloc[idx].to_dict()
                project['similarity_score'] = float(similarities[idx])
                project['github_url'] = extract_github_url_enhanced(project.get('description', ''))
                similar_projects.append(project)
        
        return similar_projects
    
    except Exception as e:
        st.error(f"Error in AI matching: {str(e)}")
        return []

# Market Intelligence Functions
def analyze_market_validation(similar_projects, user_query):
    """Comprehensive market validation analysis"""
    if not similar_projects:
        return {}
    
    try:
        # Market saturation analysis
        categories = [p.get('category', 'Unknown') for p in similar_projects]
        category_counts = pd.Series(categories).value_counts()
        
        # Calculate various metrics
        avg_similarity = np.mean([p.get('similarity_score', 0) for p in similar_projects])
        market_saturation = min(len(similar_projects) / 10, 1.0)  # Normalize to 0-1
        
        # Success indicators
        projects_with_urls = sum(1 for p in similar_projects if p.get('project_url'))
        projects_with_github = sum(1 for p in similar_projects if p.get('github_url'))
        
        # Market gap analysis
        market_gap_score = 1 - avg_similarity
        validation_score = (projects_with_urls + projects_with_github) / (len(similar_projects) * 2)
        
        # Competition level assessment
        if len(similar_projects) <= 2:
            competition_level = "Low"
            opportunity_score = 0.8
        elif len(similar_projects) <= 5:
            competition_level = "Medium"
            opportunity_score = 0.6
        else:
            competition_level = "High"
            opportunity_score = 0.4
        
        return {
            'market_saturation': market_saturation,
            'avg_similarity': avg_similarity,
            'category_distribution': category_counts.to_dict(),
            'projects_with_urls': projects_with_urls,
            'projects_with_github': projects_with_github,
            'total_competitors': len(similar_projects),
            'market_gap_score': market_gap_score,
            'validation_score': validation_score,
            'competition_level': competition_level,
            'opportunity_score': opportunity_score,
            'market_maturity': "Emerging" if market_saturation < 0.3 else "Growing" if market_saturation < 0.7 else "Mature"
        }
    
    except Exception as e:
        st.error(f"Error in market analysis: {str(e)}")
        return {}

def generate_revenue_insights(similar_projects, user_query):
    """Generate comprehensive revenue insights"""
    try:
        # Define revenue model keywords
        revenue_models = {
            'subscription': ['saas', 'subscription', 'monthly', 'annual', 'recurring', 'membership'],
            'freemium': ['freemium', 'free', 'premium', 'upgrade', 'basic', 'pro'],
            'marketplace': ['marketplace', 'commission', 'transaction', 'platform', 'exchange'],
            'b2b': ['enterprise', 'business', 'corporate', 'b2b', 'enterprise', 'saas'],
            'advertising': ['ads', 'advertising', 'sponsored', 'monetization', 'revenue'],
            'consulting': ['consulting', 'services', 'agency', 'custom', 'implementation'],
            'licensing': ['license', 'api', 'sdk', 'integration', 'partnership']
        }
        
        revenue_insights = {}
        model_scores = {}
        
        for model, keywords in revenue_models.items():
            count = 0
            total_score = 0
            
            for project in similar_projects:
                description = str(project.get('description', '')).lower()
                title = str(project.get('title', '')).lower()
                category = str(project.get('category', '')).lower()
                
                text = f"{description} {title} {category}"
                
                # Count keyword matches
                matches = sum(1 for keyword in keywords if keyword in text)
                if matches > 0:
                    count += 1
                    total_score += matches
            
            revenue_insights[model] = count
            model_scores[model] = total_score
        
        # Calculate market size estimates
        market_size_estimate = len(similar_projects) * 1000000  # Rough estimate
        
        return {
            'revenue_models': revenue_insights,
            'model_scores': model_scores,
            'top_model': max(revenue_insights, key=revenue_insights.get) if revenue_insights else None,
            'market_size_estimate': market_size_estimate,
            'revenue_potential': 'High' if len(similar_projects) < 5 else 'Medium' if len(similar_projects) < 10 else 'Low'
        }
    
    except Exception as e:
        st.error(f"Error in revenue analysis: {str(e)}")
        return {}

def create_action_plan(user_query, market_analysis, revenue_insights):
    """Create comprehensive action plan"""
    try:
        plan = {
            'immediate_actions': [],
            'short_term': [],
            'long_term': [],
            'resources_needed': [],
            'risks': [],
            'opportunities': [],
            'timeline': {}
        }
        
        # Immediate actions based on market analysis
        if market_analysis.get('market_saturation', 0) > 0.7:
            plan['immediate_actions'].append("Focus on unique differentiation and competitive advantages")
            plan['risks'].append("High competition - need strong unique value proposition")
            plan['opportunities'].append("Established market with proven demand")
        else:
            plan['immediate_actions'].append("Validate market demand through customer interviews")
            plan['risks'].append("Unproven market - need extensive validation")
            plan['opportunities'].append("First-mover advantage in emerging market")
        
        if market_analysis.get('validation_score', 0) > 0.5:
            plan['immediate_actions'].append("Study successful competitors and their strategies")
            plan['short_term'].append("Analyze competitor pricing and feature sets")
        else:
            plan['immediate_actions'].append("Pioneer the market space with innovative approach")
            plan['short_term'].append("Build MVP and gather early user feedback")
        
        # Revenue strategy
        if revenue_insights.get('top_model'):
            top_model = revenue_insights['top_model']
            plan['immediate_actions'].append(f"Research {top_model} business models in your space")
            plan['short_term'].append(f"Develop {top_model} pricing strategy")
        
        # Resource requirements
        plan['resources_needed'].extend([
            "Market research budget",
            "Development team or technical co-founder",
            "Legal consultation for business structure",
            "Marketing and customer acquisition budget"
        ])
        
        # Timeline
        plan['timeline'] = {
            'week_1_2': "Market validation and customer interviews",
            'week_3_4': "MVP development and testing",
            'month_2_3': "Beta launch and user feedback collection",
            'month_4_6': "Full launch and marketing campaign"
        }
        
        return plan
    
    except Exception as e:
        st.error(f"Error creating action plan: {str(e)}")
        return {}

# ============================================================================
# ENHANCED AGENTIC ENGAGEMENT ANALYSIS SYSTEM
# ============================================================================

def analyze_technology_stack(project):
    """Deep technology stack analysis for a project"""
    try:
        description = str(project.get('description', '')).lower()
        title = str(project.get('title', '')).lower()
        text = f"{description} {title}"
        
        # Technology stack detection patterns
        tech_patterns = {
            'Frontend': ['react', 'vue', 'angular', 'html', 'css', 'javascript', 'typescript', 'frontend', 'ui', 'ux'],
            'Backend': ['python', 'node', 'java', 'go', 'rust', 'backend', 'api', 'server', 'database'],
            'AI/ML': ['ai', 'ml', 'machine learning', 'artificial intelligence', 'tensorflow', 'pytorch', 'model'],
            'Mobile': ['ios', 'android', 'mobile', 'app', 'react native', 'flutter', 'swift', 'kotlin'],
            'Cloud': ['aws', 'azure', 'gcp', 'cloud', 'docker', 'kubernetes', 'microservices'],
            'Data': ['data', 'analytics', 'visualization', 'etl', 'pipeline', 'warehouse', 'sql'],
            'Blockchain': ['blockchain', 'crypto', 'web3', 'ethereum', 'smart contract', 'defi'],
            'IoT': ['iot', 'sensor', 'hardware', 'embedded', 'arduino', 'raspberry pi']
        }
        
        detected_tech = {}
        for category, keywords in tech_patterns.items():
            matches = sum(1 for keyword in keywords if keyword in text)
            if matches > 0:
                detected_tech[category] = {
                    'confidence': min(matches * 20, 100),
                    'keywords_found': [kw for kw in keywords if kw in text]
                }
        
        # Business model detection
        business_patterns = {
            'SaaS': ['saas', 'subscription', 'software as a service', 'monthly', 'recurring'],
            'Marketplace': ['marketplace', 'platform', 'connect', 'buyers', 'sellers'],
            'E-commerce': ['ecommerce', 'online store', 'shop', 'retail', 'payment'],
            'Freemium': ['freemium', 'free trial', 'premium', 'upgrade'],
            'Enterprise': ['enterprise', 'b2b', 'business', 'corporate', 'solution']
        }
        
        business_model = None
        max_confidence = 0
        for model, keywords in business_patterns.items():
            matches = sum(1 for keyword in keywords if keyword in text)
            confidence = matches * 25
            if confidence > max_confidence:
                max_confidence = confidence
                business_model = model
        
        return {
            'tech_stack': detected_tech,
            'business_model': business_model,
            'model_confidence': max_confidence,
            'complexity_score': len(detected_tech) * 15,
            'innovation_level': 'High' if len(detected_tech) >= 3 else 'Medium' if len(detected_tech) >= 2 else 'Low'
        }
    
    except Exception as e:
        return {'error': str(e), 'tech_stack': {}, 'business_model': 'Unknown'}

def generate_engagement_strategies(project, user_query, similarity_score):
    """Generate specific collaboration opportunities and engagement strategies"""
    try:
        analysis = analyze_technology_stack(project)
        
        strategies = {
            'collaboration_opportunities': [],
            'learning_opportunities': [],
            'networking_strategies': [],
            'partnership_potential': 'Low'
        }
        
        # Collaboration opportunities based on similarity and tech stack
        if similarity_score > 0.7:
            strategies['collaboration_opportunities'].extend([
                "🤝 Direct collaboration - High similarity suggests potential for joint development",
                "📊 Knowledge sharing sessions - Exchange insights and methodologies",
                "🔄 Cross-promotion opportunities - Leverage similar audiences"
            ])
            strategies['partnership_potential'] = 'High'
        elif similarity_score > 0.4:
            strategies['collaboration_opportunities'].extend([
                "💡 Complementary features - Identify areas for mutual enhancement",
                "🎯 Market insights exchange - Share market research and user feedback",
                "🛠️ Technical consultancy - Offer expertise in your specialized areas"
            ])
            strategies['partnership_potential'] = 'Medium'
        else:
            strategies['collaboration_opportunities'].extend([
                "🌱 Long-term relationship building - Plant seeds for future opportunities",
                "📚 Case study development - Document different approaches to similar problems"
            ])
        
        # Learning opportunities based on tech stack
        for tech, details in analysis['tech_stack'].items():
            strategies['learning_opportunities'].append(
                f"📖 Learn {tech} implementation - {len(details['keywords_found'])} relevant technologies detected"
            )
        
        # Networking strategies
        if project.get('github_url'):
            strategies['networking_strategies'].append("💻 Contribute to their open source repository")
        if project.get('project_url'):
            strategies['networking_strategies'].append("🌐 Engage with their community through their website")
        
        strategies['networking_strategies'].extend([
            "📧 Reach out via professional networks (LinkedIn, Twitter)",
            "🎤 Propose joint speaking opportunities at conferences",
            "📝 Collaborate on technical blog posts or research papers"
        ])
        
        return strategies
    
    except Exception as e:
        return {'error': str(e), 'collaboration_opportunities': [], 'learning_opportunities': []}

def create_engagement_timeline(project, user_query, strategies):
    """Create realistic engagement timelines with actionable steps"""
    try:
        timeline = {
            'immediate_actions': [],
            'week_1_2': [],
            'month_1': [],
            'month_3': [],
            'month_6': []
        }
        
        # Immediate actions (Next 24-48 hours)
        timeline['immediate_actions'] = [
            "🔍 Research the project team and their background",
            "📊 Analyze their market positioning and unique value proposition",
            "📋 Prepare a value proposition for potential collaboration"
        ]
        
        if project.get('project_url'):
            timeline['immediate_actions'].append("🌐 Visit and thoroughly explore their website/platform")
        if project.get('github_url'):
            timeline['immediate_actions'].append("💻 Review their codebase and contribution guidelines")
        
        # Week 1-2 actions
        timeline['week_1_2'] = [
            "📧 Draft initial outreach message highlighting mutual interests",
            "🤝 Identify specific collaboration opportunities",
            "📈 Prepare a brief presentation of your project's complementary aspects"
        ]
        
        # Month 1 actions
        timeline['month_1'] = [
            "📞 Schedule introductory call or video meeting",
            "📊 Share detailed project overview and explore synergies",
            "🎯 Define potential collaboration scope and objectives"
        ]
        
        # Month 3 actions
        timeline['month_3'] = [
            "🚀 Launch pilot collaboration or joint initiative",
            "📈 Establish regular communication and progress tracking",
            "🔄 Iterate based on initial collaboration results"
        ]
        
        # Month 6 actions
        timeline['month_6'] = [
            "📊 Evaluate collaboration outcomes and ROI",
            "🌟 Explore expanded partnership opportunities",
            "📢 Consider joint marketing or community initiatives"
        ]
        
        return timeline
    
    except Exception as e:
        return {'error': str(e), 'immediate_actions': []}

def generate_competitive_intelligence(project, similar_projects, user_query):
    """Provide detailed competitive analysis and differentiation strategies"""
    try:
        analysis = analyze_technology_stack(project)
        
        intelligence = {
            'competitive_position': 'Unknown',
            'differentiation_opportunities': [],
            'market_gaps': [],
            'strategic_advantages': [],
            'risk_factors': []
        }
        
        # Analyze competitive position
        tech_complexity = analysis.get('complexity_score', 0)
        if tech_complexity > 60:
            intelligence['competitive_position'] = 'Technology Leader'
            intelligence['strategic_advantages'].append("🔬 Advanced technology stack")
        elif tech_complexity > 30:
            intelligence['competitive_position'] = 'Technology Follower'
        else:
            intelligence['competitive_position'] = 'Niche Player'
        
        # Differentiation opportunities
        intelligence['differentiation_opportunities'] = [
            "🎯 Focus on underserved market segments",
            "⚡ Improve user experience and interface design",
            "📱 Expand to additional platforms or channels",
            "🔧 Add specialized features for specific use cases",
            "🌍 Target different geographical markets"
        ]
        
        # Market gaps analysis
        intelligence['market_gaps'] = [
            "💰 Pricing strategy optimization opportunities",
            "🎨 Enhanced customization and personalization",
            "🔗 Better integration with existing tools",
            "📊 Advanced analytics and reporting features",
            "🛡️ Enhanced security and compliance features"
        ]
        
        # Risk factors
        intelligence['risk_factors'] = [
            "⚠️ Market saturation in core segments",
            "💸 Potential price competition",
            "🔄 Technology obsolescence risk",
            "🏢 Large competitor market entry",
            "📋 Regulatory or compliance changes"
        ]
        
        return intelligence
    
    except Exception as e:
        return {'error': str(e), 'competitive_position': 'Unknown'}

def create_actionable_next_steps(project, user_query, engagement_strategies, timeline):
    """Generate concrete, actionable next steps for project engagement"""
    try:
        next_steps = {
            'priority_actions': [],
            'resource_requirements': [],
            'success_metrics': [],
            'risk_mitigation': []
        }
        
        # Priority actions (ranked by importance and feasibility)
        next_steps['priority_actions'] = [
            {
                'action': '🔍 Conduct deep project analysis',
                'description': 'Research team, technology, market position, and funding status',
                'effort': 'Low',
                'impact': 'High',
                'timeframe': '1-2 days'
            },
            {
                'action': '📧 Craft personalized outreach message',
                'description': 'Highlight specific value propositions and collaboration opportunities',
                'effort': 'Medium',
                'impact': 'High',
                'timeframe': '1 week'
            },
            {
                'action': '🤝 Propose specific collaboration',
                'description': 'Present concrete collaboration proposal with clear benefits',
                'effort': 'High',
                'impact': 'Very High',
                'timeframe': '2-4 weeks'
            }
        ]
        
        # Resource requirements
        next_steps['resource_requirements'] = [
            "⏰ Time investment: 5-10 hours for initial research and outreach",
            "👥 Team involvement: Business development and technical leads",
            "💰 Budget: Minimal for initial engagement, potential costs for collaboration",
            "🛠️ Tools: CRM system, communication platforms, project management tools"
        ]
        
        # Success metrics
        next_steps['success_metrics'] = [
            "📈 Response rate to initial outreach (target: >30%)",
            "🤝 Number of meaningful conversations initiated (target: 2-3)",
            "📊 Collaboration proposals developed (target: 1-2)",
            "⚡ Time to first meaningful engagement (target: <2 weeks)"
        ]
        
        # Risk mitigation strategies
        next_steps['risk_mitigation'] = [
            "📋 Prepare alternative collaboration models if initial approach fails",
            "🔄 Maintain pipeline of multiple potential partners",
            "⚖️ Ensure legal frameworks are in place for any collaboration",
            "📊 Define clear success criteria and exit strategies"
        ]
        
        return next_steps
    
    except Exception as e:
        return {'error': str(e), 'priority_actions': []}

# Main application
def main():
    # Professional header
    st.markdown('<h1 class="main-header">🚀 Project Explorer Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Venture Intelligence Platform - Discover, Analyze & Launch Your Next Big Idea</p>', unsafe_allow_html=True)
    
    # Automatically load data on app startup
    if 'df' not in st.session_state:
        with st.spinner("📊 Loading project data..."):
            df = load_enhanced_data()
            if df is not None:
                st.session_state.df = df
                st.success(f"✅ Loaded {len(df)} projects successfully!")
            else:
                st.error("❌ Failed to load project data. Please check the file path.")
                return
    
    # Sidebar for navigation
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        page = st.selectbox(
            "Choose your analysis:",
            ["🏠 Landing Page", "🔍 AI Idea Matcher", "📊 Market Intelligence", "📈 Analytics Dashboard", "🛠️ CSV Analyzer"]
        )
        
        st.markdown("---")
        st.markdown("## 📊 Quick Stats")
        if 'df' in st.session_state and st.session_state.df is not None:
            df = st.session_state.df
            st.metric("Total Projects", len(df))
            
            # Safely check for category column
            if 'category' in df.columns:
                st.metric("Categories", df['category'].nunique())
            else:
                st.metric("Categories", 0)
            
            # Safely check for github_url column
            if 'github_url' in df.columns:
                st.metric("With GitHub", df['github_url'].notna().sum())
            else:
                st.metric("With GitHub", 0)
    
    # Page routing
    if page == "🏠 Landing Page":
        show_landing_page()
    elif page == "🔍 AI Idea Matcher":
        show_ai_matcher()
    elif page == "📊 Market Intelligence":
        show_market_intelligence()
    elif page == "📈 Analytics Dashboard":
        show_analytics_dashboard()
    elif page == "🛠️ CSV Analyzer":
        show_csv_analyzer()

def show_landing_page():
    """Professional landing page"""
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h2 style="color: white; margin-bottom: 2rem;">🎯 Transform Your Ideas Into Successful Ventures</h2>
        <p style="font-size: 1.2rem; color: #ccc; margin-bottom: 3rem;">
            The world's most comprehensive platform for project discovery, market validation, and venture intelligence.
            Whether you're a startup founder, investor, or innovator, find your next opportunity here.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="insight-card">
            <h3>🤖 AI-Powered Matching</h3>
            <p>Advanced algorithms find the most relevant projects and opportunities for your ideas.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-card">
            <h3>📊 Market Intelligence</h3>
            <p>Comprehensive market analysis, competitive landscape, and revenue potential insights.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="warning-card">
            <h3>🚀 Action Planning</h3>
            <p>Get personalized action plans, timelines, and resource recommendations for your venture.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h3 style="color: white;">Ready to Explore?</h3>
        <p style="color: #ccc;">Your project data is automatically loaded! Start with our AI Idea Matcher to discover opportunities.</p>
    </div>
    """, unsafe_allow_html=True)

def show_ai_matcher():
    """Enhanced AI Idea Matcher"""
    st.markdown("## 🤖 AI Project Idea Matcher")
    st.markdown("### Discover Similar Projects & Market Opportunities")
    
    # Automatically load data from the specific path
    if 'df' not in st.session_state:
        with st.spinner("📊 Loading project data..."):
            df = load_enhanced_data()
            if df is not None:
                st.session_state.df = df
                st.success(f"✅ Loaded {len(df)} projects successfully!")
            else:
                st.error("❌ Failed to load project data. Please check the file path.")
                return
    
    if 'df' in st.session_state and st.session_state.df is not None:
        df = st.session_state.df
        
        # Enhanced input interface
        st.markdown("""
        <div class="insight-card">
            <h3>💡 Describe Your Project Idea</h3>
            <p>Be specific about your technology, target audience, and key features for better matches.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            user_query = st.text_area(
                "Your project idea (2-3 sentences):",
                placeholder="Example: I want to build a mobile app for real estate agents that uses AI to help with property management and client communication. The app should include features like automated property matching, client scheduling, and market analysis tools.",
                height=120
            )
        
        with col2:
            st.markdown("### 💡 Tips for Better Matches")
            st.markdown("""
            - **Be specific** about technology, industry, or features
            - **Mention your target audience** or use case
            - **Include key functionality** you want to build
            - **Describe the problem** you're solving
            """)
        
        if st.button("🔍 Find Similar Projects", type="primary", use_container_width=True):
            if user_query.strip():
                st.session_state.user_idea = user_query
                
                with st.spinner("🤖 Analyzing your idea and finding similar projects..."):
                    # Find similar projects
                    similar_projects = find_similar_projects_enhanced(user_query, df, top_k=5)
                    
                    if similar_projects:
                        st.session_state.analysis_results = {
                            'similar_projects': similar_projects,
                            'user_query': user_query
                        }
                        
                        st.success(f"✅ Found {len(similar_projects)} similar projects!")
                        
                        # Display results in professional cards
                        display_project_matches(similar_projects, user_query)
                        
                        # Show market intelligence
                        show_market_intelligence_results(similar_projects, user_query)
                    else:
                        st.warning("No similar projects found. Try being more specific or upload different data.")

def display_project_matches(similar_projects, user_query):
    """Enhanced display with agentic engagement analysis"""
    st.markdown("---")
    st.markdown("## 🎯 AI-Powered Project Analysis & Engagement Strategy")
    
    # User query display
    st.markdown(f"""
    <div class="insight-card">
        <h3>🎯 Your Project Idea:</h3>
        <p style="font-size: 1.1rem; line-height: 1.6;">{user_query}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display enhanced matches with agentic analysis
    for i, project in enumerate(similar_projects):
        similarity_score = project.get('similarity_score', 0)
        similarity_percentage = similarity_score * 100
        
        # Run agentic analysis
        with st.spinner(f"🤖 Running deep analysis for {project.get('title', 'Project')}..."):
            tech_analysis = analyze_technology_stack(project)
            engagement_strategies = generate_engagement_strategies(project, user_query, similarity_score)
            timeline = create_engagement_timeline(project, user_query, engagement_strategies)
            competitive_intel = generate_competitive_intelligence(project, similar_projects, user_query)
            next_steps = create_actionable_next_steps(project, user_query, engagement_strategies, timeline)
        
        # Project header
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 1rem; padding: 2rem; margin: 2rem 0; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h2 style="margin: 0;">🎯 Match #{i + 1}: {project.get('title', 'Unknown')}</h2>
                <div style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 2rem; font-weight: bold;">
                    {similarity_percentage:.1f}% Match
                </div>
            </div>
            <p style="margin: 0; opacity: 0.9;">Partnership Potential: <strong>{engagement_strategies.get('partnership_potential', 'Unknown')}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for different analysis sections
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Project Overview", 
            "🔬 Technology Analysis", 
            "🤝 Engagement Strategy", 
            "⏰ Action Timeline", 
            "🎯 Competitive Intelligence", 
            "🚀 Next Steps"
        ])
        
        with tab1:
            # Basic project information
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📋 Project Details")
                st.write(f"**Category:** {project.get('category', 'Uncategorized')}")
                st.write(f"**Subcategory:** {project.get('subcategory_1', 'General')}")
                st.write(f"**Business Model:** {tech_analysis.get('business_model', 'Unknown')}")
                st.write(f"**Innovation Level:** {tech_analysis.get('innovation_level', 'Unknown')}")
            
            with col2:
                st.markdown("### 📈 Analysis Metrics")
                coords = project.get('umap_coords', (0, 0, 0))
                st.write(f"**UMAP Position:** ({coords[0]:.3f}, {coords[1]:.3f}, {coords[2]:.3f})")
                st.write(f"**Complexity Score:** {tech_analysis.get('complexity_score', 0)}/100")
                st.write(f"**Competitive Position:** {competitive_intel.get('competitive_position', 'Unknown')}")
            
            # Description
            st.markdown("### 📝 Project Description")
            description = project.get('description', 'No description available')
            st.info(description[:500] + ('...' if len(description) > 500 else ''))
            
            # Links
            col1, col2 = st.columns(2)
            with col1:
                if project.get('project_url') and pd.notna(project['project_url']) and project['project_url'] != '':
                    st.link_button("🌐 Visit Project Website", project['project_url'])
                else:
                    st.button("❌ No URL Available", disabled=True, key=f"no_project_url_{i}")
            
            with col2:
                if project.get('github_url'):
                    st.link_button("📚 View on GitHub", project['github_url'])
                else:
                    st.button("❌ No GitHub URL", disabled=True, key=f"no_github_url_{i}")
        
        with tab2:
            st.markdown("### 🔬 Technology Stack Analysis")
            
            tech_stack = tech_analysis.get('tech_stack', {})
            if tech_stack:
                for tech_category, details in tech_stack.items():
                    with st.expander(f"🛠️ {tech_category} - {details['confidence']}% Confidence"):
                        st.write(f"**Keywords Found:** {', '.join(details['keywords_found'])}")
                        st.progress(details['confidence'] / 100)
            else:
                st.info("No specific technology stack detected from project description.")
            
            # Business model insights
            if tech_analysis.get('business_model'):
                st.markdown("### 💼 Business Model Analysis")
                st.success(f"**Detected Model:** {tech_analysis['business_model']} ({tech_analysis.get('model_confidence', 0)}% confidence)")
        
        with tab3:
            st.markdown("### 🤝 Engagement Strategy Recommendations")
            
            # Collaboration opportunities
            st.markdown("#### 🤝 Collaboration Opportunities")
            for opportunity in engagement_strategies.get('collaboration_opportunities', []):
                st.write(f"• {opportunity}")
            
            # Learning opportunities
            if engagement_strategies.get('learning_opportunities'):
                st.markdown("#### 📚 Learning Opportunities")
                for learning in engagement_strategies['learning_opportunities']:
                    st.write(f"• {learning}")
            
            # Networking strategies
            st.markdown("#### 🌐 Networking Strategies")
            for strategy in engagement_strategies.get('networking_strategies', []):
                st.write(f"• {strategy}")
        
        with tab4:
            st.markdown("### ⏰ Realistic Engagement Timeline")
            
            # Immediate actions
            st.markdown("#### 🚨 Immediate Actions (24-48 hours)")
            for action in timeline.get('immediate_actions', []):
                st.write(f"• {action}")
            
            # Short-term actions
            st.markdown("#### 📅 Week 1-2")
            for action in timeline.get('week_1_2', []):
                st.write(f"• {action}")
            
            # Medium-term actions
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📆 Month 1")
                for action in timeline.get('month_1', []):
                    st.write(f"• {action}")
            
            with col2:
                st.markdown("#### 📈 Month 3")
                for action in timeline.get('month_3', []):
                    st.write(f"• {action}")
            
            # Long-term actions
            st.markdown("#### 🎯 Month 6")
            for action in timeline.get('month_6', []):
                st.write(f"• {action}")
        
        with tab5:
            st.markdown("### 🎯 Competitive Intelligence")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏆 Strategic Advantages")
                for advantage in competitive_intel.get('strategic_advantages', []):
                    st.success(advantage)
                
                st.markdown("#### 🎯 Differentiation Opportunities")
                for diff in competitive_intel.get('differentiation_opportunities', []):
                    st.info(diff)
            
            with col2:
                st.markdown("#### 🔍 Market Gaps")
                for gap in competitive_intel.get('market_gaps', []):
                    st.write(f"💡 {gap}")
                
                st.markdown("#### ⚠️ Risk Factors")
                for risk in competitive_intel.get('risk_factors', []):
                    st.warning(risk)
        
        with tab6:
            st.markdown("### 🚀 Actionable Next Steps")
            
            # Priority actions
            st.markdown("#### 🎯 Priority Actions")
            for action_item in next_steps.get('priority_actions', []):
                with st.expander(f"{action_item['action']} - {action_item['impact']} Impact"):
                    st.write(f"**Description:** {action_item['description']}")
                    st.write(f"**Effort Required:** {action_item['effort']}")
                    st.write(f"**Timeframe:** {action_item['timeframe']}")
            
            # Resource requirements
            st.markdown("#### 🛠️ Resource Requirements")
            for requirement in next_steps.get('resource_requirements', []):
                st.write(f"• {requirement}")
            
            # Success metrics
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 📊 Success Metrics")
                for metric in next_steps.get('success_metrics', []):
                    st.write(f"• {metric}")
            
            with col2:
                st.markdown("#### 🛡️ Risk Mitigation")
                for risk_mitigation in next_steps.get('risk_mitigation', []):
                    st.write(f"• {risk_mitigation}")
        
        st.markdown("---")
        st.markdown("---")

def show_market_intelligence_results(similar_projects, user_query):
    """Show market intelligence results"""
    st.markdown("## 📊 Market Intelligence Analysis")
    
    # Analyze market data
    market_analysis = analyze_market_validation(similar_projects, user_query)
    revenue_insights = generate_revenue_insights(similar_projects, user_query)
    action_plan = create_action_plan(user_query, market_analysis, revenue_insights)
    
    if market_analysis:
        # Market validation metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Market Saturation", f"{market_analysis.get('market_saturation', 0):.1%}")
        
        with col2:
            st.metric("Opportunity Score", f"{market_analysis.get('opportunity_score', 0):.1%}")
        
        with col3:
            st.metric("Competition Level", market_analysis.get('competition_level', 'Unknown'))
        
        with col4:
            st.metric("Market Maturity", market_analysis.get('market_maturity', 'Unknown'))
        
        # Market opportunity gauge
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=market_analysis.get('opportunity_score', 0) * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Market Opportunity", 'font': {'size': 20}},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Revenue insights
        if revenue_insights:
            st.markdown("### 💰 Revenue Potential")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if revenue_insights.get('revenue_models'):
                    fig = px.bar(
                        x=list(revenue_insights['revenue_models'].keys()),
                        y=list(revenue_insights['revenue_models'].values()),
                        title="Revenue Models in Similar Projects",
                        labels={'x': 'Revenue Model', 'y': 'Number of Projects'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 💡 Revenue Recommendations")
                if revenue_insights.get('top_model'):
                    st.success(f"**Most Common Model:** {revenue_insights['top_model'].title()}")
                    st.info(f"**Revenue Potential:** {revenue_insights.get('revenue_potential', 'Unknown')}")
                    st.info(f"**Estimated Market Size:** ${revenue_insights.get('market_size_estimate', 0):,.0f}")
        
        # Action plan
        if action_plan:
            st.markdown("### 🚀 Action Plan")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### ✅ Immediate Actions")
                for action in action_plan.get('immediate_actions', []):
                    st.write(f"• {action}")
            
            with col2:
                st.markdown("#### ⚠️ Potential Risks")
                for risk in action_plan.get('risks', []):
                    st.write(f"• {risk}")
            
            # Download action plan
            if st.button("📥 Download Action Plan", type="primary"):
                action_plan_text = f"""
# Action Plan for: {user_query}

## Immediate Actions:
{chr(10).join([f"- {action}" for action in action_plan.get('immediate_actions', [])])}

## Short Term Goals:
{chr(10).join([f"- {goal}" for goal in action_plan.get('short_term', [])])}

## Long Term Vision:
{chr(10).join([f"- {vision}" for vision in action_plan.get('long_term', [])])}

## Resources Needed:
{chr(10).join([f"- {resource}" for resource in action_plan.get('resources_needed', [])])}

## Risk Mitigation:
{chr(10).join([f"- {risk}" for risk in action_plan.get('risks', [])])}
                """
                
                st.download_button(
                    label="📥 Download Action Plan",
                    data=action_plan_text,
                    file_name="action_plan.md",
                    mime="text/markdown"
                )

def show_market_intelligence():
    """Dedicated market intelligence page"""
    st.markdown("## 📊 Market Intelligence Dashboard")
    st.markdown("### Comprehensive Market Analysis & Validation")
    
    if 'analysis_results' in st.session_state and st.session_state.analysis_results:
        similar_projects = st.session_state.analysis_results.get('similar_projects', [])
        user_query = st.session_state.analysis_results.get('user_query', '')
        
        if similar_projects:
            show_market_intelligence_results(similar_projects, user_query)
        else:
            st.warning("No analysis results available. Please use the AI Idea Matcher first.")
    else:
        st.info("Please use the AI Idea Matcher to generate market intelligence data.")

def show_analytics_dashboard():
    """Analytics dashboard"""
    st.markdown("## 📈 Analytics Dashboard")
    st.markdown("### Project Data Insights & Trends")
    
    if 'df' in st.session_state and st.session_state.df is not None:
        df = st.session_state.df
        
        # Basic metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Projects", len(df))
        
        with col2:
            # Safely check for category column
            if 'category' in df.columns:
                st.metric("Categories", df['category'].nunique())
            else:
                st.metric("Categories", 0)
        
        with col3:
            # Safely check for project_url column
            if 'project_url' in df.columns:
                st.metric("With URLs", df['project_url'].notna().sum())
            else:
                st.metric("With URLs", 0)
        
        with col4:
            # Safely check for github_url column
            if 'github_url' in df.columns:
                st.metric("With GitHub", df['github_url'].notna().sum())
            else:
                st.metric("With GitHub", 0)
        
        # Category distribution
        if 'category' in df.columns:
            st.markdown("### 📊 Category Distribution")
            fig = px.pie(
                df, 
                names='category', 
                title="Projects by Category"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Category information not available in the dataset.")
        
        # 3D visualization
        st.markdown("### 🌐 3D Project Map")
        if 'category' in df.columns:
            fig = px.scatter_3d(
                df,
                x='x',
                y='y', 
                z='z',
                color='category',
                hover_data=['title', 'category'],
                title="3D Project Distribution"
            )
        else:
            fig = px.scatter_3d(
                df,
                x='x',
                y='y', 
                z='z',
                hover_data=['title'],
                title="3D Project Distribution"
            )
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.error("❌ No data available. Please ensure the CSV file exists at the specified path.")

def show_csv_analyzer():
    """CSV Analyzer Agent"""
    st.markdown("## 🛠️ CSV Analyzer Agent")
    st.markdown("### Intelligent Data Structure Analysis & Enhancement")
    
    uploaded_file = st.file_uploader(
        "📁 Upload CSV/Excel file for analysis",
        type=['csv', 'xlsx'],
        help="Upload any CSV or Excel file to analyze its structure and get recommendations"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ Loaded {len(df)} rows and {len(df.columns)} columns")
            
            # Basic data metrics
            st.markdown("### 📊 Data Overview")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Rows", len(df))
            
            with col2:
                st.metric("Columns", len(df.columns))
            
            with col3:
                st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            
            # Column analysis
            st.markdown("### 🔍 Column Analysis")
            
            column_analysis = []
            for col in df.columns:
                col_info = {
                    'column': col,
                    'type': str(df[col].dtype),
                    'null_count': df[col].isnull().sum(),
                    'null_percentage': (df[col].isnull().sum() / len(df)) * 100,
                    'unique_values': df[col].nunique(),
                    'sample_values': df[col].dropna().head(3).tolist()
                }
                column_analysis.append(col_info)
            
            # Display column analysis
            for col_info in column_analysis:
                with st.expander(f"📋 {col_info['column']} ({col_info['type']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Null values:** {col_info['null_count']} ({col_info['null_percentage']:.1f}%)")
                        st.write(f"**Unique values:** {col_info['unique_values']}")
                    
                    with col2:
                        st.write(f"**Sample values:** {col_info['sample_values']}")
            
            # Column mapping suggestions
            st.markdown("### 🎯 Column Mapping Suggestions")
            
            mapping_suggestions = {
                'title': ['name', 'title', 'project_name', 'project'],
                'description': ['description', 'desc', 'summary', 'details'],
                'category': ['category', 'type', 'domain', 'industry'],
                'subcategory_1': ['subcategory', 'sub_category', 'subtype'],
                'project_url': ['url', 'website', 'link', 'project_url'],
                'github_url': ['github', 'github_url', 'repo', 'repository'],
                'x': ['umap_x', 'x', 'dimension_1', 'coord_x'],
                'y': ['umap_y', 'y', 'dimension_2', 'coord_y'],
                'z': ['umap_z', 'z', 'dimension_3', 'coord_z']
            }
            
            suggested_mapping = {}
            for target_col, possible_names in mapping_suggestions.items():
                for col in df.columns:
                    if col.lower() in [name.lower() for name in possible_names]:
                        suggested_mapping[target_col] = col
                        break
            
            if suggested_mapping:
                st.success("✅ Suggested column mappings found!")
                for target, source in suggested_mapping.items():
                    st.write(f"**{target}** ← {source}")
            else:
                st.warning("⚠️ No automatic mappings found. Manual mapping may be required.")
            
            # Generate enhanced CSV
            if st.button("🚀 Generate Enhanced CSV", type="primary"):
                # Create enhanced dataframe
                enhanced_df = df.copy()
                
                # Apply suggested mappings
                for target, source in suggested_mapping.items():
                    if source in enhanced_df.columns:
                        enhanced_df[target] = enhanced_df[source]
                
                # Add metadata
                enhanced_df['analysis_date'] = datetime.now().strftime('%Y-%m-%d')
                enhanced_df['source_file'] = uploaded_file.name
                
                # Download enhanced CSV
                csv_data = enhanced_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Enhanced CSV",
                    data=csv_data,
                    file_name=f"enhanced_{uploaded_file.name}",
                    mime="text/csv"
                )
                
                st.success("✅ Enhanced CSV generated successfully!")
        
        except Exception as e:
            st.error(f"Error analyzing file: {str(e)}")

# Run the application
if __name__ == "__main__":
    main()
