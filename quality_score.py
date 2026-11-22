
def calculate_quality_score(report):

    info = report["layer_info"]
    geometry = report["geometry"]
    duplicates = report["duplicates"]
    attributes = report["attributes"]
    crs = report["crs"]

    total = info["feature_count"]
    field_count = info["field_count"]
    if total == 0:
     return {
        "overall_score": None,
        "geometry_score": None,
        "attribute_score": None,
        "duplicate_score": None,
        "crs_score": None,
        "status": "Not assessed - Empty layer"
    }

    # Geometry Score
    geometry_errors = (
        geometry["missing_geometry"]
        + geometry["empty_geometry"]
        + geometry["invalid_geometry"]
    )

    geometry_score = (
        max(0, 100 * (1 - geometry_errors / total))
        if total > 0 else 0
    )

    # Duplicate Score
    duplicate_count = duplicates["duplicate_count"]

    duplicate_score = (
        max(0, 100 * (1 - duplicate_count / total))
        if total > 0 else 0
    )

    # Attribute Score
    missing_values = sum(
        v["null_values"] + v["empty_values"]
        for v in attributes["fields"].values()
    )

    total_cells = total * field_count

    attribute_score = (
        max(0, 100 * (1 - missing_values / total_cells))
        if total_cells > 0 else 0
    )

    # CRS Score
    crs_score = 100 if crs["crs_valid"] else 0

    # Weighted Overall Score
    overall_score = (
        geometry_score * 0.35
        + attribute_score * 0.30
        + duplicate_score * 0.20
        + crs_score * 0.15
    )

    return {
        "overall_score": round(overall_score, 2),
        "geometry_score": round(geometry_score, 2),
        "attribute_score": round(attribute_score, 2),
        "duplicate_score": round(duplicate_score, 2),
        "crs_score": round(crs_score, 2)
    }
