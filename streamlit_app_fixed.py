import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import re
import string

# Try to import optional dependencies
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    st.warning("⚠️ scikit-learn not available. AI matching features will be disabled.")

try:
    import nltk
    from nltk.corpus import stopwords
    NLTK_AVAILABLE = True
    # NLTK data downloads (with error handling)
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
    st.warning("⚠️ NLTK not available. Text processing features will be limited.")

# Page config
st.set_page_config(
    page_title="Project Explorer",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #00D4AA, #D946EF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .stPlotlyChart {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 0.5rem;
        padding: 1rem;
    }
    .upload-section {
        background: rgba(0, 212, 170, 0.1);
        padding: 2rem;
        border-radius: 1rem;
        border: 2px dashed rgba(0, 212, 170, 0.3);
        text-align: center;
        margin: 2rem 0;
    }
    .category-badge {
        background: linear-gradient(45deg, #00D4AA, #D946EF);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        display: inline-block;
        margin: 0.2rem;
        font-size: 0.8rem;
    }
    .project-link {
        color: #00D4AA;
        text-decoration: none;
        font-weight: bold;
    }
    .project-link:hover {
        color: #D946EF;
        text-decoration: underline;
    }
    .chatbot-container {
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.1), rgba(217, 70, 239, 0.1));
        border-radius: 1rem;
        padding: 2rem;
        border: 1px solid rgba(0, 212, 170, 0.3);
        margin: 2rem 0;
    }
    .chat-message {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #00D4AA;
    }
    .user-message {
        background: rgba(217, 70, 239, 0.1);
        border-left: 4px solid #D946EF;
    }
    .project-match {
        background: rgba(0, 212, 170, 0.1);
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(0, 212, 170, 0.3);
    }
    .similarity-score {
        background: linear-gradient(45deg, #00D4AA, #D946EF);
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# File upload section
st.markdown("---")
st.markdown("### 📁 Upload Your Project CSV File")
st.markdown("Upload your project data file to explore the 3D project space")

uploaded_file = st.file_uploader(
    "Choose your CSV file",
    type=['csv'],
    help="Upload your projects dataset"
)

# Load data function with duplicate column handling
@st.cache_data
def load_project_data(uploaded_file):
    """Load project data with proper column mapping and duplicate handling"""
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Handle duplicate column names
            if df.columns.duplicated().any():
                st.warning("⚠️ Found duplicate column names. Renaming duplicates...")
                # Get duplicate column names
                duplicates = df.columns[df.columns.duplicated()].unique()
                for dup_col in duplicates:
                    # Find all occurrences of this column
                    dup_indices = df.columns[df.columns == dup_col]
                    # Rename duplicates with suffix
                    for i, idx in enumerate(dup_indices[1:], 1):
                        df.columns.values[idx] = f"{dup_col}_{i}"
                st.success("✅ Duplicate columns renamed successfully!")
            
            # Map column names to expected format
            column_mapping = {
                'name': 'title',
                'project_url': 'project_url',
                'detailed_description': 'description',
                'cleaned_tag_category': 'category',
                'subcategory_1': 'subcategory_1',
                'subcategory_2': 'subcategory_2',
                'subcategory_3': 'subcategory_3',
                'umap_dim_1': 'x',
                'umap_dim_2': 'y',
                'umap_dim_3': 'z'
            }
            
            # Rename columns if they exist
            for old_col, new_col in column_mapping.items():
                if old_col in df.columns:
                    df = df.rename(columns={old_col: new_col})
            
            # Convert UMAP coordinates to numeric
            for col in ['x', 'y', 'z']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Clean category data
            if 'category' in df.columns:
                df['category'] = df['category'].fillna('Uncategorized')
            
            # Clean subcategory data
            for col in ['subcategory_1', 'subcategory_2', 'subcategory_3']:
                if col in df.columns:
                    df[col] = df[col].fillna('')
            
            st.success(f"✅ Successfully loaded {len(df)} projects!")
            return df
            
        except Exception as e:
            st.error(f"❌ Error loading CSV file: {str(e)}")
            return None
    return None

# AI Chatbot functions (only if dependencies available)
def preprocess_text(text):
    """Preprocess text for similarity matching"""
    if pd.isna(text) or text == '':
        return ''
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Simple tokenization
    tokens = text.split()
    
    # Remove stopwords if NLTK is available
    if NLTK_AVAILABLE:
        try:
            stop_words = set(stopwords.words('english'))
            tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
        except:
            tokens = [token for token in tokens if len(token) > 2]
    else:
        tokens = [token for token in tokens if len(token) > 2]
    
    return ' '.join(tokens)

def extract_github_url(description):
    """Extract GitHub URL from project description"""
    if pd.isna(description) or description == '':
        return None
    
    # Look for GitHub URLs in the description
    github_patterns = [
        r'https?://github\.com/[^\s\)]+',
        r'github\.com/[^\s\)]+',
        r'GitHub URL[:\s]*([^\s\)]+)',
        r'GitHub Repository[:\s]*([^\s\)]+)'
    ]
    
    for pattern in github_patterns:
        matches = re.findall(pattern, description, re.IGNORECASE)
        if matches:
            url = matches[0]
            if not url.startswith('http'):
                url = 'https://' + url
            return url
    
    return None

def find_similar_projects(user_query, df, top_k=3):
    """Find similar projects based on user query"""
    if df is None or len(df) == 0:
        return []
    
    if not SKLEARN_AVAILABLE:
        st.error("❌ AI matching not available. Please install scikit-learn: pip install scikit-learn")
        return []
    
    try:
        # Preprocess user query
        processed_query = preprocess_text(user_query)
        
        # Create combined text for each project
        project_texts = []
        for _, row in df.iterrows():
            combined_text = f"{row.get('title', '')} {row.get('description', '')} {row.get('category', '')} {row.get('subcategory_1', '')} {row.get('subcategory_2', '')} {row.get('subcategory_3', '')}"
            processed_text = preprocess_text(combined_text)
            project_texts.append(processed_text)
        
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(project_texts)
        query_vector = vectorizer.transform([processed_query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
        
        # Get top matches
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0:  # Only include relevant matches
                project = df.iloc[idx]
                github_url = extract_github_url(project.get('description', ''))
                
                results.append({
                    'title': project.get('title', ''),
                    'description': project.get('description', ''),
                    'category': project.get('category', ''),
                    'subcategory_1': project.get('subcategory_1', ''),
                    'project_url': project.get('project_url', ''),
                    'github_url': github_url,
                    'similarity_score': similarities[idx],
                    'umap_coords': (project.get('x', 0), project.get('y', 0), project.get('z', 0))
                })
        
        return results
    except Exception as e:
        st.error(f"Error in similarity matching: {str(e)}")
        return []

# Load data
df = load_project_data(uploaded_file)

if df is not None and len(df) > 0:
    # Google-style Landing Page
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 2rem; margin: 2rem 0;">
        <div style="margin-bottom: 2rem;">
            <h1 style="font-size: 4rem; font-weight: 300; color: #333; margin-bottom: 0.5rem;">Project Explorer</h1>
            <div style="font-size: 1.5rem; color: #666; margin-bottom: 2rem;">Discover Similar Projects & Find Your Next Big Idea</div>
            <div style="display: inline-block; background: linear-gradient(45deg, #4285f4, #34a853, #fbbc05, #ea4335); padding: 1rem; border-radius: 50%; margin-bottom: 2rem;">
                <span style="font-size: 3rem;">🌐</span>
            </div>
        </div>
        
        <div style="max-width: 600px; margin: 0 auto; background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <h2 style="color: #333; margin-bottom: 1rem;">🚀 What's Your Project Idea?</h2>
            <p style="color: #666; margin-bottom: 1rem;">Describe your idea in 2 sentences and we'll find the most similar projects to inspire you.</p>
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
                <strong>💡 Example:</strong> "I want to build a mobile app for real estate agents that uses AI to help with property management and client communication. The app should include features like automated property matching, client scheduling, and market analysis tools."
            </div>
            <div style="display: flex; gap: 1rem; justify-content: center; margin-top: 1rem;">
                <span style="background: #4285f4; color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; font-size: 0.9rem;">🔍 AI-Powered Matching</span>
                <span style="background: #34a853; color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; font-size: 0.9rem;">📊 3D Visualization</span>
                <span style="background: #fbbc05; color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; font-size: 0.9rem;">🌐 Project Links</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Idea Matching Section
    st.markdown("---")
    st.markdown("### 🤖 AI Project Idea Matcher")
    st.markdown("**Tell us about your idea and we'll find the most relevant projects:**")
    
    with st.container():
        st.markdown("""
        <div class="chatbot-container">
            <h3>💡 How it works:</h3>
            <ul>
                <li>Describe your project idea in 2 sentences</li>
                <li>Our AI analyzes your description and finds similar projects</li>
                <li>Get project URLs, GitHub links, and detailed descriptions</li>
                <li>See similarity scores to understand how well each project matches</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced chat interface
        col1, col2 = st.columns([2, 1])
        
        with col1:
            user_query = st.text_area(
                "Describe your project idea (2 sentences):",
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
                with st.spinner("🤖 Analyzing your idea and finding similar projects..."):
                    # Find similar projects
                    similar_projects = find_similar_projects(user_query, df, top_k=3)
                    
                    if similar_projects:
                        st.success(f"✅ Found {len(similar_projects)} similar projects!")
                        
                        # Display user query in a beautiful card
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 1rem; margin: 2rem 0;">
                            <h3 style="margin-bottom: 1rem;">🎯 Your Project Idea:</h3>
                            <p style="font-size: 1.1rem; line-height: 1.6;">{user_query}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display bot response
                        st.markdown(f"""
                        <div class="chat-message">
                            <strong>🤖 AI Assistant:</strong> I found {len(similar_projects)} projects that closely match your idea! 
                            Here are the best matches with their details:
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display project matches in beautiful cards
                        for i, project in enumerate(similar_projects):
                            similarity_percentage = project['similarity_score'] * 100
                            
                            st.markdown(f"""
                            <div style="background: white; border: 2px solid #e0e0e0; border-radius: 1rem; padding: 2rem; margin: 1rem 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                                    <h3 style="color: #333; margin: 0;">🎯 Match #{i + 1}: {project['title']}</h3>
                                    <div style="background: linear-gradient(45deg, #00D4AA, #D946EF); color: white; padding: 0.5rem 1rem; border-radius: 2rem; font-weight: bold;">
                                        {similarity_percentage:.1f}% Match
                                    </div>
                                </div>
                                
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                                    <div>
                                        <strong>Category:</strong> {project['category']}<br>
                                        <strong>Subcategory:</strong> {project['subcategory_1'] if project['subcategory_1'] else 'N/A'}
                                    </div>
                                    <div>
                                        <strong>UMAP Coordinates:</strong><br>
                                        ({project['umap_coords'][0]:.3f}, {project['umap_coords'][1]:.3f}, {project['umap_coords'][2]:.3f})
                                    </div>
                                </div>
                                
                                <div style="background: #f8f9fa; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
                                    <strong>Description:</strong><br>
                                    {project['description'][:300]}{'...' if len(project['description']) > 300 else ''}
                                </div>
                                
                                <div style="display: flex; gap: 1rem; justify-content: center;">
                                    {f'<a href="{project["project_url"]}" target="_blank" style="background: #4285f4; color: white; padding: 0.75rem 1.5rem; text-decoration: none; border-radius: 0.5rem; font-weight: bold;">🌐 Visit Project Website</a>' if project['project_url'] and pd.notna(project['project_url']) and project['project_url'] != '' else '<span style="background: #ccc; color: white; padding: 0.75rem 1.5rem; border-radius: 0.5rem;">❌ No URL Available</span>'}
                                    
                                    {f'<a href="{project["github_url"]}" target="_blank" style="background: #333; color: white; padding: 0.75rem 1.5rem; text-decoration: none; border-radius: 0.5rem; font-weight: bold;">📚 View on GitHub</a>' if project['github_url'] else '<span style="background: #ccc; color: white; padding: 0.75rem 1.5rem; border-radius: 0.5rem;">❌ No GitHub URL</span>'}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Summary metrics
                        st.markdown("---")
                        st.markdown("### 📊 Match Summary")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Total Matches", len(similar_projects))
                        
                        with col2:
                            avg_similarity = np.mean([p['similarity_score'] for p in similar_projects]) * 100
                            st.metric("Avg Similarity", f"{avg_similarity:.1f}%")
                        
                        with col3:
                            categories_found = len(set([p['category'] for p in similar_projects]))
                            st.metric("Categories Found", categories_found)
                        
                        with col4:
                            best_match = max(similar_projects, key=lambda x: x['similarity_score'])
                            st.metric("Best Match", f"{best_match['similarity_score']*100:.1f}%")
                        
                        # Show UMAP coordinates for matches
                        if any(p['umap_coords'] != (0, 0, 0) for p in similar_projects):
                            st.markdown("### 🗺️ Where to Find These Projects in 3D Space")
                            for i, project in enumerate(similar_projects):
                                if project['umap_coords'] != (0, 0, 0):
                                    st.write(f"**{project['title']}:** UMAP({project['umap_coords'][0]:.3f}, {project['umap_coords'][1]:.3f}, {project['umap_coords'][2]:.3f})")
                        
                    else:
                        st.warning("❌ No similar projects found. Try describing your idea in more detail or using different keywords.")
                        
                        # Suggest categories
                        if 'category' in df.columns:
                            st.markdown("### 💡 Available Project Categories:")
                            categories = df['category'].value_counts().head(10)
                            for cat, count in categories.items():
                                st.write(f"• **{cat}** ({count} projects)")
            else:
                st.warning("Please describe your project idea to find similar projects.")

else:
    st.warning("⚠️ Please upload your project CSV file to see the analytics dashboard.")
    
    # Show expected format
    st.markdown("### 📋 Expected CSV Format")
    st.markdown("""
    Your CSV file should include these columns:
    
    | Column | Description |
    |--------|-------------|
    | `name` | Project names |
    | `project_url` | Project URLs |
    | `detailed_description` | Project descriptions |
    | `cleaned_tag_category` | Project categories |
    | `subcategory_1`, `subcategory_2`, `subcategory_3` | Subcategories |
    | `umap_dim_1`, `umap_dim_2`, `umap_dim_3` | UMAP coordinates |
    
    **Note:** The app automatically maps your column names and provides creative 3D visualizations.
    """)
    
    # Instructions
    st.markdown("### 🎯 How to Use")
    st.markdown("""
    1. **Upload your CSV file** using the file uploader above
    2. **Use the AI chatbot** to find similar projects based on your ideas
    3. **Explore categories** and subcategories in the sidebar filters
    4. **View 3D visualizations** with different coloring options
    5. **Click on data points** to visit project websites
    6. **Search projects** by name or description
    7. **Export filtered data** for further analysis
    """)
    
    # CSV Analyzer Section
    st.markdown("---")
    st.markdown("## 📊 CSV Analyzer Agent")
    st.markdown("### Analyze and structure your project data for optimal 3D visualization")
    
    # CSV Analyzer functionality
    csv_upload = st.file_uploader(
        "Upload CSV/Excel for Analysis:",
        type=['csv', 'xlsx', 'xls'],
        key="csv_analyzer",
        help="Upload your project data file to analyze and structure it"
    )
    
    if csv_upload is not None:
        try:
            # Load data
            if csv_upload.name.endswith('.csv'):
                csv_df = pd.read_csv(csv_upload)
            else:
                csv_df = pd.read_excel(csv_upload)
            
            st.success(f"✅ Successfully loaded {len(csv_df)} rows and {len(csv_df.columns)} columns")
            
            # Basic analysis
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Rows", len(csv_df))
                st.metric("Total Columns", len(csv_df.columns))
            
            with col2:
                null_percentage = (csv_df.isnull().sum().sum() / (len(csv_df) * len(csv_df.columns))) * 100
                st.metric("Missing Data", f"{null_percentage:.1f}%")
                
                # Check for UMAP columns
                umap_cols = [col for col in csv_df.columns if 'umap' in col.lower()]
                st.metric("UMAP Columns", len(umap_cols))
            
            with col3:
                # Check for essential columns
                essential_cols = ['name', 'title', 'description', 'category', 'url']
                found_cols = sum(1 for col in csv_df.columns if any(essential in col.lower() for essential in essential_cols))
                st.metric("Essential Columns", f"{found_cols}/5")
                
                # Structure score
                structure_score = min(100, (found_cols / 5) * 100 - null_percentage)
                st.metric("Structure Score", f"{structure_score:.0f}/100")
            
            # Column analysis
            st.subheader("📋 Column Analysis")
            
            for col in csv_df.columns:
                with st.expander(f"Column: {col}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Data Type:** {csv_df[col].dtype}")
                        st.write(f"**Unique Values:** {csv_df[col].nunique()}")
                        st.write(f"**Null Values:** {csv_df[col].isnull().sum()}")
                    
                    with col2:
                        st.write(f"**Sample Values:**")
                        sample_values = csv_df[col].dropna().head(3).tolist()
                        for val in sample_values:
                            st.write(f"• {val}")
            
            # Column mapping suggestions
            st.subheader("🔄 Column Mapping Suggestions")
            
            # Auto-detect mappings
            mapping = {}
            for col in csv_df.columns:
                col_lower = col.lower()
                
                if any(keyword in col_lower for keyword in ['name', 'title', 'project_name']):
                    mapping[col] = 'title'
                elif any(keyword in col_lower for keyword in ['url', 'link', 'website']):
                    mapping[col] = 'project_url'
                elif any(keyword in col_lower for keyword in ['desc', 'description', 'details']):
                    mapping[col] = 'description'
                elif any(keyword in col_lower for keyword in ['category', 'cat', 'type']):
                    mapping[col] = 'category'
                elif any(keyword in col_lower for keyword in ['umap_1', 'umap_dim_1', 'x']):
                    mapping[col] = 'x'
                elif any(keyword in col_lower for keyword in ['umap_2', 'umap_dim_2', 'y']):
                    mapping[col] = 'y'
                elif any(keyword in col_lower for keyword in ['umap_3', 'umap_dim_3', 'z']):
                    mapping[col] = 'z'
                else:
                    mapping[col] = col
            
            # Display mappings
            st.markdown("**Suggested column mappings for Project Explorer:**")
            for original_col, suggested_mapping in mapping.items():
                st.write(f"• **{original_col}** → `{suggested_mapping}`")
            
            # Generate enhanced CSV
            if st.button("🚀 Generate Enhanced CSV", type="primary"):
                enhanced_df = csv_df.copy()
                
                # Apply mappings
                enhanced_df = enhanced_df.rename(columns=mapping)
                
                # Add missing columns
                if 'title' not in enhanced_df.columns:
                    enhanced_df['title'] = enhanced_df.iloc[:, 0] if len(enhanced_df.columns) > 0 else 'Untitled Project'
                
                if 'description' not in enhanced_df.columns:
                    enhanced_df['description'] = 'No description available'
                
                if 'category' not in enhanced_df.columns:
                    enhanced_df['category'] = 'Uncategorized'
                
                if 'project_url' not in enhanced_df.columns:
                    enhanced_df['project_url'] = ''
                
                # Generate UMAP coordinates if missing
                if not all(col in enhanced_df.columns for col in ['x', 'y', 'z']):
                    np.random.seed(42)
                    enhanced_df['x'] = np.random.randn(len(enhanced_df))
                    enhanced_df['y'] = np.random.randn(len(enhanced_df))
                    enhanced_df['z'] = np.random.randn(len(enhanced_df))
                
                st.success("✅ Enhanced CSV generated successfully!")
                
                # Show preview
                st.subheader("📊 Enhanced Data Preview")
                st.dataframe(enhanced_df.head(), use_container_width=True)
                
                # Download option
                csv = enhanced_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Enhanced CSV",
                    data=csv,
                    file_name=f"enhanced_{csv_upload.name}",
                    mime="text/csv"
                )
        
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.error(f"Error type: {type(e).__name__}")
            import traceback
            st.code(traceback.format_exc())
