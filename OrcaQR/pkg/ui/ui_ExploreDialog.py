# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ExploreDialogWXzpWU.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QGridLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QWidget)

class Ui_ExploreDialog(object):
    def setupUi(self, ExploreDialog):
        if not ExploreDialog.objectName():
            ExploreDialog.setObjectName(u"ExploreDialog")
        ExploreDialog.resize(459, 405)
        self.gridLayout = QGridLayout(ExploreDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.cancel_box = QDialogButtonBox(ExploreDialog)
        self.cancel_box.setObjectName(u"cancel_box")
        font = QFont()
        font.setFamilies([u"Helvetica Neue"])
        self.cancel_box.setFont(font)
        self.cancel_box.setOrientation(Qt.Horizontal)
        self.cancel_box.setStandardButtons(QDialogButtonBox.Cancel)

        self.gridLayout_2.addWidget(self.cancel_box, 0, 0, 1, 1)

        self.view_button = QPushButton(ExploreDialog)
        self.view_button.setObjectName(u"view_button")
        self.view_button.setFont(font)

        self.gridLayout_2.addWidget(self.view_button, 0, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 4, 0, 1, 1)

        self.detected_list = QListWidget(ExploreDialog)
        self.detected_list.setObjectName(u"detected_list")
        font1 = QFont()
        font1.setFamilies([u"Helvetica Neue"])
        font1.setPointSize(13)
        self.detected_list.setFont(font1)
        self.detected_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.detected_list.setSelectionRectVisible(True)
        self.detected_list.setSortingEnabled(True)

        self.gridLayout.addWidget(self.detected_list, 3, 0, 1, 1)

        self.category_list = QListWidget(ExploreDialog)
        self.category_list.setObjectName(u"category_list")
        self.category_list.setFont(font1)
        self.category_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.category_list.setSelectionRectVisible(True)

        self.gridLayout.addWidget(self.category_list, 1, 0, 1, 1)

        self.avail_options_label = QLabel(ExploreDialog)
        self.avail_options_label.setObjectName(u"avail_options_label")
        font2 = QFont()
        font2.setFamilies([u"Helvetica Neue"])
        font2.setBold(True)
        self.avail_options_label.setFont(font2)

        self.gridLayout.addWidget(self.avail_options_label, 0, 0, 1, 1)

        self.detected_options_label = QLabel(ExploreDialog)
        self.detected_options_label.setObjectName(u"detected_options_label")
        self.detected_options_label.setFont(font2)

        self.gridLayout.addWidget(self.detected_options_label, 2, 0, 1, 1)


        self.retranslateUi(ExploreDialog)
        self.cancel_box.accepted.connect(ExploreDialog.accept)
        self.cancel_box.rejected.connect(ExploreDialog.reject)

        QMetaObject.connectSlotsByName(ExploreDialog)
    # setupUi

    def retranslateUi(self, ExploreDialog):
        ExploreDialog.setWindowTitle(QCoreApplication.translate("ExploreDialog", u"Explorer", None))
        self.view_button.setText(QCoreApplication.translate("ExploreDialog", u"View", None))
        self.avail_options_label.setText(QCoreApplication.translate("ExploreDialog", u"Select Category", None))
        self.detected_options_label.setText(QCoreApplication.translate("ExploreDialog", u"Detected Options", None))
    # retranslateUi

