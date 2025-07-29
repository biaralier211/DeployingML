"""
Interaction tracking services for KMart ML API
"""

import json
import pandas as pd
from typing import List, Dict, Any
from src.models.models import (
    ProductViewInteraction, FavoritesInteraction, CartInteraction,
    ChatInteraction, ReviewInteraction, SearchInteraction, InteractionResponse
)

class InteractionServices:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def track_product_view(self, interaction: ProductViewInteraction) -> InteractionResponse:
        """Track product view interactions (card tap and details page)"""
        try:
            # Validate interaction type
            if interaction.interaction_type not in ['view', 'view_details']:
                raise ValueError("Invalid interaction type. Must be 'view' or 'view_details'")
            
            # Get product details for metadata
            product_info = self.data_manager.get_product_info(interaction.product_id)
            if product_info is not None:
                price = self.data_manager.extract_price(product_info)
                
                interaction.metadata.update({
                    'product_name': product_info.get('name', 'Unknown Product'),
                    'category': product_info.get('category', ''),
                    'price': price,
                    'source': interaction.metadata.get('source', 'flutter_app')
                })
            
            # Save interaction
            interaction_data = {
                'user_id': interaction.user_id,
                'product_id': interaction.product_id,
                'interaction_type': interaction.interaction_type,
                'metadata': interaction.metadata
            }
            
            interaction_id = self.data_manager.save_interaction(interaction_data)
            
            if interaction_id:
                return InteractionResponse(
                    success=True,
                    message=f"Product {interaction.interaction_type} tracked successfully",
                    interaction_id=interaction_id
                )
            else:
                raise Exception("Failed to save interaction")
        
        except Exception as e:
            raise Exception(f"Error tracking product view: {str(e)}")
    
    def track_favorites(self, interaction: FavoritesInteraction) -> InteractionResponse:
        """Track favorites/likes interactions"""
        try:
            # Validate interaction type
            if interaction.interaction_type not in ['like', 'unlike']:
                raise ValueError("Invalid interaction type. Must be 'like' or 'unlike'")
            
            # Get product details for metadata
            product_info = self.data_manager.get_product_info(interaction.product_id)
            if product_info is not None:
                price = self.data_manager.extract_price(product_info)
                
                interaction.metadata.update({
                    'product_name': product_info.get('name', 'Unknown Product'),
                    'category': product_info.get('category', ''),
                    'price': price
                })
            
            # Save interaction
            interaction_data = {
                'user_id': interaction.user_id,
                'product_id': interaction.product_id,
                'interaction_type': interaction.interaction_type,
                'metadata': interaction.metadata
            }
            
            interaction_id = self.data_manager.save_interaction(interaction_data)
            
            if interaction_id:
                return InteractionResponse(
                    success=True,
                    message=f"Product {interaction.interaction_type} tracked successfully",
                    interaction_id=interaction_id
                )
            else:
                raise Exception("Failed to save interaction")
        
        except Exception as e:
            raise Exception(f"Error tracking favorites interaction: {str(e)}")
    
    def track_cart(self, interaction: CartInteraction) -> InteractionResponse:
        """Track shopping cart interactions"""
        try:
            # Validate interaction type
            if interaction.interaction_type != 'add_to_cart':
                raise ValueError("Invalid interaction type. Must be 'add_to_cart'")
            
            # Get product details for metadata
            product_info = self.data_manager.get_product_info(interaction.product_id)
            if product_info is not None:
                price = self.data_manager.extract_price(product_info)
                
                interaction.metadata.update({
                    'product_name': product_info.get('name', 'Unknown Product'),
                    'category': product_info.get('category', ''),
                    'price': price,
                    'quantity': interaction.metadata.get('quantity', 1)
                })
            
            # Save interaction
            interaction_data = {
                'user_id': interaction.user_id,
                'product_id': interaction.product_id,
                'interaction_type': interaction.interaction_type,
                'quantity': interaction.metadata.get('quantity', 1),
                'metadata': interaction.metadata
            }
            
            interaction_id = self.data_manager.save_interaction(interaction_data)
            
            if interaction_id:
                return InteractionResponse(
                    success=True,
                    message="Product added to cart tracked successfully",
                    interaction_id=interaction_id
                )
            else:
                raise Exception("Failed to save interaction")
        
        except Exception as e:
            raise Exception(f"Error tracking cart interaction: {str(e)}")
    
    def track_chat(self, interaction: ChatInteraction) -> InteractionResponse:
        """Track chat interactions"""
        try:
            # Validate interaction type
            if interaction.interaction_type != 'chat_message':
                raise ValueError("Invalid interaction type. Must be 'chat_message'")
            
            # Get product details for metadata
            product_info = self.data_manager.get_product_info(interaction.product_id)
            if product_info is not None:
                interaction.metadata.update({
                    'product_name': product_info.get('name', 'Unknown Product'),
                    'seller_info': interaction.metadata.get('seller_info', ''),
                    'message_length': interaction.metadata.get('message_length', 0),
                    'chat_room_id': interaction.metadata.get('chat_room_id', '')
                })
            
            # Save interaction
            interaction_data = {
                'user_id': interaction.user_id,
                'product_id': interaction.product_id,
                'interaction_type': interaction.interaction_type,
                'metadata': interaction.metadata
            }
            
            interaction_id = self.data_manager.save_interaction(interaction_data)
            
            if interaction_id:
                return InteractionResponse(
                    success=True,
                    message="Chat interaction tracked successfully",
                    interaction_id=interaction_id
                )
            else:
                raise Exception("Failed to save interaction")
        
        except Exception as e:
            raise Exception(f"Error tracking chat interaction: {str(e)}")
    
    def track_review(self, interaction: ReviewInteraction) -> InteractionResponse:
        """Track review and rating interactions"""
        try:
            # Validate interaction type
            if interaction.interaction_type != 'rating':
                raise ValueError("Invalid interaction type. Must be 'rating'")
            
            # Get product details for metadata
            product_info = self.data_manager.get_product_info(interaction.product_id)
            if product_info is not None:
                interaction.metadata.update({
                    'product_name': product_info.get('name', 'Unknown Product'),
                    'category': product_info.get('category', ''),
                    'rating_value': interaction.metadata.get('rating_value', 0),
                    'previous_rating': interaction.metadata.get('previous_rating', None)
                })
            
            # Save interaction
            interaction_data = {
                'user_id': interaction.user_id,
                'product_id': interaction.product_id,
                'interaction_type': interaction.interaction_type,
                'rating': interaction.metadata.get('rating_value', 0),
                'review': interaction.metadata.get('review_text', ''),
                'metadata': interaction.metadata
            }
            
            interaction_id = self.data_manager.save_interaction(interaction_data)
            
            if interaction_id:
                return InteractionResponse(
                    success=True,
                    message="Review interaction tracked successfully",
                    interaction_id=interaction_id
                )
            else:
                raise Exception("Failed to save interaction")
        
        except Exception as e:
            raise Exception(f"Error tracking review interaction: {str(e)}")
    
    def track_search(self, interaction: SearchInteraction) -> InteractionResponse:
        """Track search interactions"""
        try:
            # Validate interaction type
            if interaction.interaction_type != 'search':
                raise ValueError("Invalid interaction type. Must be 'search'")
            
            # Save interaction
            interaction_data = {
                'user_id': interaction.user_id,
                'product_id': '',  # No product for search
                'interaction_type': interaction.interaction_type,
                'metadata': interaction.metadata
            }
            
            interaction_id = self.data_manager.save_interaction(interaction_data)
            
            if interaction_id:
                return InteractionResponse(
                    success=True,
                    message="Search interaction tracked successfully",
                    interaction_id=interaction_id
                )
            else:
                raise Exception("Failed to save interaction")
        
        except Exception as e:
            raise Exception(f"Error tracking search interaction: {str(e)}")
    
    def get_user_interactions(self, user_id: str, limit: int = 50) -> Dict[str, Any]:
        """Get all interactions for a specific user"""
        try:
            user_interactions = self.data_manager.interaction_df[self.data_manager.interaction_df['userId'] == user_id]
            user_interactions = user_interactions.sort_values('timestamp', ascending=False).head(limit)
            
            interactions = []
            for _, row in user_interactions.iterrows():
                # Safely parse metadata JSON
                try:
                    metadata = json.loads(row.get('metadata', '{}')) if pd.notna(row.get('metadata')) and row.get('metadata') != '{}' else {}
                except (json.JSONDecodeError, TypeError):
                    metadata = {}
                
                interaction = {
                    'interaction_id': row['interactionId'],
                    'product_id': row['productId'],
                    'interaction_type': row['interactionType'],
                    'timestamp': row['timestamp'].isoformat(),
                    'quantity': row.get('quantity', ''),
                    'rating': row.get('rating', ''),
                    'review': row.get('review', ''),
                    'metadata': metadata
                }
                interactions.append(interaction)
            
            return {
                'user_id': user_id,
                'total_interactions': len(interactions),
                'interactions': interactions
            }
        
        except Exception as e:
            raise Exception(f"Error getting user interactions: {str(e)}")
    
    def get_product_interactions(self, product_id: str, limit: int = 50) -> Dict[str, Any]:
        """Get all interactions for a specific product"""
        try:
            product_interactions = self.data_manager.interaction_df[self.data_manager.interaction_df['productId'] == product_id]
            product_interactions = product_interactions.sort_values('timestamp', ascending=False).head(limit)
            
            interactions = []
            for _, row in product_interactions.iterrows():
                # Safely parse metadata JSON
                try:
                    metadata = json.loads(row.get('metadata', '{}')) if pd.notna(row.get('metadata')) and row.get('metadata') != '{}' else {}
                except (json.JSONDecodeError, TypeError):
                    metadata = {}
                
                interaction = {
                    'interaction_id': row['interactionId'],
                    'user_id': row['userId'],
                    'interaction_type': row['interactionType'],
                    'timestamp': row['timestamp'].isoformat(),
                    'quantity': row.get('quantity', ''),
                    'rating': row.get('rating', ''),
                    'review': row.get('review', ''),
                    'metadata': metadata
                }
                interactions.append(interaction)
            
            return {
                'product_id': product_id,
                'total_interactions': len(interactions),
                'interactions': interactions
            }
        
        except Exception as e:
            raise Exception(f"Error getting product interactions: {str(e)}") 