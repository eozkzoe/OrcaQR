# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SearchDialogQDqisg.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QSpinBox, QWidget)

class Ui_SearchDialog(object):
    def setupUi(self, SearchDialog):
        if not SearchDialog.objectName():
            SearchDialog.setObjectName(u"SearchDialog")
        SearchDialog.resize(400, 249)
        SearchDialog.setModal(True)
        self.gridLayout = QGridLayout(SearchDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.starts_with_edit = QLineEdit(SearchDialog)
        self.starts_with_edit.setObjectName(u"starts_with_edit")
        self.starts_with_edit.setEnabled(False)
        font = QFont()
        font.setFamilies([u"Helvetica Neue"])
        self.starts_with_edit.setFont(font)

        self.gridLayout_3.addWidget(self.starts_with_edit, 1, 1, 1, 1)

        self.starts_with_label = QLabel(SearchDialog)
        self.starts_with_label.setObjectName(u"starts_with_label")
        self.starts_with_label.setFont(font)

        self.gridLayout_3.addWidget(self.starts_with_label, 1, 0, 1, 1)

        self.ends_with_label = QLabel(SearchDialog)
        self.ends_with_label.setObjectName(u"ends_with_label")
        self.ends_with_label.setFont(font)

        self.gridLayout_3.addWidget(self.ends_with_label, 1, 2, 1, 1)

        self.ends_with_edit = QLineEdit(SearchDialog)
        self.ends_with_edit.setObjectName(u"ends_with_edit")
        self.ends_with_edit.setEnabled(False)
        self.ends_with_edit.setFont(font)

        self.gridLayout_3.addWidget(self.ends_with_edit, 1, 3, 1, 1)

        self.matching_checkbox = QCheckBox(SearchDialog)
        self.matching_checkbox.setObjectName(u"matching_checkbox")
        self.matching_checkbox.setFont(font)

        self.gridLayout_3.addWidget(self.matching_checkbox, 0, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_3, 6, 1, 1, 1)

        self.specific_selection_layout = QGridLayout()
        self.specific_selection_layout.setObjectName(u"specific_selection_layout")
        self.specific_selection_label = QLabel(SearchDialog)
        self.specific_selection_label.setObjectName(u"specific_selection_label")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.specific_selection_label.sizePolicy().hasHeightForWidth())
        self.specific_selection_label.setSizePolicy(sizePolicy)
        self.specific_selection_label.setFont(font)

        self.specific_selection_layout.addWidget(self.specific_selection_label, 1, 0, 1, 1)

        self.specific_selection_edit = QLineEdit(SearchDialog)
        self.specific_selection_edit.setObjectName(u"specific_selection_edit")
        self.specific_selection_edit.setEnabled(False)
        self.specific_selection_edit.setFont(font)
        self.specific_selection_edit.setClearButtonEnabled(False)

        self.specific_selection_layout.addWidget(self.specific_selection_edit, 2, 0, 1, 1)

        self.specific_selection_check = QCheckBox(SearchDialog)
        self.specific_selection_check.setObjectName(u"specific_selection_check")
        self.specific_selection_check.setFont(font)
        self.specific_selection_check.setMouseTracking(True)

        self.specific_selection_layout.addWidget(self.specific_selection_check, 0, 0, 1, 1)


        self.gridLayout.addLayout(self.specific_selection_layout, 3, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 4, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(SearchDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 9, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.from_label = QLabel(SearchDialog)
        self.from_label.setObjectName(u"from_label")
        self.from_label.setFont(font)

        self.gridLayout_2.addWidget(self.from_label, 0, 0, 1, 1)

        self.to_label = QLabel(SearchDialog)
        self.to_label.setObjectName(u"to_label")
        self.to_label.setFont(font)

        self.gridLayout_2.addWidget(self.to_label, 0, 2, 1, 1)

        self.to_spin = QSpinBox(SearchDialog)
        self.to_spin.setObjectName(u"to_spin")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.to_spin.sizePolicy().hasHeightForWidth())
        self.to_spin.setSizePolicy(sizePolicy1)
        self.to_spin.setFont(font)
        self.to_spin.setMinimum(1)

        self.gridLayout_2.addWidget(self.to_spin, 0, 3, 1, 1)

        self.from_spin = QSpinBox(SearchDialog)
        self.from_spin.setObjectName(u"from_spin")
        sizePolicy1.setHeightForWidth(self.from_spin.sizePolicy().hasHeightForWidth())
        self.from_spin.setSizePolicy(sizePolicy1)
        self.from_spin.setFont(font)
        self.from_spin.setMinimum(1)

        self.gridLayout_2.addWidget(self.from_spin, 0, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 1, 1, 1, 1)


        self.retranslateUi(SearchDialog)
        self.buttonBox.accepted.connect(SearchDialog.accept)
        self.buttonBox.rejected.connect(SearchDialog.reject)

        QMetaObject.connectSlotsByName(SearchDialog)
    # setupUi

    def retranslateUi(self, SearchDialog):
        SearchDialog.setWindowTitle(QCoreApplication.translate("SearchDialog", u"Search Selection", None))
        self.starts_with_edit.setText("")
        self.starts_with_edit.setPlaceholderText(QCoreApplication.translate("SearchDialog", u"e.g. A01", None))
        self.starts_with_label.setText(QCoreApplication.translate("SearchDialog", u"Starts WIth", None))
        self.ends_with_label.setText(QCoreApplication.translate("SearchDialog", u"Ends With", None))
        self.ends_with_edit.setPlaceholderText(QCoreApplication.translate("SearchDialog", u"e.g. -30", None))
        self.matching_checkbox.setText(QCoreApplication.translate("SearchDialog", u"Matching", None))
        self.specific_selection_label.setText(QCoreApplication.translate("SearchDialog", u"Separate by dashes (-) and commas (,)", None))
        self.specific_selection_edit.setPlaceholderText(QCoreApplication.translate("SearchDialog", u"e.g. 12-15, 18, 19", None))
        self.specific_selection_check.setText(QCoreApplication.translate("SearchDialog", u"Specific Selection", None))
        self.from_label.setText(QCoreApplication.translate("SearchDialog", u"From", None))
        self.to_label.setText(QCoreApplication.translate("SearchDialog", u"To", None))
    # retranslateUi

