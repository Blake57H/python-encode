# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'source_loading_overlay.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_SourceLoadingForm(object):
    def setupUi(self, SourceLoadingForm):
        if not SourceLoadingForm.objectName():
            SourceLoadingForm.setObjectName(u"SourceLoadingForm")
        SourceLoadingForm.resize(400, 169)
        SourceLoadingForm.setMinimumSize(QSize(400, 169))
        SourceLoadingForm.setLayoutDirection(Qt.LeftToRight)
        self.verticalLayout = QVBoxLayout(SourceLoadingForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.label_currentItem = QLabel(SourceLoadingForm)
        self.label_currentItem.setObjectName(u"label_currentItem")
        self.label_currentItem.setAlignment(Qt.AlignCenter)
        self.label_currentItem.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_currentItem)

        self.progressBar_currentItem = QProgressBar(SourceLoadingForm)
        self.progressBar_currentItem.setObjectName(u"progressBar_currentItem")
        self.progressBar_currentItem.setValue(24)

        self.verticalLayout.addWidget(self.progressBar_currentItem)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.widget = QWidget(SourceLoadingForm)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_cancel = QPushButton(self.widget)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout.addWidget(self.pushButton_cancel)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(SourceLoadingForm)

        QMetaObject.connectSlotsByName(SourceLoadingForm)
    # setupUi

    def retranslateUi(self, SourceLoadingForm):
        SourceLoadingForm.setWindowTitle(QCoreApplication.translate("SourceLoadingForm", u"Form", None))
        self.label_currentItem.setText(QCoreApplication.translate("SourceLoadingForm", u"Loading [SubsPlease] Rikei ga Koi ni Ochita no de Shoumei shitemita S2 (01-12) (1080p) [Batch] (1/24)", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("SourceLoadingForm", u"Cancel", None))
    # retranslateUi

