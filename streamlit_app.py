import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Project Explorer Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add performance optimization
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_cached_data(uploaded_file):
    """Cache uploaded data for better performance"""
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return None

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
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🚀 Project Explorer Analytics</h1>', unsafe_allow_html=True)
st.markdown("### Interactive analytics and visualizations for your 3D project dataset")

# File upload section
st.markdown("---")
st.markdown("### 📁 Upload Your CSV File")
st.markdown("Upload your project dataset to see interactive analytics and visualizations")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=['csv'],
    help="Upload your project dataset CSV file. Expected columns: title, category, description, x, y, z, launch_year, etc."
)

# Sample data generation function
@st.cache_data
def generate_sample_data():
    """Generate sample project data for demonstration"""
    np.random.seed(42)
    n_projects = 100
    
    categories = ['AI/ML', 'Web Development', 'Mobile App', 'Data Science', 'Blockchain', 'IoT', 'Game Dev', 'AR/VR']
    
    data = {
        'title': [f'Project {i+1}' for i in range(n_projects)],
        'category': np.random.choice(categories, n_projects),
        'description': [f'Description for project {i+1}' for i in range(n_projects)],
        'x': np.random.normal(0, 10, n_projects),
        'y': np.random.normal(0, 10, n_projects),
        'z': np.random.normal(0, 5, n_projects),
        'launch_year': np.random.randint(2018, 2025, n_projects),
        'team_size': np.random.randint(1, 20, n_projects),
        'funding': np.random.uniform(0, 1000000, n_projects),
        'success_rate': np.random.uniform(0.1, 1.0, n_projects)
    }
    return pd.DataFrame(data)

# Load data function
@st.cache_data
def load_data(uploaded_file):
    """Load data from uploaded file or generate sample data"""
    if uploaded_file is not None:
        try:
            df = load_cached_data(uploaded_file)
            st.success(f"✅ Successfully loaded {len(df)} projects from your CSV file!")
            
            # Show data info
            with st.expander("📊 Data Overview"):
                st.write(f"**Total Rows:** {len(df)}")
                st.write(f"**Total Columns:** {len(df.columns)}")
                
                # Show original columns
                st.write("**Original Columns:**", ", ".join(df.columns.tolist()))
                
                # Show UMAP dimensions if found
                umap_cols = [col for col in df.columns if 'umap_dim' in col]
                if umap_cols:
                    st.write(f"**UMAP Dimensions Found:** {len(umap_cols)}")
                    st.write("UMAP columns:", ", ".join(umap_cols))
                
                # Show coordinate ranges if available
                if all(col in df.columns for col in ['x', 'y', 'z']):
                    st.write("**Coordinate Ranges:**")
                    st.write(f"X: {df['x'].min():.2f} to {df['x'].max():.2f}")
                    st.write(f"Y: {df['y'].min():.2f} to {df['y'].max():.2f}")
                    st.write(f"Z: {df['z'].min():.2f} to {df['z'].max():.2f}")
                
                st.write("**First few rows:**")
                st.dataframe(df.head(), use_container_width=True)
            
            return df
        except Exception as e:
            st.error(f"❌ Error loading CSV file: {str(e)}")
            st.info("💡 Please check your CSV file format and try again.")
            return None
    else:
        # Show sample data option
        st.info("📋 No file uploaded. Showing sample data for demonstration.")
        st.markdown("""
        **To use your own data:**
        1. Upload a CSV file with your project data
        2. Expected columns: `title`, `category`, `description`, `x`, `y`, `z`, `launch_year`, etc.
        3. The app will automatically detect and analyze your data
        """)
        return generate_sample_data()

# Load data
df = load_data(uploaded_file)

if df is not None and len(df) > 0:
    # Data preprocessing
    # Map your actual column names to expected names
    column_mapping = {
        'name': 'title',
        'project_ur': 'project_url',
        'detailed_d': 'description',
        'cleaned_ta': 'category',
        'subcatego': 'subcategory',
        'umap_dim_1': 'x',
        'umap_dim_2': 'y', 
        'umap_dim_3': 'z'
    }
    
    # Rename columns if they exist
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})
    
    # Ensure we have required columns, add defaults if missing
    required_columns = {
        'title': 'Project Title',
        'category': 'Category',
        'description': 'Description',
        'x': 0,
        'y': 0,
        'z': 0,
        'launch_year': datetime.now().year,
        'team_size': 1,
        'funding': 0,
        'success_rate': 0.5
    }
    
    # Add missing columns with defaults
    for col, default_value in required_columns.items():
        if col not in df.columns:
            if isinstance(default_value, str):
                df[col] = default_value
            else:
                df[col] = default_value
            st.warning(f"⚠️ Column '{col}' not found in your CSV. Using default values.")
    
    # Convert numeric columns
    numeric_columns = ['x', 'y', 'z', 'launch_year', 'team_size', 'funding', 'success_rate']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Handle UMAP dimensions specifically
    umap_cols = [col for col in df.columns if 'umap_dim' in col]
    if len(umap_cols) >= 3:
        # Map the first 3 UMAP dimensions to x, y, z
        df['x'] = pd.to_numeric(df[umap_cols[0]], errors='coerce').fillna(0)
        df['y'] = pd.to_numeric(df[umap_cols[1]], errors='coerce').fillna(0)
        df['z'] = pd.to_numeric(df[umap_cols[2]], errors='coerce').fillna(0)
        st.success(f"✅ Found UMAP dimensions: {umap_cols[:3]}")
    
    # Extract year from project URLs if available
    if 'project_url' in df.columns and 'launch_year' not in df.columns:
        # Try to extract year from URLs or use current year
        df['launch_year'] = datetime.now().year
        st.info("📅 Using current year as launch year (extract from URLs if needed)")
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Category filter
    if 'category' in df.columns:
        # Clean category data - remove NaN and empty values
        valid_categories = df['category'].dropna().unique()
        valid_categories = [cat for cat in valid_categories if str(cat).strip() != '']
        
        if len(valid_categories) > 0:
            categories = ['All'] + sorted(valid_categories)
            selected_categories = st.sidebar.multiselect(
                "Select Categories",
                options=categories,
                default=['All']
            )
        else:
            selected_categories = ['All']
            st.sidebar.info("📊 No valid categories found")
    else:
        selected_categories = ['All']
        st.sidebar.info("📊 No category column found")
    
    # Year range filter
    if 'launch_year' in df.columns:
        min_year = int(df['launch_year'].min())
        max_year = int(df['launch_year'].max())
        if min_year < max_year:
            year_range = st.sidebar.slider(
                "Launch Year Range",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year)
            )
        else:
            year_range = (min_year, min_year + 1)
    else:
        year_range = (2020, 2025)
    
    # Team size filter
    if 'team_size' in df.columns:
        min_team = int(df['team_size'].min())
        max_team = int(df['team_size'].max())
        if min_team < max_team:
            team_size_range = st.sidebar.slider(
                "Team Size Range",
                min_value=min_team,
                max_value=max_team,
                value=(min_team, max_team)
            )
        else:
            team_size_range = (min_team, min_team + 1)
    else:
        team_size_range = (1, 10)
    
    # Apply filters
    filtered_df = df.copy()
    
    if 'All' not in selected_categories and 'category' in df.columns:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]
    
    if 'launch_year' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['launch_year'] >= year_range[0]) &
            (filtered_df['launch_year'] <= year_range[1])
        ]
    
    if 'team_size' in df.columns:
        filtered_df = filtered_df[
            (filtered_df['team_size'] >= team_size_range[0]) &
            (filtered_df['team_size'] <= team_size_range[1])
        ]
    
    # Main content
    st.markdown("---")
    
    # Quick Stats
    st.subheader("📊 Quick Stats")
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
        if 'launch_year' in filtered_df.columns:
            avg_year = round(filtered_df['launch_year'].mean(), 1)
            st.metric(
                "Avg Launch Year", 
                avg_year
            )
        else:
            st.metric("Avg Launch Year", "N/A")
    
    with col4:
        if 'funding' in filtered_df.columns:
            total_funding = f"${filtered_df['funding'].sum():,.0f}"
            st.metric(
                "Total Funding", 
                total_funding
            )
        else:
            st.metric("Total Funding", "N/A")
    
    # UMAP Stats
    umap_cols = [col for col in filtered_df.columns if 'umap_dim' in col]
    if umap_cols:
        st.subheader("🧬 UMAP Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("UMAP Dimensions", len(umap_cols))
        
        with col2:
            if len(umap_cols) >= 1:
                range_1 = f"{filtered_df[umap_cols[0]].min():.2f} to {filtered_df[umap_cols[0]].max():.2f}"
                st.metric(f"{umap_cols[0]} Range", range_1)
        
        with col3:
            if len(umap_cols) >= 2:
                range_2 = f"{filtered_df[umap_cols[1]].min():.2f} to {filtered_df[umap_cols[1]].max():.2f}"
                st.metric(f"{umap_cols[1]} Range", range_2)
    

    
    st.markdown("---")
    
    # Charts Section
    st.subheader("📈 Analytics Dashboard")
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        if 'category' in filtered_df.columns:
            st.subheader("📊 Project Distribution by Category")
            category_counts = filtered_df['category'].value_counts()
            fig_pie = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title='Projects by Category',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("📊 Category data not available for pie chart")
    
    with col2:
        if 'launch_year' in filtered_df.columns:
            st.subheader("📈 Launch Year Trends")
            year_counts = filtered_df['launch_year'].value_counts().sort_index()
            fig_line = px.line(
                x=year_counts.index,
                y=year_counts.values,
                title='Projects Launched by Year',
                labels={'x': 'Year', 'y': 'Number of Projects'}
            )
            fig_line.update_traces(line_color='#00D4AA', line_width=3)
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("📈 Launch year data not available for trend chart")
    
    # Team Size vs Success Rate
    if 'team_size' in filtered_df.columns and 'success_rate' in filtered_df.columns:
        st.subheader("👥 Team Size vs Success Rate")
        fig_scatter = px.scatter(
            filtered_df,
            x='team_size',
            y='success_rate',
            color='category' if 'category' in filtered_df.columns else None,
            size='funding' if 'funding' in filtered_df.columns else None,
            hover_data=['title', 'launch_year'] if 'title' in filtered_df.columns and 'launch_year' in filtered_df.columns else None,
            title='Team Size vs Success Rate (bubble size = funding)',
            labels={'team_size': 'Team Size', 'success_rate': 'Success Rate'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # UMAP Analysis Section
    umap_cols = [col for col in filtered_df.columns if 'umap_dim' in col]
    if umap_cols:
        st.subheader("🧬 UMAP Dimensionality Analysis")
        st.markdown("**UMAP (Uniform Manifold Approximation and Projection)** is a dimension reduction technique that preserves both local and global structure in your data.")
        
        # Show UMAP dimensions info
        col1, col2 = st.columns(2)
        with col1:
            st.metric("UMAP Dimensions", len(umap_cols))
        with col2:
            st.metric("Data Points", len(filtered_df))
        
        # Show UMAP dimension distributions
        if len(umap_cols) >= 2:
            st.subheader("📊 UMAP Dimension Distributions")
            fig_umap = px.scatter(
                filtered_df,
                x=umap_cols[0],
                y=umap_cols[1],
                color='category' if 'category' in filtered_df.columns else None,
                size='team_size' if 'team_size' in filtered_df.columns else None,
                hover_data=['title'] if 'title' in filtered_df.columns else None,
                title=f'UMAP Projection: {umap_cols[0]} vs {umap_cols[1]}',
                labels={umap_cols[0]: f'{umap_cols[0]}', umap_cols[1]: f'{umap_cols[1]}'}
            )
            st.plotly_chart(fig_umap, use_container_width=True)
    
    # 3D Visualization
    if all(col in filtered_df.columns for col in ['x', 'y', 'z']):
        st.subheader("🌌 3D Project Space Visualization")
        
        # Add color options for 3D plot
        color_options = ['Index', 'Category', 'Launch Year'] if 'launch_year' in filtered_df.columns else ['Index', 'Category']
        selected_color = st.selectbox("Color by:", color_options)
        
        if selected_color == 'Category' and 'category' in filtered_df.columns:
            color_data = filtered_df['category']
            color_title = "Category"
        elif selected_color == 'Launch Year' and 'launch_year' in filtered_df.columns:
            color_data = filtered_df['launch_year']
            color_title = "Launch Year"
        else:
            color_data = filtered_df.index
            color_title = "Index"
        
        fig_3d = go.Figure(data=[go.Scatter3d(
            x=filtered_df['x'],
            y=filtered_df['y'],
            z=filtered_df['z'],
            mode='markers',
            marker=dict(
                size=filtered_df['team_size'] * 2 if 'team_size' in filtered_df.columns else 8,
                color=color_data,
                colorscale='Viridis',
                opacity=0.8,
                colorbar=dict(title=color_title)
            ),
            text=filtered_df['title'] if 'title' in filtered_df.columns else [f'Project {i}' for i in range(len(filtered_df))],
            hovertemplate='<b>%{text}</b><br>' +
                          ('Category: ' + filtered_df['category'] + '<br>' if 'category' in filtered_df.columns else '') +
                          ('Team Size: ' + filtered_df['team_size'].astype(str) + '<br>' if 'team_size' in filtered_df.columns else '') +
                          ('Launch Year: ' + filtered_df['launch_year'].astype(str) + '<br>' if 'launch_year' in filtered_df.columns else '') +
                          'X: %{x:.2f}<br>' +
                          'Y: %{y:.2f}<br>' +
                          'Z: %{z:.2f}<extra></extra>'
        )])
        
        fig_3d.update_layout(
            title=f'3D Project Space - Colored by {color_title}',
            scene=dict(
                xaxis_title='X Coordinate',
                yaxis_title='Y Coordinate',
                zaxis_title='Z Coordinate',
                bgcolor='rgba(0,0,0,0)'
            ),
            width=800,
            height=600,
            showlegend=False
        )
        
        st.plotly_chart(fig_3d, use_container_width=True)
        
        # Add 3D plot controls
        st.markdown("**3D Plot Controls:**")
        st.markdown("- **Rotate:** Click and drag to rotate the view")
        st.markdown("- **Zoom:** Scroll to zoom in/out")
        st.markdown("- **Pan:** Right-click and drag to pan")
        st.markdown("- **Reset:** Double-click to reset the view")
        
    else:
        st.info("🌌 3D coordinates (x, y, z) not available for 3D visualization")
    
    # Funding Analysis
    if 'funding' in filtered_df.columns:
        st.subheader("💰 Funding Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            if 'category' in filtered_df.columns:
                st.subheader("Funding by Category")
                funding_by_category = filtered_df.groupby('category')['funding'].sum().sort_values(ascending=True)
                fig_bar = px.bar(
                    x=funding_by_category.values,
                    y=funding_by_category.index,
                    orientation='h',
                    title='Total Funding by Category',
                    labels={'x': 'Funding ($)', 'y': 'Category'}
                )
                fig_bar.update_traces(marker_color='#D946EF')
                st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            st.subheader("Funding Distribution")
            fig_hist = px.histogram(
                filtered_df,
                x='funding',
                nbins=20,
                title='Funding Distribution',
                labels={'funding': 'Funding ($)', 'count': 'Number of Projects'}
            )
            fig_hist.update_traces(marker_color='#00D4AA')
            st.plotly_chart(fig_hist, use_container_width=True)
    
    # Data Table
    st.markdown("---")
    st.subheader("📋 Project Data Table")
    
    # Add search functionality
    search_term = st.text_input("🔍 Search projects by title or description:")
    if search_term and 'title' in filtered_df.columns and 'description' in filtered_df.columns:
        search_filter = filtered_df[
            filtered_df['title'].str.contains(search_term, case=False, na=False) |
            filtered_df['description'].str.contains(search_term, case=False, na=False)
        ]
        display_df = search_filter
    else:
        display_df = filtered_df
    
    # Display the data table
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )
    
    # Export functionality
    st.markdown("---")
    st.subheader("📤 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f'project_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv'
        )
    
    with col2:
        st.info("💡 **Tip**: Use the filters in the sidebar to customize your data export!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🚀 Project Explorer Analytics Dashboard | Built with Streamlit</p>
        <p>Data last updated: {}</p>
    </div>
    """.format(datetime.now().strftime("%B %d, %Y")), unsafe_allow_html=True)

else:
    st.warning("⚠️ Please upload a CSV file to see the analytics dashboard.")
    
    # Show expected format
    st.markdown("### 📋 Expected CSV Format")
    st.markdown("""
    Your CSV file should include some of these columns:
    
    | Column | Description | Example |
    |--------|-------------|---------|
    | `name` | Project name | "AI Chatbot" |
    | `project_ur` | Project URL | "https://example.com" |
    | `detailed_d` | Project description | "An intelligent chatbot..." |
    | `cleaned_ta` | Project category/tags | "AI/ML" |
    | `subcatego` | Subcategory | "Chatbot" |
    | `umap_dim_1`, `umap_dim_2`, `umap_dim_3` | UMAP coordinates | 1.2, 3.4, 5.6 |
    | `launch_year` | Year launched | 2023 |
    | `team_size` | Number of team members | 5 |
    | `funding` | Project funding | 100000 |
    | `success_rate` | Success probability | 0.8 |
    
    **Note:** The app automatically maps your column names and will use default values for missing ones.
    **UMAP Support:** The app specifically recognizes `umap_dim_*` columns for 3D visualization.
    """)
    
    # Show sample data
    st.markdown("### 🎯 Sample Data Preview")
    sample_df = generate_sample_data()
    st.dataframe(sample_df.head(10), use_container_width=True)
