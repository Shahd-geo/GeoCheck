def check_crs(layer, expected_crs=None):

    if layer is None or not layer.isValid():
        return {"error": "Invalid layer"}

    crs = layer.crs()

    if not crs.isValid():
        return {
            "layer": layer.name(),
            "crs_valid": False,
            "authid": None,
            "matches_expected": None
        }

    authid = crs.authid()

    matches = None

    if expected_crs is not None:
        matches = crs == expected_crs

    return {
        "layer": layer.name(),
        "crs_valid": True,
        "authid": authid,
        "description": crs.description(),
        "matches_expected": matches
    }