"""
ML services for KMart ML API
"""

import numpy as np
import torch
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
from typing import List, Dict, Any
from src.models.models import ProductRecommendation, SearchResult, TrendingProduct, SimilarProduct

class MLServices:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def get_recommendations(self, user_id: str, num_recommendations: int = 5) -> List[ProductRecommendation]:
        """Get product recommendations for a user"""
        try:
            # Find user index
            user_index = None
            for idx, uid in self.data_manager.user_map.items():
                if uid == user_id:
                    user_index = idx
                    break
            
            if user_index is None:
                # Handle new user (cold start)
                user_index = 0  # Use default recommendations
            
            # Get recommendations
            user_items = csr_matrix((1, self.data_manager.cf_model.item_factors.shape[0]), dtype=np.float32)
            
            item_indices, scores = self.data_manager.cf_model.recommend(
                user_index, 
                user_items, 
                N=num_recommendations
            )
            
            recommendations = []
            for item_idx, score in zip(item_indices, scores):
                if abs(score) < 1e6:  # Filter out invalid scores
                    product_id = self.data_manager.item_map[item_idx]
                    
                    # Get product details
                    product_info = self.data_manager.get_product_info(product_id)
                    if product_info is not None:
                        price = self.data_manager.extract_price(product_info)
                        
                        recommendations.append(ProductRecommendation(
                            product_id=product_id,
                            name=product_info.get('name', 'Unknown Product'),
                            description=product_info.get('description', ''),
                            price=price,
                            score=float(score)
                        ))
            
            return recommendations[:num_recommendations]
        
        except Exception as e:
            raise Exception(f"Error getting recommendations: {str(e)}")
    
    def search_products(self, query: str, num_results: int = 5) -> List[SearchResult]:
        """Search products using semantic search"""
        try:
            # Embed the query
            inputs = self.data_manager.tokenizer([query], padding=True, truncation=True, return_tensors="pt")
            with torch.no_grad():
                model_output = self.data_manager.model(**inputs)
            query_emb = model_output.last_hidden_state.mean(dim=1).numpy()
            
            # Calculate similarities
            similarities = cosine_similarity(query_emb, self.data_manager.product_embeddings)[0]
            top_indices = similarities.argsort()[::-1][:num_results]
            
            results = []
            for idx in top_indices:
                product_info = self.data_manager.product_df.iloc[idx]
                price = self.data_manager.extract_price(product_info)
                
                results.append(SearchResult(
                    product_id=product_info.get('id', ''),
                    name=product_info.get('name', 'Unknown Product'),
                    description=product_info.get('description', ''),
                    price=price,
                    score=float(similarities[idx])
                ))
            
            return results
        
        except Exception as e:
            raise Exception(f"Error searching products: {str(e)}")
    
    def get_trending_products(self, days: int = 7, limit: int = 10) -> List[TrendingProduct]:
        """Get trending products based on recent interactions"""
        try:
            # Filter recent interactions
            recent = self.data_manager.interaction_df[
                self.data_manager.interaction_df['timestamp'] > (datetime.now() - timedelta(days=days))
            ]
            
            # If no recent interactions, fall back to overall popular products
            if recent.empty:
                print(f"No recent interactions found in last {days} days, using overall popular products")
                trending_counts = self.data_manager.interaction_df['productId'].value_counts().head(limit)
            else:
                # Count interactions per product
                trending_counts = recent['productId'].value_counts().head(limit)
            
            trending_products = []
            for product_id, count in trending_counts.items():
                # Get product details
                product_info = self.data_manager.get_product_info(product_id)
                if product_info is not None:
                    price = self.data_manager.extract_price(product_info)
                    
                    trending_products.append(TrendingProduct(
                        product_id=product_id,
                        name=product_info.get('name', 'Unknown Product'),
                        description=product_info.get('description', ''),
                        price=price,
                        interaction_count=int(count)
                    ))
            
            return trending_products
        
        except Exception as e:
            raise Exception(f"Error getting trending products: {str(e)}")
    
    def get_similar_products(self, product_id: str, limit: int = 5) -> List[SimilarProduct]:
        """Get similar products based on product embeddings"""
        try:
            # Find the product index
            product_index = None
            for idx, row in self.data_manager.product_df.iterrows():
                if row['id'] == product_id:
                    product_index = idx
                    break
            
            if product_index is None:
                raise Exception("Product not found")
            
            # Get the product's embedding
            product_embedding = self.data_manager.product_embeddings[product_index].reshape(1, -1)
            
            # Calculate similarities with all other products
            similarities = cosine_similarity(product_embedding, self.data_manager.product_embeddings)[0]
            
            # Get top similar products (excluding the product itself)
            similar_indices = similarities.argsort()[::-1][1:limit+1]  # Skip the first (itself)
            
            similar_products = []
            for idx in similar_indices:
                product_info = self.data_manager.product_df.iloc[idx]
                price = self.data_manager.extract_price(product_info)
                
                similar_products.append(SimilarProduct(
                    product_id=product_info.get('id', ''),
                    name=product_info.get('name', 'Unknown Product'),
                    description=product_info.get('description', ''),
                    price=price,
                    similarity_score=float(similarities[idx])
                ))
            
            return similar_products
        
        except Exception as e:
            raise Exception(f"Error getting similar products: {str(e)}") 