
from qgis.PyQt.QtCore import QThread, pyqtSignal
from qgis.PyQt.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QMessageBox
)

from ..core.quality_manager import run_quality_check
from ..core.excel_report import export_report_to_excel
from ..core.quality_score import calculate_quality_score


# =====================================
# Excel Export Thread
# =====================================

class ExcelExportThread(QThread):

    export_finished = pyqtSignal(str)
    export_failed = pyqtSignal(str)

    def __init__(self, report, output_path, parent=None):
        super().__init__(parent)

        self.report = report
        self.output_path = output_path

    def run(self):

        try:
            result = export_report_to_excel(
                self.report,
                self.output_path
            )

            self.export_finished.emit(result)

        except Exception as error:
            self.export_failed.emit(str(error))


# =====================================
# GeoCheck Main Dialog
# =====================================

class GeoCheckDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle(
            "GeoCheck - Spatial Data Quality"
        )

        self.setMinimumSize(550, 550)

        self.report = None
        self.export_thread = None

        # Main Layout
        layout = QVBoxLayout()

        # Title
        title = QLabel("GeoCheck")

        title.setStyleSheet(
            "font-size: 24px; "
            "font-weight: bold; "
            "color: #2471A3;"
        )

        subtitle = QLabel(
            "Spatial Data Quality Assessment Tool"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Layer Selection
        layout.addWidget(
            QLabel("Select GIS Layer:")
        )

        self.layer_combo = QComboBox()

        layout.addWidget(self.layer_combo)

        self.load_layers()

        # Run Checks Button
        self.run_button = QPushButton(
            "Run All Checks"
        )

        self.run_button.clicked.connect(
            self.run_checks
        )

        layout.addWidget(self.run_button)

        # Results
        layout.addWidget(
            QLabel("Quality Assessment Results:")
        )

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)

        layout.addWidget(self.results_text)

        # Export Button
        self.export_button = QPushButton(
            "Export Excel Report"
        )

        self.export_button.setEnabled(False)

        self.export_button.clicked.connect(
            self.export_report
        )

        layout.addWidget(self.export_button)

        self.setLayout(layout)

    # =================================
    # Load GIS Layers
    # =================================

    def load_layers(self):

        from qgis.core import (
            QgsProject,
            QgsMapLayerType
        )

        self.layer_combo.clear()

        layers = (
            QgsProject.instance()
            .mapLayers()
            .values()
        )

        for layer in layers:

            if layer.type() == QgsMapLayerType.VectorLayer:

                self.layer_combo.addItem(
                    layer.name(),
                    layer.id()
                )

    # =================================
    # Run Quality Checks
    # =================================

    def run_checks(self):

        from qgis.core import QgsProject

        layer_id = self.layer_combo.currentData()

        layer = QgsProject.instance().mapLayer(
            layer_id
        )

        if layer is None:

            QMessageBox.warning(
                self,
                "GeoCheck",
                "Please select a valid layer."
            )

            return

        self.run_button.setEnabled(False)
        self.export_button.setEnabled(False)

        try:

            self.report = run_quality_check(layer)

            if "error" in self.report:

                raise ValueError(
                    self.report["error"]
                )

            score = calculate_quality_score(self.report)

            if score["overall_score"] is None:
                score_text = "Not assessed - Empty layer"
            else:
                score_text = f"{score['overall_score']}/100"

            geometry = self.report["geometry"]
            duplicates = self.report["duplicates"]
            attributes = self.report["attributes"]
            crs = self.report["crs"]
            info = self.report["layer_info"]

            null_total = sum(
                value["null_values"]
                for value in attributes["fields"].values()
            )

            empty_total = sum(
                value["empty_values"]
                for value in attributes["fields"].values()
            )

            geometry_score_text = (
                "Not assessed"
                if score["geometry_score"] is None
                else str(score["geometry_score"])
            )

            attribute_score_text = (
                "Not assessed"
                if score["attribute_score"] is None
                else str(score["attribute_score"])
            )

            duplicate_score_text = (
                "Not assessed"
                if score["duplicate_score"] is None
                else str(score["duplicate_score"])
            )

            crs_score_text = (
                "Not assessed"
                if score["crs_score"] is None
                else str(score["crs_score"])
            )

            output = (
                f"--- OVERALL QUALITY SCORE ---\n"
                f"Score: {score_text}\n"
                f"Geometry Score: {geometry_score_text}\n"
                f"Attribute Score: {attribute_score_text}\n"
                f"Duplicate Score: {duplicate_score_text}\n"
                f"CRS Score: {crs_score_text}\n\n"

                f"Layer: {info['name']}\n"
                f"Features: {info['feature_count']}\n"
                f"Geometry: {info['geometry_type']}\n"
                f"CRS: {info['crs']}\n"
                f"Fields: {info['field_count']}\n\n"

                f"--- Geometry Check ---\n"
                f"Missing: {geometry['missing_geometry']}\n"
                f"Empty: {geometry['empty_geometry']}\n"
                f"Invalid: {geometry['invalid_geometry']}\n\n"

                f"--- Duplicate Check ---\n"
                f"Duplicates: {duplicates['duplicate_count']}\n\n"

                f"--- Attribute Check ---\n"
                f"Null Values: {null_total}\n"
                f"Empty Values: {empty_total}\n\n"

                f"--- CRS Check ---\n"
                f"Valid: {crs['crs_valid']}\n"
                f"CRS: {crs['authid']}\n"
            )

            self.results_text.setPlainText(output)

            self.export_button.setEnabled(True)

        except Exception as error:

            self.report = None

            QMessageBox.critical(
                self,
                "GeoCheck Error",
                str(error)
            )

        finally:

            self.run_button.setEnabled(True)

    # =================================
    # Export Excel Report
    # =================================

    def export_report(self):

        if self.report is None:
            return

        if (
            self.export_thread is not None
            and self.export_thread.isRunning()
        ):
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save GeoCheck Excel Report",
            "GeoCheck_Report.xlsx",
            "Excel Files (*.xlsx)"
        )

        if not output_path:
            return

        if not output_path.lower().endswith(".xlsx"):
            output_path += ".xlsx"

        self.export_button.setEnabled(False)
        self.export_button.setText("Exporting...")

        self.export_thread = ExcelExportThread(
            self.report,
            output_path,
            self
        )

        self.export_thread.export_finished.connect(
            self.export_success
        )

        self.export_thread.export_failed.connect(
            self.export_error
        )

        self.export_thread.finished.connect(
            self.cleanup_export_thread
        )

        self.export_thread.start()

    # =================================
    # Export Success
    # =================================

    def export_success(self, output_path):

        self.export_button.setEnabled(True)

        self.export_button.setText(
            "Export Excel Report"
        )

        QMessageBox.information(
            self,
            "GeoCheck",
            f"Excel report exported successfully!\n{output_path}"
        )

    # =================================
    # Export Error
    # =================================

    def export_error(self, error_message):

        self.export_button.setEnabled(True)

        self.export_button.setText(
            "Export Excel Report"
        )

        QMessageBox.critical(
            self,
            "Export Error",
            error_message
        )

    # =================================
    # Cleanup Export Thread
    # =================================

    def cleanup_export_thread(self):

        thread = self.export_thread
        self.export_thread = None

        if thread is not None:
            thread.deleteLater()
