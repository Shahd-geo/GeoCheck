from qgis.core import QgsWkbTypes


def inspect_layer(layer):

    if layer is None:
        return {"error": "No layer selected"}

    if not layer.isValid():
        return {"error": "Invalid Layer"}

    return {
        "name": layer.name(),
        "geometry_type": QgsWkbTypes.displayString(layer.wkbType()),
        "feature_count": layer.featureCount(),
        "crs": layer.crs().authid(),
        "field_count": len(layer.fields()),
        "field_names": [field.name() for field in layer.fields()]
    }