# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FlabelLrZKZz.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QFrame, QGraphicsView, QGridLayout, QGroupBox,
    QHeaderView, QLayout, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QSplitter,
    QTableWidget, QTableWidgetItem, QWidget)
import resources_rc

class Ui_Flabel(object):
    def setupUi(self, Flabel):
        if not Flabel.objectName():
            Flabel.setObjectName(u"Flabel")
        Flabel.resize(1012, 578)
        Flabel.setMinimumSize(QSize(600, 300))
        Flabel.setBaseSize(QSize(1024, 576))
        self.actionAbout_Flabel = QAction(Flabel)
        self.actionAbout_Flabel.setObjectName(u"actionAbout_Flabel")
        self.actionPrint = QAction(Flabel)
        self.actionPrint.setObjectName(u"actionPrint")
        self.centralwidget = QWidget(Flabel)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetNoConstraint)
        self.gridLayout_3.setContentsMargins(10, 0, 10, 10)
        self.master_group = QGroupBox(self.centralwidget)
        self.master_group.setObjectName(u"master_group")
        self.master_group.setFlat(True)
        self.gridLayout_2 = QGridLayout(self.master_group)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.master_group)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setMaximumSize(QSize(16777215, 16777215))
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(3)
        self.left_group = QGroupBox(self.splitter)
        self.left_group.setObjectName(u"left_group")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.left_group.sizePolicy().hasHeightForWidth())
        self.left_group.setSizePolicy(sizePolicy1)
        self.left_group.setAutoFillBackground(False)
        self.left_group.setStyleSheet(u"QPushButton { text-align: left }")
        self.left_group.setFlat(True)
        self.gridLayout_18 = QGridLayout(self.left_group)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(0, 0, 0, 0)
        self.label_browser_table = QTableWidget(self.left_group)
        if (self.label_browser_table.columnCount() < 2):
            self.label_browser_table.setColumnCount(2)
        if (self.label_browser_table.rowCount() < 20):
            self.label_browser_table.setRowCount(20)
        self.label_browser_table.setObjectName(u"label_browser_table")
        self.label_browser_table.setEnabled(False)
        sizePolicy.setHeightForWidth(self.label_browser_table.sizePolicy().hasHeightForWidth())
        self.label_browser_table.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Helvetica Neue"])
        self.label_browser_table.setFont(font)
        self.label_browser_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.label_browser_table.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.label_browser_table.setProperty("showDropIndicator", False)
        self.label_browser_table.setDragEnabled(False)
        self.label_browser_table.setDragDropOverwriteMode(False)
        self.label_browser_table.setAlternatingRowColors(True)
        self.label_browser_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.label_browser_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.label_browser_table.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.label_browser_table.setGridStyle(Qt.SolidLine)
        self.label_browser_table.setSortingEnabled(False)
        self.label_browser_table.setWordWrap(True)
        self.label_browser_table.setCornerButtonEnabled(False)
        self.label_browser_table.setRowCount(20)
        self.label_browser_table.setColumnCount(2)
        self.label_browser_table.horizontalHeader().setCascadingSectionResizes(True)
        self.label_browser_table.horizontalHeader().setMinimumSectionSize(50)
        self.label_browser_table.horizontalHeader().setDefaultSectionSize(100)
        self.label_browser_table.horizontalHeader().setProperty("showSortIndicator", False)
        self.label_browser_table.horizontalHeader().setStretchLastSection(False)
        self.label_browser_table.verticalHeader().setMinimumSectionSize(20)
        self.label_browser_table.verticalHeader().setProperty("showSortIndicator", False)

        self.gridLayout_18.addWidget(self.label_browser_table, 10, 0, 1, 1, Qt.AlignLeft)

        self.select_all_check = QCheckBox(self.left_group)
        self.select_all_check.setObjectName(u"select_all_check")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.select_all_check.sizePolicy().hasHeightForWidth())
        self.select_all_check.setSizePolicy(sizePolicy2)
        self.select_all_check.setFont(font)
        self.select_all_check.setMouseTracking(True)

        self.gridLayout_18.addWidget(self.select_all_check, 8, 0, 1, 1)

        self.explore_button = QPushButton(self.left_group)
        self.explore_button.setObjectName(u"explore_button")
        self.explore_button.setEnabled(False)
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.explore_button.sizePolicy().hasHeightForWidth())
        self.explore_button.setSizePolicy(sizePolicy3)
        font1 = QFont()
        font1.setFamilies([u"Helvetica Neue"])
        font1.setPointSize(14)
        font1.setBold(True)
        self.explore_button.setFont(font1)
        self.explore_button.setCursor(QCursor(Qt.ArrowCursor))
        self.explore_button.setMouseTracking(True)
        icon = QIcon()
        icon.addFile(u":/resources/icons/grey_view.png", QSize(), QIcon.Normal, QIcon.Off)
        self.explore_button.setIcon(icon)
        self.explore_button.setAutoDefault(False)
        self.explore_button.setFlat(True)

        self.gridLayout_18.addWidget(self.explore_button, 4, 0, 1, 1)

        self.load_quantity_button = QPushButton(self.left_group)
        self.load_quantity_button.setObjectName(u"load_quantity_button")
        sizePolicy3.setHeightForWidth(self.load_quantity_button.sizePolicy().hasHeightForWidth())
        self.load_quantity_button.setSizePolicy(sizePolicy3)
        self.load_quantity_button.setFont(font1)
        self.load_quantity_button.setMouseTracking(True)
        icon1 = QIcon()
        iconThemeName = u"document-open"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u":/resources/icons/grey_quantity.png", QSize(), QIcon.Normal, QIcon.On)

        self.load_quantity_button.setIcon(icon1)
        self.load_quantity_button.setFlat(True)

        self.gridLayout_18.addWidget(self.load_quantity_button, 3, 0, 1, 1)

        self.settings_button = QPushButton(self.left_group)
        self.settings_button.setObjectName(u"settings_button")
        self.settings_button.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.settings_button.sizePolicy().hasHeightForWidth())
        self.settings_button.setSizePolicy(sizePolicy3)
        self.settings_button.setFont(font1)
        self.settings_button.setCursor(QCursor(Qt.ArrowCursor))
        icon2 = QIcon()
        iconThemeName = u"preferences-system"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u":/resources/icons/grey_settings.png", QSize(), QIcon.Normal, QIcon.On)

        self.settings_button.setIcon(icon2)
        self.settings_button.setFlat(True)

        self.gridLayout_18.addWidget(self.settings_button, 11, 0, 1, 1)

        self.print_button = QPushButton(self.left_group)
        self.print_button.setObjectName(u"print_button")
        sizePolicy3.setHeightForWidth(self.print_button.sizePolicy().hasHeightForWidth())
        self.print_button.setSizePolicy(sizePolicy3)
        self.print_button.setFont(font1)
        self.print_button.setCursor(QCursor(Qt.ArrowCursor))
        self.print_button.setMouseTracking(True)
        self.print_button.setLayoutDirection(Qt.LeftToRight)
        icon3 = QIcon()
        iconThemeName = u"printer"
        if QIcon.hasThemeIcon(iconThemeName):
            icon3 = QIcon.fromTheme(iconThemeName)
        else:
            icon3.addFile(u":/resources/icons/grey_print.png", QSize(), QIcon.Normal, QIcon.Off)

        self.print_button.setIcon(icon3)
        self.print_button.setFlat(True)

        self.gridLayout_18.addWidget(self.print_button, 0, 0, 1, 1)

        self.load_labels_button = QPushButton(self.left_group)
        self.load_labels_button.setObjectName(u"load_labels_button")
        sizePolicy3.setHeightForWidth(self.load_labels_button.sizePolicy().hasHeightForWidth())
        self.load_labels_button.setSizePolicy(sizePolicy3)
        self.load_labels_button.setFont(font1)
        self.load_labels_button.setCursor(QCursor(Qt.ArrowCursor))
        self.load_labels_button.setMouseTracking(True)
        self.load_labels_button.setStyleSheet(u"")
        icon4 = QIcon()
        iconThemeName = u"document-open"
        if QIcon.hasThemeIcon(iconThemeName):
            icon4 = QIcon.fromTheme(iconThemeName)
        else:
            icon4.addFile(u":/resources/icons/grey_label.png", QSize(), QIcon.Normal, QIcon.On)

        self.load_labels_button.setIcon(icon4)
        self.load_labels_button.setFlat(True)

        self.gridLayout_18.addWidget(self.load_labels_button, 2, 0, 1, 1)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.search_bar = QLineEdit(self.left_group)
        self.search_bar.setObjectName(u"search_bar")
        self.search_bar.setFont(font)

        self.gridLayout_6.addWidget(self.search_bar, 1, 1, 1, 1)

        self.search_bar_button = QPushButton(self.left_group)
        self.search_bar_button.setObjectName(u"search_bar_button")
        font2 = QFont()
        font2.setFamilies([u"Helvetica Neue"])
        font2.setBold(False)
        self.search_bar_button.setFont(font2)

        self.gridLayout_6.addWidget(self.search_bar_button, 1, 2, 1, 1)


        self.gridLayout_18.addLayout(self.gridLayout_6, 5, 0, 1, 1)

        self.splitter.addWidget(self.left_group)
        self.main_group = QGroupBox(self.splitter)
        self.main_group.setObjectName(u"main_group")
        sizePolicy1.setHeightForWidth(self.main_group.sizePolicy().hasHeightForWidth())
        self.main_group.setSizePolicy(sizePolicy1)
        self.main_group.setFlat(True)
        self.main_grid_layout = QGridLayout(self.main_group)
        self.main_grid_layout.setObjectName(u"main_grid_layout")
        self.main_grid_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.main_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.preview_grid = QGridLayout()
        self.preview_grid.setObjectName(u"preview_grid")
        self.preview_grid.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.ToolFrame = QFrame(self.main_group)
        self.ToolFrame.setObjectName(u"ToolFrame")
        sizePolicy2.setHeightForWidth(self.ToolFrame.sizePolicy().hasHeightForWidth())
        self.ToolFrame.setSizePolicy(sizePolicy2)
        self.ToolFrame.setFont(font)
        self.ToolFrame.setFrameShape(QFrame.StyledPanel)
        self.ToolFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.ToolFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.save_pdf_button = QPushButton(self.ToolFrame)
        self.save_pdf_button.setObjectName(u"save_pdf_button")
        self.save_pdf_button.setEnabled(False)
        sizePolicy4 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.save_pdf_button.sizePolicy().hasHeightForWidth())
        self.save_pdf_button.setSizePolicy(sizePolicy4)
        icon5 = QIcon()
        iconThemeName = u"document-save-as"
        if QIcon.hasThemeIcon(iconThemeName):
            icon5 = QIcon.fromTheme(iconThemeName)
        else:
            icon5.addFile(u":/resources/icons/grey_save_pdf.png", QSize(), QIcon.Normal, QIcon.On)

        self.save_pdf_button.setIcon(icon5)
        self.save_pdf_button.setIconSize(QSize(20, 20))
        self.save_pdf_button.setAutoDefault(False)
        self.save_pdf_button.setFlat(True)

        self.gridLayout.addWidget(self.save_pdf_button, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 4, 1, 1)

        self.refresh_button = QPushButton(self.ToolFrame)
        self.refresh_button.setObjectName(u"refresh_button")
        self.refresh_button.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.refresh_button.sizePolicy().hasHeightForWidth())
        self.refresh_button.setSizePolicy(sizePolicy4)
        icon6 = QIcon()
        iconThemeName = u"view-refresh"
        if QIcon.hasThemeIcon(iconThemeName):
            icon6 = QIcon.fromTheme(iconThemeName)
        else:
            icon6.addFile(u":/resources/icons/grey_refresh.png", QSize(), QIcon.Normal, QIcon.On)

        self.refresh_button.setIcon(icon6)
        self.refresh_button.setIconSize(QSize(20, 20))
        self.refresh_button.setFlat(True)

        self.gridLayout.addWidget(self.refresh_button, 0, 2, 1, 1)

        self.save_zpl_button = QPushButton(self.ToolFrame)
        self.save_zpl_button.setObjectName(u"save_zpl_button")
        self.save_zpl_button.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.save_zpl_button.sizePolicy().hasHeightForWidth())
        self.save_zpl_button.setSizePolicy(sizePolicy4)
        icon7 = QIcon()
        icon7.addFile(u":/resources/icons/grey_zpl.png", QSize(), QIcon.Normal, QIcon.Off)
        self.save_zpl_button.setIcon(icon7)
        self.save_zpl_button.setIconSize(QSize(20, 20))
        self.save_zpl_button.setFlat(True)

        self.gridLayout.addWidget(self.save_zpl_button, 0, 3, 1, 1)

        self.search_button = QPushButton(self.ToolFrame)
        self.search_button.setObjectName(u"search_button")
        self.search_button.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.search_button.sizePolicy().hasHeightForWidth())
        self.search_button.setSizePolicy(sizePolicy4)
        icon8 = QIcon()
        iconThemeName = u"system-search"
        if QIcon.hasThemeIcon(iconThemeName):
            icon8 = QIcon.fromTheme(iconThemeName)
        else:
            icon8.addFile(u":/resources/icons/grey_search.png", QSize(), QIcon.Normal, QIcon.On)

        self.search_button.setIcon(icon8)
        self.search_button.setIconSize(QSize(20, 20))
        self.search_button.setFlat(True)

        self.gridLayout.addWidget(self.search_button, 0, 0, 1, 1)


        self.preview_grid.addWidget(self.ToolFrame, 0, 0, 1, 1)

        self.preview_display = QGraphicsView(self.main_group)
        self.preview_display.setObjectName(u"preview_display")
        self.preview_display.setEnabled(True)
        self.preview_display.setBaseSize(QSize(0, 0))
        self.preview_display.setFont(font)

        self.preview_grid.addWidget(self.preview_display, 1, 0, 1, 1)


        self.main_grid_layout.addLayout(self.preview_grid, 0, 1, 1, 1)

        self.element_browser = QTableWidget(self.main_group)
        if (self.element_browser.rowCount() < 4):
            self.element_browser.setRowCount(4)
        self.element_browser.setObjectName(u"element_browser")
        sizePolicy1.setHeightForWidth(self.element_browser.sizePolicy().hasHeightForWidth())
        self.element_browser.setSizePolicy(sizePolicy1)
        self.element_browser.setFont(font)
        self.element_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.element_browser.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.element_browser.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.element_browser.setDragEnabled(False)
        self.element_browser.setDragDropOverwriteMode(False)
        self.element_browser.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.element_browser.setDefaultDropAction(Qt.IgnoreAction)
        self.element_browser.setAlternatingRowColors(True)
        self.element_browser.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.element_browser.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.element_browser.setTextElideMode(Qt.ElideRight)
        self.element_browser.setSortingEnabled(True)
        self.element_browser.setWordWrap(False)
        self.element_browser.setRowCount(4)
        self.element_browser.setColumnCount(0)
        self.element_browser.horizontalHeader().setVisible(True)
        self.element_browser.horizontalHeader().setCascadingSectionResizes(True)
        self.element_browser.horizontalHeader().setMinimumSectionSize(50)
        self.element_browser.horizontalHeader().setDefaultSectionSize(150)
        self.element_browser.horizontalHeader().setProperty("showSortIndicator", True)
        self.element_browser.horizontalHeader().setStretchLastSection(False)
        self.element_browser.verticalHeader().setMinimumSectionSize(20)
        self.element_browser.verticalHeader().setProperty("showSortIndicator", False)

        self.main_grid_layout.addWidget(self.element_browser, 1, 1, 1, 1)

        self.main_grid_layout.setRowStretch(0, 3)
        self.main_grid_layout.setRowStretch(1, 1)
        self.splitter.addWidget(self.main_group)

        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.master_group, 0, 0, 1, 1)

        Flabel.setCentralWidget(self.centralwidget)

        self.retranslateUi(Flabel)

        QMetaObject.connectSlotsByName(Flabel)
    # setupUi

    def retranslateUi(self, Flabel):
        Flabel.setWindowTitle(QCoreApplication.translate("Flabel", u"Flabel", None))
        self.actionAbout_Flabel.setText(QCoreApplication.translate("Flabel", u"About Flabel", None))
        self.actionPrint.setText(QCoreApplication.translate("Flabel", u"Print", None))
        self.master_group.setTitle("")
        self.left_group.setTitle("")
        self.select_all_check.setText(QCoreApplication.translate("Flabel", u"Select All", None))
        self.explore_button.setText(QCoreApplication.translate("Flabel", u"   Explore", None))
        self.load_quantity_button.setText(QCoreApplication.translate("Flabel", u"   Load Quantity", None))
        self.settings_button.setText(QCoreApplication.translate("Flabel", u"   Settings     ", None))
        self.print_button.setText(QCoreApplication.translate("Flabel", u"   Print        ", None))
        self.load_labels_button.setText(QCoreApplication.translate("Flabel", u"   Load Labels", None))
        self.search_bar.setPlaceholderText(QCoreApplication.translate("Flabel", u"Search...", None))
        self.search_bar_button.setText(QCoreApplication.translate("Flabel", u"Search", None))
        self.refresh_button.setText("")
        self.search_button.setText("")
    # retranslateUi

