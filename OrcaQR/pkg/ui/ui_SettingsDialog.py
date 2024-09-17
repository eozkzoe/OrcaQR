# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsDialogqKISeD.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QAbstractScrollArea, QApplication,
    QCheckBox, QComboBox, QDialog, QDialogButtonBox,
    QFormLayout, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QRadioButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)
import resources_rc

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(558, 778)
        self.verticalLayout = QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(SettingsDialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -172, 519, 883))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_settings_group = QGroupBox(self.scrollAreaWidgetContents)
        self.label_settings_group.setObjectName(u"label_settings_group")
        font = QFont()
        font.setFamilies([u"Helvetica Neue"])
        font.setBold(True)
        self.label_settings_group.setFont(font)
        self.formLayout = QFormLayout(self.label_settings_group)
        self.formLayout.setObjectName(u"formLayout")
        self.units_label = QLabel(self.label_settings_group)
        self.units_label.setObjectName(u"units_label")
        font1 = QFont()
        font1.setFamilies([u"Helvetica Neue"])
        font1.setBold(False)
        self.units_label.setFont(font1)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.units_label)

        self.units_combobox = QComboBox(self.label_settings_group)
        self.units_combobox.setObjectName(u"units_combobox")
        self.units_combobox.setEnabled(False)
        self.units_combobox.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.units_combobox)

        self.resolution_label = QLabel(self.label_settings_group)
        self.resolution_label.setObjectName(u"resolution_label")
        self.resolution_label.setFont(font1)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.resolution_label)

        self.resolution_combobox = QComboBox(self.label_settings_group)
        self.resolution_combobox.setObjectName(u"resolution_combobox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resolution_combobox.sizePolicy().hasHeightForWidth())
        self.resolution_combobox.setSizePolicy(sizePolicy)
        self.resolution_combobox.setFont(font)
        self.resolution_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.resolution_combobox.setMinimumContentsLength(5)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.resolution_combobox)

        self.size_label = QLabel(self.label_settings_group)
        self.size_label.setObjectName(u"size_label")
        self.size_label.setFont(font1)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.size_label)

        self.label_size_layout = QHBoxLayout()
        self.label_size_layout.setObjectName(u"label_size_layout")
        self.size_combobox = QComboBox(self.label_settings_group)
        self.size_combobox.setObjectName(u"size_combobox")
        sizePolicy.setHeightForWidth(self.size_combobox.sizePolicy().hasHeightForWidth())
        self.size_combobox.setSizePolicy(sizePolicy)
        self.size_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.size_combobox.setMinimumContentsLength(8)

        self.label_size_layout.addWidget(self.size_combobox)

        self.wxh_label = QLabel(self.label_settings_group)
        self.wxh_label.setObjectName(u"wxh_label")
        self.wxh_label.setFont(font1)

        self.label_size_layout.addWidget(self.wxh_label)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.label_size_layout)

        self.label_data_label = QLabel(self.label_settings_group)
        self.label_data_label.setObjectName(u"label_data_label")
        self.label_data_label.setFont(font1)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_data_label)

        self.label_data_list = QListWidget(self.label_settings_group)
        self.label_data_list.setObjectName(u"label_data_list")
        self.label_data_list.setMinimumSize(QSize(0, 100))
        self.label_data_list.setFont(font)
        self.label_data_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.label_data_list.setDragEnabled(True)
        self.label_data_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.label_data_list.setDefaultDropAction(Qt.MoveAction)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.label_data_list)

        self.label_rows_label = QLabel(self.label_settings_group)
        self.label_rows_label.setObjectName(u"label_rows_label")
        self.label_rows_label.setFont(font1)

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_rows_label)

        self.label_rows_groupbox = QGroupBox(self.label_settings_group)
        self.label_rows_groupbox.setObjectName(u"label_rows_groupbox")
        self.label_rows_groupbox.setFlat(False)
        self.horizontalLayout_3 = QHBoxLayout(self.label_rows_groupbox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.label_rows_v_layout = QVBoxLayout()
        self.label_rows_v_layout.setObjectName(u"label_rows_v_layout")

        self.horizontalLayout_3.addLayout(self.label_rows_v_layout)


        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.label_rows_groupbox)

        self.qr_data_label = QLabel(self.label_settings_group)
        self.qr_data_label.setObjectName(u"qr_data_label")
        self.qr_data_label.setFont(font1)

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.qr_data_label)

        self.qr_data_list = QListWidget(self.label_settings_group)
        self.qr_data_list.setObjectName(u"qr_data_list")
        self.qr_data_list.setMinimumSize(QSize(0, 100))
        self.qr_data_list.setFont(font)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.qr_data_list)

        self.permitted_characters_label = QLabel(self.label_settings_group)
        self.permitted_characters_label.setObjectName(u"permitted_characters_label")
        self.permitted_characters_label.setFont(font1)

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.permitted_characters_label)

        self.permitted_characters_list = QListWidget(self.label_settings_group)
        self.permitted_characters_list.setObjectName(u"permitted_characters_list")
        self.permitted_characters_list.setMinimumSize(QSize(0, 100))
        self.permitted_characters_list.setFont(font)

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.permitted_characters_list)

        self.layout_options_layout = QHBoxLayout()
        self.layout_options_layout.setSpacing(10)
        self.layout_options_layout.setObjectName(u"layout_options_layout")
        self.show_titles_checkbox = QCheckBox(self.label_settings_group)
        self.show_titles_checkbox.setObjectName(u"show_titles_checkbox")
        self.show_titles_checkbox.setFont(font1)

        self.layout_options_layout.addWidget(self.show_titles_checkbox, 0, Qt.AlignVCenter)

        self.alignment_groupbox = QGroupBox(self.label_settings_group)
        self.alignment_groupbox.setObjectName(u"alignment_groupbox")
        self.alignment_layout = QHBoxLayout(self.alignment_groupbox)
        self.alignment_layout.setSpacing(10)
        self.alignment_layout.setObjectName(u"alignment_layout")
        self.alignment_layout.setContentsMargins(5, 0, 0, 0)
        self.left_align_button = QRadioButton(self.alignment_groupbox)
        self.left_align_button.setObjectName(u"left_align_button")
        font2 = QFont()
        font2.setFamilies([u"Helvetica Neue"])
        font2.setBold(False)
        font2.setKerning(True)
        self.left_align_button.setFont(font2)
        self.left_align_button.setMouseTracking(True)
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
        self.center_align_button.setFont(font1)
        self.center_align_button.setMouseTracking(True)
        icon1 = QIcon()
        iconThemeName = u"document-properties"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u":/resources/icons/grey_center_align.png", QSize(), QIcon.Normal, QIcon.On)

        self.center_align_button.setIcon(icon1)
        self.center_align_button.setCheckable(True)

        self.alignment_layout.addWidget(self.center_align_button)

        self.right_align_button = QRadioButton(self.alignment_groupbox)
        self.right_align_button.setObjectName(u"right_align_button")
        self.right_align_button.setFont(font1)
        self.right_align_button.setMouseTracking(True)
        icon2 = QIcon()
        iconThemeName = u"document-properties"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u":/resources/icons/grey_right_align.png", QSize(), QIcon.Normal, QIcon.On)

        self.right_align_button.setIcon(icon2)
        self.right_align_button.setCheckable(True)

        self.alignment_layout.addWidget(self.right_align_button)


        self.layout_options_layout.addWidget(self.alignment_groupbox)


        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.layout_options_layout)

        self.show_titles_label = QLabel(self.label_settings_group)
        self.show_titles_label.setObjectName(u"show_titles_label")
        self.show_titles_label.setFont(font1)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.show_titles_label)


        self.gridLayout_4.addWidget(self.label_settings_group, 1, 0, 1, 1)

        self.general_settings_group = QGroupBox(self.scrollAreaWidgetContents)
        self.general_settings_group.setObjectName(u"general_settings_group")
        self.general_settings_group.setMinimumSize(QSize(0, 250))
        self.general_settings_group.setFont(font)
        self.formLayout_2 = QFormLayout(self.general_settings_group)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.dark_mode_label = QLabel(self.general_settings_group)
        self.dark_mode_label.setObjectName(u"dark_mode_label")
        self.dark_mode_label.setFont(font1)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.dark_mode_label)

        self.dark_mode_checkbox = QCheckBox(self.general_settings_group)
        self.dark_mode_checkbox.setObjectName(u"dark_mode_checkbox")
        self.dark_mode_checkbox.setEnabled(False)
        self.dark_mode_checkbox.setChecked(True)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.dark_mode_checkbox)

        self.language_label = QLabel(self.general_settings_group)
        self.language_label.setObjectName(u"language_label")
        self.language_label.setFont(font1)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.language_label)

        self.language_combobox = QComboBox(self.general_settings_group)
        self.language_combobox.setObjectName(u"language_combobox")
        self.language_combobox.setEnabled(False)
        self.language_combobox.setFont(font)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.language_combobox)

        self.working_dir_label = QLabel(self.general_settings_group)
        self.working_dir_label.setObjectName(u"working_dir_label")
        self.working_dir_label.setFont(font1)

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.working_dir_label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.working_dir_edit = QLineEdit(self.general_settings_group)
        self.working_dir_edit.setObjectName(u"working_dir_edit")
        self.working_dir_edit.setFont(font)

        self.horizontalLayout.addWidget(self.working_dir_edit)

        self.search_dir_button = QPushButton(self.general_settings_group)
        self.search_dir_button.setObjectName(u"search_dir_button")
        self.search_dir_button.setFont(font)

        self.horizontalLayout.addWidget(self.search_dir_button)


        self.formLayout_2.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout)

        self.show_columns_label = QLabel(self.general_settings_group)
        self.show_columns_label.setObjectName(u"show_columns_label")
        self.show_columns_label.setFont(font1)

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.show_columns_label)

        self.show_columns_list = QListWidget(self.general_settings_group)
        self.show_columns_list.setObjectName(u"show_columns_list")
        self.show_columns_list.setMinimumSize(QSize(0, 100))
        self.show_columns_list.setFont(font)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.show_columns_list)


        self.gridLayout_4.addWidget(self.general_settings_group, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_4)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.save_settings_box = QDialogButtonBox(SettingsDialog)
        self.save_settings_box.setObjectName(u"save_settings_box")
        self.save_settings_box.setOrientation(Qt.Horizontal)
        self.save_settings_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.save_settings_box)

        self.copyright_label = QLabel(SettingsDialog)
        self.copyright_label.setObjectName(u"copyright_label")

        self.verticalLayout.addWidget(self.copyright_label)


        self.retranslateUi(SettingsDialog)
        self.save_settings_box.accepted.connect(SettingsDialog.accept)
        self.save_settings_box.rejected.connect(SettingsDialog.reject)

        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Settings", None))
        self.label_settings_group.setTitle(QCoreApplication.translate("SettingsDialog", u"Label settings", None))
        self.units_label.setText(QCoreApplication.translate("SettingsDialog", u"Units", None))
        self.resolution_label.setText(QCoreApplication.translate("SettingsDialog", u"Label Resolution (DPI)", None))
        self.resolution_combobox.setCurrentText("")
        self.size_label.setText(QCoreApplication.translate("SettingsDialog", u"Label Size", None))
        self.wxh_label.setText(QCoreApplication.translate("SettingsDialog", u"(Width x Height)", None))
        self.label_data_label.setText(QCoreApplication.translate("SettingsDialog", u"Label Data", None))
        self.label_rows_label.setText(QCoreApplication.translate("SettingsDialog", u"Label Rows", None))
        self.label_rows_groupbox.setTitle("")
        self.qr_data_label.setText(QCoreApplication.translate("SettingsDialog", u"QR Data", None))
        self.permitted_characters_label.setText(QCoreApplication.translate("SettingsDialog", u"Permitted characters", None))
        self.show_titles_checkbox.setText(QCoreApplication.translate("SettingsDialog", u"Show Titles", None))
        self.alignment_groupbox.setTitle("")
        self.left_align_button.setText("")
        self.center_align_button.setText("")
        self.right_align_button.setText("")
        self.show_titles_label.setText(QCoreApplication.translate("SettingsDialog", u"Layout Options", None))
        self.general_settings_group.setTitle(QCoreApplication.translate("SettingsDialog", u"General", None))
        self.dark_mode_label.setText(QCoreApplication.translate("SettingsDialog", u"Dark mode", None))
        self.dark_mode_checkbox.setText("")
        self.language_label.setText(QCoreApplication.translate("SettingsDialog", u"Language", None))
        self.working_dir_label.setText(QCoreApplication.translate("SettingsDialog", u"Working Directory", None))
        self.search_dir_button.setText(QCoreApplication.translate("SettingsDialog", u"Choose Folder", None))
        self.show_columns_label.setText(QCoreApplication.translate("SettingsDialog", u"Show Columns", None))
        self.copyright_label.setText(QCoreApplication.translate("SettingsDialog", u"\u00a9 2023 Fling Asia ", None))
    # retranslateUi

