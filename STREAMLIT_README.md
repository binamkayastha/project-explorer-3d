# Streamlit Integration for Project Explorer 3D

This guide explains how to set up and use the Streamlit integration with your 3D Project Explorer application.

## 🚀 Quick Start

### 1. Install Dependencies

First, install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install streamlit pandas plotly numpy
```

### 2. Run the Streamlit App

Navigate to your project directory and run:

```bash
streamlit run streamlit_app.py
```

The Streamlit app will start on `http://localhost:8501`

### 3. Access the Integration

1. Start your React application (if not already running)
2. Navigate to `http://localhost:5173/streamlit` (or your React app URL)
3. The Streamlit integration page will automatically detect and connect to your Streamlit app

## 📊 Features

The Streamlit integration provides:

- **Interactive Analytics Dashboard**: Charts, graphs, and visualizations
- **3D Project Visualization**: Plotly 3D scatter plots of your project data
- **Data Filtering**: Filter by category, year, team size, etc.
- **Export Functionality**: Download filtered data as CSV
- **Real-time Updates**: Live data updates and interactions
- **Responsive Design**: Works on desktop and mobile devices

## 🔧 Configuration

### Customizing the Streamlit App

The `streamlit_app.py` file includes:

- **Data Loading**: Automatically loads your CSV file or generates sample data
- **Interactive Filters**: Sidebar filters for data exploration
- **Multiple Chart Types**: Pie charts, line charts, scatter plots, 3D visualizations
- **Export Features**: Download filtered data

### Data Format

The Streamlit app expects CSV data with these columns:

```csv
title,category,description,x,y,z,launch_year,team_size,funding,success_rate
Project A,AI/ML,Description here,1.2,3.4,5.6,2023,5,100000,0.8
Project B,Web Dev,Another description,2.1,4.3,6.5,2022,3,50000,0.6
```

### Customizing the URL

To change the Streamlit URL, modify the `defaultStreamlitUrl` variable in `src/pages/Streamlit.tsx`:

```typescript
const defaultStreamlitUrl = 'http://your-custom-url:8501';
```

## 🎨 Customization

### Adding New Charts

To add new visualizations to the Streamlit app:

1. Open `streamlit_app.py`
2. Add new chart code in the appropriate section
3. Use Plotly Express or Graph Objects for custom charts

Example:

```python
# Add a new chart
st.subheader("New Custom Chart")
fig = px.bar(filtered_df, x='category', y='funding')
st.plotly_chart(fig, use_container_width=True)
```

### Styling

The Streamlit app includes custom CSS for better styling. Modify the CSS section in `streamlit_app.py`:

```python
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
</style>
""", unsafe_allow_html=True)
```

## 🔗 Integration Features

### Navigation

- Use the navigation bar to switch between 3D Viewer and Analytics
- The navigation shows the current active page
- Seamless integration between React and Streamlit

### Data Sharing

The integration supports:

- **Automatic Data Detection**: Streamlit app automatically loads your CSV data
- **Filtered Exports**: Export filtered data from Streamlit
- **Real-time Updates**: Changes in filters update all visualizations

### Responsive Design

- Works on desktop, tablet, and mobile devices
- Adaptive layouts for different screen sizes
- Touch-friendly controls for mobile users

## 🛠️ Troubleshooting

### Common Issues

1. **Streamlit Not Starting**
   - Check if port 8501 is available
   - Ensure all dependencies are installed
   - Check Python version compatibility

2. **Data Not Loading**
   - Verify CSV file format
   - Check file path in `streamlit_app.py`
   - Ensure CSV has required columns

3. **Connection Issues**
   - Verify Streamlit is running on `http://localhost:8501`
   - Check browser console for errors
   - Ensure no firewall blocking the connection

### Debug Mode

Enable debug logging in the React app:

```typescript
// In src/pages/Streamlit.tsx
console.log('Streamlit connection status:', isConnected);
console.log('Streamlit URL:', streamlitUrl);
```

## 📈 Advanced Features

### Custom Data Processing

Add custom data processing functions:

```python
@st.cache_data
def process_data(df):
    # Add custom processing logic
    df['processed_column'] = df['original_column'] * 2
    return df

# Use in your app
processed_df = process_data(df)
```

### Interactive Widgets

Add more interactive elements:

```python
# Add a date picker
selected_date = st.date_input("Select Date", value=datetime.now())

# Add a file uploader
uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
```

### Real-time Data Updates

For real-time data updates, you can:

1. Use Streamlit's auto-refresh feature
2. Implement WebSocket connections
3. Use external data sources with periodic updates

## 🎯 Best Practices

1. **Performance**: Use `@st.cache_data` for expensive operations
2. **User Experience**: Provide clear loading states and error messages
3. **Data Validation**: Validate input data before processing
4. **Responsive Design**: Test on different screen sizes
5. **Error Handling**: Implement proper error handling for all operations

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [React Router Documentation](https://reactrouter.com/)

## 🤝 Contributing

To contribute to the Streamlit integration:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This integration is part of the Project Explorer 3D application and follows the same license terms.
