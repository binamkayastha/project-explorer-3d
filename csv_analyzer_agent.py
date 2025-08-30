import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Any
import json
import re
from datetime import datetime

class CSVAnalyzerAgent:
    def __init__(self):
        """Initialize the CSV analyzer agent"""
        self.analysis_results = {}
        
    def analyze_csv_structure(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze CSV structure and provide insights"""
        analysis = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "column_info": {},
            "data_quality": {},
            "suggestions": [],
            "structure_score": 0
        }
        
        # Analyze each column
        for col in df.columns:
            col_analysis = {
                "dtype": str(df[col].dtype),
                "null_count": df[col].isnull().sum(),
                "null_percentage": (df[col].isnull().sum() / len(df)) * 100,
                "unique_values": df[col].nunique(),
                "sample_values": df[col].dropna().head(3).tolist()
            }
            
            # Detect column type
            col_analysis["detected_type"] = self._detect_column_type(df[col])
            
            analysis["column_info"][col] = col_analysis
        
        # Calculate structure score
        analysis["structure_score"] = self._calculate_structure_score(analysis)
        
        # Generate suggestions
        analysis["suggestions"] = self._generate_suggestions(analysis)
        
        return analysis
    
    def _detect_column_type(self, series: pd.Series) -> str:
        """Detect the type of data in a column"""
        if series.dtype == 'object':
            # Check if it's URL
            if series.str.contains('http|www', na=False).any():
                return 'url'
            # Check if it's email
            elif series.str.contains('@', na=False).any():
                return 'email'
            # Check if it's date
            elif series.str.contains(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}', na=False).any():
                return 'date'
            # Check if it's category
            elif series.nunique() < len(series) * 0.5:
                return 'category'
            else:
                return 'text'
        elif series.dtype in ['int64', 'float64']:
            return 'numeric'
        else:
            return 'other'
    
    def _calculate_structure_score(self, analysis: Dict) -> int:
        """Calculate a score for how well-structured the data is"""
        score = 100
        
        # Deduct points for missing data
        for col_info in analysis["column_info"].values():
            if col_info["null_percentage"] > 20:
                score -= 10
            elif col_info["null_percentage"] > 10:
                score -= 5
        
        # Deduct points for too many unique values in categorical columns
        for col_info in analysis["column_info"].values():
            if col_info["detected_type"] == "category" and col_info["unique_values"] > 50:
                score -= 15
        
        return max(0, score)
    
    def _generate_suggestions(self, analysis: Dict) -> List[str]:
        """Generate suggestions for improving the data structure"""
        suggestions = []
        
        # Check for missing essential columns
        essential_columns = ['name', 'title', 'description', 'category', 'url']
        missing_columns = [col for col in essential_columns if not any(col in existing_col.lower() for existing_col in analysis["column_info"].keys())]
        
        if missing_columns:
            suggestions.append(f"Consider adding these essential columns: {', '.join(missing_columns)}")
        
        # Check for high null percentages
        for col, info in analysis["column_info"].items():
            if info["null_percentage"] > 30:
                suggestions.append(f"Column '{col}' has {info['null_percentage']:.1f}% missing data - consider cleaning or removing")
        
        # Check for UMAP coordinates
        umap_columns = [col for col in analysis["column_info"].keys() if 'umap' in col.lower()]
        if not umap_columns:
            suggestions.append("No UMAP coordinates found - consider adding UMAP dimensions for 3D visualization")
        
        return suggestions
    
    def suggest_column_mapping(self, df: pd.DataFrame) -> Dict[str, str]:
        """Suggest column mappings for the Project Explorer"""
        mapping = {}
        
        for col in df.columns:
            col_lower = col.lower()
            
            # Map common variations
            if any(keyword in col_lower for keyword in ['name', 'title', 'project_name']):
                mapping[col] = 'title'
            elif any(keyword in col_lower for keyword in ['url', 'link', 'website']):
                mapping[col] = 'project_url'
            elif any(keyword in col_lower for keyword in ['desc', 'description', 'details']):
                mapping[col] = 'description'
            elif any(keyword in col_lower for keyword in ['category', 'cat', 'type']):
                mapping[col] = 'category'
            elif any(keyword in col_lower for keyword in ['subcategory', 'sub_cat', 'sub']):
                mapping[col] = 'subcategory'
            elif any(keyword in col_lower for keyword in ['umap_1', 'umap_dim_1', 'x']):
                mapping[col] = 'x'
            elif any(keyword in col_lower for keyword in ['umap_2', 'umap_dim_2', 'y']):
                mapping[col] = 'y'
            elif any(keyword in col_lower for keyword in ['umap_3', 'umap_dim_3', 'z']):
                mapping[col] = 'z'
            else:
                mapping[col] = col  # Keep original name
        
        return mapping
    
    def generate_enhanced_csv(self, df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
        """Generate an enhanced CSV with proper structure"""
        enhanced_df = df.copy()
        
        # Apply column mapping
        enhanced_df = enhanced_df.rename(columns=mapping)
        
        # Add missing essential columns with defaults
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
            enhanced_df = self._generate_umap_coordinates(enhanced_df)
        
        return enhanced_df
    
    def _generate_umap_coordinates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate synthetic UMAP coordinates based on data patterns"""
        # Use existing numeric columns or create random coordinates
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) >= 3:
            # Use first 3 numeric columns
            df['x'] = df[numeric_cols[0]]
            df['y'] = df[numeric_cols[1]] if len(numeric_cols) > 1 else np.random.randn(len(df))
            df['z'] = df[numeric_cols[2]] if len(numeric_cols) > 2 else np.random.randn(len(df))
        else:
            # Generate random coordinates
            np.random.seed(42)  # For reproducibility
            df['x'] = np.random.randn(len(df))
            df['y'] = np.random.randn(len(df))
            df['z'] = np.random.randn(len(df))
        
        return df

def main():
    st.set_page_config(
        page_title="CSV Analyzer Agent",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 CSV Analyzer Agent for Project Explorer")
    st.markdown("### Analyze and structure your project data for optimal 3D visualization")
    
    # Initialize agent
    agent = CSVAnalyzerAgent()
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your CSV/Excel file:",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your project data file to analyze and structure it"
    )
    
    if uploaded_file is not None:
        try:
            # Load data
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ Successfully loaded {len(df)} rows and {len(df.columns)} columns")
            
            # Analyze structure
            with st.spinner("Analyzing your data structure..."):
                analysis = agent.analyze_csv_structure(df)
            
            # Display analysis results
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Structure Score", f"{analysis['structure_score']}/100")
                st.metric("Total Rows", analysis['total_rows'])
                st.metric("Total Columns", analysis['total_columns'])
            
            with col2:
                st.metric("Data Quality", "Good" if analysis['structure_score'] > 70 else "Needs Improvement")
                
                # Show suggestions
                if analysis['suggestions']:
                    st.subheader("💡 Suggestions for Improvement")
                    for suggestion in analysis['suggestions']:
                        st.warning(suggestion)
            
            # Column analysis
            st.subheader("📋 Column Analysis")
            
            for col, info in analysis['column_info'].items():
                with st.expander(f"Column: {col}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Type:** {info['detected_type']}")
                        st.write(f"**Data Type:** {info['dtype']}")
                        st.write(f"**Unique Values:** {info['unique_values']}")
                    
                    with col2:
                        st.write(f"**Null Values:** {info['null_count']} ({info['null_percentage']:.1f}%)")
                        st.write(f"**Sample Values:** {info['sample_values']}")
            
            # Column mapping suggestions
            st.subheader("🔄 Suggested Column Mapping")
            mapping = agent.suggest_column_mapping(df)
            
            # Create editable mapping
            st.markdown("**Review and edit the column mappings:**")
            
            mapping_container = st.container()
            with mapping_container:
                cols = st.columns(3)
                for i, (original_col, suggested_mapping) in enumerate(mapping.items()):
                    with cols[i % 3]:
                        new_mapping = st.selectbox(
                            f"{original_col} →",
                            ['title', 'description', 'category', 'subcategory', 'project_url', 'x', 'y', 'z', 'keep_original'],
                            index=['title', 'description', 'category', 'subcategory', 'project_url', 'x', 'y', 'z', 'keep_original'].index(suggested_mapping) if suggested_mapping in ['title', 'description', 'category', 'subcategory', 'project_url', 'x', 'y', 'z'] else 8
                        )
                        if new_mapping != 'keep_original':
                            mapping[original_col] = new_mapping
                        else:
                            mapping[original_col] = original_col
            
            # Generate enhanced CSV
            if st.button("🚀 Generate Enhanced CSV", type="primary"):
                with st.spinner("Generating enhanced CSV structure..."):
                    enhanced_df = agent.generate_enhanced_csv(df, mapping)
                    
                    st.success("✅ Enhanced CSV generated successfully!")
                    
                    # Show preview
                    st.subheader("📊 Enhanced Data Preview")
                    st.dataframe(enhanced_df.head(), use_container_width=True)
                    
                    # Download option
                    csv = enhanced_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Enhanced CSV",
                        data=csv,
                        file_name=f"enhanced_{uploaded_file.name}",
                        mime="text/csv"
                    )
                    
                    # Show data quality metrics
                    st.subheader("📈 Data Quality Metrics")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Projects with URLs", len(enhanced_df[enhanced_df['project_url'] != '']))
                        st.metric("Categories", enhanced_df['category'].nunique())
                    
                    with col2:
                        st.metric("Projects with Descriptions", len(enhanced_df[enhanced_df['description'] != 'No description available']))
                        st.metric("Subcategories", enhanced_df['subcategory'].nunique() if 'subcategory' in enhanced_df.columns else 0)
                    
                    with col3:
                        st.metric("3D Coordinates", "✅ Generated" if all(col in enhanced_df.columns for col in ['x', 'y', 'z']) else "❌ Missing")
                        st.metric("Ready for 3D", "✅ Yes" if analysis['structure_score'] > 70 else "⚠️ Needs Work")
            
            # Data visualization
            st.subheader("📊 Data Visualization")
            
            if 'category' in df.columns:
                # Category distribution
                fig = px.pie(
                    values=df['category'].value_counts().values,
                    names=df['category'].value_counts().index,
                    title="Project Categories Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Show data patterns
            if len(df.select_dtypes(include=[np.number]).columns) >= 2:
                numeric_cols = df.select_dtypes(include=[np.number]).columns[:2]
                fig = px.scatter(
                    df,
                    x=numeric_cols[0],
                    y=numeric_cols[1],
                    title=f"Data Pattern: {numeric_cols[0]} vs {numeric_cols[1]}"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
    
    else:
        # Show instructions
        st.info("""
        **📋 How to use the CSV Analyzer Agent:**
        
        1. **Upload your project data** (CSV or Excel file)
        2. **Review the analysis** - see data quality and structure insights
        3. **Adjust column mappings** - map your columns to Project Explorer format
        4. **Generate enhanced CSV** - get a properly structured file ready for 3D visualization
        5. **Download and use** - import the enhanced CSV into your Project Explorer
        
        **🎯 Expected CSV Structure:**
        - `title` - Project names
        - `description` - Project descriptions
        - `category` - Project categories
        - `subcategory` - Project subcategories
        - `project_url` - Project URLs
        - `x`, `y`, `z` - UMAP coordinates for 3D visualization
        """)

if __name__ == "__main__":
    main()
