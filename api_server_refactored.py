"""
KMart ML API Server - Refactored Version
Clean, modular, and organized structure
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.data.data_manager import DataManager
from src.api.api_routes import router, init_services

# Create FastAPI app
app = FastAPI(
    title="KMart ML API", 
    description="API for product recommendations, search, and trending products"
)

# Add CORS middleware for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080", 
        "http://localhost:8000",
        "https://your-flutter-app-domain.com",  # Replace with your actual domain
        "https://*.railway.app",  # Allow all Railway subdomains
        "capacitor://localhost",
        "ionic://localhost"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data manager and services
data_manager = DataManager()
data_manager.load_models()
init_services(data_manager)

# Include all routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 