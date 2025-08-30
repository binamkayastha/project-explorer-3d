"""
Streamlit Integration for Public APIs
Adds startup data functionality to the existing Streamlit app using free public APIs
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any, Optional
import sys
import os

# Add the integrations directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from .api_manager import StartupDataManager
except ImportError:
    # Fallback for direct import
    from api_manager import StartupDataManager

def initialize_startup_manager():
    """
    Initialize the startup data manager (no API keys needed for public APIs)
    """
    return StartupDataManager()

def render_startup_search_section():
    """
    Render the startup search section in Streamlit
    """
    st.markdown("## 🔍 Project Search & Discovery")
    st.markdown("Search for projects and packages across GitHub, NPM, and PyPI")
    
    # Search form
    with st.form("startup_search_form"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "Search Query",
                placeholder="e.g., AI, machine learning, web framework...",
                help="Enter keywords to search for projects and packages"
            )
        
        with col2:
            search_limit = st.number_input("Results", min_value=5, max_value=50, value=20, step=5)
        
        # Source selection
        sources = st.multiselect(
            "Data Sources",
            options=['github', 'npm', 'pypi'],
            default=['github', 'npm', 'pypi'],
            help="Select which platforms to search"
        )
        
        submitted = st.form_submit_button("🔍 Search Projects", use_container_width=True)
    
    if submitted and search_query:
        with st.spinner("Searching projects..."):
            try:
                manager = initialize_startup_manager()
                startups = manager.search_startups(search_query, search_limit, sources)
                
                if startups:
                    st.success(f"Found {len(startups)} projects!")
                    display_startup_results(startups)
                else:
                    st.warning("No projects found. Try different keywords or sources.")
                    
            except Exception as e:
                st.error(f"Error searching projects: {str(e)}")

def display_startup_results(startups: List[Dict]):
    """
    Display startup search results in an interactive format
    
    Args:
        startups (List[Dict]): List of startup data
    """
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(startups)
    
    # Add popularity metrics
    df['popularity_score'] = df.apply(lambda row: 
        row.get('stars', 0) + row.get('downloads', 0) + row.get('forks', 0), axis=1
    )
    
    # Display results in tabs
    tab1, tab2, tab3 = st.tabs(["📊 Summary", "🏢 Project List", "📈 Analytics"])
    
    with tab1:
        render_startup_summary(df)
    
    with tab2:
        render_startup_list(df)
    
    with tab3:
        render_startup_analytics(df)

def render_startup_summary(df: pd.DataFrame):
    """
    Render startup search summary
    
    Args:
        df (pd.DataFrame): Startup data
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Projects", len(df))
    
    with col2:
        total_stars = df.get('stars', pd.Series([0])).sum()
        st.metric("Total Stars", f"{total_stars:,}")
    
    with col3:
        total_downloads = df.get('downloads', pd.Series([0])).sum()
        st.metric("Total Downloads", f"{total_downloads:,}")
    
    with col4:
        sources_count = df['source'].nunique()
        st.metric("Data Sources", sources_count)
    
    # Source distribution
    st.markdown("### 📊 Data Source Distribution")
    source_counts = df['source'].value_counts()
    fig = px.pie(
        values=source_counts.values,
        names=source_counts.index,
        title="Projects by Data Source"
    )
    st.plotly_chart(fig, use_container_width=True)

def render_startup_list(df: pd.DataFrame):
    """
    Render startup list with detailed information
    
    Args:
        df (pd.DataFrame): Startup data
    """
    st.markdown("### 🏢 Project Details")
    
    # Add filters
    col1, col2 = st.columns(2)
    
    with col1:
        source_filter = st.multiselect(
            "Filter by Source",
            options=df['source'].unique(),
            default=df['source'].unique()
        )
    
    with col2:
        popularity_filter = st.selectbox(
            "Sort by Popularity",
            options=["Stars", "Downloads", "Forks", "Name"],
            index=0
        )
    
    # Apply filters
    filtered_df = df[df['source'].isin(source_filter)]
    
    # Sort by popularity
    if popularity_filter == "Stars":
        filtered_df = filtered_df.sort_values('stars', ascending=False)
    elif popularity_filter == "Downloads":
        filtered_df = filtered_df.sort_values('downloads', ascending=False)
    elif popularity_filter == "Forks":
        filtered_df = filtered_df.sort_values('forks', ascending=False)
    else:
        filtered_df = filtered_df.sort_values('name')
    
    # Display projects in cards
    for idx, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if row.get('logo_url'):
                    st.image(row['logo_url'], width=80)
                else:
                    st.image("https://via.placeholder.com/80x80?text=📦", width=80)
            
            with col2:
                st.markdown(f"**{row['name']}**")
                st.markdown(f"*{row.get('high_concept', row.get('description', ''))}*")
                
                # Popularity metrics
                metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                with metrics_col1:
                    if 'stars' in row and row['stars'] > 0:
                        st.metric("⭐ Stars", f"{row['stars']:,}")
                with metrics_col2:
                    if 'downloads' in row and row['downloads'] > 0:
                        st.metric("📥 Downloads", f"{row['downloads']:,}")
                with metrics_col3:
                    if 'forks' in row and row['forks'] > 0:
                        st.metric("🍴 Forks", f"{row['forks']:,}")
                
                st.markdown(f"🔗 **Source:** {row['source'].title()}")
                
                if row.get('company_url'):
                    st.markdown(f"🌐 [Visit Project]({row['company_url']})")
                
                # Add expandable details
                with st.expander("📋 More Details"):
                    st.markdown(f"**Description:** {row.get('description', 'No description available')}")
                    if 'language' in row and row['language']:
                        st.markdown(f"**Language:** {row['language']}")
                    if 'version' in row and row['version']:
                        st.markdown(f"**Version:** {row['version']}")
                    if 'created_at' in row and row['created_at']:
                        st.markdown(f"**Created:** {row['created_at']}")
            
            st.divider()

def render_startup_analytics(df: pd.DataFrame):
    """
    Render startup analytics and insights
    
    Args:
        df (pd.DataFrame): Startup data
    """
    st.markdown("### 📈 Analytics & Insights")
    
    # Language distribution (GitHub only)
    github_df = df[df['source'] == 'github']
    if not github_df.empty and 'language' in github_df.columns:
        st.markdown("#### 🛠️ Programming Language Distribution")
        language_counts = github_df['language'].value_counts().head(10)
        
        fig = px.bar(
            x=language_counts.index,
            y=language_counts.values,
            title="Top Programming Languages",
            labels={'x': 'Language', 'y': 'Number of Projects'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Popularity distribution
    if 'stars' in df.columns:
        st.markdown("#### ⭐ Stars Distribution")
        stars_ranges = pd.cut(
            df[df['stars'] > 0]['stars'],
            bins=[0, 100, 1000, 10000, float('inf')],
            labels=['< 100', '100-1K', '1K-10K', '> 10K']
        )
        stars_dist = stars_ranges.value_counts()
        
        fig = px.bar(
            x=stars_dist.index,
            y=stars_dist.values,
            title="Stars Distribution",
            labels={'x': 'Stars Range', 'y': 'Number of Projects'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top popular projects
    if 'stars' in df.columns:
        st.markdown("#### 🏆 Top Starred Projects")
        top_starred = df[df['stars'] > 0].nlargest(10, 'stars')
        
        fig = px.bar(
            data_frame=top_starred,
            x='name',
            y='stars',
            title="Top 10 Starred Projects",
            labels={'name': 'Project', 'stars': 'Stars'}
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

def render_trending_startups_section():
    """
    Render the trending startups section
    """
    st.markdown("## 🔥 Trending Projects")
    st.markdown("Discover trending projects across different platforms")
    
    # Category selection
    categories = ['AI', 'Machine Learning', 'Web Framework', 'Data Science', 'All']
    selected_category = st.selectbox("Select Category", categories, index=4)
    
    if st.button("🚀 Get Trending Projects", use_container_width=True):
        with st.spinner("Fetching trending projects..."):
            try:
                manager = initialize_startup_manager()
                category = None if selected_category == 'All' else selected_category
                trending = manager.get_trending_startups(category, limit=15)
                
                if trending:
                    st.success(f"Found {len(trending)} trending projects!")
                    display_trending_startups(trending)
                else:
                    st.warning("No trending projects found.")
                    
            except Exception as e:
                st.error(f"Error fetching trending projects: {str(e)}")

def display_trending_startups(startups: List[Dict]):
    """
    Display trending startups in a grid layout
    
    Args:
        startups (List[Dict]): List of trending startup data
    """
    # Convert to DataFrame
    df = pd.DataFrame(startups)
    
    # Display in grid
    cols = st.columns(3)
    for idx, row in df.iterrows():
        col_idx = idx % 3
        with cols[col_idx]:
            with st.container():
                st.markdown(f"### {row['name']}")
                st.markdown(f"*{row.get('high_concept', '')}*")
                
                # Popularity metrics
                if 'stars' in row and row['stars'] > 0:
                    st.markdown(f"⭐ **{row['stars']:,} stars**")
                if 'downloads' in row and row['downloads'] > 0:
                    st.markdown(f"📥 **{row['downloads']:,} downloads**")
                if 'forks' in row and row['forks'] > 0:
                    st.markdown(f"🍴 **{row['forks']:,} forks**")
                
                st.markdown(f"📊 **Trending Score:** {row.get('trending_score', 'N/A')}")
                st.markdown(f"🔗 **{row['source'].title()}**")
                
                if row.get('company_url'):
                    st.markdown(f"[🌐 Visit]({row['company_url']})")
                
                st.divider()

def render_api_settings_section():
    """
    Render API settings and configuration section
    """
    st.markdown("## ⚙️ API Settings")
    st.markdown("Configure your public API usage (no registration required!)")
    
    with st.expander("🔑 API Information", expanded=False):
        st.markdown("""
        ### 🎉 No API Keys Required!
        
        This integration uses **free public APIs** that don't require registration:
        
        - **GitHub API**: Search repositories and get project data
        - **NPM API**: Search JavaScript packages
        - **PyPI API**: Search Python packages
        
        ### 📊 Rate Limits
        - **GitHub**: 60 requests/hour (unauthenticated)
        - **NPM**: No strict limits
        - **PyPI**: No strict limits
        
        ### 🚀 Benefits
        - ✅ No registration required
        - ✅ No API keys needed
        - ✅ Real-time data
        - ✅ Multiple platforms
        - ✅ Free to use
        """)
        
        # API usage stats
        if st.button("📊 Check API Usage"):
            try:
                manager = initialize_startup_manager()
                usage_stats = manager.get_api_usage_stats()
                
                st.markdown("### 📈 API Usage Statistics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Requests Made", usage_stats['total_requests'])
                
                with col2:
                    st.metric("Remaining", usage_stats['total_remaining'])
                
                with col3:
                    st.metric("APIs Used", len(usage_stats['public_apis']['apis_used']))
                
                st.markdown("**APIs Used:** " + ", ".join(usage_stats['public_apis']['apis_used']))
                    
            except Exception as e:
                st.error(f"Error checking API usage: {str(e)}")

def render_insights_section():
    """
    Render comprehensive insights section
    """
    st.markdown("## 🧠 Market Insights")
    st.markdown("Get comprehensive insights and analytics from public platforms")
    
    with st.form("insights_form"):
        insight_query = st.text_input(
            "Enter search term for insights",
            placeholder="e.g., AI, machine learning, web framework...",
            help="Get comprehensive market insights for this term"
        )
        
        submitted = st.form_submit_button("🔍 Get Insights", use_container_width=True)
    
    if submitted and insight_query:
        with st.spinner("Generating insights..."):
            try:
                manager = initialize_startup_manager()
                insights = manager.get_combined_insights(insight_query)
                
                if insights and insights.get('total_projects_found', 0) > 0:
                    display_insights(insights)
                else:
                    st.warning("No insights available for this query.")
                    
            except Exception as e:
                st.error(f"Error generating insights: {str(e)}")

def display_insights(insights: Dict[str, Any]):
    """
    Display comprehensive insights
    
    Args:
        insights (Dict[str, Any]): Insights data
    """
    st.markdown(f"### 📊 Insights for: **{insights['search_query']}**")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Projects", insights['total_projects_found'])
    
    with col2:
        total_stars = insights['total_stars']
        st.metric("Total Stars", f"{total_stars:,}")
    
    with col3:
        total_downloads = insights['total_downloads']
        st.metric("Total Downloads", f"{total_downloads:,}")
    
    with col4:
        platform_diversity = insights.get('platform_diversity', 0)
        st.metric("Platforms", platform_diversity)
    
    # Source distribution
    st.markdown("#### 📈 Data Source Distribution")
    source_dist = insights['source_distribution']
    fig = px.pie(
        values=list(source_dist.values()),
        names=list(source_dist.keys()),
        title="Projects by Data Source"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Language distribution
    if 'language_distribution' in insights and insights['language_distribution']:
        st.markdown("#### 🛠️ Programming Language Distribution")
        language_dist = insights['language_distribution']
        fig = px.bar(
            x=list(language_dist.keys()),
            y=list(language_dist.values()),
            title="Projects by Programming Language"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Popularity analysis
    if 'popularity_score' in insights:
        st.markdown("#### 📊 Popularity Analysis")
        popularity_score = insights['popularity_score']
        st.metric("Popularity Score", f"{popularity_score:.2f}")
        
        if popularity_score > 10:
            st.success("🔥 High popularity - This is a trending topic!")
        elif popularity_score > 5:
            st.info("📈 Moderate popularity - Growing interest")
        else:
            st.warning("📉 Low popularity - Niche topic")

def add_startup_data_to_sidebar():
    """
    Add startup data options to the sidebar
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🚀 Public API Data")
    
    if st.sidebar.button("🔍 Search Projects"):
        st.session_state['show_startup_search'] = True
    
    if st.sidebar.button("🔥 Trending Projects"):
        st.session_state['show_trending'] = True
    
    if st.sidebar.button("🧠 Market Insights"):
        st.session_state['show_insights'] = True
    
    if st.sidebar.button("⚙️ API Settings"):
        st.session_state['show_api_settings'] = True

def render_startup_data_pages():
    """
    Render startup data pages based on sidebar selection
    """
    if st.session_state.get('show_startup_search', False):
        render_startup_search_section()
        st.session_state['show_startup_search'] = False
    
    if st.session_state.get('show_trending', False):
        render_trending_startups_section()
        st.session_state['show_trending'] = False
    
    if st.session_state.get('show_insights', False):
        render_insights_section()
        st.session_state['show_insights'] = False
    
    if st.session_state.get('show_api_settings', False):
        render_api_settings_section()
        st.session_state['show_api_settings'] = False
