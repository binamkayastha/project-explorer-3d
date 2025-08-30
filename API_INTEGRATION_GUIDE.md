# 🚀 API Integration Guide - Crunchbase & AngelList

## 📋 Overview

This guide explains how to use the integrated Crunchbase and AngelList APIs in Project Explorer Pro. The integration provides real-time startup and company data to enhance your project analysis and market research capabilities.

## 🔑 API Setup

### Crunchbase API

1. **Get Free API Key:**
   - Visit [Crunchbase Data](https://data.crunchbase.com/)
   - Sign up for a free account
   - Navigate to API section
   - Generate your API key

2. **Free Tier Limits:**
   - 1,000 requests per day
   - Basic company information
   - Limited search capabilities

### AngelList API

1. **Get Access Token:**
   - Visit [AngelList Developer Portal](https://angel.co/api)
   - Create a developer account
   - Generate your access token

2. **Free Tier Limits:**
   - 500 requests per day
   - Basic startup information
   - Limited data fields

## 🛠️ Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables (Optional)

```bash
# For Crunchbase API
export CRUNCHBASE_API_KEY="your_crunchbase_api_key"

# For AngelList API
export ANGELLIST_TOKEN="your_angellist_token"
```

### 3. Run the Enhanced App

```bash
streamlit run streamlit_app_with_apis.py --server.port 8512
```

## 📊 Features

### 🔍 Startup Search
- Search across both Crunchbase and AngelList
- Filter by funding, location, and category
- Real-time results with detailed information

### 📈 Market Insights
- Comprehensive analytics and trends
- Funding distribution analysis
- Source data comparison

### 🔥 Trending Startups
- Discover trending companies by category
- Real-time market intelligence
- Funding and growth metrics

### ⚙️ API Management
- Usage statistics and monitoring
- Rate limit tracking
- Connection testing

## 🎯 Usage Examples

### Basic Startup Search

```python
from src.integrations import StartupDataManager

# Initialize manager
manager = StartupDataManager(
    crunchbase_api_key="your_key",
    angellist_token="your_token"
)

# Search for startups
startups = manager.search_startups("AI", limit=20)
print(f"Found {len(startups)} startups")
```

### Get Trending Startups

```python
# Get trending startups in AI category
trending = manager.get_trending_startups("AI", limit=10)

for startup in trending:
    print(f"{startup['name']}: {startup['funding_total']}")
```

### Comprehensive Insights

```python
# Get market insights
insights = manager.get_combined_insights("fintech")

print(f"Total startups: {insights['total_startups_found']}")
print(f"Total funding: ${insights['total_funding']:,.0f}")
```

## 📁 File Structure

```
src/integrations/
├── __init__.py                 # Package initialization
├── crunchbase_api.py          # Crunchbase API client
├── angellist_api.py           # AngelList API client
├── api_manager.py             # Unified API manager
└── streamlit_integration.py   # Streamlit UI components
```

## 🔧 API Classes

### CrunchbaseAPI

```python
class CrunchbaseAPI:
    def search_companies(query: str, limit: int = 10) -> List[Dict]
    def get_company_details(company_uuid: str) -> Optional[Dict]
    def get_funding_rounds(company_uuid: str) -> List[Dict]
    def get_company_people(company_uuid: str) -> List[Dict]
    def get_trending_companies(category: str = None) -> List[Dict]
    def get_api_usage() -> Dict
```

### AngelListAPI

```python
class AngelListAPI:
    def search_startups(query: str, limit: int = 10) -> List[Dict]
    def get_startup_details(startup_id: int) -> Optional[Dict]
    def get_startup_funding_rounds(startup_id: int) -> List[Dict]
    def get_startup_team(startup_id: int) -> List[Dict]
    def get_trending_startups(market: str = None) -> List[Dict]
    def get_markets() -> List[Dict]
    def get_locations() -> List[Dict]
    def get_api_usage() -> Dict
```

### StartupDataManager

```python
class StartupDataManager:
    def search_startups(query: str, limit: int = 20, sources: List[str] = None) -> List[Dict]
    def get_trending_startups(category: str = None, limit: int = 20) -> List[Dict]
    def get_startup_details(startup_id: str, source: str) -> Optional[Dict]
    def get_funding_rounds(startup_id: str, source: str) -> List[Dict]
    def get_team_members(startup_id: str, source: str) -> List[Dict]
    def get_combined_insights(query: str) -> Dict[str, Any]
    def get_api_usage_stats() -> Dict[str, Dict]
```

## 📊 Data Formats

### Startup Data Structure

```python
{
    'id': 'unique_identifier',
    'name': 'Company Name',
    'description': 'Company description',
    'high_concept': 'Brief concept',
    'company_url': 'https://company.com',
    'logo_url': 'https://logo.png',
    'funding_total': 1000000,
    'market': 'AI/ML',
    'location': 'San Francisco, CA',
    'source': 'crunchbase',  # or 'angellist'
    'source_id': 'original_id'
}
```

### Funding Round Structure

```python
{
    'id': 'round_id',
    'round_type': 'Series A',
    'funding_amount': 5000000,
    'announced_on': '2023-01-15',
    'investor_count': 3,
    'source': 'crunchbase'
}
```

### Team Member Structure

```python
{
    'id': 'person_id',
    'name': 'John Doe',
    'title': 'CEO',
    'bio': 'Professional bio',
    'avatar_url': 'https://avatar.png',
    'source': 'angellist'
}
```

## 🎨 Streamlit Integration

### Adding to Sidebar

```python
from src.integrations import add_startup_data_to_sidebar

# Add startup data options to sidebar
add_startup_data_to_sidebar()
```

### Rendering Pages

```python
from src.integrations import render_startup_data_pages

# Render startup data pages
render_startup_data_pages()
```

## ⚠️ Error Handling

### Rate Limiting

The APIs automatically handle rate limiting:

```python
# Check usage before making requests
usage = manager.get_api_usage_stats()
if usage['crunchbase']['remaining_requests'] < 10:
    print("Warning: Low API quota remaining")
```

### Connection Errors

```python
try:
    startups = manager.search_startups("AI")
except Exception as e:
    print(f"API Error: {str(e)}")
    # Fallback to cached data or mock data
```

## 🔄 Caching Strategy

### Session State Caching

```python
# Cache API results in session state
if 'cached_startups' not in st.session_state:
    st.session_state.cached_startups = {}

# Use cached data if available
cache_key = f"search_{query}_{limit}"
if cache_key in st.session_state.cached_startups:
    startups = st.session_state.cached_startups[cache_key]
else:
    startups = manager.search_startups(query, limit)
    st.session_state.cached_startups[cache_key] = startups
```

## 📈 Performance Optimization

### Batch Requests

```python
# Batch multiple searches
queries = ["AI", "fintech", "healthtech"]
all_startups = []

for query in queries:
    startups = manager.search_startups(query, limit=5)
    all_startups.extend(startups)
```

### Async Processing

```python
import asyncio
import aiohttp

async def async_search_startups(queries):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for query in queries:
            task = search_startup_async(session, query)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results
```

## 🧪 Testing

### Unit Tests

```python
import pytest
from src.integrations import StartupDataManager

def test_startup_search():
    manager = StartupDataManager()
    startups = manager.search_startups("test", limit=5)
    assert len(startups) <= 5
    assert all('name' in startup for startup in startups)

def test_api_usage():
    manager = StartupDataManager()
    usage = manager.get_api_usage_stats()
    assert 'crunchbase' in usage
    assert 'angellist' in usage
```

### Integration Tests

```python
def test_full_workflow():
    manager = StartupDataManager()
    
    # Search startups
    startups = manager.search_startups("AI", limit=10)
    assert len(startups) > 0
    
    # Get insights
    insights = manager.get_combined_insights("AI")
    assert insights['total_startups_found'] > 0
    
    # Check usage
    usage = manager.get_api_usage_stats()
    assert usage['crunchbase']['requests_made'] > 0
```

## 🚀 Advanced Features

### Custom Filters

```python
def filter_startups_by_funding(startups, min_funding=1000000):
    return [s for s in startups if s.get('funding_total', 0) >= min_funding]

def filter_startups_by_location(startups, location):
    return [s for s in startups if location.lower() in s.get('location', '').lower()]
```

### Data Enrichment

```python
def enrich_startup_data(startup):
    # Add calculated fields
    startup['funding_category'] = categorize_funding(startup.get('funding_total', 0))
    startup['age'] = calculate_company_age(startup.get('founded_on'))
    startup['growth_score'] = calculate_growth_score(startup)
    return startup

def categorize_funding(amount):
    if amount == 0:
        return 'Bootstrap'
    elif amount < 1000000:
        return 'Seed'
    elif amount < 10000000:
        return 'Series A'
    else:
        return 'Series B+'
```

## 📚 Best Practices

### 1. API Key Management
- Store API keys securely (environment variables)
- Rotate keys regularly
- Monitor usage to avoid rate limits

### 2. Error Handling
- Always wrap API calls in try-catch blocks
- Implement fallback mechanisms
- Log errors for debugging

### 3. Caching
- Cache frequently requested data
- Implement TTL (Time To Live) for cache
- Clear cache when data becomes stale

### 4. Rate Limiting
- Monitor API usage closely
- Implement exponential backoff
- Queue requests when approaching limits

### 5. Data Validation
- Validate API responses
- Handle missing or malformed data
- Implement data sanitization

## 🔮 Future Enhancements

### Planned Features
- [ ] Real-time data streaming
- [ ] Advanced analytics dashboard
- [ ] Machine learning insights
- [ ] Export functionality
- [ ] Webhook integrations
- [ ] Multi-language support

### API Improvements
- [ ] GraphQL support
- [ ] WebSocket connections
- [ ] Batch processing
- [ ] Advanced filtering
- [ ] Custom aggregations

## 📞 Support

### Documentation
- [Crunchbase API Docs](https://data.crunchbase.com/docs)
- [AngelList API Docs](https://angel.co/api)

### Community
- GitHub Issues: Report bugs and feature requests
- Discord: Join our community for discussions
- Email: support@projectexplorerpro.com

### Troubleshooting

Common issues and solutions:

1. **API Key Invalid**
   - Verify key format and permissions
   - Check account status
   - Regenerate if necessary

2. **Rate Limit Exceeded**
   - Implement caching
   - Reduce request frequency
   - Upgrade API plan if needed

3. **Connection Timeout**
   - Check internet connection
   - Verify API endpoints
   - Implement retry logic

4. **Data Inconsistencies**
   - Validate response format
   - Handle missing fields
   - Implement data normalization

---

**Happy coding! 🚀**

*For more information, visit [Project Explorer Pro Documentation](https://docs.projectexplorerpro.com)*
