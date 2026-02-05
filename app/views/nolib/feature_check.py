from app.models.features import Features

def render_feature_check(features: Features) -> None:
    print("\n" + "=" * 30)
    print("Checking for required and optional libraries...")

    if not features.has_pandas:
        print("+ Warning: pandas library not found. Dataset loading and analysis features will be unavailable.")
    if not features.has_numpy:
        print("+ Warning: numpy library not found. Analysis features will be unavailable.")
    if not features.has_matplotlib:
        print("+ Warning: matplotlib library not found. Visualization features will be unavailable.")
    if not features.has_requests:
        print("+ Warning: requests library not found. Dataset fetching features will be unavailable.")
    if not features.has_rich:
        print("+ Warning: rich library not found. We can't really proceed without this.")

    print("Feature check complete.")
    print("=" * 30)