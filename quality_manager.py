from .layer_inspector import inspect_layer
from .geometry_checker import check_geometry
from .duplicate_checker import check_duplicates
from .attribute_checker import check_attributes
from .crs_checker import check_crs


def run_quality_check(layer, expected_crs=None):

    if layer is None or not layer.isValid():
        return {"error": "Invalid layer"}

    report = {
        "layer_info": inspect_layer(layer),
        "geometry": check_geometry(layer),
        "duplicates": check_duplicates(layer),
        "attributes": check_attributes(layer),
        "crs": check_crs(layer, expected_crs)
    }

    return report
