import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import plotly.offline as pyo

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
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🚀 Sundai Projects Explorer</h1>', unsafe_allow_html=True)
st.markdown("### Interactive 3D Analytics for Sundai Projects Dataset")

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

# Load data
df = load_sundai_data(uploaded_file)

if df is not None and len(df) > 0:
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
            
            for category in filtered_df['category'].unique():
                cat_data = filtered_df[filtered_df['category'] == category]
                fig_3d.add_trace(go.Scatter3d(
                    x=cat_data['x'],
                    y=cat_data['y'],
                    z=cat_data['z'],
                    mode='markers',
                    name=category,
                    marker=dict(
                        size=8,
                        opacity=0.8
                    ),
                    text=cat_data['title'],
                    hovertemplate='<b>%{text}</b><br>' +
                                  'Category: ' + category + '<br>' +
                                  'X: %{x:.3f}<br>' +
                                  'Y: %{y:.3f}<br>' +
                                  'Z: %{z:.3f}<extra></extra>'
                ))
            
            fig_3d.update_layout(
                title='3D Project Space - Category Clusters',
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
        
        elif viz_option == "Subcategory Groups":
            # Color by subcategory
            fig_3d = go.Figure()
            
            # Get top subcategories for coloring
            top_subcats = filtered_df['subcategory_1'].value_counts().head(8).index.tolist()
            
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
                            opacity=0.7
                        ),
                        text=subcat_data['title'],
                        hovertemplate='<b>%{text}</b><br>' +
                                      'Subcategory: ' + subcat + '<br>' +
                                      'X: %{x:.3f}<br>' +
                                      'Y: %{y:.3f}<br>' +
                                      'Z: %{z:.3f}<extra></extra>'
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
                    hovertemplate='<b>%{text}</b><br>' +
                                  'X: %{x:.3f}<br>' +
                                  'Y: %{y:.3f}<br>' +
                                  'Z: %{z:.3f}<extra></extra>'
                ))
            
            fig_3d.update_layout(
                title='3D Project Space - Subcategory Groups',
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
                hovertemplate='<b>%{text}</b><br>' +
                              'Distance: %{marker.color:.3f}<br>' +
                              'X: %{x:.3f}<br>' +
                              'Y: %{y:.3f}<br>' +
                              'Z: %{z:.3f}<extra></extra>'
            )])
            
            fig_3d.update_layout(
                title='3D Project Space - Distance from Origin',
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
            
            fig_3d = go.Figure(data=[go.Scatter3d(
                x=filtered_df['x'],
                y=filtered_df['y'],
                z=filtered_df['z'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=color_data,
                    colorscale='Viridis',
                    opacity=0.8,
                    colorbar=dict(title=color_title)
                ),
                text=filtered_df['title'],
                hovertemplate='<b>%{text}</b><br>' +
                              color_title + ': %{marker.color}<br>' +
                              'X: %{x:.3f}<br>' +
                              'Y: %{y:.3f}<br>' +
                              'Z: %{z:.3f}<extra></extra>'
            )])
            
            fig_3d.update_layout(
                title=f'Interactive 3D Project Space - Colored by {color_title}',
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
        
        # 3D plot controls
        st.markdown("**3D Plot Controls:**")
        st.markdown("- **Rotate:** Click and drag to rotate the view")
        st.markdown("- **Zoom:** Scroll to zoom in/out")
        st.markdown("- **Pan:** Right-click and drag to pan")
        st.markdown("- **Reset:** Double-click to reset the view")
        st.markdown("- **Hover:** Hover over points to see project details")
    
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
    
    # Display projects table
    if 'title' in display_df.columns:
        st.dataframe(
            display_df[['title', 'category', 'subcategory_1'] if 'subcategory_1' in display_df.columns else ['title', 'category']],
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
    2. **Explore categories** and subcategories in the sidebar filters
    3. **View 3D visualizations** with different coloring options
    4. **Search projects** by name or description
    5. **Export filtered data** for further analysis
    """)
