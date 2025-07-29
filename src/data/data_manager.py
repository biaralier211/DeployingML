"""
Data management for KMart ML API - Optimized for Render deployment
"""

import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import os
import json
from typing import Dict, Any

class DataManager:
    def __init__(self):
        self.product_df = None
        self.interaction_df = None
        
    def load_models(self):
        """Load all data and initialize lightweight models"""
        print("Loading models...")
        
        try:
            # Load product data
            if os.path.exists("data_csv/product_data_cleaned.csv"):
                self.product_df = pd.read_csv("data_csv/product_data_cleaned.csv")
            else:
                # Create sample data if file doesn't exist
                self.product_df = self._create_sample_data()
            
            # Load interaction data if available
            if os.path.exists("data_csv/product_interactions_data_fixed.csv"):
                self.interaction_df = pd.read_csv("data_csv/product_interactions_data_fixed.csv")
                self.interaction_df['timestamp'] = pd.to_datetime(self.interaction_df['timestamp'], errors='coerce')
            else:
                # Create empty interaction dataframe
                self.interaction_df = pd.DataFrame(columns=[
                    'interactionId', 'userId', 'productId', 'interactionType', 
                    'timestamp', 'quantity', 'value', 'rating', 'review', 
                    'sentiment', 'socialSharePlatform', 'metadata'
                ])
            
            print("Models loaded successfully!")
            
        except Exception as e:
            print(f"Warning: Error loading data: {e}")
            # Create minimal sample data
            self.product_df = self._create_sample_data()
            self.interaction_df = pd.DataFrame()
    
    def _create_sample_data(self):
        """Create sample product data for testing"""
        sample_products = [
            {
                'id': 'prod_001',
                'name': 'Wireless Bluetooth Headphones',
                'description': 'High-quality wireless headphones with noise cancellation',
                'price': 89.99,
                'rating': 4.5,
                'category': 'Electronics',
                'condition': 'New',
                'location': 'Warehouse A'
            },
            {
                'id': 'prod_002',
                'name': 'Smart Fitness Watch',
                'description': 'Track your fitness goals with this advanced smartwatch',
                'price': 199.99,
                'rating': 4.3,
                'category': 'Electronics',
                'condition': 'New',
                'location': 'Warehouse B'
            },
            {
                'id': 'prod_003',
                'name': 'Organic Cotton T-Shirt',
                'description': 'Comfortable organic cotton t-shirt in various colors',
                'price': 24.99,
                'rating': 4.7,
                'category': 'Clothing',
                'condition': 'New',
                'location': 'Warehouse C'
            },
            {
                'id': 'prod_004',
                'name': 'Stainless Steel Water Bottle',
                'description': 'Keep your drinks cold for 24 hours with this insulated bottle',
                'price': 34.99,
                'rating': 4.6,
                'category': 'Home & Garden',
                'condition': 'New',
                'location': 'Warehouse A'
            },
            {
                'id': 'prod_005',
                'name': 'Wireless Charging Pad',
                'description': 'Fast wireless charging pad compatible with all smartphones',
                'price': 49.99,
                'rating': 4.4,
                'category': 'Electronics',
                'condition': 'New',
                'location': 'Warehouse B'
            }
        ]
        
        return pd.DataFrame(sample_products)
    
    def save_interaction(self, interaction_data: Dict[str, Any]) -> str:
        """Save interaction to CSV file"""
        try:
            # Generate unique interaction ID
            interaction_id = f"int_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{interaction_data['user_id']}"
            
            # Prepare data for CSV
            csv_data = {
                'interactionId': interaction_id,
                'userId': interaction_data['user_id'],
                'productId': interaction_data.get('product_id', ''),
                'interactionType': interaction_data['interaction_type'],
                'timestamp': datetime.now().isoformat(),
                'quantity': interaction_data.get('quantity', ''),
                'value': interaction_data.get('value', ''),
                'rating': interaction_data.get('rating', ''),
                'review': interaction_data.get('review', ''),
                'sentiment': interaction_data.get('sentiment', ''),
                'socialSharePlatform': interaction_data.get('socialSharePlatform', ''),
                'metadata': json.dumps(interaction_data.get('metadata', {}))
            }
            
            # Append to interaction dataframe
            new_row = pd.DataFrame([csv_data])
            self.interaction_df = pd.concat([self.interaction_df, new_row], ignore_index=True)
            
            # Save to CSV (optional - for persistence)
            try:
                self.interaction_df.to_csv("data_csv/product_interactions_data_fixed.csv", index=False)
            except Exception as e:
                print(f"Warning: Could not save interactions to file: {e}")
            
            return interaction_id
            
        except Exception as e:
            raise Exception(f"Error saving interaction: {str(e)}")
    
    def get_product_info(self, product_id: str):
        """Get product information by ID"""
        try:
            if self.product_df is not None:
                product = self.product_df[self.product_df['id'] == product_id]
                if not product.empty:
                    return product.iloc[0].to_dict()
            return None
        except Exception as e:
            print(f"Error getting product info: {e}")
            return None
    
    def extract_price(self, product_info):
        """Extract price from product information"""
        try:
            if isinstance(product_info, dict):
                return float(product_info.get('price', 0.0))
            elif hasattr(product_info, 'get'):
                return float(product_info.get('price', 0.0))
            else:
                return 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def get_user_interactions(self, user_id: str, limit: int = 50):
        """Get all interactions for a specific user"""
        try:
            if self.interaction_df is not None and not self.interaction_df.empty:
                user_interactions = self.interaction_df[
                    self.interaction_df['userId'] == user_id
                ].head(limit)
                return user_interactions.to_dict('records')
            return []
        except Exception as e:
            print(f"Error getting user interactions: {e}")
            return []
    
    def get_product_interactions(self, product_id: str, limit: int = 50):
        """Get all interactions for a specific product"""
        try:
            if self.interaction_df is not None and not self.interaction_df.empty:
                product_interactions = self.interaction_df[
                    self.interaction_df['productId'] == product_id
                ].head(limit)
                return product_interactions.to_dict('records')
            return []
        except Exception as e:
            print(f"Error getting product interactions: {e}")
            return [] 