"""
Data management for KMart ML API
"""

import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import os
from transformers import AutoTokenizer, AutoModel
import torch
import json
from typing import Dict, Any

class DataManager:
    def __init__(self):
        self.cf_model = None
        self.user_map = None
        self.item_map = None
        self.product_df = None
        self.interaction_df = None
        self.tokenizer = None
        self.model = None
        self.product_embeddings = None
        
    def load_models(self):
        """Load all ML models and data"""
        print("Loading models...")
        
        # Load collaborative filtering model
        with open("collaborative_filtering_model.pkl", "rb") as f:
            self.cf_model = pickle.load(f)
        
        # Load mappings
        with open("user_id_map.pkl", "rb") as f:
            self.user_map = pickle.load(f)
        with open("product_id_map.pkl", "rb") as f:
            self.item_map = pickle.load(f)
        
        # Load product data
        self.product_df = pd.read_csv("data_csv/product_data_cleaned.csv")
        
        # Load search model
        MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModel.from_pretrained(MODEL_NAME)
        
        # Load or generate product embeddings
        self._load_product_embeddings()
        
        # Load interaction data
        self.interaction_df = pd.read_csv("data_csv/product_interactions_data_fixed.csv")
        self.interaction_df['timestamp'] = pd.to_datetime(self.interaction_df['timestamp'], errors='coerce')
        
        print("Models loaded successfully!")
    
    def _load_product_embeddings(self):
        """Load or generate product embeddings"""
        if os.path.exists("product_embeddings.npy"):
            self.product_embeddings = np.load("product_embeddings.npy")
        else:
            print("Generating product embeddings...")
            if 'description' in self.product_df.columns:
                texts = (self.product_df['name'] + " " + self.product_df['description']).fillna("")
            else:
                texts = self.product_df['name'].fillna("")
            
            self.product_embeddings = self._embed_texts(texts)
            np.save("product_embeddings.npy", self.product_embeddings)
    
    def _embed_texts(self, texts):
        """Generate embeddings for text"""
        inputs = self.tokenizer(list(texts), padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            model_output = self.model(**inputs)
        embeddings = model_output.last_hidden_state.mean(dim=1)
        return embeddings.numpy()
    
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
            
            # Append to CSV file
            new_row = pd.DataFrame([csv_data])
            new_row.to_csv("data_csv/product_interactions_data_fixed.csv", mode='a', header=False, index=False)
            
            # Update the loaded interaction_df without reloading the entire file
            new_row['timestamp'] = pd.to_datetime(new_row['timestamp'], format='mixed')
            self.interaction_df = pd.concat([self.interaction_df, new_row], ignore_index=True)
            
            return interaction_id
        except Exception as e:
            print(f"Error saving interaction: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_product_info(self, product_id: str):
        """Get product information by ID"""
        product_info = self.product_df[self.product_df['id'] == product_id]
        if not product_info.empty:
            return product_info.iloc[0]
        return None
    
    def extract_price(self, product_info):
        """Extract price from product info"""
        price_str = product_info.get('priceAndDiscount', '0')
        try:
            # Remove 'Ugx' prefix and convert to float
            price = float(price_str.replace('Ugx', '').replace(',', ''))
        except:
            price = 0.0
        return price 