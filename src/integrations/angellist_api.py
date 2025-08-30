"""
AngelList API Integration Module
Handles free tier API calls to fetch startup and investment data
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AngelListAPI:
    """
    AngelList API client for free tier access
    """
    
    def __init__(self, access_token: str = None):
        """
        Initialize AngelList API client
        
        Args:
            access_token (str): AngelList access token (optional for free tier)
        """
        self.access_token = access_token
        self.base_url = "https://api.angel.co/1"
        self.session = requests.Session()
        
        # Free tier limits
        self.rate_limit = 500  # requests per day
        self.requests_made = 0
        self.last_request_time = None
        
        # Headers for API requests
        self.headers = {
            'User-Agent': 'ProjectExplorerPro/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        if access_token:
            self.headers['Authorization'] = f'Bearer {access_token}'
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """
        Make API request with rate limiting
        
        Args:
            endpoint (str): API endpoint
            params (Dict): Query parameters
            
        Returns:
            Optional[Dict]: API response or None if failed
        """
        try:
            # Rate limiting check
            if self.requests_made >= self.rate_limit:
                logger.warning("Rate limit reached for AngelList API")
                return None
            
            # Add delay between requests
            if self.last_request_time:
                time_since_last = time.time() - self.last_request_time
                if time_since_last < 1:  # 1 second delay
                    time.sleep(1 - time_since_last)
            
            url = f"{self.base_url}/{endpoint}"
            response = self.session.get(url, headers=self.headers, params=params)
            
            self.last_request_time = time.time()
            self.requests_made += 1
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                logger.warning("Rate limit exceeded")
                return None
            else:
                logger.error(f"API request failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error making API request: {str(e)}")
            return None
    
    def search_startups(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for startups using free tier API
        
        Args:
            query (str): Search query
            limit (int): Number of results to return
            
        Returns:
            List[Dict]: List of startup data
        """
        params = {
            'query': query,
            'per_page': min(limit, 20),  # Free tier limit
            'page': 1
        }
        
        response = self._make_request('startups', params)
        
        if response and 'startups' in response:
            startups = []
            for startup in response['startups']:
                startup_data = {
                    'id': startup.get('id', ''),
                    'name': startup.get('name', ''),
                    'description': startup.get('description', ''),
                    'high_concept': startup.get('high_concept', ''),
                    'product_desc': startup.get('product_desc', ''),
                    'company_url': startup.get('company_url', ''),
                    'logo_url': startup.get('logo_url', ''),
                    'founded_on': startup.get('founded_on', ''),
                    'market': startup.get('market', ''),
                    'location': startup.get('location', ''),
                    'funding_total': startup.get('funding_total', 0),
                    'funding_stage': startup.get('funding_stage', ''),
                    'source': 'angellist'
                }
                startups.append(startup_data)
            
            return startups
        
        return []
    
    def get_startup_details(self, startup_id: int) -> Optional[Dict]:
        """
        Get detailed startup information
        
        Args:
            startup_id (int): Startup ID
            
        Returns:
            Optional[Dict]: Startup details
        """
        response = self._make_request(f'startups/{startup_id}')
        
        if response:
            return {
                'id': response.get('id', ''),
                'name': response.get('name', ''),
                'description': response.get('description', ''),
                'high_concept': response.get('high_concept', ''),
                'product_desc': response.get('product_desc', ''),
                'company_url': response.get('company_url', ''),
                'logo_url': response.get('logo_url', ''),
                'founded_on': response.get('founded_on', ''),
                'market': response.get('market', ''),
                'location': response.get('location', ''),
                'funding_total': response.get('funding_total', 0),
                'funding_stage': response.get('funding_stage', ''),
                'team_size': response.get('team_size', ''),
                'followers_count': response.get('followers_count', 0),
                'source': 'angellist'
            }
        
        return None
    
    def get_startup_funding_rounds(self, startup_id: int) -> List[Dict]:
        """
        Get funding rounds for a startup
        
        Args:
            startup_id (int): Startup ID
            
        Returns:
            List[Dict]: List of funding rounds
        """
        response = self._make_request(f'startups/{startup_id}/funding_rounds')
        
        if response and 'funding_rounds' in response:
            funding_rounds = []
            for round_data in response['funding_rounds']:
                funding_round = {
                    'id': round_data.get('id', ''),
                    'round_type': round_data.get('round_type', ''),
                    'funding_amount': round_data.get('funding_amount', 0),
                    'announced_on': round_data.get('announced_on', ''),
                    'investor_count': round_data.get('investor_count', 0),
                    'source': 'angellist'
                }
                funding_rounds.append(funding_round)
            
            return funding_rounds
        
        return []
    
    def get_startup_team(self, startup_id: int) -> List[Dict]:
        """
        Get team members for a startup
        
        Args:
            startup_id (int): Startup ID
            
        Returns:
            List[Dict]: List of team members
        """
        response = self._make_request(f'startups/{startup_id}/roles')
        
        if response and 'roles' in response:
            team_members = []
            for role in response['roles']:
                person = role.get('person', {})
                team_member = {
                    'id': person.get('id', ''),
                    'name': person.get('name', ''),
                    'title': role.get('title', ''),
                    'bio': person.get('bio', ''),
                    'avatar_url': person.get('avatar_url', ''),
                    'source': 'angellist'
                }
                team_members.append(team_member)
            
            return team_members
        
        return []
    
    def get_trending_startups(self, market: str = None) -> List[Dict]:
        """
        Get trending startups (free tier limited data)
        
        Args:
            market (str): Optional market filter
            
        Returns:
            List[Dict]: List of trending startups
        """
        # For free tier, we'll search for popular markets
        search_terms = ['AI', 'Fintech', 'Healthtech', 'Edtech', 'E-commerce']
        if market:
            search_terms = [market]
        
        all_startups = []
        for term in search_terms:
            startups = self.search_startups(term, limit=5)
            all_startups.extend(startups)
        
        # Remove duplicates based on ID
        unique_startups = {}
        for startup in all_startups:
            if startup['id'] not in unique_startups:
                unique_startups[startup['id']] = startup
        
        return list(unique_startups.values())[:10]
    
    def get_markets(self) -> List[Dict]:
        """
        Get available markets/categories
        
        Returns:
            List[Dict]: List of markets
        """
        response = self._make_request('markets')
        
        if response and 'markets' in response:
            markets = []
            for market in response['markets']:
                market_data = {
                    'id': market.get('id', ''),
                    'name': market.get('name', ''),
                    'display_name': market.get('display_name', ''),
                    'tag_type': market.get('tag_type', ''),
                    'source': 'angellist'
                }
                markets.append(market_data)
            
            return markets
        
        return []
    
    def get_locations(self) -> List[Dict]:
        """
        Get available locations
        
        Returns:
            List[Dict]: List of locations
        """
        response = self._make_request('locations')
        
        if response and 'locations' in response:
            locations = []
            for location in response['locations']:
                location_data = {
                    'id': location.get('id', ''),
                    'name': location.get('name', ''),
                    'display_name': location.get('display_name', ''),
                    'tag_type': location.get('tag_type', ''),
                    'source': 'angellist'
                }
                locations.append(location_data)
            
            return locations
        
        return []
    
    def get_api_usage(self) -> Dict:
        """
        Get current API usage statistics
        
        Returns:
            Dict: Usage statistics
        """
        return {
            'requests_made': self.requests_made,
            'rate_limit': self.rate_limit,
            'remaining_requests': self.rate_limit - self.requests_made,
            'last_request_time': self.last_request_time
        }
    
    def reset_usage_counter(self):
        """Reset the usage counter (call daily)"""
        self.requests_made = 0
        self.last_request_time = None


# Example usage and testing
if __name__ == "__main__":
    # Initialize API client
    api = AngelListAPI()
    
    # Search for startups
    startups = api.search_startups("AI", limit=5)
    print(f"Found {len(startups)} startups")
    
    # Get trending startups
    trending = api.get_trending_startups()
    print(f"Found {len(trending)} trending startups")
    
    # Get markets
    markets = api.get_markets()
    print(f"Found {len(markets)} markets")
    
    # Print usage stats
    usage = api.get_api_usage()
    print(f"API Usage: {usage}")
