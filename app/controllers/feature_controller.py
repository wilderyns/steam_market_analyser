from app.views.nolib.feature_check import render_feature_check
from app.models.appstate import AppState
from app.services.feature_service import detect_features


def feature_controller(state: AppState):
    """
    During app initilisation, calls feature service to detect features and handles output display
    
    Args:
        state (AppState): application state controller
        
    Returns:
        True if all is well, False if Rich isn't available
        #TODO: When the Nolib display variant is done allow things to progress
    
    Exceptions:
        RuntimeError: if Rich is unavailable 
    """
    print("Getting everything ready...")
    state.features = detect_features()
    render_feature_check(state.features)
    
    if not state.features.has_rich:
        # Rich library not detected, for now we'll quit, TODO: implement RIch not being required
        print("Sorry, the Python library Rich is required to use this application.")
        print("Please install with pip install rich")
        print("Quitting")
        raise RuntimeError("Rich library required, quitting.")
        return False
    else: 
        return True