# GeoCheck – Spatial Data Quality Assessment Tool

**GeoCheck** is a QGIS plugin developed to assess the quality of vector spatial data through a set of automated validation checks.

The plugin helps GIS professionals identify common spatial data quality issues, evaluate dataset quality, and generate structured Excel reports to support spatial data validation and quality assurance workflows.

## Features

GeoCheck provides the following quality assessment capabilities:

- **Geometry Validation:** Identifies missing, empty, and invalid geometries.
- **Duplicate Detection:** Detects duplicate geometries within a spatial dataset.
- **Attribute Validation:** Identifies NULL and empty attribute values across fields.
- **Coordinate Reference System (CRS) Validation:** Checks whether a layer has a valid coordinate reference system.
- **Quality Scoring:** Calculates an overall spatial data quality score based on weighted assessment criteria.
- **Excel Reporting:** Exports assessment results into a structured Excel workbook for further review and documentation.

## Quality Scoring Methodology

GeoCheck calculates an overall quality score using four weighted assessment components:

| Assessment Component | Weight |
|---|---:|
| Geometry Quality | 35% |
| Attribute Quality | 30% |
| Duplicate Detection | 20% |
| CRS Validation | 15% |
| **Total** | **100%** |

Each component contributes to the overall score according to its assigned weight.

**Empty layers** are classified as *Not Assessed* because no features are available for quality evaluation.

## Excel Reporting

GeoCheck generates an Excel workbook containing five worksheets:

1. **Summary:** Overall quality score, layer information, and assessment results.
2. **Geometry:** Missing, empty, and invalid geometry counts.
3. **Duplicates:** Identifiers of detected duplicate features.
4. **Attributes:** NULL and empty value counts for each attribute field.
5. **CRS:** Coordinate reference system validation details.

## Requirements

- QGIS 3.28 or later.
- Python environment provided by QGIS.
- `openpyxl` library for Excel report generation.

## Installation

1. Download the GeoCheck ZIP package from the repository.
2. Open QGIS.
3. Navigate to **Plugins → Manage and Install Plugins**.
4. Select **Install from ZIP**.
5. Browse to the downloaded GeoCheck ZIP package.
6. Click **Install Plugin**.
7. Enable GeoCheck from the Installed Plugins section.

## How to Use

1. Open a QGIS project containing vector layers.
2. Launch GeoCheck from the QGIS toolbar or Plugins menu.
3. Select the vector layer you want to assess.
4. Click **Run All Checks**.
5. Review the spatial data quality assessment results.
6. Click **Export Excel Report** to save the assessment results as an Excel workbook.

## Project Structure

```text
GeoCheck/
├── core/
│   ├── __init__.py
│   ├── attribute_checker.py
│   ├── crs_checker.py
│   ├── duplicate_checker.py
│   ├── excel_report.py
│   ├── geometry_checker.py
│   ├── layer_inspector.py
│   ├── quality_manager.py
│   └── quality_score.py
├── gui/
│   ├── __init__.py
│   └── geocheck_dialog.py
├── __init__.py
├── geocheck_plugin.py
└── metadata.txt
```

## Limitations

- Quality scores are based on the implemented validation checks and their assigned weights.
- Duplicate detection identifies exact duplicate geometries; it does not assess all forms of spatial overlap or topological equivalence.
- CRS validation checks whether a coordinate reference system is valid, but does not determine whether it is suitable for a specific analysis.
- Empty layers are reported as *Not Assessed* rather than assigned a numerical quality score.

## Author

**Shahd Al Abdali**

GIS Graduate | Spatial Data Quality | GIS Applications

## License

License information will be added in a future release.
