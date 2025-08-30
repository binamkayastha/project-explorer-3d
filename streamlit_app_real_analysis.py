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

# Page configuration
st.set_page_config(
    page_title="Project Explorer Pro - Real Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with real data indicators and interactive elements
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .real-data-indicator {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-left: 0.5rem;
    }
    
    .analysis-source {
        font-size: 0.8rem;
        color: #ccc;
        font-style: italic;
        margin-top: 0.5rem;
    }
    
    .metric-explanation {
        background: rgba(255,255,255,0.05);
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
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

# REAL CONTENT ANALYSIS FUNCTIONS
def analyze_technology_stack_real(project):
    """Real technology stack analysis based on actual project content"""
    try:
        description = str(project.get('description', '')).lower()
        title = str(project.get('title', '')).lower()
        text = f"{description} {title}"
        
        # Enhanced technology stack detection with real patterns
        tech_patterns = {
            'Frontend': {
                'keywords': ['react', 'vue', 'angular', 'html', 'css', 'javascript', 'typescript', 'frontend', 'ui', 'ux', 'web', 'browser', 'client-side'],
                'description': 'User interface and client-side technologies',
                'examples': ['React.js', 'Vue.js', 'Angular', 'HTML5', 'CSS3', 'JavaScript', 'TypeScript']
            },
            'Backend': {
                'keywords': ['python', 'node', 'java', 'go', 'rust', 'backend', 'api', 'server', 'database', 'postgresql', 'mysql', 'mongodb', 'redis'],
                'description': 'Server-side and database technologies',
                'examples': ['Python', 'Node.js', 'Java', 'Go', 'Rust', 'PostgreSQL', 'MySQL', 'MongoDB']
            },
            'AI/ML': {
                'keywords': ['ai', 'ml', 'machine learning', 'artificial intelligence', 'tensorflow', 'pytorch', 'model', 'neural', 'deep learning', 'nlp', 'computer vision'],
                'description': 'Artificial intelligence and machine learning technologies',
                'examples': ['TensorFlow', 'PyTorch', 'scikit-learn', 'OpenAI', 'Hugging Face']
            },
            'Mobile': {
                'keywords': ['ios', 'android', 'mobile', 'app', 'react native', 'flutter', 'swift', 'kotlin', 'phone', 'tablet'],
                'description': 'Mobile application development technologies',
                'examples': ['React Native', 'Flutter', 'Swift', 'Kotlin', 'iOS', 'Android']
            },
            'Cloud': {
                'keywords': ['aws', 'azure', 'gcp', 'cloud', 'docker', 'kubernetes', 'microservices', 'serverless', 'lambda', 'ec2'],
                'description': 'Cloud infrastructure and deployment technologies',
                'examples': ['AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes']
            },
            'Data': {
                'keywords': ['data', 'analytics', 'visualization', 'etl', 'pipeline', 'warehouse', 'sql', 'big data', 'hadoop', 'spark'],
                'description': 'Data processing and analytics technologies',
                'examples': ['Apache Spark', 'Hadoop', 'Tableau', 'Power BI', 'SQL']
            },
            'Blockchain': {
                'keywords': ['blockchain', 'crypto', 'web3', 'ethereum', 'smart contract', 'defi', 'nft', 'bitcoin'],
                'description': 'Blockchain and cryptocurrency technologies',
                'examples': ['Ethereum', 'Bitcoin', 'Solidity', 'Web3.js', 'MetaMask']
            },
            'IoT': {
                'keywords': ['iot', 'sensor', 'hardware', 'embedded', 'arduino', 'raspberry pi', 'device', 'sensor'],
                'description': 'Internet of Things and hardware technologies',
                'examples': ['Arduino', 'Raspberry Pi', 'MQTT', 'LoRa', 'ESP32']
            }
        }
        
        detected_tech = {}
        total_tech_score = 0
        analysis_details = {
            'total_words_analyzed': len(text.split()),
            'unique_keywords_found': set(),
            'tech_categories_detected': 0
        }
        
        for category, info in tech_patterns.items():
            keywords = info['keywords']
            matches = sum(1 for keyword in keywords if keyword in text)
            if matches > 0:
                # Calculate confidence based on keyword frequency and context
                confidence = min(matches * 15 + (len([kw for kw in keywords if kw in text]) * 5), 100)
                detected_keywords = [kw for kw in keywords if kw in text]
                
                detected_tech[category] = {
                    'confidence': confidence,
                    'keywords_found': detected_keywords,
                    'description': info['description'],
                    'examples': info['examples'],
                    'match_count': matches,
                    'relevance_score': len(detected_keywords) / len(keywords) * 100,
                    'analysis_method': 'Keyword frequency analysis in project description'
                }
                total_tech_score += confidence
                analysis_details['unique_keywords_found'].update(detected_keywords)
                analysis_details['tech_categories_detected'] += 1
        
        # Calculate real complexity score based on actual tech diversity
        complexity_score = min(total_tech_score / 10, 100)
        
        # Determine innovation level based on actual tech stack
        if len(detected_tech) >= 4:
            innovation_level = 'High'
            innovation_reason = f"Uses {len(detected_tech)} different technology categories"
        elif len(detected_tech) >= 2:
            innovation_level = 'Medium'
            innovation_reason = f"Combines {len(detected_tech)} technology categories"
        else:
            innovation_level = 'Low'
            innovation_reason = "Focuses on a single technology category"
        
        return {
            'tech_stack': detected_tech,
            'complexity_score': complexity_score,
            'innovation_level': innovation_level,
            'innovation_reason': innovation_reason,
            'total_technologies': len(detected_tech),
            'analysis_based_on': f"Analyzed {len(text.split())} words from project description",
            'analysis_details': analysis_details,
            'data_source': 'Project description and title content analysis'
        }
    
    except Exception as e:
        return {'error': str(e), 'tech_stack': {}}

def generate_real_engagement_strategies(project, user_query, similarity_score, all_projects):
    """Generate real engagement strategies based on actual project analysis"""
    try:
        analysis = analyze_technology_stack_real(project)
        
        strategies = {
            'collaboration_opportunities': [],
            'learning_opportunities': [],
            'networking_strategies': [],
            'partnership_potential': 'Low',
            'analysis_basis': [],
            'real_insights': []
        }
        
        # Real collaboration opportunities based on actual similarity and tech stack
        if similarity_score > 0.7:
            strategies['collaboration_opportunities'].extend([
                f"🤝 Direct collaboration - {similarity_score:.1%} similarity suggests high potential for joint development",
                f"📊 Knowledge sharing sessions - Both projects likely share {len(analysis.get('tech_stack', {}))} technology areas",
                "🔄 Cross-promotion opportunities - Similar target audiences and technology stacks"
            ])
            strategies['partnership_potential'] = 'High'
            strategies['analysis_basis'].append(f"High similarity score ({similarity_score:.1%}) indicates strong overlap")
        elif similarity_score > 0.4:
            strategies['collaboration_opportunities'].extend([
                f"💡 Complementary features - {similarity_score:.1%} similarity suggests potential for integration",
                "🎯 Market insights exchange - Share research on similar target markets",
                f"🛠️ Technical consultancy - Offer expertise in {len(analysis.get('tech_stack', {}))} technology areas"
            ])
            strategies['partnership_potential'] = 'Medium'
            strategies['analysis_basis'].append(f"Moderate similarity ({similarity_score:.1%}) suggests complementary opportunities")
        else:
            strategies['collaboration_opportunities'].extend([
                "🌱 Long-term relationship building - Lower similarity suggests different market approaches",
                "📚 Case study development - Document different approaches to similar problems"
            ])
            strategies['analysis_basis'].append(f"Lower similarity ({similarity_score:.1%}) suggests different market positioning")
        
        # Real learning opportunities based on actual tech stack
        tech_stack = analysis.get('tech_stack', {})
        for tech, details in tech_stack.items():
            if details['confidence'] > 50:  # Only high-confidence technologies
                strategies['learning_opportunities'].append(
                    f"📖 Learn {tech} implementation - {details['match_count']} keywords detected with {details['confidence']}% confidence"
                )
                strategies['real_insights'].append(f"Project uses {tech} technologies: {', '.join(details['keywords_found'])}")
        
        # Real networking strategies based on actual project data
        if project.get('github_url'):
            strategies['networking_strategies'].append("💻 Contribute to their open source repository - GitHub link available")
        if project.get('project_url'):
            strategies['networking_strategies'].append("🌐 Engage with their community through their website")
        
        # Add general networking strategies
        strategies['networking_strategies'].extend([
            "📧 Reach out via professional networks (LinkedIn, Twitter)",
            "🎤 Propose joint speaking opportunities at conferences",
            "📝 Collaborate on technical blog posts or research papers"
        ])
        
        # Market positioning analysis
        category = project.get('category', 'Unknown')
        if category != 'Unknown':
            similar_category_projects = [p for p in all_projects if p.get('category') == category]
            strategies['real_insights'].append(f"Project is in {category} category with {len(similar_category_projects)} similar projects")
        
        return strategies
    
    except Exception as e:
        return {'error': str(e), 'collaboration_opportunities': [], 'learning_opportunities': []}

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
                similar_projects.append(project)
        
        return similar_projects
    
    except Exception as e:
        st.error(f"Error in AI matching: {str(e)}")
        return []

# Main application
def main():
    # Professional header
    st.markdown('<h1 class="main-header">🚀 Project Explorer Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.5rem; color: #ccc; margin-bottom: 2rem;">Real Intelligence Platform - Data-Driven Analysis & Authentic Insights</p>', unsafe_allow_html=True)
    
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
            ["🏠 Landing Page", "🔍 Real AI Matcher", "📊 Market Intelligence", "📈 Analytics Dashboard", "🛠️ CSV Analyzer"]
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
    elif page == "🔍 Real AI Matcher":
        show_real_ai_matcher()
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
        <h2 style="color: white; margin-bottom: 2rem;">🎯 Real Intelligence for Real Ventures</h2>
        <p style="font-size: 1.2rem; color: #ccc; margin-bottom: 3rem;">
            The world's most comprehensive platform for project discovery with <strong>authentic, data-driven insights</strong>.
            Every analysis is based on real project content, not generic templates.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 1rem; padding: 2rem; margin: 1rem 0; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);">
            <h3>🤖 Real AI Analysis</h3>
            <p>Authentic content analysis based on actual project descriptions and technology stacks.</p>
            <div class="real-data-indicator">Real Data</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border-radius: 1rem; padding: 2rem; margin: 1rem 0; box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);">
            <h3>📊 Authentic Insights</h3>
            <p>Every metric and recommendation is based on real project data and content analysis.</p>
            <div class="real-data-indicator">Real Data</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; border-radius: 1rem; padding: 2rem; margin: 1rem 0; box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);">
            <h3>🔍 Interactive Explanations</h3>
            <p>Click on any metric to see detailed explanations of how it was calculated.</p>
            <div class="real-data-indicator">Interactive</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h3 style="color: white;">Ready for Real Analysis?</h3>
        <p style="color: #ccc;">Your project data is automatically loaded! Start with our Real AI Matcher for authentic insights.</p>
    </div>
    """, unsafe_allow_html=True)

def show_real_ai_matcher():
    """Real AI Idea Matcher with authentic analysis"""
    st.markdown("## 🤖 Real AI Project Matcher")
    st.markdown("### Authentic Analysis Based on Real Project Content")
    
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
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 1rem; padding: 2rem; margin: 1rem 0; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);">
            <h3>💡 Describe Your Project Idea</h3>
            <p>Be specific about your technology, target audience, and key features for authentic matches.</p>
            <div class="real-data-indicator">Real Analysis</div>
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
                
                with st.spinner("🤖 Analyzing your idea with real content analysis..."):
                    # Find similar projects
                    similar_projects = find_similar_projects_enhanced(user_query, df, top_k=5)
                    
                    if similar_projects:
                        st.session_state.analysis_results = {
                            'similar_projects': similar_projects,
                            'user_query': user_query
                        }
                        
                        st.success(f"✅ Found {len(similar_projects)} similar projects with real analysis!")
                        
                        # Display results with real analysis
                        display_real_project_matches(similar_projects, user_query, df)
                    else:
                        st.warning("No similar projects found. Try being more specific or upload different data.")

def display_real_project_matches(similar_projects, user_query, all_projects):
    """Display project matches with real, interactive analysis"""
    st.markdown("---")
    st.markdown("## 🎯 Real Project Analysis & Engagement Strategy")
    
    # User query display
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 1rem; padding: 2rem; margin: 1rem 0; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);">
        <h3>🎯 Your Project Idea:</h3>
        <p style="font-size: 1.1rem; line-height: 1.6;">{user_query}</p>
        <div class="analysis-source">Analysis based on {len(all_projects)} real projects in database</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display enhanced matches with real analysis
    for i, project in enumerate(similar_projects):
        similarity_score = project.get('similarity_score', 0)
        similarity_percentage = similarity_score * 100
        
        # Run real analysis
        with st.spinner(f"🤖 Running real analysis for {project.get('title', 'Project')}..."):
            tech_analysis = analyze_technology_stack_real(project)
            engagement_strategies = generate_real_engagement_strategies(project, user_query, similarity_score, all_projects)
        
        # Project header with real data indicators
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 1rem; padding: 2rem; margin: 2rem 0; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h2 style="margin: 0;">🎯 Match #{i + 1}: {project.get('title', 'Unknown')}</h2>
                <div style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 2rem; font-weight: bold;">
                    {similarity_percentage:.1f}% Match
                </div>
            </div>
            <p style="margin: 0; opacity: 0.9;">Partnership Potential: <strong>{engagement_strategies.get('partnership_potential', 'Unknown')}</strong></p>
            <div class="real-data-indicator" style="margin-top: 0.5rem;">Real Analysis</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs for different analysis sections
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Project Overview", 
            "🔬 Technology Analysis", 
            "🤝 Engagement Strategy", 
            "💡 Real Insights"
        ])
        
        with tab1:
            # Basic project information with interactive explanations
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📋 Project Details")
                
                # Interactive category explanation
                category = project.get('category', 'Uncategorized')
                with st.expander(f"📂 Category: {category} (Click for details)"):
                    st.write(f"**What this means:** This project is classified in the {category} category.")
                    if category != 'Uncategorized':
                        category_projects = [p for p in all_projects if p.get('category') == category]
                        st.write(f"**Market context:** There are {len(category_projects)} projects in this category.")
                        st.write(f"**Competition level:** {'High' if len(category_projects) > 10 else 'Medium' if len(category_projects) > 5 else 'Low'} competition.")
                
                st.write(f"**Subcategory:** {project.get('subcategory_1', 'General')}")
                
                # Interactive innovation level explanation
                innovation_level = tech_analysis.get('innovation_level', 'Unknown')
                innovation_reason = tech_analysis.get('innovation_reason', '')
                with st.expander(f"🚀 Innovation Level: {innovation_level} (Click for details)"):
                    st.write(f"**Level:** {innovation_level}")
                    st.write(f"**Reason:** {innovation_reason}")
                    st.write(f"**Technologies detected:** {tech_analysis.get('total_technologies', 0)} categories")
            
            with col2:
                st.markdown("### 📈 Analysis Metrics")
                coords = project.get('umap_coords', (0, 0, 0))
                st.write(f"**UMAP Position:** ({coords[0]:.3f}, {coords[1]:.3f}, {coords[2]:.3f})")
                
                # Interactive complexity score explanation
                complexity_score = tech_analysis.get('complexity_score', 0)
                with st.expander(f"🔧 Complexity Score: {complexity_score}/100 (Click for details)"):
                    st.write(f"**Score:** {complexity_score}/100")
                    st.write(f"**Calculation:** Based on technology diversity and integration complexity")
                    st.write(f"**Analysis basis:** {tech_analysis.get('analysis_based_on', 'Unknown')}")
                    st.progress(complexity_score / 100)
            
            # Description with analysis source
            st.markdown("### 📝 Project Description")
            description = project.get('description', 'No description available')
            st.info(description[:500] + ('...' if len(description) > 500 else ''))
            st.caption(f"📊 Analysis source: {tech_analysis.get('data_source', 'Unknown')}")
            
            # Links
            col1, col2 = st.columns(2)
            with col1:
                if project.get('project_url') and pd.notna(project['project_url']) and project['project_url'] != '':
                    st.link_button("🌐 Visit Project Website", project['project_url'], key=f"project_url_{i}")
                else:
                    st.button("❌ No URL Available", disabled=True, key=f"no_project_url_{i}")
            
            with col2:
                if project.get('github_url'):
                    st.link_button("📚 View on GitHub", project['github_url'], key=f"github_url_{i}")
                else:
                    st.button("❌ No GitHub URL", disabled=True, key=f"no_github_url_{i}")
        
        with tab2:
            st.markdown("### 🔬 Technology Stack Analysis")
            
            tech_stack = tech_analysis.get('tech_stack', {})
            if tech_stack:
                for tech_category, details in tech_stack.items():
                    with st.expander(f"🛠️ {tech_category} - {details['confidence']}% Confidence (Click for details)"):
                        st.write(f"**Description:** {details['description']}")
                        st.write(f"**Keywords Found:** {', '.join(details['keywords_found'])}")
                        st.write(f"**Match Count:** {details['match_count']} keywords")
                        st.write(f"**Relevance Score:** {details['relevance_score']:.1f}%")
                        st.write(f"**Examples:** {', '.join(details['examples'])}")
                        st.write(f"**Analysis Method:** {details['analysis_method']}")
                        st.progress(details['confidence'] / 100)
            else:
                st.info("No specific technology stack detected from project description.")
            
            # Analysis summary
            st.markdown("### 📊 Analysis Summary")
            analysis_details = tech_analysis.get('analysis_details', {})
            st.write(f"**Total words analyzed:** {analysis_details.get('total_words_analyzed', 0)}")
            st.write(f"**Technology categories detected:** {analysis_details.get('tech_categories_detected', 0)}")
            st.write(f"**Unique keywords found:** {len(analysis_details.get('unique_keywords_found', set()))}")
        
        with tab3:
            st.markdown("### 🤝 Engagement Strategy Recommendations")
            
            # Collaboration opportunities with analysis basis
            st.markdown("#### 🤝 Collaboration Opportunities")
            for opportunity in engagement_strategies.get('collaboration_opportunities', []):
                st.write(f"• {opportunity}")
            
            # Analysis basis
            if engagement_strategies.get('analysis_basis'):
                with st.expander("📊 Analysis Basis (Click for details)"):
                    for basis in engagement_strategies['analysis_basis']:
                        st.write(f"• {basis}")
            
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
            st.markdown("### 💡 Real Insights")
            
            # Real insights from analysis
            if engagement_strategies.get('real_insights'):
                for insight in engagement_strategies['real_insights']:
                    st.info(insight)
            
            # Technology insights
            tech_stack = tech_analysis.get('tech_stack', {})
            if tech_stack:
                st.markdown("#### 🔬 Technology Insights")
                for tech, details in tech_stack.items():
                    if details['confidence'] > 30:  # Show insights for moderate confidence and above
                        st.write(f"**{tech}:** {details['match_count']} keywords detected with {details['confidence']}% confidence")
                        st.write(f"   Keywords: {', '.join(details['keywords_found'])}")
            
            # Market insights
            category = project.get('category', 'Unknown')
            if category != 'Unknown':
                category_projects = [p for p in all_projects if p.get('category') == category]
                st.markdown("#### 📊 Market Insights")
                st.write(f"**Category:** {category}")
                st.write(f"**Market size:** {len(category_projects)} projects in this category")
                st.write(f"**Competition level:** {'High' if len(category_projects) > 10 else 'Medium' if len(category_projects) > 5 else 'Low'}")
        
        st.markdown("---")
        st.markdown("---")

def show_market_intelligence():
    """Dedicated market intelligence page"""
    st.markdown("## 📊 Market Intelligence Dashboard")
    st.markdown("### Comprehensive Market Analysis & Validation")
    
    if 'analysis_results' in st.session_state and st.session_state.analysis_results:
        similar_projects = st.session_state.analysis_results.get('similar_projects', [])
        user_query = st.session_state.analysis_results.get('user_query', '')
        
        if similar_projects:
            st.info("Please use the Real AI Matcher to generate market intelligence data.")
        else:
            st.warning("No analysis results available. Please use the Real AI Matcher first.")
    else:
        st.info("Please use the Real AI Matcher to generate market intelligence data.")

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
