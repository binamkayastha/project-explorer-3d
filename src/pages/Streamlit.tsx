import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ExternalLink, Play, Settings, Download, Upload } from 'lucide-react';
import Navigation from '@/components/Navigation';

const Streamlit: React.FC = () => {
  const [streamlitUrl, setStreamlitUrl] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [streamlitStatus, setStreamlitStatus] = useState<'idle' | 'starting' | 'running' | 'error'>('idle');

  // Default Streamlit URL - you can change this to your actual Streamlit app URL
  const defaultStreamlitUrl = 'http://localhost:8501';

  useEffect(() => {
    // Try to connect to Streamlit on component mount
    checkStreamlitConnection();
  }, []);

  const checkStreamlitConnection = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(defaultStreamlitUrl, { 
        method: 'HEAD',
        mode: 'no-cors' // This will work for local development
      });
      setIsConnected(true);
      setStreamlitUrl(defaultStreamlitUrl);
      setStreamlitStatus('running');
    } catch (error) {
      console.log('Streamlit not running locally, will show setup instructions');
      setIsConnected(false);
      setStreamlitStatus('idle');
    } finally {
      setIsLoading(false);
    }
  };

  const startStreamlitApp = async () => {
    setIsLoading(true);
    setStreamlitStatus('starting');
    
    // Simulate starting Streamlit (in real implementation, you'd call your backend)
    setTimeout(() => {
      setStreamlitStatus('running');
      setIsConnected(true);
      setStreamlitUrl(defaultStreamlitUrl);
      setIsLoading(false);
    }, 2000);
  };

  const openStreamlitApp = () => {
    if (streamlitUrl) {
      window.open(streamlitUrl, '_blank');
    }
  };

  return (
    <>
      <Navigation />
      <div className="min-h-screen bg-cosmic-deep p-8">
        <div className="max-w-6xl mx-auto space-y-8">
          {/* Header */}
          <div className="text-center space-y-4">
            <h1 className="text-4xl font-bold text-gradient-cosmic">
              Streamlit Integration
            </h1>
            <p className="text-xl text-muted-foreground">
              Connect your 3D Project Explorer with Streamlit for enhanced analytics
            </p>
          </div>

          {/* Status Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="glass-panel">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Play className="w-5 h-5 text-cosmic-aurora" />
                  Streamlit Status
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Badge 
                    variant={streamlitStatus === 'running' ? 'default' : 'secondary'}
                    className={streamlitStatus === 'running' ? 'bg-cosmic-aurora text-black' : ''}
                  >
                    {streamlitStatus === 'running' ? 'Running' : 
                     streamlitStatus === 'starting' ? 'Starting...' : 
                     streamlitStatus === 'error' ? 'Error' : 'Not Running'}
                  </Badge>
                  {streamlitStatus === 'running' && (
                    <p className="text-sm text-muted-foreground">
                      Connected to {streamlitUrl}
                    </p>
                  )}
                </div>
              </CardContent>
            </Card>

            <Card className="glass-panel">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="w-5 h-5 text-cosmic-plasma" />
                  Configuration
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <p className="text-sm text-muted-foreground">
                    Port: 8501
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Host: localhost
                  </p>
                </div>
              </CardContent>
            </Card>

            <Card className="glass-panel">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Download className="w-5 h-5 text-cosmic-star" />
                  Data Export
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Button 
                    variant="outline" 
                    size="sm" 
                    className="btn-ghost-cosmic w-full"
                    onClick={() => {/* Export data to Streamlit */}}
                  >
                    <Upload className="w-4 h-4 mr-2" />
                    Export to Streamlit
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Streamlit App Embed */}
            <div className="lg:col-span-2">
              <Card className="glass-panel h-[600px]">
                <CardHeader>
                  <CardTitle>Streamlit Dashboard</CardTitle>
                  <CardDescription>
                    Interactive analytics and visualizations for your project data
                  </CardDescription>
                </CardHeader>
                <CardContent className="h-full p-0">
                  {isConnected && streamlitStatus === 'running' ? (
                    <iframe
                      src={streamlitUrl}
                      className="w-full h-full border-0 rounded-b-lg"
                      title="Streamlit App"
                      sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
                    />
                  ) : (
                    <div className="h-full flex items-center justify-center">
                      <div className="text-center space-y-4">
                        <div className="w-16 h-16 mx-auto rounded-full bg-cosmic-nebula/20 flex items-center justify-center">
                          {isLoading ? (
                            <div className="cosmic-spinner" />
                          ) : (
                            <Play className="w-8 h-8 text-cosmic-aurora" />
                          )}
                        </div>
                        <div>
                          <h3 className="text-lg font-semibold text-foreground">
                            {isLoading ? 'Starting Streamlit...' : 'Streamlit Not Running'}
                          </h3>
                          <p className="text-muted-foreground">
                            {isLoading 
                              ? 'Please wait while we start the Streamlit application...'
                              : 'Click the button below to start the Streamlit app'
                            }
                          </p>
                        </div>
                        {!isLoading && (
                          <Button 
                            onClick={startStreamlitApp}
                            className="btn-cosmic"
                          >
                            <Play className="w-4 h-4 mr-2" />
                            Start Streamlit App
                          </Button>
                        )}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Quick Actions */}
              <Card className="glass-panel">
                <CardHeader>
                  <CardTitle>Quick Actions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <Button 
                    variant="outline" 
                    className="btn-ghost-cosmic w-full justify-start"
                    onClick={openStreamlitApp}
                    disabled={!isConnected}
                  >
                    <ExternalLink className="w-4 h-4 mr-2" />
                    Open in New Tab
                  </Button>
                  <Button 
                    variant="outline" 
                    className="btn-ghost-cosmic w-full justify-start"
                    onClick={checkStreamlitConnection}
                    disabled={isLoading}
                  >
                    <Settings className="w-4 h-4 mr-2" />
                    Refresh Connection
                  </Button>
                </CardContent>
              </Card>

              {/* Setup Instructions */}
              <Card className="glass-panel">
                <CardHeader>
                  <CardTitle>Setup Instructions</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 text-sm">
                    <div>
                      <h4 className="font-medium text-foreground mb-1">1. Install Streamlit</h4>
                      <code className="block bg-cosmic-nebula/30 px-2 py-1 rounded text-xs">
                        pip install streamlit
                      </code>
                    </div>
                    <div>
                      <h4 className="font-medium text-foreground mb-1">2. Create Streamlit App</h4>
                      <p className="text-muted-foreground text-xs">
                        Create a Python file (e.g., app.py) with your Streamlit code
                      </p>
                    </div>
                    <div>
                      <h4 className="font-medium text-foreground mb-1">3. Run Streamlit</h4>
                      <code className="block bg-cosmic-nebula/30 px-2 py-1 rounded text-xs">
                        streamlit run app.py
                      </code>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Features */}
              <Card className="glass-panel">
                <CardHeader>
                  <CardTitle>Streamlit Features</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-cosmic-aurora rounded-full" />
                      <span>Interactive Charts</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-cosmic-plasma rounded-full" />
                      <span>Data Tables</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-cosmic-star rounded-full" />
                      <span>Real-time Updates</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-cosmic-aurora rounded-full" />
                      <span>Custom Widgets</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Sample Streamlit Code */}
          <Card className="glass-panel">
            <CardHeader>
              <CardTitle>Sample Streamlit App Code</CardTitle>
              <CardDescription>
                Here's a basic example of how to create a Streamlit app for your project data
              </CardDescription>
            </CardHeader>
            <CardContent>
              <pre className="bg-cosmic-nebula/30 p-4 rounded-lg overflow-x-auto text-sm">
{`import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Project Explorer Analytics",
    page_icon="🚀",
    layout="wide"
)

# Title
st.title("🚀 Project Explorer Analytics")
st.markdown("Interactive analytics for your 3D project dataset")

# Sample data (replace with your actual data loading)
@st.cache_data
def load_data():
    # Load your CSV data here
    # df = pd.read_csv('your_projects.csv')
    
    # Sample data for demonstration
    data = {
        'title': ['Project A', 'Project B', 'Project C'],
        'category': ['AI', 'Web', 'Mobile'],
        'x': [1, 2, 3],
        'y': [4, 5, 6],
        'z': [7, 8, 9],
        'launch_year': [2023, 2022, 2024]
    }
    return pd.DataFrame(data)

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_category = st.sidebar.selectbox(
    "Select Category",
    ['All'] + list(df['category'].unique())
)

# Filter data
if selected_category != 'All':
    filtered_df = df[df['category'] == selected_category]
else:
    filtered_df = df

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Project Distribution")
    fig = px.pie(filtered_df, names='category', title='Projects by Category')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📈 Launch Year Trends")
    fig = px.histogram(filtered_df, x='launch_year', title='Projects by Launch Year')
    st.plotly_chart(fig, use_container_width=True)

# 3D Scatter Plot
st.subheader("🌌 3D Project Visualization")
fig = go.Figure(data=[go.Scatter3d(
    x=filtered_df['x'],
    y=filtered_df['y'],
    z=filtered_df['z'],
    mode='markers',
    marker=dict(
        size=8,
        color=filtered_df['launch_year'],
        colorscale='Viridis',
        opacity=0.8
    ),
    text=filtered_df['title'],
    hovertemplate='<b>%{text}</b><br>' +
                  'X: %{x}<br>' +
                  'Y: %{y}<br>' +
                  'Z: %{z}<extra></extra>'
)])

fig.update_layout(
    title='3D Project Space',
    scene=dict(
        xaxis_title='X Coordinate',
        yaxis_title='Y Coordinate',
        zaxis_title='Z Coordinate'
    ),
    width=800,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# Data table
st.subheader("📋 Project Data")
st.dataframe(filtered_df, use_container_width=True)

# Metrics
st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Projects", len(filtered_df))

with col2:
    st.metric("Categories", filtered_df['category'].nunique())

with col3:
    st.metric("Avg Launch Year", round(filtered_df['launch_year'].mean(), 1))

with col4:
    st.metric("Latest Project", filtered_df['launch_year'].max())`}
              </pre>
            </CardContent>
          </Card>
        </div>
      </div>
    </>
  );
};

export default Streamlit;
