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
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🚀 Project Explorer Analytics</h1>', unsafe_allow_html=True)
st.markdown("### Interactive analytics and visualizations for your 3D project dataset")

# Sample data generation function
@st.cache_data
def load_data():
    """Load or generate sample project data"""
    try:
        # Try to load from CSV file
        df = pd.read_csv('sundai_projects_ready.csv')
        st.success("✅ Loaded data from CSV file")
    except FileNotFoundError:
        # Generate sample data if CSV not found
        st.warning("⚠️ CSV file not found. Using sample data.")
        
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
        df = pd.DataFrame(data)
    
    return df

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Category filter
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=['All'] + list(df['category'].unique()),
    default=['All']
)

# Year range filter
year_range = st.sidebar.slider(
    "Launch Year Range",
    min_value=int(df['launch_year'].min()),
    max_value=int(df['launch_year'].max()),
    value=(int(df['launch_year'].min()), int(df['launch_year'].max()))
)

# Team size filter
team_size_range = st.sidebar.slider(
    "Team Size Range",
    min_value=int(df['team_size'].min()),
    max_value=int(df['team_size'].max()),
    value=(int(df['team_size'].min()), int(df['team_size'].max()))
)

# Apply filters
filtered_df = df.copy()

if 'All' not in selected_categories:
    filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]

filtered_df = filtered_df[
    (filtered_df['launch_year'] >= year_range[0]) &
    (filtered_df['launch_year'] <= year_range[1]) &
    (filtered_df['team_size'] >= team_size_range[0]) &
    (filtered_df['team_size'] <= team_size_range[1])
]

# Main content
st.markdown("---")

# Key Metrics
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Projects", 
        len(filtered_df),
        delta=f"{len(filtered_df) - len(df)} from total"
    )

with col2:
    st.metric(
        "Categories", 
        filtered_df['category'].nunique()
    )

with col3:
    avg_year = round(filtered_df['launch_year'].mean(), 1)
    st.metric(
        "Avg Launch Year", 
        avg_year
    )

with col4:
    total_funding = f"${filtered_df['funding'].sum():,.0f}"
    st.metric(
        "Total Funding", 
        total_funding
    )

st.markdown("---")

# Charts Section
st.subheader("📈 Analytics Dashboard")

# Create two columns for charts
col1, col2 = st.columns(2)

with col1:
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

with col2:
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

# Team Size vs Success Rate
st.subheader("👥 Team Size vs Success Rate")
fig_scatter = px.scatter(
    filtered_df,
    x='team_size',
    y='success_rate',
    color='category',
    size='funding',
    hover_data=['title', 'launch_year'],
    title='Team Size vs Success Rate (bubble size = funding)',
    labels={'team_size': 'Team Size', 'success_rate': 'Success Rate'}
)
st.plotly_chart(fig_scatter, use_container_width=True)

# 3D Visualization
st.subheader("🌌 3D Project Space Visualization")
fig_3d = go.Figure(data=[go.Scatter3d(
    x=filtered_df['x'],
    y=filtered_df['y'],
    z=filtered_df['z'],
    mode='markers',
    marker=dict(
        size=filtered_df['team_size'] * 2,
        color=filtered_df['launch_year'],
        colorscale='Viridis',
        opacity=0.8,
        colorbar=dict(title="Launch Year")
    ),
    text=filtered_df['title'],
    hovertemplate='<b>%{text}</b><br>' +
                  'Category: ' + filtered_df['category'] + '<br>' +
                  'Team Size: ' + filtered_df['team_size'].astype(str) + '<br>' +
                  'Launch Year: ' + filtered_df['launch_year'].astype(str) + '<br>' +
                  'X: %{x:.2f}<br>' +
                  'Y: %{y:.2f}<br>' +
                  'Z: %{z:.2f}<extra></extra>'
)])

fig_3d.update_layout(
    title='3D Project Space (Marker size = Team Size)',
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

# Funding Analysis
st.subheader("💰 Funding Analysis")
col1, col2 = st.columns(2)

with col1:
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
if search_term:
    search_filter = filtered_df[
        filtered_df['title'].str.contains(search_term, case=False, na=False) |
        filtered_df['description'].str.contains(search_term, case=False, na=False)
    ]
    display_df = search_filter
else:
    display_df = filtered_df

# Display the data table
st.dataframe(
    display_df[['title', 'category', 'launch_year', 'team_size', 'funding', 'success_rate']],
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
