from app.models.features import Features

# type: ignore

def detect_features() -> Features:
    """
    Try and import the required Python libraries and return an instance of the Features class with results
    
    Args:
        None
        
    Returns:
        Features: Class with attributes for each feature's status as a bool
    """
    f = Features()

    try:
        import pandas 
        f.has_pandas = True
    except ImportError:
        pass

    try:
        import numpy 
        f.has_numpy = True
    except ImportError:
        pass

    try:
        import matplotlib 
        f.has_matplotlib = True
    except ImportError:
        pass

    try:
        import requests  
        f.has_requests = True
    except ImportError:
        pass

    try:
        import rich 
        f.has_rich = True
    except ImportError:
        pass

    return f

# type: ignore