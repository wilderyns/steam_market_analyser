# type: ignore
# This module checks to see if all the dependencies exist and then
# sets feature flags accordingly.

class Features:
    def __init__(self) -> None:
        self.has_pandas = False
        self.has_numpy = False
        self.has_matplotlib = False
        self.has_requests = False
        self.has_rich = False

def check_features() -> Features:
    features = Features()
    
    print("\n" + "=" * 30)
    print("Checking for required and optional libraries...")
    
    try:
        import pandas
        features.has_pandas = True
    except ImportError:
        features.has_pandas = False
        print ("+ Warning: pandas library not found. Dataset loading and analysis features will be unavailable.")
        
    try:
        import numpy
        features.has_numpy = True
    except ImportError:
        features.has_numpy = False
        print ("+ Warning: numpy library not found. Analysis features will be unavailable.")
        
    try:
        import matplotlib
        features.has_matplotlib = True
    except ImportError:
        features.has_matplotlib = False
        print ("+ Warning: matplotlib library not found. Visualization features will be unavailable.")
        
    try:
        import requests
        features.has_requests = True
    except ImportError:
        features.has_requests = False
        print ("+ Warning: requests library not found. Dataset fetching features will be unavailable.")
        
    try:
        import rich
        features.has_rich = True
    except ImportError:
        features.has_rich = False
        print ("+ Warning: rich library not found. Tabular views will look awful.")
    
    print ("Feature check complete.")
    print("=" * 30)
    return features

# type: ignore
