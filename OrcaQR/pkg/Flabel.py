"""
Label generator for qr-barcode-type labels

Python 3.10 and above required

Allows the user to view, load, and rearrange labels before
printing/saving them into zpl/pdf format

This program will use classes ONLY when Qt widgets
or classes NEED to be ovecwritten

Othecwise, functional style is used as much as possible

All lists are in ascending order as per Qt's selectedRows method

Please stick to minimal dependencies for easier compilation!
Modules like Numpy, Pandas, scipy tend to cause compilation issues

DEFINITIONS:
 - position: relative location by index on a label
 - bbox: always a (left, top, right, bottom), same as cv2 xyxy format
 - coords: (left, top)
 - element: general items of any type at a location
 - asset: the image/barcode/qr etc. objects
 - xxx_asset: xxx indicates the type of asset
 - map: always a dictionary containing the position and its associated info
 - label:   strictly refers to the entire label, not the text or string within,
            refer to label_text or label_string for that
 - browser row/col: refers to the row as seen, not the index count on the headers
 - PPI vs DPI: as image/pdf, use PPI, when using ZPL, convert to mm then to DPI
 - label size: (width, height)

 TODO: Error handler module to abstract ugly errors away from ErrorDialog
 TODO: Create settings file to load from at startup (default dir, label_settings)
 TODO: Create setup wizard for resources and setting installation dir, default dir
 TODO: Translate English/Thai
 TODO: Light mode icons
 TODO: Resizable option for text/barcodes
"""

from typing import Union
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsView,
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QAbstractItemView,
    QLineEdit,
    QProgressDialog,
    QListWidget,
    QListWidgetItem,
    QComboBox,
    QRadioButton,
)
from PySide6.QtCore import (
    Qt,
    QObject,
    QAbstractTableModel,
    QModelIndex,
    QRect,
    QPoint,
    QSize,
    QSizeF,
    QTimer,
    QRegularExpression,
    QMarginsF,
    QCoreApplication,
)

from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QAbstractPrintDialog

from PySide6.QtGui import (
    QColor,
    QPixmap,
    QImage,
    QResizeEvent,
    QPainter,
    QTransform,
    QPageSize,
    QIntValidator,
    QRegularExpressionValidator,
    QPageLayout,
    QFont,
)
import os
import sys
from .ui.ui_Flabel import Ui_Flabel
from .ui.ui_SearchDialog import Ui_SearchDialog
from .ui.ui_SettingsDialog import Ui_SettingsDialog
from .ui.ui_ExcelDialog import Ui_ExcelDialog
from .ui.ui_ExploreDialog import Ui_ExploreDialog
from .utils import exttools, pdfprep, labeltools
from .utils import zplparser as zpp
import qdarktheme
import re
import traceback
import code
import pathlib

from openpyxl import load_workbook


class UI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Variables and API
        self.preview_scene = PreviewDisplay(self)
        self.label_rect = None
        self.temp_label_paths = []
        self.label_rect = QRect()
        self.END_COLUMN_POSITION = 140
        self.START_COLUMN_POSITION = 45
        self.quantities = None
        self.selected_row_indexes = []
        self.label_excel_filepath = None
        self.quantity_excel_filename = None
        self.label_texts = None
        self.element_fn_map = None
        self.selected_rows_info = []
        self.quantities_loaded = False
        self.global_settings = GlobalSettings()
        self.label_info = LabelInfo()  # load the defaults

        # UI Elements
        self.ui = Ui_Flabel()
        self.ui.setupUi(self)

        # Preview display
        self.ui.preview_display.setScene(self.preview_scene)
        self.ui.preview_display.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.ui.preview_display.setCacheMode(QGraphicsView.CacheBackground)
        self.ui.preview_display.show()

        # Splitter

        self.END_COLUMN_POSITION = (
            self.ui.label_browser_table.columnViewportPosition(0)
            + self.ui.label_browser_table.columnWidth(0)
            + 47
        )
        self.ui.splitter.moveSplitter(
            self.END_COLUMN_POSITION + 21, 1
        )  # forcibly update the splitter to new column sizes
        self.ui.splitter.setSizes([100, 600])

        # Signals
        self.ui.load_labels_button.clicked.connect(
            lambda: self.open_file_dialog("labels")
        )
        self.ui.search_button.clicked.connect(
            lambda: self.search_select(len(self.label_texts))
        )
        self.ui.save_pdf_button.clicked.connect(lambda: self.open_file_dialog("pdf"))
        self.ui.save_zpl_button.clicked.connect(lambda: self.open_file_dialog("zpl"))
        self.ui.refresh_button.clicked.connect(self.global_refresh)
        self.ui.print_button.clicked.connect(self.print_images)

        self.ui.search_bar.textChanged.connect(self.search_table)
        self.ui.search_bar_button.clicked.connect(
            lambda: self.select_searched(self.item_indexes)
        )
        self.ui.select_all_check.stateChanged.connect(self.select_all_changed)
        self.ui.label_browser_table.itemSelectionChanged.connect(
            lambda: self.change_button_states("browser")
        )
        self.ui.label_browser_table.itemSelectionChanged.connect(
            self.view_label_selection
        )
        self.ui.label_browser_table.itemChanged.connect(self.edit_labels)

        self.ui.load_quantity_button.clicked.connect(self.load_quantity_clicked)
        self.ui.explore_button.clicked.connect(self.explore_clicked)
        self.ui.element_browser.itemChanged.connect(self.edit_quantity)

        # Amendments to properties
        self.ui.label_browser_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Fixed
        )
        self.ui.settings_button.clicked.connect(self.open_settings)
        # self.ui.element_browser.verticalHeader().setDragEnabled(True)
        # self.ui.element_browser.verticalHeader().setSectionsMovable(True)
        # self.ui.element_browser.verticalHeader().setDragDropMode(
        #     QAbstractItemView.InternalMove
        # )
        # self.ui.element_browser.dropMimeData

        self.ui.element_browser.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

    def load_browser_model(
        self, show_cols: dict[str, bool], rows: dict[str, str]
    ) -> None:
        self.ui.label_browser_table.itemChanged.disconnect(self.edit_labels)
        try:
            # self.label_model = LabelBrowserModel(labels)
            column_headers = [col for col, show_bool in show_cols.items() if show_bool]
            self.ui.label_browser_table.setRowCount(len(rows))
            self.ui.label_browser_table.setColumnCount(len(column_headers))
            self.ui.label_browser_table.setHorizontalHeaderLabels(column_headers)

            for i, label_row in enumerate(rows):
                i_item = QTableWidgetItem(str(i + 1))
                self.ui.label_browser_table.setVerticalHeaderItem(i, i_item)
                j = 0
                for h, l in label_row.items():
                    if (h in show_cols.keys()) and show_cols[h]:
                        l_item = QTableWidgetItem(l)
                        self.ui.label_browser_table.setItem(i, j, l_item)
                        j += 1
            # CLEAR EVERYTHING, done here bcos of settings page
            self.element_fn_map = {}
            self.element_maps = {}
            self.temp_label_paths = []
            self.img_coords_maps = {}
            self.desc_maps = {}
            self.quantities = None
            self.ui.label_browser_table.show()
            self.ui.label_browser_table.resizeColumnsToContents()
            self.END_COLUMN_POSITION = (
                self.ui.label_browser_table.columnViewportPosition(
                    len(column_headers) - 1
                )
                + self.ui.label_browser_table.columnWidth(len(column_headers) - 1)
                + 47
            )
            self.START_COLUMN_POSITION = (
                self.ui.label_browser_table.columnViewportPosition(0)
                + self.ui.label_browser_table.columnWidth(0)
                + 45
            )
            self.ui.splitter.moveSplitter(
                self.END_COLUMN_POSITION + 21, 1
            )  # forcibly update the splitter to new column sizes
        except Exception as exc:
            trace_exc = traceback.format_exc()
            print(f"Error loading label model: {trace_exc}")
            error_dialog = ErrorDialog("Error loading labels", self)
            ret = error_dialog.exec()
            if ret == QDialog.Accepted:
                info_dialog = InfoDialog(str(exc), self)
                info_dialog.exec()
        self.ui.label_browser_table.itemChanged.connect(self.edit_labels)

    def load_element_model(
        self,
        label_map: dict[int, str],
        desc_maps: list[dict[int, str]],
    ) -> None:
        """
        Load editable: quantity, layout, font_size, ecl
        non editable: description

        also disconnects editing until loading is complete
        """
        self.ui.element_browser.clear()
        self.ui.element_browser.itemChanged.disconnect(self.edit_quantity)
        try:
            label_map = {i: t for i, t in label_map.items() if t != "title"}
            label_map = {i: v for i, v in enumerate(label_map.values())}
            self.ui.element_browser.setRowCount(len(desc_maps))
            self.ui.element_browser.setColumnCount(len(label_map) + 1)
            self.ui.element_browser.setHorizontalHeaderItem(
                0, QTableWidgetItem("Quantity")
            )
            for pos, header in label_map.items():
                match header:
                    case "qr":
                        header_item = QTableWidgetItem("QR")
                    case "bar":
                        header_item = QTableWidgetItem("Barcode")
                    case "text":
                        header_item = QTableWidgetItem("Text")
                self.ui.element_browser.setHorizontalHeaderItem(pos + 1, header_item)
            for i, desc_map in enumerate(desc_maps):
                desc_map = dict(sorted(desc_map.items()))
                offset = 0
                for ele, desc in enumerate(desc_map.values()):
                    if desc is None:
                        offset += 1
                        continue
                    desc_item = QTableWidgetItem(desc)
                    desc_item.setFlags(~Qt.ItemIsEditable)
                    self.ui.element_browser.setItem(i, ele + 1 - offset, desc_item)

                index = self.selected_row_indexes[i].row() + 1
                index_item = QTableWidgetItem(str(index))

                self.ui.element_browser.setVerticalHeaderItem(i, index_item)
            self.load_quantity(self.quantities)
        except Exception as exc:
            trace_exc = traceback.format_exc()
            print(f"Error loading element model: {trace_exc}")
            error_dialog = ErrorDialog("Error loading label details", self)
            ret = error_dialog.exec()
            if ret == QDialog.Accepted:
                info_dialog = InfoDialog(str(exc), self)
                info_dialog.exec()
        self.ui.element_browser.itemChanged.connect(self.edit_quantity)

    def view_label_selection(self, item=None) -> None:
        """
        Updates the currently selected labels for generation
        """
        self.selected_rows_info.clear()
        self.selected_row_indexes.clear()
        self.selected_row_indexes = (
            self.ui.label_browser_table.selectionModel().selectedRows()
        )
        if not self.selected_row_indexes:
            return
        self.progress_dialog = ProgressDialog(max=len(self.selected_row_indexes))
        for i in self.selected_row_indexes:
            _selected_row_info = []
            for data in self.label_info.label_data:
                selected_text = self.label_texts[i.row()][data]
                _selected_row_info.append(
                    (
                        selected_text,
                        data,
                    )
                )
            self.selected_rows_info.append(_selected_row_info)
        self.gen_from_selection(self.selected_rows_info, self.progress_dialog)
        self.update_preview(
            self.temp_label_paths,
            labeltools.get_label_size(self.label_info.label_settings),
        )
        self.load_element_model(self.label_info.label_map, self.desc_maps)

    def gen_from_selection(self, selected_rows_info, progress_dialog):
        label_size_pix = labeltools.get_label_size(self.label_info.label_settings)

        try:
            self.position_text_pair_rows = labeltools.text_mapping(
                self.label_info.text_encoding_map,
                self.label_info.label_map,
                selected_rows_info,
            )
            _element_fn_map = labeltools.element_mapper_factory(
                self.label_info.label_map
            )
            self.element_fn_map = dict(_element_fn_map)

            (
                self.element_maps,
                self.label_info.module_size,
            ) = labeltools.create_element_maps(
                element_region_map=self.label_info.element_regions_map,
                regions=self.label_info.regions,
                element_fn_map=self.element_fn_map,
                position_text_pair_rows=self.position_text_pair_rows,
                font_name=self.label_info.font_name,
                title_font_name=self.label_info.title_font_name,
            )
            self.label_info.margins = (
                self.label_info.module_size,
                self.label_info.module_size,
            )
            self.img_coords_maps, self.desc_maps = labeltools.gen_asset_maps(
                self.element_maps,
                self.element_fn_map,
                self.label_info.element_regions_map,
                self.label_info.label_map,
                self.label_info.regions,
                self.label_info.element_resizable_map,
                self.label_info.margins,
                self.label_info.alignment,
                progress_dialog,
            )
            temp_label_array = labeltools.gen_labels(
                self.img_coords_maps, label_size_pix, self.label_info.margins
            )

        except AssertionError as ass:
            trace_exc = traceback.format_exc(ass)
            print(f"Error loading label selection: {trace_exc}")
            error_dialog = ErrorDialog("Error loading label selection", self)
            ret = error_dialog.exec()
            if ret == QDialog.Accepted:
                info_dialog = InfoDialog(
                    "One of your labels selected is of a different specification", self
                )
                info_dialog.exec()

        self.temp_label_paths = [t.name for t in temp_label_array]

    def update_preview(
        self, temp_label_array: list[object], label_size_pix: tuple[int, int]
    ) -> None:
        updated_rects, bottom_right_point, label_rect = self.preview_scene.load_scene(
            temp_label_array, label_size_pix
        )
        if label_rect is None:
            return
        self.label_rect = label_rect
        view_rect = QRect(0, 0, bottom_right_point.x(), bottom_right_point.y())
        self.ui.preview_display.updateScene(updated_rects)
        self.ui.preview_display.setSceneRect(view_rect)
        self.ui.preview_display.fitInView(self.label_rect, Qt.KeepAspectRatio)

    # def rearrange_label(self, item):
    #     def get_logical_rows(header):
    #         for vrow in range(header.count()):
    #             lrow = header.logicalIndex(vrow)
    #             element = self.ui.element_browser.verticalHeaderItem(lrow).text()
    #             print(element)

    #     if item == (header := self.ui.element_browser.verticalHeader()):
    #         get_logical_rows(header)

    def load_quantity_clicked(self, index):
        if index == 0:
            ret = self.open_file_dialog("quantity")
            if ret is None:
                return
            rows, _ = exttools.read_excel(
                self.quantity_excel_filename[0], type="quantity"
            )
            self.quantities = [str(i[0]) for i in rows]
            self.quantities_loaded = True

    def load_quantity(self, quantities):
        """
        Takes the current row indexes, and loads the corresponding quantity
        """
        # default quantity list is a list of ones
        if not self.quantities_loaded:
            max_row_index = max(index.row() for index in self.selected_row_indexes) + 1
            quantities = [1] * max_row_index
            self.quantities = quantities
        for i, q in enumerate(self.quantities):
            for count in range(len(self.selected_row_indexes)):
                if i == (
                    self.selected_row_indexes[count].row()
                ):  # check if quantity index matches row index
                    quant_item = QTableWidgetItem(str(q))
                    self.ui.element_browser.setItem(count, 0, quant_item)

    def explore_clicked(self):
        """
        explore dialog that allows user to view by category or value
        """

        def view_by_category(rows):
            self.load_browser_model(self.global_settings.show_cols, rows)

        self.explore_dialog = ExploreDialog(self.label_texts, view_by_category, self)
        self.explore_dialog.show()

    """
    Resize overwrites and limitations
    """

    def resizeEvent(self, event) -> None:  # overriding function
        self.resize_viewport()
        self.resize_splitter()
        QMainWindow.resizeEvent(self, event)

    def resize_viewport(self):
        self.ui.preview_display.fitInView(self.label_rect, Qt.KeepAspectRatio)

    def resize_splitter(self):
        if self.ui.splitter.sizes()[0] > self.END_COLUMN_POSITION:
            self.ui.splitter.moveSplitter(self.END_COLUMN_POSITION, 1)

    def limit_splitter(self, pos):
        if (
            self.ui.splitter.closestLegalPosition(pos, 1)
            > self.END_COLUMN_POSITION + 20
        ):
            self.move_splitter_wrapper(self.END_COLUMN_POSITION + 15, 1)
            return

        elif self.ui.splitter.closestLegalPosition(pos, 1) < self.START_COLUMN_POSITION:
            self.move_splitter_wrapper(self.START_COLUMN_POSITION + 5, 1)
            return

    def move_splitter_wrapper(self, position, id):
        # to prevent recursion issues
        self.ui.splitter.splitterMoved.disconnect(self.limit_splitter)
        self.ui.splitter.moveSplitter(position, id)
        self.ui.splitter.splitterMoved.connect(self.limit_splitter)
        return

    """
    Slots
    """

    def select_all_changed(self, check_state):
        if check_state == 2:
            if self.label_texts is None:
                return
            confirm_dialog = ConfirmDialog(self.ui.label_browser_table.rowCount())
            ret = confirm_dialog.exec()
            if ret == QDialog.Accepted:
                self.ui.label_browser_table.selectAll()
            else:
                self.ui.select_all_check.setCheckState(Qt.CheckState.Unchecked)
            self.ui.label_browser_table.itemClicked.connect(
                lambda: self.ui.select_all_check.setCheckState(Qt.CheckState.Unchecked)
            )

        elif check_state == 0:
            self.preview_scene.clear()
            self.view_label_selection()
            # self.ui.label_browser_table.itemClicked.disconnect(
            #     lambda: self.ui.select_all_check.setCheckState(Qt.CheckState.Unchecked)
            # )

    def search_table(self, input):
        if not input:
            return
        self.matching_items = self.ui.label_browser_table.findItems(
            input, Qt.MatchContains
        )
        if self.matching_items:
            self.item_indexes = []
            for item in self.matching_items:
                self.item_indexes.append(item.row() + 1)

    def search_select(self, max_index) -> None:
        search_dialog = SearchDialog(max_index, self)
        ret = search_dialog.exec()
        selections = []
        if ret == QDialog.Accepted:
            if search_dialog.ui.specific_selection_check.isChecked():
                selections = search_dialog.get_specific_selection()
            elif search_dialog.ui.matching_checkbox.isChecked():
                starts_with, ends_with = search_dialog.get_matching_selection()
                if starts_with and ends_with:
                    pattern = f"^{re.escape(starts_with)}.*{re.escape(ends_with)}$"
                    self.matching_items = self.ui.label_browser_table.findItems(
                        pattern, Qt.MatchRegularExpression
                    )
                elif starts_with and not ends_with:
                    self.matching_items = self.ui.label_browser_table.findItems(
                        starts_with, Qt.MatchStartsWith
                    )
                elif ends_with and not starts_with:
                    self.matching_items = self.ui.label_browser_table.findItems(
                        starts_with, Qt.MatchEndsWith
                    )
                for item in self.matching_items:
                    selections.append(item.row() + 1)
            else:
                selections = search_dialog.get_range()
            if not selections:  # empty search
                return
            self.select_searched(selections)
            return

    def open_file_dialog(self, type: str) -> None:
        match type:
            case "labels":
                label_excel_filepath = QFileDialog.getOpenFileName(
                    parent=self,
                    caption=QObject.tr("Open Excel File"),
                    dir=self.global_settings.default_dir,
                    filter=QObject.tr("Excel Files (*.xlsx *.xlsm *.xltx *.xltm *xls)"),
                )
                if label_excel_filepath == ("", ""):
                    return
                else:
                    self.label_excel_filepath = label_excel_filepath[0]
                    _, file_ext = os.path.splitext(self.label_excel_filepath)
                    if file_ext == ".xls":
                        self.use_xls = True
                    else:
                        self.use_xls = False
                xl_worksheets, xl_worksheet_names = exttools.get_worksheets(
                    self.label_excel_filepath, self.use_xls
                )
                self.excel_dialog = ExcelDialog(
                    filepath=self.label_excel_filepath,
                    use_xls=self.use_xls,
                    xl_worksheets=xl_worksheets,
                    xl_worksheet_names=xl_worksheet_names,
                    label_info=self.label_info,
                    global_settings=self.global_settings,
                    parent=self,
                )
                ret = self.excel_dialog.exec()
                if ret == QDialog.Rejected:
                    return
                else:
                    (
                        self.selected_sheet,
                        self.header_dict,
                        self.label_info,
                        self.global_settings,
                    ) = self.excel_dialog.save_settings()

                try:
                    (
                        rows,
                        self.label_info.label_data,  # get the valid, updated label data
                        self.label_info.data_not_incl,
                        self.global_settings.show_cols,
                    ) = exttools.read_excel(
                        use_xls=self.use_xls,
                        sheet=self.selected_sheet,
                        header_dict=self.header_dict,
                        regex=self.label_info.label_regex,
                        label_data=self.label_info.label_data,
                        show_cols=self.global_settings.show_cols,
                    )
                    self.selected_row_indexes = []
                    if self.label_info.data_not_incl:
                        self.omit_invalid_data()
                        info_dialog = InfoDialog(
                            f"Data fields {', '.join(self.label_info.data_not_incl)} contain invalid characters, omitting..."
                        )
                        info_dialog.setWindowTitle("Invalid Data")
                        _ = info_dialog.exec()

                except Exception as exc:
                    trace_exc = traceback.format_exc(exc)
                    print(f"Excel Error {trace_exc}")
                    error_dialog = ErrorDialog("Error loading label excel file", self)
                    ret = error_dialog.exec()
                    if ret == QDialog.Accepted:
                        info_dialog = InfoDialog(str(exc), self)
                        info_dialog.exec()

                else:
                    self.label_texts = rows
                    self.load_browser_model(self.global_settings.show_cols, rows)
                    self.change_button_states("labels")

            case "pdf":
                pdf_path = QFileDialog.getSaveFileName(
                    parent=self,
                    caption=QObject.tr("Save PDF as"),
                    dir=self.global_settings.default_dir,
                    filter=QObject.tr("PDF Files (*.pdf)"),
                )
                if pdf_path[0] == "":
                    return
                self.global_settings.pdf_path = pdf_path[0]
                pdf_starter = pdfprep.create_pdf_object()
                self.pdf = pdfprep.pdf_generator(
                    pdf_starter, self.global_settings.pdf_path, self.temp_label_paths
                )

            case "zpl":
                self.zpl_path = QFileDialog.getExistingDirectory(
                    parent=self,
                    caption=QObject.tr("Save ZPLs in:"),
                    dir=self.global_settings.default_dir,
                )
                _quantities = self.get_quantities()
                _browser_header_rows = self.get_browser_header_rows()
                zpl_prompt = ZPLPrompt(parent=self)
                zpl_prompt.exec()
                if zpl_prompt.clickedButton() == zpl_prompt.use_img:
                    self.zpl_from_img(self.zpl_path, _quantities, _browser_header_rows)
                if zpl_prompt.clickedButton() == zpl_prompt.use_zpl:
                    return
                    # self.zpl_from_code(self.zpl_path, _quantities, _browser_header_rows)

            case "quantity":
                self.quantity_excel_filename = QFileDialog.getOpenFileName(
                    parent=self,
                    caption=QObject.tr("Open Excel File"),
                    dir="./",
                    filter=QObject.tr("Excel Files (*.xlsx *.xlsm *.xltx *.xltm)"),
                )
                if self.quantity_excel_filename[0] == "":
                    return None
                _, _, rows = exttools.read_excel(
                    self.quantity_excel_filename[0], type=type
                )
                self.quantities = [str(i[0] for i in rows)]

    def edit_quantity(self, item: object) -> None:
        browser_row = item.row()
        qty_row = self.ui.element_browser.verticalHeaderItem(browser_row)
        if qty_row is None:
            return
        self.quantities[int(qty_row.text())] = item.text()

    def edit_labels(self, item: object) -> None:
        browser_row = item.row()
        browser_col = item.column()
        label_texts_row = self.ui.label_browser_table.verticalHeaderItem(browser_row)
        if label_texts_row is None:
            return
        self.label_texts[int(label_texts_row.text())][browser_col] = item.text()

    def get_quantities(self):
        """
        get the current selection and find out which quantities are needed
        """
        browser_header_rows = self.get_browser_header_rows()
        quantities = [self.quantities[r - 1] for r in browser_header_rows]
        return quantities

    def get_browser_header_rows(self):
        """
        get the current selection and find out which quantities are needed
        """
        browser_header_rows = []
        for i in self.selected_row_indexes:
            browser_row = i.row()
            browser_header_row_item = self.ui.label_browser_table.verticalHeaderItem(
                browser_row
            )
            browser_header_rows.append(int(browser_header_row_item.text()))
        browser_header_rows.sort()
        return browser_header_rows

    def global_refresh(self):
        """
        refreshes all UI elements and reloads excel and labels with new settings (if changed)
        also reloads the element browser by load_element_model
        """
        try:
            (
                rows,
                self.label_info.label_data,
                self.label_info.data_not_incl,
                self.global_settings.show_cols,
            ) = exttools.read_excel(
                use_xls=self.use_xls,
                sheet=self.selected_sheet,
                header_dict=self.header_dict,
                regex=self.label_info.label_regex,
                label_data=self.label_info.label_data,
                show_cols=self.global_settings.show_cols,
            )
        except Exception as exc:
            trace_exc = traceback.format_exc(exc)
            print(f"Excel file error {trace_exc}")
            error_dialog = ErrorDialog("Error refreshing label excel file", self)
            ret = error_dialog.exec()
            if ret == QDialog.Accepted:
                info_dialog = InfoDialog(str(exc), self)
                info_dialog.exec()
        if self.label_info.data_not_incl:
            self.omit_invalid_data()
            info_dialog = InfoDialog(
                f"Data fields {', '.join(self.label_info.data_not_incl)} are invalid, omitting..."
            )
            info_dialog.setWindowTitle("Invalid Data")
            _ = info_dialog.exec()
        self.label_texts = rows
        self.load_browser_model(self.global_settings.show_cols, rows)
        self.preview_scene.clear()
        self.view_label_selection()

    def change_button_states(self, type: str) -> None:
        match type:
            case "labels":
                self.ui.splitter.splitterMoved.connect(self.limit_splitter)
                self.ui.refresh_button.setEnabled(True)
                self.ui.save_pdf_button.setDisabled(True)
                self.ui.search_button.setEnabled(True)
                self.ui.settings_button.setEnabled(True)
                self.ui.explore_button.setEnabled(True)
                self.ui.label_browser_table.setEnabled(True)

            case "browser":
                self.ui.refresh_button.setEnabled(True)
                self.ui.save_pdf_button.setEnabled(True)

    """
    Functions
    """

    def omit_invalid_data(self):
        _lm_copy = self.label_info.label_map.copy()
        for posit in self.label_info.label_map.keys():
            for p_tuple in self.label_info.text_encoding_map.values():
                if posit not in p_tuple:
                    continue
                else:
                    break
            else:
                _lm_copy.pop(posit)
        for dni in self.label_info.data_not_incl:
            self.label_info.qr_encode_bools.pop(dni)
        self.label_info.label_map = _lm_copy

    def open_settings(self) -> None:
        self.settings_dialog = SettingsDialog(
            self.label_info, self.global_settings, self.header_dict, self
        )
        ret = self.settings_dialog.exec()
        if ret == QDialog.Rejected:
            return
        else:
            (
                self.label_info,
                self.global_settings,
            ) = self.settings_dialog.save_settings()
            self.global_refresh()

    def select_searched(self, selections: list[int]) -> None:
        self.ui.label_browser_table.itemSelectionChanged.disconnect(
            self.view_label_selection
        )
        self.ui.label_browser_table.clearSelection()
        self.ui.label_browser_table.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection
        )
        for index in selections:
            try:
                self.ui.label_browser_table.selectRow(index - 1)
            except Exception as _:
                self.ui.label_browser_table.setSelectionMode(
                    QAbstractItemView.SelectionMode.ExtendedSelection
                )
                self.ui.label_browser_table.itemSelectionChanged.connect(
                    self.view_label_selection
                )
                return
        self.view_label_selection()
        self.ui.label_browser_table.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        self.ui.label_browser_table.itemSelectionChanged.connect(
            self.view_label_selection
        )

    def zpl_from_img(self, zpl_path, quantities, browser_header_rows):
        print("Image chosen")
        self.zpl_codes = []
        for i, zpl_label in enumerate(
            zpp.img_to_zpl(
                temp_label_paths=self.temp_label_paths,
                label_settings_mm=zpp.zpl_size_translator(
                    info=self.label_info.label_settings
                ),
            )
        ):
            self.zpl_codes.append(zpl_label)
            self.zpl_saver(zpl_label, zpl_path, quantities, i, browser_header_rows)

    def zpl_from_code(self, zpl_path, quantities, browser_header_rows):
        print("Code chosen")
        zpl_translator_fn = zpp.create_zpl_fn_translator(
            element_fn_map=self.element_fn_map,
            label_settings_mm=zpp.zpl_size_translator(self.label_info.label_settings),
            margins_mm=zpp.zpl_size_translator(
                zpp.zpl_size_translator(info=self.label_info.label_settings),
                self.label_info.margins,
            ),
        )
        for i, zpl_label in enumerate(
            zpp.write_zpl(
                img_coords_maps=self.img_coords_maps,
                element_maps=self.element_maps,
                margins_mm=zpp.zpl_size_translator(
                    zpp.zpl_size_translator(info=self.label_info.label_settings),
                    self.label_info.margins,
                ),
                label_settings_mm=zpp.zpl_size_translator(
                    info=self.label_info.label_settings
                ),
                zpl_translator_fn=zpl_translator_fn,
                label_map=self.label_info.label_map,
            )
        ):
            self.zpl_saver(zpl_label, zpl_path, quantities, i, browser_header_rows)

    def zpl_saver(self, zpl_label, zpl_path, quantities, i, browser_header_rows):
        excel_filename = pathlib.PurePath(self.label_excel_filepath).stem
        for q in range(int(quantities[i])):
            zpl_save_path = os.path.join(
                zpl_path,
                f"{excel_filename}_index_{browser_header_rows[i]+1}_copy_{str(q+1)}.zpl",
            )  # add 1 because excel header occupies row 1
            zpp.save_zpl(zpl_label, zpl_save_path)

    def print_zpl(self):
        try:
            printer = zpp.interface_printer(
                zpp.zpl_size_translator(info=self.label_info.label_settings)
            )
            print(printer.queue)
        except Exception as exc:
            print(exc)
        _quantities = self.get_quantities()
        _browser_header_rows = self.get_browser_header_rows()
        zpl_prompt = ZPLPrompt(parent=self)
        zpl_prompt.exec()
        if zpl_prompt.clickedButton() == zpl_prompt.use_img:
            self.zpl_codes = []
            for i, zpl_label in enumerate(
                zpp.img_to_print(
                    temp_label_paths=self.temp_label_paths,
                    label_settings_mm=zpp.zpl_size_translator(
                        info=self.label_info.label_settings
                    ),
                )
            ):
                self.zpl_printer(_quantities, i, zpl_label, printer)
        if zpl_prompt.clickedButton() == zpl_prompt.use_zpl:
            return

    def print_images(self):
        print_tools = PrintTools()
        printer = print_tools.create_printer(self.label_info.label_settings)
        print_dialog = PrintDialog(printer, self)

        if print_dialog.exec() == QDialog.Accepted:
            try:
                print_tools.paint(
                    printer=printer,
                    temp_label_paths=self.temp_label_paths,
                    resolution=self.label_info.label_settings[1],
                    label_rect=self.label_rect,
                    margins=self.label_info.margins,
                )
            except AssertionError as ass:
                trace_exc = traceback.format_exc(ass)
                print(f"Printer settings error{trace_exc}")
                error_dialog = ErrorDialog("Mismatched Printer Settings", self)
                ret = error_dialog.exec()
                if ret == QDialog.Accepted:
                    info_dialog = InfoDialog(str(ass), self)
                    info_dialog.exec()


class PrintDialog(QPrintDialog):
    def __init__(self, printer, parent):
        super().__init__(printer, parent)
        self.setWindowTitle("Print Labels")
        self.setOption(QAbstractPrintDialog.PrintDialogOption.PrintSelection, on=False)
        self.setOption(QAbstractPrintDialog.PrintDialogOption.PrintPageRange, on=False)
        self.setOption(
            QAbstractPrintDialog.PrintDialogOption.PrintCurrentPage, on=False
        )
        self.setOption(
            QAbstractPrintDialog.PrintDialogOption.PrintCollateCopies, on=False
        )
        self.setOption(
            QAbstractPrintDialog.PrintDialogOption.PrintCurrentPage, on=False
        )
        self.setOption(
            QAbstractPrintDialog.PrintDialogOption.PrintShowPageSize, on=False
        )


class PrintTools:
    def create_printer(self, label_settings, rotated=True):
        self.rotated = rotated
        if rotated:
            label_settings = (
                (label_settings[0][1], label_settings[0][0]),
                label_settings[1],
                label_settings[2],
            )
        printer = QPrinter(mode=QPrinter.PrinterMode.ScreenResolution)
        printer.Unit(QPrinter.Inch)
        printer.setColorMode(QPrinter.GrayScale)
        printer.setPageOrder(QPrinter.FirstPageFirst)
        printer.setDuplex(QPrinter.DuplexNone)
        printer.setOutputFormat(QPrinter.NativeFormat)
        page_size = QPageSize(
            QSizeF(float(label_settings[0][0]), float(label_settings[0][1])),
            QPageSize.Inch,
            name="",
            matchPolicy=QPageSize.SizeMatchPolicy.ExactMatch,
        )
        printer.setPageSize(page_size)
        printer.setPageMargins(QMarginsF(0, 0, 0, 0), units=QPageLayout.Inch)
        printer.setResolution(label_settings[1])

        return printer

    def paint(self, printer, temp_label_paths, resolution, label_rect, margins):
        assert resolution == printer.resolution(), (
            f"Resolution is different from printer settings.\n"
            f"Current printer settings: \t{printer.resolution()}DPI\n"
            f"Label resolution: \t\t{resolution}DPI\n"
            f"Please set your label and printer settings to the same DPI"
        )
        painter = QPainter(printer)
        for label_path in temp_label_paths:
            label_image = QImage(label_path)
            if self.rotated:
                label_rect = QRect(
                    0, margins[0], label_rect.height(), label_rect.width()
                )
                if printer.printerName() == "":  # printing to file
                    label_rect = QRect(0, 0, label_rect.width(), label_rect.height())
                transform = QTransform()
                label_image = label_image.transformed(
                    transform.rotate(90.0), mode=Qt.SmoothTransformation
                )
            painter.drawImage(label_rect, label_image)
            if temp_label_paths.index(label_path) < len(temp_label_paths) - 1:
                printer.newPage()
        painter.end()

    # def print_zpl(self):
    #     try:
    #         printer = zpp.interface_printer(
    #             zpp.zpl_size_translator(info=self.label_info.label_settings)
    #         )
    #         print(printer.queue)
    #     except Exception as exc:
    #         print(exc)
    #     _quantities = self.get_quantities()
    #     _browser_header_rows = self.get_browser_header_rows()
    #     zpl_prompt = ZPLPrompt(parent=self)
    #     zpl_prompt.exec()
    #     if zpl_prompt.clickedButton() == zpl_prompt.use_img:
    #         self.zpl_codes = []
    #         for i, (zpl_label, image, label_info.label_settings_print) in enumerate(
    #             zpp.img_to_print(
    #                 temp_label_paths=self.temp_label_paths,
    #                 label_info.label_settings_mm=zpp.zpl_size_translator(info=self.label_info.label_settings),
    #             )
    #         ):
    #             image_byte = bytes(image.tobytes())
    #             printer.print_graphic(
    #                 0,
    #                 0,
    #                 int(label_info.label_settings_print[0][0] * label_info.label_settings_print[1]),
    #                 int(label_info.label_settings_print[0][1] * label_info.label_settings_print[1]),
    #                 image_byte,
    #                 1,
    #             )
    #     if zpl_prompt.clickedButton() == zpl_prompt.use_zpl:
    #         return

    # def zpl_printer(self, quantities, i, zpl_label, printer):
    #     for q in range(int(quantities[i])):
    #         zpl_code = zpl_label.dumpZPL()
    #         zpl_label.preview()
    #         printer.output(zpl_code)
    #         self.zpl_codes.append(zpl_code)


class PreviewDisplay(QGraphicsScene):
    def __init__(self, parent):
        # storing already rendered rects and pixmaps to prevent redrawing
        super().__init__(parent=parent)
        self.starting_rect = QRect()
        self.starting_rect.setRect(0, 0, 0, 0)
        self._current_rects = [
            self.starting_rect,
        ]
        self._new_rects = [
            self.starting_rect,
        ]
        self._current_pixmaps = []  # for caching
        self.margin = 20

    def load_scene(
        self, temp_label_array: list[object], label_size_pix: tuple[int, int]
    ) -> tuple[list[object], object, object]:
        """
        Takes in the array of temp_label locations,
        clears previous scene,
        creates a rect for each based on label size and
        appends them to the current scene, also returns
        the rectangles it has added for updating
        """
        if self._current_rects:
            self.clear()

        for i, temp_label in enumerate(temp_label_array):
            # create new rects first using current selection
            x, y = (
                self._new_rects[i].bottomLeft().x(),
                self._new_rects[i].bottomLeft().y() + self.margin,
            )
            self._add_rects(label_size_pix, x, y)
            self._add_to_scene(temp_label, x, y)

        # compare and update any added or removed rects
        rects_to_update = self._update_rects()
        try:
            return (
                rects_to_update,
                self._current_rects[-1].bottomRight(),
                self._current_rects[1],
            )
        except IndexError as ixe:
            return (
                rects_to_update,
                self._current_rects[-1].bottomRight(),
                None,
            )

    def _add_to_scene(self, temp_label: object, x: int, y: int) -> None:
        # TODO: utilise the QPixmap's cache ability to reduce redrawing images
        temp_label_pixmap = QPixmap(temp_label)  # use QPixmap for cache ability
        pix_pointer = self.addPixmap(temp_label_pixmap)
        # print(f"Setting {temp_label} pixmap to pos {x},{y}")
        pix_pointer.setPos(x, y)

    def _add_rects(self, label_size_pix: tuple[int, int], x: int, y: int) -> object:
        rect = QRect()
        rect.setRect(x, y, label_size_pix[0], label_size_pix[1])
        self._new_rects.append(rect)

    def _update_rects(self) -> list[object]:
        """
        After updating scene, update the old rects with the new selection
        """
        self._current_rects = self._new_rects[:]
        if len(self._new_rects) > len(self._current_rects):
            _updated_rects = list(set(self._current_rects).difference(self._new_rects))
        else:
            _updated_rects = self._new_rects[:]
        self._new_rects.clear()
        self._new_rects = [
            self.starting_rect,
        ]
        return _updated_rects


class ErrorDialog(QDialog):
    def __init__(self, user_msg, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Error")
        self.setModal(True)

        ack_button = QDialogButtonBox.Open | QDialogButtonBox.Close
        self.button_box = QDialogButtonBox(ack_button)
        self.button_box.button(QDialogButtonBox.Open).setText("More Info")
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        user_msg_label = QLabel(user_msg)
        self.layout.addWidget(user_msg_label)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)


class InfoDialog(QDialog):
    def __init__(self, error_msg, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Error Info")
        self.setModal(True)

        close_button = QDialogButtonBox.Close
        self.button_box = QDialogButtonBox(close_button)
        self.button_box.button(QDialogButtonBox.Close).setText("Done")
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        error_label = QLabel(error_msg)
        self.layout.addWidget(error_label)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)


class SearchDialog(QDialog):
    def __init__(self, max_index, parent=None):
        super().__init__(parent=parent)
        self.max_index = max_index  # max index allowed to search
        self.ui = Ui_SearchDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setText("Search")
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.specific_selection_check.stateChanged.connect(self.specific_state_check)
        self.ui.matching_checkbox.stateChanged.connect(self.matching_state_check)
        self.specific_regex = QRegularExpression(
            rf"^(?:\d{{1,{len(str(max_index))}}}(?:,[ ]?\d{{1,{len(str(max_index))}}}|-\d{{1,{len(str(max_index))}}})*)?$"
        )
        self.specific_index_validator = QRegularExpressionValidator(
            self.specific_regex, self.ui.specific_selection_edit
        )
        self.ui.from_spin.setMaximum(max_index)
        self.ui.to_spin.setMaximum(max_index)
        self.ui.specific_selection_edit.setValidator(self.specific_index_validator)

    def specific_state_check(self, check_state):
        if check_state == 2:
            self.ui.from_spin.setDisabled(True)
            self.ui.to_spin.setDisabled(True)
            self.ui.matching_checkbox.setCheckState(Qt.Unchecked)
            self.ui.matching_checkbox.setDisabled(True)
            self.ui.starts_with_edit.setDisabled(True)
            self.ui.ends_with_edit.setDisabled(True)
            self.ui.specific_selection_edit.setEnabled(True)

        elif check_state == 0:
            self.ui.from_spin.setEnabled(True)
            self.ui.to_spin.setEnabled(True)
            self.ui.matching_checkbox.setEnabled(True)
            self.ui.starts_with_edit.setEnabled(True)
            self.ui.ends_with_edit.setEnabled(True)
            self.ui.specific_selection_edit.setDisabled(True)

    def matching_state_check(self, check_state):
        if check_state == 2:
            self.ui.from_spin.setDisabled(True)
            self.ui.to_spin.setDisabled(True)
            self.ui.specific_selection_check.setCheckState(Qt.Unchecked)
            self.ui.specific_selection_check.setDisabled(True)
            self.ui.starts_with_edit.setEnabled(True)
            self.ui.ends_with_edit.setEnabled(True)
            self.ui.specific_selection_edit.setDisabled(True)

        elif check_state == 0:
            self.ui.from_spin.setEnabled(True)
            self.ui.to_spin.setEnabled(True)
            self.ui.matching_checkbox.setEnabled(True)
            self.ui.starts_with_edit.setDisabled(True)
            self.ui.ends_with_edit.setDisabled(True)
            self.ui.specific_selection_edit.setEnabled(True)

    def get_range(self):
        _from_index = self.ui.from_spin.value()
        _to_index = self.ui.to_spin.value()
        selection_list = [i for i in range(_from_index, _to_index + 1)]
        return selection_list

    def get_specific_selection(self):
        entry_text = self.ui.specific_selection_edit.text()
        selection_list = []
        selections = re.findall(r"(\d+)(?:-(\d+))?(\s*,\s*|$)", entry_text)
        for start, end, _ in selections:
            if end:
                selection_range = range(int(start), int(end) + 1)
                selection_list.extend(list(selection_range))
            else:
                selection_list.append(int(start))

        return selection_list

    def get_matching_selection(self):
        starts_with = self.ui.starts_with_edit.text()
        ends_with = self.ui.ends_with_edit.text()
        return starts_with, ends_with


class DialogDataTools(
    QDialog
):  # to hold common functions btwn excel and setting QDialogs
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.master = parent
        self.size_map = {
            0: ("3x4 (Max 2 Fields)", (3, 4)),
            1: ("6x3 (Max 5 Fields)", (6, 3)),
        }
        self.row_combo_map = {}
        self.row_texts = []
        self.row_font = QFont()
        self.row_font.setFamilies(["Helvetica Neue"])
        self.row_font.setKerning(True)

    def check_show_cols(self, item: object):
        state = item.checkState()
        if state == Qt.CheckState.Checked:
            self.global_settings.show_cols.update({item.text(): True})
        elif state == Qt.CheckState.Unchecked:
            self.global_settings.show_cols.update({item.text(): False})

    def size_check(self, index: int):
        match index:
            case 0:
                if (x := len(self.label_info.label_data) - 2) > 0:
                    for i in range(x):
                        self.ui.label_data_list.item(i + 2).setCheckState(Qt.Unchecked)
                self.label_info.max_fields = 2
                info_dialog = InfoDialog(
                    f"This layout provides a maximum of {self.label_info.max_fields} label data fields",
                    parent=self.master,
                )
                info_dialog.setWindowTitle("Maximum Fields Exceeded")
                _ = info_dialog.exec()
            case 1:
                self.label_info.max_fields = 5
        _ls = self.label_info.label_settings
        size = self.size_map[index][1]
        self.label_info.label_settings = (size, _ls[1], _ls[2])

    def check_label_data(self, item: object):
        """
        Check label state -> update QR encoding list, and data location
        """
        state = item.checkState()
        if state == Qt.CheckState.Checked:
            self.label_info.label_data.append(item.text())
            qr_item = QListWidgetItem(item.text())
            qr_item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            qr_item.setCheckState(Qt.Unchecked)
            self.ui.qr_data_list.addItem(qr_item)
            self.label_info.qr_encode_bools.update({item.text(): False})
            self.row_texts.append(item.text())
            self.match_label_data_count(item)

        elif state == Qt.CheckState.Unchecked:
            self.label_info.label_data.remove(item.text())
            del self.label_info.qr_encode_bools[item.text()]
            qr_item = self.ui.qr_data_list.findItems(
                item.text(), Qt.MatchFlag.MatchExactly
            )
            self.row_texts.remove(item.text())
            self.match_label_data_count(item)
            if qr_item:
                _ = self.ui.qr_data_list.takeItem(self.ui.qr_data_list.row(qr_item[0]))
                # self.ui.first_row_combobox.removeItem(
                #     self.ui.first_row_combobox.findText(
                #         item.text(), Qt.MatchFlag.MatchExactly
                #     )
                # )
                # self.ui.second_row_combobox.removeItem(
                #     self.ui.second_row_combobox.findText(
                #         item.text(), Qt.MatchFlag.MatchExactly
                #     )
                # )

    def match_label_data_count(self, item=None):
        if len(self.row_texts) > self.label_info.max_fields:
            item.setCheckState(Qt.CheckState.Unchecked)
            self.ui.show_columns_list.findItems(item.text(), Qt.MatchFlag.MatchExactly)[
                0
            ].setCheckState(Qt.CheckState.Unchecked)
            info_dialog = InfoDialog(
                f"This layout provides a maximum of {self.label_info.max_fields} label data fields"
            )
            info_dialog.setWindowTitle("Invalid selection")
            _ = info_dialog.exec()

        if (x := max(self.row_combo_map.keys(), default=-1)) + 1 > len(self.row_texts):
            # if there are more widgets than texts, hide them (not prune)
            getattr(self.ui, f"row_widget{x}").setVisible(False)
            self.row_combo_map.popitem()
            delattr(self.ui, f"row_widget{x}")

        elif len(self.row_texts) > (
            x := max(self.row_combo_map.keys(), default=-1) + 1
        ):
            # if there are more texts than widget maps
            # either create a new row or set visible if it exists already
            setattr(self.ui, f"label_row_h_layout{x}", QHBoxLayout())
            __label_row_h_layout = getattr(self.ui, f"label_row_h_layout{x}")
            __label_row_h_layout.setObjectName(f"label_row_h_layout{x}")
            setattr(self.ui, f"row_widget{x}", QWidget(self.ui.label_rows_groupbox))
            __row_widget = getattr(self.ui, f"row_widget{x}")
            __row_widget.setObjectName(f"row_widget{x}")
            __row_widget.setFont(self.row_font)
            setattr(self.ui, f"row_widget{x}_h_layout", QHBoxLayout(__row_widget))
            __row_widget_h_layout = getattr(self.ui, f"row_widget{x}_h_layout")
            __row_widget_h_layout.setObjectName(f"row_widget{x}_h_layout")
            __row_widget_h_layout.setContentsMargins(0, 0, 0, 0)
            setattr(self.ui, f"row_combobox{x}", QComboBox(__row_widget))
            __row_combobox = getattr(self.ui, f"row_combobox{x}")
            __row_combobox.setObjectName(f"row_combobox{x}")
            __row_combobox.setFont(self.row_font)
            __row_combobox.setMinimumContentsLength(8)
            __row_widget_h_layout.addWidget(__row_combobox)
            setattr(self.ui, f"row_bar_radio{x}", QRadioButton(__row_widget))
            __row_bar_radio = getattr(self.ui, f"row_bar_radio{x}")
            __row_bar_radio.setObjectName(f"row_bar_radio{x}")
            __row_bar_radio.setFont(self.row_font)
            __row_widget_h_layout.addWidget(__row_bar_radio)
            setattr(self.ui, f"row_text_radio{x}", QRadioButton(__row_widget))
            __row_text_radio = getattr(self.ui, f"row_text_radio{x}")
            __row_text_radio.setObjectName(f"row_text_radio{x}")
            __row_text_radio.setFont(self.row_font)
            __row_widget_h_layout.addWidget(__row_text_radio)
            __label_row_h_layout.addWidget(__row_widget)
            self.ui.label_rows_v_layout.addLayout(__label_row_h_layout)
            __row_text_radio.setText("Text")
            __row_bar_radio.setText("Barcode")
            self.row_combo_map.update({x: __row_combobox})
            __row_widget.setVisible(True)
            __row_combobox.addItems(self.row_texts)
            __row_combobox.setCurrentIndex(__row_combobox.count() - 1)
        else:
            pass
        for cw in self.row_combo_map.values():
            cur_id = cw.currentIndex()
            cw.clear()
            cw.addItems(self.row_texts)
            cw.setCurrentIndex(cur_id)
            # case 0:
            #     self.ui.first_row_groupbox.setDisabled(True)
            #     self.ui.second_row_groupbox.setDisabled(True)
            #     self.ui.first_row_combobox.setCurrentText("")
            #     self.ui.second_row_combobox.setCurrentText("")
            #     self.ui.first_row_combobox.setDisabled(True)
            #     self.ui.second_row_combobox.setDisabled(True)

            # case 1:
            #     self.ui.first_row_groupbox.setEnabled(True)
            #     self.ui.first_text_radio.setChecked(True)
            #     self.ui.second_text_radio.setChecked(False)
            #     self.ui.second_row_groupbox.setEnabled(True)
            #     self.ui.first_row_combobox.setEnabled(True)
            #     self.ui.first_row_combobox.setCurrentIndex(
            #         self.ui.qr_data_list.count() - 1
            #     )
            #     self.ui.second_row_combobox.setEnabled(True)
            #     self.ui.second_row_combobox.setCurrentIndex(
            #         self.ui.qr_data_list.count() - 1
            #     )

            # case 2:
            #     self.ui.first_row_groupbox.setEnabled(True)
            #     self.ui.second_row_groupbox.setEnabled(True)
            #     self.ui.first_text_radio.setChecked(True)
            #     self.ui.second_text_radio.setChecked(True)
            #     self.ui.first_row_combobox.setEnabled(True)
            #     self.ui.second_row_combobox.setEnabled(True)
            #     self.ui.first_row_combobox.setCurrentIndex(
            #         self.ui.qr_data_list.count() - 2
            #     )
            #     self.ui.second_row_combobox.setCurrentIndex(
            #         self.ui.qr_data_list.count() - 1
            #     )

            # case _:
            #     item.setCheckState(Qt.CheckState.Unchecked)
            #     self.ui.show_columns_list.findItems(
            #         item.text(), Qt.MatchFlag.MatchExactly
            #     )[0].setCheckState(Qt.CheckState.Unchecked)
            #     info_dialog = InfoDialog("Maximum of 2 label data fields")
            #     info_dialog.setWindowTitle("Invalid selection")
            #     _ = info_dialog.exec()

    def check_alignment(self):
        if self.ui.left_align_button.isChecked():
            self.label_info.alignment = "left"
        if self.ui.center_align_button.isChecked():
            self.label_info.alignment = "center"
        if self.ui.right_align_button.isChecked():
            self.label_info.alignment = "right"

    def check_show_titles(self, state):
        if state == 0:
            if self.label_info.show_titles:
                self.label_info.label_map = {
                    i: t for i, t in self.label_info.label_map.items() if t != "title"
                }
                self.label_info.label_map = {
                    i: v for i, v in enumerate(self.label_info.label_map.values())
                }
                self.label_info.show_titles = False
        elif state == 2:
            self.label_info.show_titles = True

    def check_label_map(self):
        self.label_info.label_data.clear()
        valid_keys = list(range(max(self.row_combo_map.keys()) + 1))
        self.label_info.label_map = {
            i: field
            for i, field in self.label_info.label_map.items()
            if i in valid_keys
        }
        for i, cw in self.row_combo_map.items():
            _li = i + 1
            if self.label_info.show_titles:
                _li *= 2
            if (t := cw.currentText()) and hasattr(self.ui, f"row_widget{i}"):
                self.label_info.label_data.append(t)
                if not (
                    getattr(self.ui, f"row_text_radio{i}").isChecked()
                    or getattr(self.ui, f"row_bar_radio{i}").isChecked()
                ):
                    self.label_info.label_map.pop(_li, None)
                    continue
                if self.label_info.show_titles:
                    self.label_info.label_data.append(t)
                    self.label_info.label_map.update({_li - 1: "title"})
                if getattr(self.ui, f"row_text_radio{i}").isChecked():
                    self.label_info.label_map.update({_li: "text"})
                elif getattr(self.ui, f"row_bar_radio{i}").isChecked():
                    self.label_info.label_map.update({_li: "bar"})

            else:
                self.label_info.label_map.pop(_li, None)
                if self.label_info.show_titles:
                    self.label_info.label_map.pop(_li - 1, None)

    def check_qr_data(self, item: object):
        state = item.checkState()
        if state == Qt.CheckState.Checked:
            self.label_info.qr_encode_bools.update({item.text(): True})
        elif state == Qt.CheckState.Unchecked:
            self.label_info.qr_encode_bools.update({item.text(): False})

    def sort_show_cols(self, header_dict, show_cols):
        __show_cols = {}
        for header, _ in header_dict.items():
            if show_cols.get(header):
                __show_cols[header] = True
        return __show_cols

    def accept(self) -> None:
        if not self.label_info.label_data or not any(
            self.label_info.qr_encode_bools.values()
        ):
            info_dialog = InfoDialog(
                f"You did not select any QR or label information. Please select at least one.",
                parent=self.master,
            )
            info_dialog.setWindowTitle("No selection made")
            _ = info_dialog.exec()
            return
        else:
            return super().accept()


class SettingsDialog(DialogDataTools):
    def __init__(self, label_info, global_settings, header_dict, parent=None):
        super().__init__(parent=parent)
        self.label_info = label_info
        self.global_settings = global_settings
        self.header_dict = header_dict
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.ui.save_settings_box.button(QDialogButtonBox.Ok).setText("Apply")
        self.ui.save_settings_box.accepted.connect(self.accept)
        self.ui.save_settings_box.rejected.connect(self.reject)

        self.ui.working_dir_edit.setPlaceholderText(os.path.abspath(__file__))
        self.ui.working_dir_edit.editingFinished.connect(self.dir_edited)

        self.resolutions = ["144", "203", "300"]
        self.languages = ["English", "แบบไทย"]
        self.units = ["Inches", "Pixels", "mm"]
        self.load_fields()
        self.match_label_data_count()
        self.set_radios(self.label_info.alignment, self.label_info.label_map)

        # button signals
        self.ui.dark_mode_checkbox.stateChanged.connect(self.dark_mode_check)
        self.ui.language_combobox.currentTextChanged.connect(self.language_check)
        self.ui.search_dir_button.clicked.connect(self.search_folder)
        self.ui.show_columns_list.itemChanged.connect(self.check_show_cols)
        self.ui.units_combobox.currentTextChanged.connect(self.units_check)
        self.ui.resolution_combobox.currentTextChanged.connect(self.resolution_check)
        self.ui.size_combobox.currentIndexChanged.connect(self.size_check)
        self.ui.label_data_list.itemChanged.connect(self.check_label_data)
        self.ui.show_titles_checkbox.stateChanged.connect(self.check_show_titles)
        self.ui.qr_data_list.itemChanged.connect(self.check_qr_data)
        self.ui.permitted_characters_list.itemChanged.connect(self.permitted_check)

    def load_fields(self):
        self.ui.show_columns_list.clear()
        self.ui.label_data_list.clear()
        self.ui.qr_data_list.clear()
        self.ui.permitted_characters_list.clear()

        self.load_comboboxes(
            self.languages,
            self.units,
            self.resolutions,
            self.label_info.label_data,
            self.label_info.label_settings,
        )
        self.load_checkboxes(self.label_info.show_titles)
        self.load_show_list(self.header_dict, self.global_settings.show_cols)
        self.load_label_list(
            self.header_dict,
            self.label_info.label_data,
        )
        self.load_qr_list(self.label_info.qr_encode_bools)
        self.load_permitted_list(
            self.label_info.allowed_chars,
            self.label_info.unallowed_chars,
        )

    def load_comboboxes(
        self,
        languages: list[str],
        units: list[str],
        resolutions: list[str],
        label_data: list[str],
        label_settings: tuple[int],
    ):
        self.ui.language_combobox.addItems(languages)
        self.ui.units_combobox.addItems(units)
        self.ui.resolution_combobox.addItems(resolutions)
        self.ui.resolution_combobox.setCurrentIndex(
            self.resolutions.index(str(label_settings[1]))
        )
        self.ui.size_combobox.addItems([v[0] for _, v in self.size_map.items()])
        self.ui.size_combobox.setCurrentIndex(
            [i for i, (_, t) in self.size_map.items() if t == label_settings[0]][0]
        )
        if label_data:
            for ld in label_data:
                self.row_texts.append(ld)
                self.match_label_data_count()

    def load_checkboxes(
        self,
        show_titles: bool,
    ):
        if show_titles:
            self.ui.show_titles_checkbox.setCheckState(Qt.Checked)
        else:
            self.ui.show_titles_checkbox.setCheckState(Qt.Unchecked)

    def load_show_list(self, header_dict: dict[str, int], show_cols: dict[str, bool]):
        for header in header_dict.keys():
            item = QListWidgetItem(str(header))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if show_cols.get(header):
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.ui.show_columns_list.addItem(item)

    def load_label_list(
        self,
        header_dict: dict[str, int],
        label_data: list[str],
    ):
        for header in header_dict.keys():
            item = QListWidgetItem(str(header))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if header in label_data:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.ui.label_data_list.addItem(item)

        # for data in data_not_incl:
        #     item = QListWidgetItem(str(data))
        #     item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        #     item.setCheckState(Qt.Unchecked)
        #     item.setDisabled(True)
        #     self.ui.label_data_list.addItem(item)

    def load_qr_list(self, qr_encode_bools: dict[str, bool]):
        for col, b in qr_encode_bools.items():
            item = QListWidgetItem(str(col))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if b:
                item.setCheckState(Qt.Checked)
            if not b:
                item.setCheckState(Qt.Unchecked)
            self.ui.qr_data_list.addItem(item)

    def load_permitted_list(self, allowed_chars: list[str], unallowed_chars: list[str]):
        for char in allowed_chars:
            item = QListWidgetItem(str(char).capitalize())
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            self.ui.permitted_characters_list.addItem(item)

        for char in unallowed_chars:
            item = QListWidgetItem(str(char).capitalize())
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.ui.permitted_characters_list.addItem(item)

    def set_radios(self, alignment, label_map: dict[int, str]):
        index_offset = 0
        match alignment:
            case "left":
                self.ui.left_align_button.setChecked(True)
            case "center":
                self.ui.center_align_button.setChecked(True)
            case "right":
                self.ui.right_align_button.setChecked(True)

        for row, ele_type in label_map.items():
            if ele_type == "qr" or ele_type == "title":
                index_offset += 1
                continue
            match ele_type:
                case "text":
                    getattr(self.ui, f"row_text_radio{row-index_offset}").setChecked(
                        True
                    )
                case "bar":
                    getattr(self.ui, f"row_bar_radio{row-index_offset}").setChecked(
                        True
                    )

    def dark_mode_check(self, state: int):
        if state == 0:
            qdarktheme.setup_theme("light")
        elif state == 2:
            qdarktheme.setup_theme(custom_colors={"primary": "#A5A5A5"})

    def language_check(self, option):
        pass

    def dir_edited(self):
        user_edited_dir = self.ui.working_dir_edit.text()
        try:
            assert (
                os.path.exists(user_edited_dir) == True
            ), f"{user_edited_dir} is an invalid path or does not exist,\nfiles will not save properly, defaulting to previous path"
        except AssertionError as ass:
            error_dialog = ErrorDialog("Invalid path detected")
            ret = error_dialog.exec()
            if ret == QDialog.Accepted:
                info_dialog = InfoDialog(str(ass), self)
                info_dialog.exec()
            self.ui.working_dir_edit.setText(self.global_settings.default_dir)

    def search_folder(self):
        chosen_dir = QFileDialog.getExistingDirectory(
            parent=self,
            caption=QObject.tr("Select default directory"),
            dir=self.global_settings.default_dir,
        )
        if self.global_settings.default_dir != chosen_dir and os.path.exists(
            chosen_dir
        ):
            self.global_settings.default_dir = chosen_dir
            self.ui.working_dir_edit.setText(chosen_dir)
        else:
            return

    def units_check(self, option: str):
        _ls = self.label_info.label_settings
        self.label_info.label_settings = (_ls[0], _ls[1], option.lower())

    def resolution_check(self, option: str):
        _ls = self.label_info.label_settings
        self.label_info.label_settings = (_ls[0], int(option), _ls[2])

    def permitted_check(self, item: object):
        state = item.checkState()
        if state == Qt.CheckState.Checked:
            if item.text() not in self.label_info.allowed_chars:
                self.label_info.allowed_chars.append(item.text())
        if state == Qt.CheckState.Unchecked:
            if item.text() in self.label_info.allowed_chars:
                self.label_info.allowed_chars.remove(item.text())
        self.construct_regex(self.label_info.allowed_chars, self.label_info.label_regex)

    def construct_regex(self, pattern_dict: dict[str, bool], current_regex: str):
        regex_pattern = current_regex

        if pattern_dict.get("alphabets") and "[a-zA-Z]" not in regex_pattern:
            regex_pattern += "[a-zA-Z]"

        if pattern_dict.get("numbers") and "\\d" not in regex_pattern:
            regex_pattern += "\\d"

        if pattern_dict.get("dashes") and "-" not in regex_pattern:
            regex_pattern += "-"

        if pattern_dict.get("spaces") and "\\s" not in regex_pattern:
            regex_pattern += "\\s"

        if pattern_dict.get("brackets") and "[\\[\\]]" not in regex_pattern:
            regex_pattern += "[\\[\\]]"

        if pattern_dict.get("colons") and ":" not in regex_pattern:
            regex_pattern += ":"

        return regex_pattern

    def save_settings(self):
        self.check_label_map()
        self.check_alignment()
        self.global_settings.show_cols = self.sort_show_cols(
            self.header_dict, self.global_settings.show_cols
        )
        return self.label_info, self.global_settings


class ExcelDialog(DialogDataTools):
    def __init__(
        self,
        filepath,
        use_xls,
        xl_worksheets,
        xl_worksheet_names,
        label_info,
        global_settings,
        parent=None,
    ):
        super().__init__(parent=parent)
        self.use_xls = use_xls
        self.xl_worksheets = xl_worksheets
        self.label_info = label_info
        self.label_info.reset_label_data()  # dont reset settings like dpi, size etc.
        self.global_settings = global_settings
        self.global_settings.reset_cols()
        self.ui = Ui_ExcelDialog()
        self.ui.setupUi(self)
        self.ui.file_chosen_label.setText(os.path.basename(filepath))
        self.ui.select_worksheet_combobox.addItems(xl_worksheet_names)
        self.ui.select_worksheet_combobox.setCurrentIndex(0)
        self.load_headers(0)  # must occur
        self.ui.select_worksheet_combobox.currentIndexChanged.connect(self.load_headers)
        self.ui.show_columns_list.itemChanged.connect(self.check_show_cols)
        self.ui.label_data_list.itemChanged.connect(self.check_label_data)
        self.ui.show_titles_checkbox.stateChanged.connect(self.check_show_titles)
        self.ui.qr_data_list.itemChanged.connect(self.check_qr_data)
        self.ui.size_combobox.addItems([v[0] for _, v in self.size_map.items()])
        self.ui.size_combobox.currentIndexChanged.connect(self.size_check)

    def load_headers(self, i: int):
        self.header_dict = exttools.get_headers(self.xl_worksheets[i], self.use_xls)
        self.ui.show_columns_list.clear()
        self.ui.label_data_list.clear()
        self.ui.qr_data_list.clear()
        for header in self.header_dict.keys():
            item = QListWidgetItem(str(header))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.ui.show_columns_list.addItem(item)
        for header in self.header_dict.keys():
            item = QListWidgetItem(str(header))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.ui.label_data_list.addItem(item)

    def iter_list(self, list_widget: object):
        for i in range(list_widget.count()):
            yield list_widget.item(i)

    def save_settings(self):
        xl_index = self.ui.select_worksheet_combobox.currentIndex()
        self.header_dict = dict(
            sorted(self.header_dict.items(), key=lambda item: item[1])
        )
        self.check_label_map()
        self.check_alignment()
        self.global_settings.show_cols = self.sort_show_cols(
            self.header_dict, self.global_settings.show_cols
        )
        return (
            self.xl_worksheets[xl_index],
            self.header_dict,
            self.label_info,
            self.global_settings,
        )


class ExploreDialog(QDialog):
    def __init__(self, label_texts, view_fn, parent=None):
        super().__init__(parent=parent)
        self.setModal(False)
        self.label_texts = label_texts
        self.view_fn = view_fn
        self.current_option = None
        self.cat = None
        self.ui = Ui_ExploreDialog()
        self.ui.setupUi(self)
        self.load_categories()
        self.ui.view_button.clicked.connect(self.view_option)
        self.ui.category_list.currentTextChanged.connect(self.detect_options)

    def load_categories(self):
        for header in self.label_texts[0].keys():
            item = QListWidgetItem(str(header))
            self.ui.category_list.addItem(item)

    def detect_options(self, cat):
        self.cat = cat
        self.ui.detected_list.clearSelection()
        self.ui.detected_list.clear()
        option_candidates = [
            label_row_dict.get(cat) for label_row_dict in self.label_texts
        ]
        options = list(set(option_candidates))
        for o in options:
            item = QListWidgetItem(str(o))
            self.ui.detected_list.addItem(item)

    def view_option(self):
        selected_item = self.ui.detected_list.currentItem()
        if selected_item is None:
            return
        selected_option = selected_item.text()
        option_rows = [
            label_row_dict
            for label_row_dict in self.label_texts
            if label_row_dict.get(self.cat) == selected_option
        ]
        self.view_fn(option_rows)


class ConfirmDialog(QDialog):
    def __init__(self, label_data_count, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Confirm Select All?")
        self.setModal(True)

        ack_button = QDialogButtonBox.Yes | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(ack_button)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        user_msg_label = QLabel(
            f"Select all {label_data_count} labels?\nIt may take a while for a large number of labels"
        )
        self.layout.addWidget(user_msg_label)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)


class ProgressDialog(QProgressDialog):
    def __init__(
        self,
        label_text="Loading...",
        cancel_button_text="Cancel",
        max=100,
        min=0,
        parent=None,
    ):
        super().__init__(
            maximum=max,
            minimum=min,
            cancelButtonText=cancel_button_text,
            labelText=label_text,
            parent=parent,
        )
        self.setWindowModality(Qt.WindowModal)
        self.setAutoClose(True)
        self.setAutoReset(True)
        self.setCancelButton(None)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )

    @staticmethod
    def cancel_print(printer):
        printer.abort()

    @staticmethod
    def cancel_load(ui):
        ui.select_all_check.setCheckState(Qt.CheckState.Unchecked)
        ui.preview_scene.clear()
        ui.label_browser_table.clearSelection()
        ui.label_browser_table.setCurrentItem(ui.label_browser_table.item(0, 0))
        ui.view_label_selection()


class ZPLPrompt(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setIcon(QMessageBox.Question)
        # self.setText("Save using Image or ZPL")
        # self.setInformativeText(
        #     f"Image draws the image pixel by pixel, ZPL re-writes labels from scratch using"
        #     f" pure code. ZPL is higher quality, but slower to process and may vary from preview"
        # )
        self.setText("Confirm selection?")
        self.setInformativeText(
            f"This operation may take up significant space and time"
        )
        # self.use_img = self.addButton("Use Image", QMessageBox.AcceptRole)
        # self.use_zpl = self.addButton("Use ZPL code", QMessageBox.RejectRole)
        self.use_img = self.addButton("Yes", QMessageBox.AcceptRole)
        self.use_zpl = self.addButton("Cancel", QMessageBox.RejectRole)


class LabelInfo:
    def __init__(self):
        # default settings
        self.label_settings = ((3, 4), 203, "inches")
        self.max_fields = 2
        self.alignment = "left"
        self._landscape = False
        self.allowed_chars = ["alphabets", "numbers", "dashes"]
        self.unallowed_chars = ["spaces", "brackets", "colons"]
        self.font_name = "OCRB_Regular"
        self.title_font_name = "OCRA_Bold"
        self.label_regex = r"^[a-zA-Z0-9\-]{1,}$"
        self.module_size = None
        self.show_titles = False
        self.label_map = {
            0: "qr",
        }
        self._element_resizable_map = {
            0: False,
        }
        self._element_regions_map = {
            0: 0,
        }
        self._regions = {
            0: {None: None},
        }
        self._label_data = []
        self.data_not_incl = []
        self._qr_encode_bools = {}
        self._text_encoding_map = {}
        self.margins = None
        self._region_clusters = {}

    def reset_label_data(self):
        self.label_map = {
            0: "qr",
        }
        self._element_resizable_map = {
            0: False,
        }
        self.label_data = []
        self.data_not_incl = []
        self.qr_encode_bools = {}
        self.text_encoding_map = {}
        self.element_seeds = {}

    @property
    def landscape(self):
        if self.label_settings[0][0] > self.label_settings[0][1]:
            return True
        else:
            return False

    @property
    def regions(self):
        _label_width = self.label_settings[0][0]
        _label_height = self.label_settings[0][1]
        _ppi = self.label_settings[1]
        _type = self.label_settings[2]
        if _type == "inches":
            _label_width *= _ppi
            _label_height *= _ppi
        if self.landscape:
            self._regions.update(
                {
                    0: {
                        "xyxy": (0, 0, _label_height, _label_height),
                        "size": (_label_height, _label_height),
                    },
                    1: {
                        "elements": [i for i in self.label_map.keys() if i != 0],
                        "xyxy": (_label_height, 0, _label_width, _label_height),
                        "size": (_label_width - _label_height, _label_height),
                    },
                }
            )
        else:
            self._regions.update(
                {
                    0: {
                        "xyxy": (0, 0, _label_width, _label_width),
                        "size": (_label_width, _label_width),
                    },
                    1: {
                        "xyxy": (0, _label_width, _label_width, _label_height),
                        "size": (_label_width, _label_height - _label_width),
                    },
                }
            )
        return self._regions

    @property
    def element_regions_map(self):
        # if width is greater than height, its a landscape scheme
        for i, ele_type in self.label_map.items():
            if ele_type == "qr":
                self._element_regions_map.update({i: 0})
            else:
                self._element_regions_map.update({i: 1})
        return self._element_regions_map

    @property
    def text_encoding_map(self):
        return self._text_encoding_map

    @text_encoding_map.setter
    def text_encoding_map(self, col_encode_info):
        if not col_encode_info:
            return
        cols_to_update = col_encode_info[0]
        qr_encode_bools = col_encode_info[1]
        self._text_encoding_map.clear()
        for i, col in enumerate(cols_to_update, 1):
            if existing_pos := self._text_encoding_map.get(col):
                if existing_pos is not None:
                    updated_pos = (
                        *existing_pos,
                        i,
                    )
                    self._text_encoding_map.update({col: updated_pos})
                    continue
            elif qr_encode_bools[col]:
                self._text_encoding_map.update({col: (0, i)})
            else:
                self._text_encoding_map.update({col: (i,)})

    @property
    def element_resizable_map(self):
        return self._element_resizable_map

    @element_resizable_map.setter
    def element_resizable_map(self, cols_to_update):
        # by default, all resizable
        # TODO: maybe? let user choose which to resize
        if not cols_to_update:
            return
        self._element_resizable_map.update(
            {
                index: True
                for index, _ in enumerate(cols_to_update, 1)
                # index: False if index < len(cols_to_update) else True
                # for index, _ in enumerate(cols_to_update, 1)
            }
        )

    # @property
    # def qr_encode_bools(self):
    #     return self._qr_encode_bools

    # @qr_encode_bools.setter
    # def qr_encode_bools(self, cols_to_update):
    #     if not cols_to_update:
    #         return
    #     self._qr_encode_bools.update({col: False for col in cols_to_update})

    @property
    def label_data(self):
        return self._label_data

    @label_data.setter
    def label_data(self, cols_to_update):
        # should only be used for initial loading or reloading of all cols
        self._label_data = []
        if not cols_to_update or cols_to_update is None:
            return
        for col in cols_to_update:
            if col in self._label_data:
                continue
            else:
                self._label_data.append(col)
        self.element_resizable_map = cols_to_update
        self.text_encoding_map = (cols_to_update, self.qr_encode_bools)


class GlobalSettings:
    def __init__(self):
        self.default_dir = "./"
        self.pdf_path = "./"
        self.language = "English"
        self.theme = "dark"
        self.show_cols = {}

    def reset_cols(self):
        self.show_cols = {}


"""keep these templates for future reference"""

# class ElementBrowserModel(QAbstractListModel):
#     def __init__(self, data=None):
#         QAbstractListModel.__init__(self)
#         self.load_data(data)

#     def load_data(self, d):
#         self.labels = d
#         self.row_count = len(self.labels)

#     def rowCount(self, parent=QModelIndex()):
#         return self.row_count

#     def headerData(self, section, orientation, role):
#         if role != Qt.DisplayRole:
#             return None
#         if orientation == Qt.Horizontal:
#             return ("Labels",)[section]
#         else:
#             return f"{section}"

#     def data(self, index, role=Qt.DisplayRole):
#         row = index.row()

#         if not index.isValid():
#             return None

#         if role == Qt.DisplayRole:
#             return self.labels[row]
#         elif role == Qt.BackgroundRole:
#             return QColor(Qt.black)
#         elif role == Qt.TextAlignmentRole:
#             return Qt.AlignCenter

# class ElementBrowserModel(QAbstractTableModel):
#     def __init__(self, data=None):
#         QAbstractTableModel.__init__(self)
#         self.load_data(data)

#     def load_data(self, d):
#         self.labels = d
#         self.row_count = len(self.labels)

#     def rowCount(self, parent=QModelIndex()):
#         return self.row_count

#     def headerData(self, section, orientation, role):
#         if role != Qt.DisplayRole:
#             return None
#         if orientation == Qt.Horizontal:
#             return ("Labels",)[section]
#         else:
#             return f"{section}"

#     def data(self, index, role=Qt.DisplayRole):
#         row = index.row()

#         if not index.isValid():
#             return None

#         if role == Qt.DisplayRole:
#             return self.labels[row]
#         elif role == Qt.BackgroundRole:
#             return QColor(Qt.black)
#         elif role == Qt.TextAlignmentRole:
#             return Qt.AlignCenter


def run():
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme(custom_colors={"primary": "#A5A5A5"})
    MainWindow = UI()
    MainWindow.show()
    app.exec()
