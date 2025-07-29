#!/usr/bin/env python3
"""
Test script to verify all dependencies can be imported
"""

def test_imports():
    """Test importing all required packages"""
    try:
        print("Testing imports...")
        
        # Core API dependencies
        import fastapi
        print(f"✓ fastapi {fastapi.__version__}")
        
        import uvicorn
        print(f"✓ uvicorn {uvicorn.__version__}")
        
        import pydantic
        print(f"✓ pydantic {pydantic.__version__}")
        
        # Data processing
        import pandas
        print(f"✓ pandas {pandas.__version__}")
        
        import numpy
        print(f"✓ numpy {numpy.__version__}")
        
        import scipy
        print(f"✓ scipy {scipy.__version__}")
        
        # ML libraries
        import sklearn
        print(f"✓ scikit-learn {sklearn.__version__}")
        
        import sentence_transformers
        print(f"✓ sentence-transformers {sentence_transformers.__version__}")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_imports() 