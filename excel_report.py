
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from datetime import datetime
from .quality_score import calculate_quality_score


def export_report_to_excel(report, output_path):

    wb = Workbook()

    # 1. Summary Sheet
    ws = wb.active
    ws.title = "Summary"

    info = report["layer_info"]
    geometry = report["geometry"]
    duplicates = report["duplicates"]
    crs = report["crs"]
    score = calculate_quality_score(report)

    summary_data = [
    ["GeoCheck - Spatial Data Quality Report"],
    ["Report Date", datetime.now().strftime("%Y-%m-%d %H:%M")],
    ["Layer Name", info["name"]],
    ["Feature Count", info["feature_count"]],

    ["Overall Quality Score", score["overall_score"] if score["overall_score"] is not None else "Not assessed"],
    ["Geometry Score", score["geometry_score"] if score["geometry_score"] is not None else "Not assessed"],
    ["Attribute Score", score["attribute_score"] if score["attribute_score"] is not None else "Not assessed"],
    ["Duplicate Score", score["duplicate_score"] if score["duplicate_score"] is not None else "Not assessed"],
    ["CRS Score", score["crs_score"] if score["crs_score"] is not None else "Not assessed"],

    ["Geometry Type", info["geometry_type"]],
    ["Field Count", info["field_count"]],
    ["CRS", info["crs"]],
    ["Missing Geometry", geometry["missing_geometry"]],
    ["Empty Geometry", geometry["empty_geometry"]],
    ["Invalid Geometry", geometry["invalid_geometry"]],
    ["Duplicate Geometries", duplicates["duplicate_count"]],
    ["CRS Valid", crs["crs_valid"]]
    ]

    for row in summary_data:
        ws.append(row)

    # 2. Geometry Sheet
    ws = wb.create_sheet("Geometry")

    ws.append(["Geometry Check", "Count"])
    ws.append(["Missing Geometry", geometry["missing_geometry"]])
    ws.append(["Empty Geometry", geometry["empty_geometry"]])
    ws.append(["Invalid Geometry", geometry["invalid_geometry"]])

    # 3. Duplicates Sheet
    ws = wb.create_sheet("Duplicates")

    ws.append(["Duplicate Feature ID", "Original Feature ID"])

    for item in duplicates["duplicates"]:
        ws.append([
            item["duplicate_id"],
            item["original_id"]
        ])

    # 4. Attributes Sheet
    ws = wb.create_sheet("Attributes")

    ws.append(["Field Name", "Null Values", "Empty Values"])

    for field, values in report["attributes"]["fields"].items():
        ws.append([
            field,
            values["null_values"],
            values["empty_values"]
        ])

    # 5. CRS Sheet
    ws = wb.create_sheet("CRS")

    ws.append(["CRS Property", "Value"])
    ws.append(["CRS Valid", crs["crs_valid"]])
    ws.append(["Actual CRS", crs["authid"]])
    ws.append(["Description", crs.get("description", "")])
    ws.append([ "Expected CRS Match", crs.get("matches_expected") or "Not specified"])

    # Format all sheets
    for sheet in wb.worksheets:

        sheet.freeze_panes = "A2"

        for cell in sheet[1]:
            cell.font = Font(
                bold=True,
                color="FFFFFF",
                size=12
            )
            cell.fill = PatternFill(
                "solid",
                fgColor="174A70"
            )
            cell.alignment = Alignment(
                horizontal="center"
            )

        for column in sheet.columns:
            max_length = max(
                len(str(cell.value or ""))
                for cell in column
            )

            column_letter = get_column_letter(
                column[0].column
            )

            sheet.column_dimensions[
                column_letter
            ].width = min(max_length + 4, 45)

    wb.save(output_path)

    return output_path

