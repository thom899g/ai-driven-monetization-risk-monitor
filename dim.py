from typing import Dict, Any
import pandas as pd

class DataIngestionModule:
    def __init__(self):
        self.data_sources = ['csv', 'json', 'api']
    
    def _validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate ingested data structure."""
        required_fields = ['revenue', 'transactions', 'market_trends']
        return all(field in data for field in required_fields)
    
    def fetch_from_csv(self, path: str) -> Dict[str, Any]:
        try:
            df = pd.read_csv(path)
            # Process dataframe to dict
            data = {
                'revenue': df['revenue'].sum(),
                'transactions': len(df),
                'market_trends': df['trend'].value_counts().to_dict()
            }
            if self._validate_data(data):
                return data
            raise ValueError("Data validation failed")
        except Exception as e:
            print(f"Error fetching from CSV: {e}")
            return None
    
    def fetch_from_json(self, path: str) -> Dict[str, Any]:
        try:
            import json
            with open(path, 'r') as f:
                data = json.load(f)
            if self._validate_data(data):
                return data
            raise ValueError("Data validation failed")
        except Exception as e:
            print(f"Error fetching from JSON: {e}")
            return None
    
    def fetch_from_api(self, url: str) -> Dict[str, Any]:
        try:
            import requests
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if self._validate_data(data):
                    return data
            raise ValueError("API request failed")
        except Exception as e:
            print(f"Error fetching from API: {e}")
            return None