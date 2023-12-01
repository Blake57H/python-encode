# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app_settings_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QToolButton,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(442, 309)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.formLayout = QFormLayout(self.frame)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_ffmpegT = QLabel(self.frame)
        self.label_ffmpegT.setObjectName(u"label_ffmpegT")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_ffmpegT)

        self.label_ffmpegC = QLabel(self.frame)
        self.label_ffmpegC.setObjectName(u"label_ffmpegC")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ffmpegC.sizePolicy().hasHeightForWidth())
        self.label_ffmpegC.setSizePolicy(sizePolicy)
        self.label_ffmpegC.setStyleSheet(u"color: red")
        self.label_ffmpegC.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_ffmpegC.setWordWrap(True)
        self.label_ffmpegC.setIndent(0)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.label_ffmpegC)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout.setItem(1, QFormLayout.LabelRole, self.horizontalSpacer)

        self.label_ffprobeT = QLabel(self.frame)
        self.label_ffprobeT.setObjectName(u"label_ffprobeT")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_ffprobeT)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout.setItem(3, QFormLayout.LabelRole, self.horizontalSpacer_2)

        self.label_ffprobeC = QLabel(self.frame)
        self.label_ffprobeC.setObjectName(u"label_ffprobeC")
        sizePolicy.setHeightForWidth(self.label_ffprobeC.sizePolicy().hasHeightForWidth())
        self.label_ffprobeC.setSizePolicy(sizePolicy)
        self.label_ffprobeC.setStyleSheet(u"color: green;")
        self.label_ffprobeC.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_ffprobeC.setWordWrap(True)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.label_ffprobeC)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_ffmpegC = QLineEdit(self.frame_2)
        self.lineEdit_ffmpegC.setObjectName(u"lineEdit_ffmpegC")
        self.lineEdit_ffmpegC.setPlaceholderText(u"ffmpeg")

        self.horizontalLayout.addWidget(self.lineEdit_ffmpegC)

        self.toolButton_findFfmpeg = QToolButton(self.frame_2)
        self.toolButton_findFfmpeg.setObjectName(u"toolButton_findFfmpeg")

        self.horizontalLayout.addWidget(self.toolButton_findFfmpeg)

        self.pushButton_verifyFfmpeg = QPushButton(self.frame_2)
        self.pushButton_verifyFfmpeg.setObjectName(u"pushButton_verifyFfmpeg")

        self.horizontalLayout.addWidget(self.pushButton_verifyFfmpeg)


        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.frame_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout.setItem(6, QFormLayout.LabelRole, self.horizontalSpacer_3)

        self.widget = QWidget(self.frame)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton_applyAppSetting = QPushButton(self.widget)
        self.pushButton_applyAppSetting.setObjectName(u"pushButton_applyAppSetting")

        self.horizontalLayout_3.addWidget(self.pushButton_applyAppSetting)


        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.widget)

        self.checkBox_roundBracketIsNotTag = QCheckBox(self.frame)
        self.checkBox_roundBracketIsNotTag.setObjectName(u"checkBox_roundBracketIsNotTag")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.checkBox_roundBracketIsNotTag)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout.setItem(4, QFormLayout.LabelRole, self.horizontalSpacer_4)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_ffprobeC = QLineEdit(self.frame_3)
        self.lineEdit_ffprobeC.setObjectName(u"lineEdit_ffprobeC")
        self.lineEdit_ffprobeC.setPlaceholderText(u"ffprobe")

        self.horizontalLayout_2.addWidget(self.lineEdit_ffprobeC)

        self.toolButton_findFfprobe = QToolButton(self.frame_3)
        self.toolButton_findFfprobe.setObjectName(u"toolButton_findFfprobe")

        self.horizontalLayout_2.addWidget(self.toolButton_findFfprobe)

        self.pushButton_verifyFfprobe = QPushButton(self.frame_3)
        self.pushButton_verifyFfprobe.setObjectName(u"pushButton_verifyFfprobe")

        self.horizontalLayout_2.addWidget(self.pushButton_verifyFfprobe)


        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.frame_3)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.gridLayout = QGridLayout(self.frame_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.toolButton_saveDirectory = QToolButton(self.frame_4)
        self.toolButton_saveDirectory.setObjectName(u"toolButton_saveDirectory")

        self.gridLayout.addWidget(self.toolButton_saveDirectory, 0, 1, 1, 1)

        self.lineEdit_saveDirectory = QLineEdit(self.frame_4)
        self.lineEdit_saveDirectory.setObjectName(u"lineEdit_saveDirectory")
        self.lineEdit_saveDirectory.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_saveDirectory, 0, 0, 1, 1)


        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.frame_4)


        self.verticalLayout.addWidget(self.frame)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)
        self.toolButton_saveDirectory.clicked.connect(Form._on_select_output_directory)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_ffmpegT.setText(QCoreApplication.translate("Form", u"ffmpeg Path", None))
        self.label_ffmpegC.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.label_ffprobeT.setText(QCoreApplication.translate("Form", u"ffprobe Path", None))
        self.label_ffprobeC.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.toolButton_findFfmpeg.setText(QCoreApplication.translate("Form", u"...", None))
        self.pushButton_verifyFfmpeg.setText(QCoreApplication.translate("Form", u"Verify", None))
        self.pushButton_applyAppSetting.setText(QCoreApplication.translate("Form", u"Apply (not yet implememted)", None))
        self.checkBox_roundBracketIsNotTag.setText(QCoreApplication.translate("Form", u"Do not treat parentheses as tag", None))
        self.label.setText(QCoreApplication.translate("Form", u"Output directory", None))
        self.toolButton_findFfprobe.setText(QCoreApplication.translate("Form", u"...", None))
        self.pushButton_verifyFfprobe.setText(QCoreApplication.translate("Form", u"Verify", None))
        self.toolButton_saveDirectory.setText(QCoreApplication.translate("Form", u"...", None))
        self.lineEdit_saveDirectory.setPlaceholderText(QCoreApplication.translate("Form", u"Default: current working directory", None))
    # retranslateUi

