import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import plotly.offline as pyo
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Page config
st.set_page_config(
    page_title="Sundai Projects Explorer",
    page_icon="🚀",
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

# Title
st.markdown('<h1 class="main-header">🚀 Sundai Projects Explorer</h1>', unsafe_allow_html=True)
st.markdown("### Interactive 3D Analytics & AI-Powered Project Finder")

# File upload section
st.markdown("---")
st.markdown("### 📁 Upload Your Sundai Projects CSV File")
st.markdown("Upload your `sundai_projects_umap.csv` file to explore the 3D project space")

uploaded_file = st.file_uploader(
    "Choose sundai_projects_umap.csv",
    type=['csv'],
    help="Upload your Sundai projects dataset with UMAP coordinates"
)

# Load data function
@st.cache_data
def load_sundai_data(uploaded_file):
    """Load Sundai projects data with proper column mapping"""
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
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
            
            st.success(f"✅ Successfully loaded {len(df)} Sundai projects!")
            return df
            
        except Exception as e:
            st.error(f"❌ Error loading CSV file: {str(e)}")
            return None
    return None

# AI Chatbot functions
def preprocess_text(text):
    """Preprocess text for similarity matching"""
    if pd.isna(text) or text == '':
        return ''
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
    
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

def find_similar_projects(user_query, df, top_k=5):
    """Find similar projects based on user query"""
    if df is None or len(df) == 0:
        return []
    
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
    try:
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

def format_project_match(project, index):
    """Format a project match for display"""
    similarity_percentage = project['similarity_score'] * 100
    
    st.markdown(f"""
    <div class="project-match">
        <h4>🎯 Match #{index + 1}: {project['title']}</h4>
        <div class="similarity-score">Similarity: {similarity_percentage:.1f}%</div>
        <p><strong>Category:</strong> {project['category']}</p>
        <p><strong>Subcategory:</strong> {project['subcategory_1'] if project['subcategory_1'] else 'N/A'}</p>
        <p><strong>Description:</strong> {project['description'][:200]}{'...' if len(project['description']) > 200 else ''}</p>
        <p><strong>UMAP Coordinates:</strong> ({project['umap_coords'][0]:.3f}, {project['umap_coords'][1]:.3f}, {project['umap_coords'][2]:.3f})</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if project['project_url'] and pd.notna(project['project_url']) and project['project_url'] != '':
            st.markdown(
                f"<a href='{project['project_url']}' target='_blank' class='project-link'>🌐 Visit Project Website</a>",
                unsafe_allow_html=True
            )
        else:
            st.write("❌ No project URL available")
    
    with col2:
        if project['github_url']:
            st.markdown(
                f"<a href='{project['github_url']}' target='_blank' class='project-link'>📚 View on GitHub</a>",
                unsafe_allow_html=True
            )
        else:
            st.write("❌ No GitHub URL found")
    
    with col3:
        st.markdown(
            f"<span class='similarity-score'>Match Score: {similarity_percentage:.1f}%</span>",
            unsafe_allow_html=True
        )

# Load data
df = load_sundai_data(uploaded_file)

if df is not None and len(df) > 0:
    # AI Chatbot Section
    st.markdown("---")
    st.markdown("### 🤖 AI Project Finder Chatbot")
    st.markdown("Describe your project idea and I'll find the best matching projects from the dataset!")
    
    with st.container():
        st.markdown("""
        <div class="chatbot-container">
            <h3>💡 How it works:</h3>
            <ul>
                <li>Describe your project idea in natural language</li>
                <li>I'll analyze your description and find similar projects</li>
                <li>Get project URLs, GitHub links, descriptions, and UMAP coordinates</li>
                <li>See similarity scores to understand how well each project matches</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Chat interface
        user_query = st.text_area(
            "Describe your project idea:",
            placeholder="Example: I want to build a mobile app for real estate agents that uses AI to help with property management and client communication...",
            height=100
        )
        
        if st.button("🔍 Find Similar Projects", type="primary"):
            if user_query.strip():
                with st.spinner("🤖 Analyzing your idea and finding similar projects..."):
                    # Find similar projects
                    similar_projects = find_similar_projects(user_query, df, top_k=5)
                    
                    if similar_projects:
                        st.success(f"✅ Found {len(similar_projects)} similar projects!")
                        
                        # Display user query
                        st.markdown(f"""
                        <div class="chat-message user-message">
                            <strong>Your Idea:</strong> {user_query}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display bot response
                        st.markdown(f"""
                        <div class="chat-message">
                            <strong>🤖 AI Assistant:</strong> I found {len(similar_projects)} projects that match your idea! 
                            Here are the best matches with their details:
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display project matches
                        for i, project in enumerate(similar_projects):
                            format_project_match(project, i)
                        
                        # Summary
                        st.markdown("---")
                        st.markdown("### 📊 Match Summary")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Total Matches", len(similar_projects))
                        
                        with col2:
                            avg_similarity = np.mean([p['similarity_score'] for p in similar_projects]) * 100
                            st.metric("Avg Similarity", f"{avg_similarity:.1f}%")
                        
                        with col3:
                            categories_found = len(set([p['category'] for p in similar_projects]))
                            st.metric("Categories Found", categories_found)
                        
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
    
    # Show data overview
    with st.expander("📊 Dataset Overview"):
        st.write(f"**Total Projects:** {len(df)}")
        st.write(f"**Total Columns:** {len(df.columns)}")
        st.write("**Columns:**", ", ".join(df.columns.tolist()))
        
        # Show UMAP coordinate ranges
        if all(col in df.columns for col in ['x', 'y', 'z']):
            st.write("**UMAP Coordinate Ranges:**")
            st.write(f"X: {df['x'].min():.3f} to {df['x'].max():.3f}")
            st.write(f"Y: {df['y'].min():.3f} to {df['y'].max():.3f}")
            st.write(f"Z: {df['z'].min():.3f} to {df['z'].max():.3f}")
        
        st.write("**Sample Data:**")
        st.dataframe(df.head(), use_container_width=True)
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Category filter
    if 'category' in df.columns:
        categories = ['All'] + sorted(df['category'].unique().tolist())
        selected_categories = st.sidebar.multiselect(
            "Select Categories",
            options=categories,
            default=['All']
        )
    else:
        selected_categories = ['All']
    
    # Subcategory filter
    if 'subcategory_1' in df.columns:
        subcategories = ['All'] + sorted([cat for cat in df['subcategory_1'].unique() if cat != ''])
        selected_subcategories = st.sidebar.multiselect(
            "Select Subcategories",
            options=subcategories,
            default=['All']
        )
    else:
        selected_subcategories = ['All']
    
    # Apply filters
    filtered_df = df.copy()
    
    if 'All' not in selected_categories and 'category' in df.columns:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]
    
    if 'All' not in selected_subcategories and 'subcategory_1' in df.columns:
        filtered_df = filtered_df[filtered_df['subcategory_1'].isin(selected_subcategories)]
    
    # Main content
    st.markdown("---")
    
    # Key Metrics
    st.subheader("📊 Project Analytics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Projects", 
            len(filtered_df),
            delta=f"{len(filtered_df) - len(df)} from total"
        )
    
    with col2:
        if 'category' in filtered_df.columns:
            st.metric(
                "Categories", 
                filtered_df['category'].nunique()
            )
        else:
            st.metric("Categories", "N/A")
    
    with col3:
        if 'subcategory_1' in filtered_df.columns:
            st.metric(
                "Subcategories", 
                filtered_df['subcategory_1'].nunique()
            )
        else:
            st.metric("Subcategories", "N/A")
    
    with col4:
        if all(col in filtered_df.columns for col in ['x', 'y', 'z']):
            # Calculate average distance from origin
            avg_distance = np.sqrt(filtered_df['x']**2 + filtered_df['y']**2 + filtered_df['z']**2).mean()
            st.metric(
                "Avg Distance", 
                f"{avg_distance:.2f}"
            )
        else:
            st.metric("Avg Distance", "N/A")
    
    # Category Analysis
    if 'category' in filtered_df.columns:
        st.subheader("📈 Category Distribution")
        col1, col2 = st.columns(2)
        
        with col1:
            # Category pie chart
            category_counts = filtered_df['category'].value_counts()
            fig_pie = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title='Projects by Category',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Category bar chart
            fig_bar = px.bar(
                x=category_counts.index,
                y=category_counts.values,
                title='Project Count by Category',
                labels={'x': 'Category', 'y': 'Number of Projects'},
                color=category_counts.values,
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Subcategory Analysis
    if 'subcategory_1' in filtered_df.columns:
        st.subheader("🏷️ Subcategory Analysis")
        
        # Get top subcategories
        subcategory_counts = filtered_df['subcategory_1'].value_counts().head(10)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_subcat = px.bar(
                x=subcategory_counts.values,
                y=subcategory_counts.index,
                orientation='h',
                title='Top 10 Subcategories',
                labels={'x': 'Number of Projects', 'y': 'Subcategory'},
                color=subcategory_counts.values,
                color_continuous_scale='Plasma'
            )
            st.plotly_chart(fig_subcat, use_container_width=True)
        
        with col2:
            # Subcategory word cloud visualization
            st.markdown("**Subcategory Distribution:**")
            for subcat, count in subcategory_counts.items():
                if subcat != '':
                    percentage = (count / len(filtered_df)) * 100
                    st.markdown(f"**{subcat}:** {count} projects ({percentage:.1f}%)")
    
    # Creative 3D Visualizations
    if all(col in filtered_df.columns for col in ['x', 'y', 'z']):
        st.subheader("🌌 Creative 3D Project Space")
        
        # 3D visualization options
        viz_option = st.selectbox(
            "Choose 3D Visualization:",
            ["Category Clusters", "Subcategory Groups", "Distance from Origin", "Interactive 3D Scatter"]
        )
        
        if viz_option == "Category Clusters":
            # Color by category
            fig_3d = go.Figure()
            
            # Create color mapping for categories
            unique_categories = filtered_df['category'].unique()
            colors = px.colors.qualitative.Set3[:len(unique_categories)]
            color_map = dict(zip(unique_categories, colors))
            
            for category in unique_categories:
                cat_data = filtered_df[filtered_df['category'] == category]
                fig_3d.add_trace(go.Scatter3d(
                    x=cat_data['x'],
                    y=cat_data['y'],
                    z=cat_data['z'],
                    mode='markers',
                    name=category,
                    marker=dict(
                        size=8,
                        opacity=0.8,
                        color=color_map[category]
                    ),
                    text=cat_data['title'],
                    customdata=cat_data['project_url'] if 'project_url' in cat_data.columns else None,
                    hovertemplate='<b>%{text}</b><br>' +
                                  'Category: ' + category + '<br>' +
                                  'X: %{x:.3f}<br>' +
                                  'Y: %{y:.3f}<br>' +
                                  'Z: %{z:.3f}<br>' +
                                  '<extra></extra>'
                ))
            
            fig_3d.update_layout(
                title='3D Project Space - Category Clusters (Click points to visit project websites)',
                scene=dict(
                    xaxis_title='UMAP Dimension 1',
                    yaxis_title='UMAP Dimension 2',
                    zaxis_title='UMAP Dimension 3',
                    bgcolor='rgba(0,0,0,0)'
                ),
                width=800,
                height=600
            )
            
            # Add click event handling
            fig_3d.update_traces(
                customdata=filtered_df['project_url'].tolist() if 'project_url' in filtered_df.columns else None
            )
            
            st.plotly_chart(fig_3d, use_container_width=True)
        
        elif viz_option == "Subcategory Groups":
            # Color by subcategory
            fig_3d = go.Figure()
            
            # Get top subcategories for coloring
            top_subcats = filtered_df['subcategory_1'].value_counts().head(8).index.tolist()
            
            # Create color mapping for subcategories
            colors = px.colors.qualitative.Set3[:len(top_subcats)]
            color_map = dict(zip(top_subcats, colors))
            
            for subcat in top_subcats:
                if subcat != '':
                    subcat_data = filtered_df[filtered_df['subcategory_1'] == subcat]
                    fig_3d.add_trace(go.Scatter3d(
                        x=subcat_data['x'],
                        y=subcat_data['y'],
                        z=subcat_data['z'],
                        mode='markers',
                        name=subcat,
                        marker=dict(
                            size=10,
                            opacity=0.7,
                            color=color_map[subcat]
                        ),
                        text=subcat_data['title'],
                        customdata=subcat_data['project_url'] if 'project_url' in subcat_data.columns else None,
                        hovertemplate='<b>%{text}</b><br>' +
                                      'Subcategory: ' + subcat + '<br>' +
                                      'X: %{x:.3f}<br>' +
                                      'Y: %{y:.3f}<br>' +
                                      'Z: %{z:.3f}<br>' +
                                      '<extra></extra>'
                    ))
            
            # Add other projects as gray dots
            other_data = filtered_df[~filtered_df['subcategory_1'].isin(top_subcats)]
            if len(other_data) > 0:
                fig_3d.add_trace(go.Scatter3d(
                    x=other_data['x'],
                    y=other_data['y'],
                    z=other_data['z'],
                    mode='markers',
                    name='Other',
                    marker=dict(
                        size=6,
                        opacity=0.4,
                        color='gray'
                    ),
                    text=other_data['title'],
                    customdata=other_data['project_url'] if 'project_url' in other_data.columns else None,
                    hovertemplate='<b>%{text}</b><br>' +
                                  'X: %{x:.3f}<br>' +
                                  'Y: %{y:.3f}<br>' +
                                  'Z: %{z:.3f}<br>' +
                                  '<extra></extra>'
                ))
            
            fig_3d.update_layout(
                title='3D Project Space - Subcategory Groups (Click points to visit project websites)',
                scene=dict(
                    xaxis_title='UMAP Dimension 1',
                    yaxis_title='UMAP Dimension 2',
                    zaxis_title='UMAP Dimension 3',
                    bgcolor='rgba(0,0,0,0)'
                ),
                width=800,
                height=600
            )
            st.plotly_chart(fig_3d, use_container_width=True)
        
        elif viz_option == "Distance from Origin":
            # Color by distance from origin
            distances = np.sqrt(filtered_df['x']**2 + filtered_df['y']**2 + filtered_df['z']**2)
            
            fig_3d = go.Figure(data=[go.Scatter3d(
                x=filtered_df['x'],
                y=filtered_df['y'],
                z=filtered_df['z'],
                mode='markers',
                marker=dict(
                    size=8,
                    color=distances,
                    colorscale='Viridis',
                    opacity=0.8,
                    colorbar=dict(title="Distance from Origin")
                ),
                text=filtered_df['title'],
                customdata=filtered_df['project_url'] if 'project_url' in filtered_df.columns else None,
                hovertemplate='<b>%{text}</b><br>' +
                              'Distance: %{marker.color:.3f}<br>' +
                              'X: %{x:.3f}<br>' +
                              'Y: %{y:.3f}<br>' +
                              'Z: %{z:.3f}<br>' +
                              '<extra></extra>'
            )])
            
            fig_3d.update_layout(
                title='3D Project Space - Distance from Origin (Click points to visit project websites)',
                scene=dict(
                    xaxis_title='UMAP Dimension 1',
                    yaxis_title='UMAP Dimension 2',
                    zaxis_title='UMAP Dimension 3',
                    bgcolor='rgba(0,0,0,0)'
                ),
                width=800,
                height=600
            )
            st.plotly_chart(fig_3d, use_container_width=True)
        
        else:  # Interactive 3D Scatter
            # Color by category with interactive features
            color_by = st.selectbox("Color by:", ["Category", "Subcategory"])
            
            if color_by == "Category":
                color_data = filtered_df['category']
                color_title = "Category"
            else:
                color_data = filtered_df['subcategory_1']
                color_title = "Subcategory"
            
            # Create numeric color mapping
            unique_values = color_data.unique()
            color_indices = {val: idx for idx, val in enumerate(unique_values)}
            numeric_colors = [color_indices[val] for val in color_data]
            
            fig_3d = go.Figure(data=[go.Scatter3d(
                x=filtered_df['x'],
                y=filtered_df['y'],
                z=filtered_df['z'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=numeric_colors,
                    colorscale='Viridis',
                    opacity=0.8,
                    colorbar=dict(title=color_title)
                ),
                text=filtered_df['title'],
                customdata=filtered_df['project_url'] if 'project_url' in filtered_df.columns else None,
                hovertemplate='<b>%{text}</b><br>' +
                              color_title + ': %{customdata}<br>' +
                              'X: %{x:.3f}<br>' +
                              'Y: %{y:.3f}<br>' +
                              'Z: %{z:.3f}<br>' +
                              '<extra></extra>'
            )])
            
            fig_3d.update_layout(
                title=f'Interactive 3D Project Space - Colored by {color_title} (Click points to visit project websites)',
                scene=dict(
                    xaxis_title='UMAP Dimension 1',
                    yaxis_title='UMAP Dimension 2',
                    zaxis_title='UMAP Dimension 3',
                    bgcolor='rgba(0,0,0,0)'
                ),
                width=800,
                height=600
            )
            st.plotly_chart(fig_3d, use_container_width=True)
        
        # 3D plot controls and click instructions
        st.markdown("**3D Plot Controls:**")
        st.markdown("- **Rotate:** Click and drag to rotate the view")
        st.markdown("- **Zoom:** Scroll to zoom in/out")
        st.markdown("- **Pan:** Right-click and drag to pan")
        st.markdown("- **Reset:** Double-click to reset the view")
        st.markdown("- **Hover:** Hover over points to see project details")
        st.markdown("- **🖱️ Click:** Click on any data point to visit the project website!")
        
        # Project links section
        if 'project_url' in filtered_df.columns:
            st.markdown("---")
            st.subheader("🔗 Quick Project Links")
            st.markdown("Click on any project below to visit its website:")
            
            # Display project links in a grid
            col1, col2, col3 = st.columns(3)
            for idx, (_, row) in enumerate(filtered_df.iterrows()):
                if pd.notna(row['project_url']) and row['project_url'] != '':
                    with [col1, col2, col3][idx % 3]:
                        st.markdown(
                            f"<a href='{row['project_url']}' target='_blank' class='project-link'>"
                            f"🌐 {row['title'][:30]}{'...' if len(row['title']) > 30 else ''}</a>",
                            unsafe_allow_html=True
                        )
    
    # 2D UMAP Projections
    if all(col in filtered_df.columns for col in ['x', 'y']):
        st.subheader("📊 2D UMAP Projections")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # X vs Y projection
            fig_2d_xy = px.scatter(
                filtered_df,
                x='x',
                y='y',
                color='category' if 'category' in filtered_df.columns else None,
                hover_data=['title'],
                title='UMAP Dimension 1 vs Dimension 2',
                labels={'x': 'UMAP Dimension 1', 'y': 'UMAP Dimension 2'}
            )
            st.plotly_chart(fig_2d_xy, use_container_width=True)
        
        with col2:
            # X vs Z projection
            fig_2d_xz = px.scatter(
                filtered_df,
                x='x',
                y='z',
                color='category' if 'category' in filtered_df.columns else None,
                hover_data=['title'],
                title='UMAP Dimension 1 vs Dimension 3',
                labels={'x': 'UMAP Dimension 1', 'y': 'UMAP Dimension 3'}
            )
            st.plotly_chart(fig_2d_xz, use_container_width=True)
    
    # Project Search and Details
    st.markdown("---")
    st.subheader("🔍 Project Search & Details")
    
    # Search functionality
    search_term = st.text_input("Search projects by name or description:")
    if search_term and 'title' in filtered_df.columns and 'description' in filtered_df.columns:
        search_filter = filtered_df[
            filtered_df['title'].str.contains(search_term, case=False, na=False) |
            filtered_df['description'].str.contains(search_term, case=False, na=False)
        ]
        display_df = search_filter
    else:
        display_df = filtered_df
    
    # Display projects table with clickable links
    if 'title' in display_df.columns:
        st.markdown("**Click on project names to visit their websites:**")
        
        # Create a custom display with clickable links
        for idx, (_, row) in enumerate(display_df.iterrows()):
            with st.expander(f"📁 {row['title']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Category:** {row.get('category', 'N/A')}")
                    if 'subcategory_1' in row and pd.notna(row['subcategory_1']) and row['subcategory_1'] != '':
                        st.write(f"**Subcategory:** {row['subcategory_1']}")
                    if 'description' in row and pd.notna(row['description']):
                        st.write(f"**Description:** {row['description'][:200]}{'...' if len(str(row['description'])) > 200 else ''}")
                
                with col2:
                    if 'project_url' in row and pd.notna(row['project_url']) and row['project_url'] != '':
                        st.markdown(
                            f"<a href='{row['project_url']}' target='_blank' class='project-link'>"
                            f"🌐 Visit Project Website</a>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.write("❌ No URL available")
    
    # Export functionality
    st.markdown("---")
    st.subheader("📤 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f'sundai_projects_filtered_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv'
        )
    
    with col2:
        st.info("💡 **Tip**: Use the filters in the sidebar to customize your data export!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🚀 Sundai Projects Explorer | Built with Streamlit</p>
        <p>Data last updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%B %d, %Y")), unsafe_allow_html=True)

else:
    st.warning("⚠️ Please upload your `sundai_projects_umap.csv` file to see the analytics dashboard.")
    
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
