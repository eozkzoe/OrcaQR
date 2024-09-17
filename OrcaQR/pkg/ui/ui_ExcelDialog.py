# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ExcelDialogrDulua.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QCheckBox,
    QComboBox, QDialog, QDialogButtonBox, QFormLayout,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QRadioButton, QSizePolicy,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_ExcelDialog(object):
    def setupUi(self, ExcelDialog):
        if not ExcelDialog.objectName():
            ExcelDialog.setObjectName(u"ExcelDialog")
        ExcelDialog.resize(479, 700)
        self.gridLayout = QGridLayout(ExcelDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.filename_label = QLabel(ExcelDialog)
        self.filename_label.setObjectName(u"filename_label")
        font = QFont()
        font.setFamilies([u"Helvetica Neue"])
        font.setBold(True)
        self.filename_label.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.filename_label)

        self.file_chosen_label = QLabel(ExcelDialog)
        self.file_chosen_label.setObjectName(u"file_chosen_label")
        self.file_chosen_label.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.file_chosen_label)

        self.select_worksheet_label = QLabel(ExcelDialog)
        self.select_worksheet_label.setObjectName(u"select_worksheet_label")
        font1 = QFont()
        font1.setFamilies([u"Helvetica Neue"])
        self.select_worksheet_label.setFont(font1)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.select_worksheet_label)

        self.select_worksheet_combobox = QComboBox(ExcelDialog)
        self.select_worksheet_combobox.setObjectName(u"select_worksheet_combobox")
        self.select_worksheet_combobox.setFont(font1)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.select_worksheet_combobox)

        self.show_columns_label = QLabel(ExcelDialog)
        self.show_columns_label.setObjectName(u"show_columns_label")
        self.show_columns_label.setFont(font1)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.show_columns_label)

        self.show_columns_list = QListWidget(ExcelDialog)
        self.show_columns_list.setObjectName(u"show_columns_list")
        self.show_columns_list.setFont(font1)
        self.show_columns_list.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.show_columns_list)

        self.label_size_label = QLabel(ExcelDialog)
        self.label_size_label.setObjectName(u"label_size_label")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_size_label)

        self.label_size_layout = QHBoxLayout()
        self.label_size_layout.setObjectName(u"label_size_layout")
        self.size_combobox = QComboBox(ExcelDialog)
        self.size_combobox.setObjectName(u"size_combobox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.size_combobox.sizePolicy().hasHeightForWidth())
        self.size_combobox.setSizePolicy(sizePolicy)
        self.size_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.size_combobox.setMinimumContentsLength(5)

        self.label_size_layout.addWidget(self.size_combobox)

        self.wxh_label = QLabel(ExcelDialog)
        self.wxh_label.setObjectName(u"wxh_label")

        self.label_size_layout.addWidget(self.wxh_label)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.label_size_layout)

        self.layout_options_label = QLabel(ExcelDialog)
        self.layout_options_label.setObjectName(u"layout_options_label")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.layout_options_label)

        self.label_data_label = QLabel(ExcelDialog)
        self.label_data_label.setObjectName(u"label_data_label")
        self.label_data_label.setFont(font1)

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_data_label)

        self.label_data_list = QListWidget(ExcelDialog)
        self.label_data_list.setObjectName(u"label_data_list")
        self.label_data_list.setFont(font1)
        self.label_data_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.label_data_list.setDragEnabled(True)
        self.label_data_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.label_data_list.setDefaultDropAction(Qt.MoveAction)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.label_data_list)

        self.label_rows_label = QLabel(ExcelDialog)
        self.label_rows_label.setObjectName(u"label_rows_label")
        self.label_rows_label.setFont(font1)

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_rows_label)

        self.label_rows_groupbox = QGroupBox(ExcelDialog)
        self.label_rows_groupbox.setObjectName(u"label_rows_groupbox")
        self.label_rows_groupbox.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_rows_groupbox.sizePolicy().hasHeightForWidth())
        self.label_rows_groupbox.setSizePolicy(sizePolicy1)
        self.horizontalLayout_3 = QHBoxLayout(self.label_rows_groupbox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.label_rows_v_layout = QVBoxLayout()
        self.label_rows_v_layout.setObjectName(u"label_rows_v_layout")

        self.horizontalLayout_3.addLayout(self.label_rows_v_layout)


        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.label_rows_groupbox)

        self.qr_data_label = QLabel(ExcelDialog)
        self.qr_data_label.setObjectName(u"qr_data_label")
        self.qr_data_label.setFont(font1)

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.qr_data_label)

        self.qr_data_list = QListWidget(ExcelDialog)
        self.qr_data_list.setObjectName(u"qr_data_list")
        self.qr_data_list.setFont(font1)
        self.qr_data_list.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.qr_data_list)

        self.layout_options_layout = QHBoxLayout()
        self.layout_options_layout.setSpacing(10)
        self.layout_options_layout.setObjectName(u"layout_options_layout")
        self.show_titles_checkbox = QCheckBox(ExcelDialog)
        self.show_titles_checkbox.setObjectName(u"show_titles_checkbox")

        self.layout_options_layout.addWidget(self.show_titles_checkbox, 0, Qt.AlignVCenter)

        self.alignment_groupbox = QGroupBox(ExcelDialog)
        self.alignment_groupbox.setObjectName(u"alignment_groupbox")
        self.alignment_layout = QHBoxLayout(self.alignment_groupbox)
        self.alignment_layout.setSpacing(10)
        self.alignment_layout.setObjectName(u"alignment_layout")
        self.alignment_layout.setContentsMargins(5, 0, 0, 0)
        self.left_align_button = QRadioButton(self.alignment_groupbox)
        self.left_align_button.setObjectName(u"left_align_button")
        icon = QIcon()
        iconThemeName = u"document-properties"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u":/resources/icons/grey_left_align.png", QSize(), QIcon.Normal, QIcon.On)

        self.left_align_button.setIcon(icon)
        self.left_align_button.setCheckable(True)
        self.left_align_button.setChecked(True)

        self.alignment_layout.addWidget(self.left_align_button)

        self.center_align_button = QRadioButton(self.alignment_groupbox)
        self.center_align_button.setObjectName(u"center_align_button")
        icon1 = QIcon()
        iconThemeName = u"document-properties"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u":/resources/icons/grey_center_align.png", QSize(), QIcon.Normal, QIcon.On)

        self.center_align_button.setIcon(icon1)

        self.alignment_layout.addWidget(self.center_align_button)

        self.right_align_button = QRadioButton(self.alignment_groupbox)
        self.right_align_button.setObjectName(u"right_align_button")
        icon2 = QIcon()
        iconThemeName = u"document-properties"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u":/resources/icons/grey_right_align.png", QSize(), QIcon.Normal, QIcon.On)

        self.right_align_button.setIcon(icon2)
        self.right_align_button.setIconSize(QSize(16, 16))

        self.alignment_layout.addWidget(self.right_align_button)


        self.layout_options_layout.addWidget(self.alignment_groupbox)


        self.formLayout.setLayout(6, QFormLayout.FieldRole, self.layout_options_layout)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(ExcelDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(ExcelDialog)
        self.buttonBox.accepted.connect(ExcelDialog.accept)
        self.buttonBox.rejected.connect(ExcelDialog.reject)

        QMetaObject.connectSlotsByName(ExcelDialog)
    # setupUi

    def retranslateUi(self, ExcelDialog):
        ExcelDialog.setWindowTitle(QCoreApplication.translate("ExcelDialog", u"Excel Settings", None))
        self.filename_label.setText(QCoreApplication.translate("ExcelDialog", u"Filename", None))
        self.file_chosen_label.setText(QCoreApplication.translate("ExcelDialog", u"-", None))
        self.select_worksheet_label.setText(QCoreApplication.translate("ExcelDialog", u"Select Worksheet", None))
        self.show_columns_label.setText(QCoreApplication.translate("ExcelDialog", u"Show columns", None))
        self.label_size_label.setText(QCoreApplication.translate("ExcelDialog", u"Label Size (Height x Width)", None))
        self.wxh_label.setText(QCoreApplication.translate("ExcelDialog", u"(Width x Height)", None))
        self.layout_options_label.setText(QCoreApplication.translate("ExcelDialog", u"Layout Options", None))
        self.label_data_label.setText(QCoreApplication.translate("ExcelDialog", u"Label Data", None))
        self.label_rows_label.setText(QCoreApplication.translate("ExcelDialog", u"Label Rows", None))
        self.label_rows_groupbox.setTitle("")
        self.qr_data_label.setText(QCoreApplication.translate("ExcelDialog", u"QR Data", None))
        self.show_titles_checkbox.setText(QCoreApplication.translate("ExcelDialog", u"Show Titles", None))
        self.alignment_groupbox.setTitle("")
        self.left_align_button.setText("")
        self.center_align_button.setText("")
        self.right_align_button.setText("")
    # retranslateUi

