def check_geometry(layer):

    if layer is None or not layer.isValid():
        return {"error": "Invalid layer"}

    missing = []
    empty = []
    invalid = []

    for feature in layer.getFeatures():

        if not feature.hasGeometry():
            missing.append(feature.id())
            continue

        geometry = feature.geometry()

        if geometry.isNull():
            missing.append(feature.id())

        elif geometry.isEmpty():
            empty.append(feature.id())

        elif not geometry.isGeosValid():
            invalid.append(feature.id())

    return {
        "layer": layer.name(),
        "total_features": layer.featureCount(),
        "missing_geometry": len(missing),
        "empty_geometry": len(empty),
        "invalid_geometry": len(invalid),
        "missing_ids": missing,
        "empty_ids": empty,
        "invalid_ids": invalid
    }