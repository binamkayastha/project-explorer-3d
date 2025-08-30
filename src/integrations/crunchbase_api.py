"""
Crunchbase API Integration Module
Handles free tier API calls to fetch company and startup data
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

class CrunchbaseAPI:
    """
    Crunchbase API client for free tier access
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Crunchbase API client
        
        Args:
            api_key (str): Crunchbase API key (optional for free tier)
        """
        self.api_key = api_key
        self.base_url = "https://api.crunchbase.com/api/v4"
        self.session = requests.Session()
        
        # Free tier limits
        self.rate_limit = 1000  # requests per day
        self.requests_made = 0
        self.last_request_time = None
        
        # Headers for API requests
        self.headers = {
            'User-Agent': 'ProjectExplorerPro/1.0',
            'Accept': 'application/json'
        }
        
        if api_key:
            self.headers['X-cb-user-key'] = api_key
    
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
                logger.warning("Rate limit reached for Crunchbase API")
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
    
    def search_companies(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for companies using free tier API
        
        Args:
            query (str): Search query
            limit (int): Number of results to return
            
        Returns:
            List[Dict]: List of company data
        """
        params = {
            'query': query,
            'limit': min(limit, 20),  # Free tier limit
            'field_ids': 'name,description,funding_total,homepage_url,profile_image_url'
        }
        
        response = self._make_request('entities/organizations', params)
        
        if response and 'entities' in response:
            companies = []
            for entity in response['entities']:
                company_data = {
                    'name': entity.get('properties', {}).get('name', ''),
                    'description': entity.get('properties', {}).get('description', ''),
                    'funding_total': entity.get('properties', {}).get('funding_total', {}).get('value_usd', 0),
                    'homepage_url': entity.get('properties', {}).get('homepage_url', ''),
                    'profile_image_url': entity.get('properties', {}).get('profile_image_url', ''),
                    'uuid': entity.get('uuid', ''),
                    'source': 'crunchbase'
                }
                companies.append(company_data)
            
            return companies
        
        return []
    
    def get_company_details(self, company_uuid: str) -> Optional[Dict]:
        """
        Get detailed company information
        
        Args:
            company_uuid (str): Company UUID
            
        Returns:
            Optional[Dict]: Company details
        """
        params = {
            'field_ids': 'name,description,funding_total,homepage_url,profile_image_url,founded_on,headquarters_location,short_description'
        }
        
        response = self._make_request(f'entities/organizations/{company_uuid}', params)
        
        if response and 'properties' in response:
            properties = response['properties']
            return {
                'name': properties.get('name', ''),
                'description': properties.get('description', ''),
                'short_description': properties.get('short_description', ''),
                'funding_total': properties.get('funding_total', {}).get('value_usd', 0),
                'homepage_url': properties.get('homepage_url', ''),
                'profile_image_url': properties.get('profile_image_url', ''),
                'founded_on': properties.get('founded_on', ''),
                'headquarters_location': properties.get('headquarters_location', {}),
                'uuid': company_uuid,
                'source': 'crunchbase'
            }
        
        return None
    
    def get_funding_rounds(self, company_uuid: str) -> List[Dict]:
        """
        Get funding rounds for a company
        
        Args:
            company_uuid (str): Company UUID
            
        Returns:
            List[Dict]: List of funding rounds
        """
        params = {
            'field_ids': 'funding_rounds'
        }
        
        response = self._make_request(f'entities/organizations/{company_uuid}/funding_rounds', params)
        
        if response and 'entities' in response:
            funding_rounds = []
            for entity in response['entities']:
                properties = entity.get('properties', {})
                funding_round = {
                    'round_type': properties.get('round_type', ''),
                    'funding_amount': properties.get('funding_amount', {}).get('value_usd', 0),
                    'announced_on': properties.get('announced_on', ''),
                    'investor_count': properties.get('investor_count', 0),
                    'uuid': entity.get('uuid', ''),
                    'source': 'crunchbase'
                }
                funding_rounds.append(funding_round)
            
            return funding_rounds
        
        return []
    
    def get_company_people(self, company_uuid: str) -> List[Dict]:
        """
        Get people associated with a company
        
        Args:
            company_uuid (str): Company UUID
            
        Returns:
            List[Dict]: List of people
        """
        params = {
            'field_ids': 'name,title,profile_image_url'
        }
        
        response = self._make_request(f'entities/organizations/{company_uuid}/people', params)
        
        if response and 'entities' in response:
            people = []
            for entity in response['entities']:
                properties = entity.get('properties', {})
                person = {
                    'name': properties.get('name', ''),
                    'title': properties.get('title', ''),
                    'profile_image_url': properties.get('profile_image_url', ''),
                    'uuid': entity.get('uuid', ''),
                    'source': 'crunchbase'
                }
                people.append(person)
            
            return people
        
        return []
    
    def get_trending_companies(self, category: str = None) -> List[Dict]:
        """
        Get trending companies (free tier limited data)
        
        Args:
            category (str): Optional category filter
            
        Returns:
            List[Dict]: List of trending companies
        """
        # For free tier, we'll search for recent companies
        search_terms = ['startup', 'tech', 'ai', 'fintech', 'healthtech']
        if category:
            search_terms = [category]
        
        all_companies = []
        for term in search_terms:
            companies = self.search_companies(term, limit=5)
            all_companies.extend(companies)
        
        # Remove duplicates based on UUID
        unique_companies = {}
        for company in all_companies:
            if company['uuid'] not in unique_companies:
                unique_companies[company['uuid']] = company
        
        return list(unique_companies.values())[:10]
    
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
    api = CrunchbaseAPI()
    
    # Search for companies
    companies = api.search_companies("AI startup", limit=5)
    print(f"Found {len(companies)} companies")
    
    # Get trending companies
    trending = api.get_trending_companies()
    print(f"Found {len(trending)} trending companies")
    
    # Print usage stats
    usage = api.get_api_usage()
    print(f"API Usage: {usage}")
