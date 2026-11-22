import hashlib


def check_duplicates(layer):

    if layer is None or not layer.isValid():
        return {"error": "Invalid layer"}

    seen = {}
    duplicates = []

    for feature in layer.getFeatures():

        if not feature.hasGeometry():
            continue

        geometry = feature.geometry()

        if geometry.isNull() or geometry.isEmpty():
            continue

        geometry_hash = hashlib.sha256(
            bytes(geometry.asWkb())
        ).hexdigest()

        if geometry_hash in seen:

            duplicates.append({
                "duplicate_id": feature.id(),
                "original_id": seen[geometry_hash]
            })

        else:
            seen[geometry_hash] = feature.id()

    return {
        "layer": layer.name(),
        "total_features": layer.featureCount(),
        "duplicate_count": len(duplicates),
        "duplicates": duplicates
    }
