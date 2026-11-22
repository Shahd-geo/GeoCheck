def check_attributes(layer):

    if layer is None or not layer.isValid():
        return {"error": "Invalid layer"}

    field_report = {}

    for field in layer.fields():

        field_name = field.name()
        null_count = 0
        empty_count = 0

        for feature in layer.getFeatures():

            value = feature[field_name]

            if value is None:
                null_count += 1

            elif isinstance(value, str) and not value.strip():
                empty_count += 1

        field_report[field_name] = {
            "null_values": null_count,
            "empty_values": empty_count
        }

    return {
        "layer": layer.name(),
        "total_features": layer.featureCount(),
        "fields": field_report
    }