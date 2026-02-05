from app.models.features import Features

# type: ignore

def detect_features() -> Features:
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