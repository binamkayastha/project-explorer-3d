import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(
    page_title="Project Explorer Test",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Project Explorer Test")
st.markdown("### Testing the application...")

# Simple file upload test
uploaded_file = st.file_uploader(
    "Upload a CSV file:",
    type=['csv'],
    help="Upload your project data file"
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Successfully loaded {len(df)} rows and {len(df.columns)} columns")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
else:
    st.info("Please upload a CSV file to test the application.")

st.markdown("---")
st.markdown("### CSV Analyzer Test")

# CSV Analyzer functionality
csv_upload = st.file_uploader(
    "Upload CSV/Excel for Analysis:",
    type=['csv', 'xlsx', 'xls'],
    key="csv_analyzer_test",
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
        
        # Generate enhanced CSV
        if st.button("🚀 Generate Enhanced CSV", type="primary"):
            enhanced_df = csv_df.copy()
            
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
