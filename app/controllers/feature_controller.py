from app.views.nolib.feature_check import render_feature_check
from app.models.appstate import AppState
from app.services.feature_service import detect_features


def feature_controller(state: AppState):
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