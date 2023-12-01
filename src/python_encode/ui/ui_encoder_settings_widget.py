# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'encoder_settings_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QRadioButton, QScrollArea, QSizePolicy, QSlider,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_Form_EncoderSettings(object):
    def setupUi(self, Form_EncoderSettings):
        if not Form_EncoderSettings.objectName():
            Form_EncoderSettings.setObjectName(u"Form_EncoderSettings")
        Form_EncoderSettings.resize(802, 620)
        Form_EncoderSettings.setLocale(QLocale(QLocale.English, QLocale.HongKong))
        self.verticalLayout = QVBoxLayout(Form_EncoderSettings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(Form_EncoderSettings)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 783, 649))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.comboBox_PresetList = QComboBox(self.groupBox)
        self.comboBox_PresetList.addItem("")
        self.comboBox_PresetList.setObjectName(u"comboBox_PresetList")

        self.verticalLayout_5.addWidget(self.comboBox_PresetList)

        self.widget_6 = QWidget(self.groupBox)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.label = QLabel(self.widget_6)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        self.horizontalLayout_5.addWidget(self.label)

        self.label_presetModifiedMark = QLabel(self.widget_6)
        self.label_presetModifiedMark.setObjectName(u"label_presetModifiedMark")
        sizePolicy.setHeightForWidth(self.label_presetModifiedMark.sizePolicy().hasHeightForWidth())
        self.label_presetModifiedMark.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setItalic(True)
        self.label_presetModifiedMark.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_presetModifiedMark)

        self.label_presetDisplayName = QLabel(self.widget_6)
        self.label_presetDisplayName.setObjectName(u"label_presetDisplayName")
        self.label_presetDisplayName.setText(u"Preset display name")

        self.horizontalLayout_5.addWidget(self.label_presetDisplayName)

        self.pushButton_ReloadPreset = QPushButton(self.widget_6)
        self.pushButton_ReloadPreset.setObjectName(u"pushButton_ReloadPreset")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_ReloadPreset.sizePolicy().hasHeightForWidth())
        self.pushButton_ReloadPreset.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.pushButton_ReloadPreset)

        self.pushButton_SavePresetAs = QPushButton(self.widget_6)
        self.pushButton_SavePresetAs.setObjectName(u"pushButton_SavePresetAs")
        sizePolicy1.setHeightForWidth(self.pushButton_SavePresetAs.sizePolicy().hasHeightForWidth())
        self.pushButton_SavePresetAs.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.pushButton_SavePresetAs)


        self.verticalLayout_5.addWidget(self.widget_6)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.groupBox_basic = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_basic.setObjectName(u"groupBox_basic")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_basic.sizePolicy().hasHeightForWidth())
        self.groupBox_basic.setSizePolicy(sizePolicy2)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_basic)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget_9 = QWidget(self.groupBox_basic)
        self.widget_9.setObjectName(u"widget_9")
        sizePolicy.setHeightForWidth(self.widget_9.sizePolicy().hasHeightForWidth())
        self.widget_9.setSizePolicy(sizePolicy)
        self.horizontalLayout_6 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, -1, -1, 0)
        self.label_16 = QLabel(self.widget_9)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_6.addWidget(self.label_16)

        self.comboBox_containerSelection = QComboBox(self.widget_9)
        self.comboBox_containerSelection.addItem("")
        self.comboBox_containerSelection.setObjectName(u"comboBox_containerSelection")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.comboBox_containerSelection.sizePolicy().hasHeightForWidth())
        self.comboBox_containerSelection.setSizePolicy(sizePolicy3)
        self.comboBox_containerSelection.setEditable(True)
        self.comboBox_containerSelection.setCurrentText(u"Dummy text (.dummy)")

        self.horizontalLayout_6.addWidget(self.comboBox_containerSelection)

        self.checkBox_enableHwaccel = QCheckBox(self.widget_9)
        self.checkBox_enableHwaccel.setObjectName(u"checkBox_enableHwaccel")

        self.horizontalLayout_6.addWidget(self.checkBox_enableHwaccel)

        self.checkBox_copyAttachment = QCheckBox(self.widget_9)
        self.checkBox_copyAttachment.setObjectName(u"checkBox_copyAttachment")

        self.horizontalLayout_6.addWidget(self.checkBox_copyAttachment)

        self.checkBox_keepChapters = QCheckBox(self.widget_9)
        self.checkBox_keepChapters.setObjectName(u"checkBox_keepChapters")

        self.horizontalLayout_6.addWidget(self.checkBox_keepChapters)


        self.verticalLayout_3.addWidget(self.widget_9)

        self.line_2 = QFrame(self.groupBox_basic)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.widget_2 = QWidget(self.groupBox_basic)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.comboBox = QComboBox(self.widget_2)
        self.comboBox.addItem("")
        self.comboBox.addItem(u"libpous")
        self.comboBox.setObjectName(u"comboBox")
        sizePolicy1.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy1)
        self.comboBox.setCurrentText(u"copy")

        self.horizontalLayout_3.addWidget(self.comboBox)

        self.radioButton_3 = QRadioButton(self.widget_2)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setChecked(True)

        self.horizontalLayout_3.addWidget(self.radioButton_3)

        self.spinBox_4 = QSpinBox(self.widget_2)
        self.spinBox_4.setObjectName(u"spinBox_4")
        sizePolicy1.setHeightForWidth(self.spinBox_4.sizePolicy().hasHeightForWidth())
        self.spinBox_4.setSizePolicy(sizePolicy1)
        self.spinBox_4.setMinimum(1)
        self.spinBox_4.setMaximum(10000)
        self.spinBox_4.setValue(96)

        self.horizontalLayout_3.addWidget(self.spinBox_4)


        self.verticalLayout_3.addWidget(self.widget_2)

        self.line = QFrame(self.groupBox_basic)
        self.line.setObjectName(u"line")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy4)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.widget = QWidget(self.groupBox_basic)
        self.widget.setObjectName(u"widget")
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.comboBox_videoCodec = QComboBox(self.widget)
        self.comboBox_videoCodec.addItem("")
        self.comboBox_videoCodec.addItem(u"libx265")
        self.comboBox_videoCodec.setObjectName(u"comboBox_videoCodec")
        self.comboBox_videoCodec.setCurrentText(u"copy")

        self.horizontalLayout_2.addWidget(self.comboBox_videoCodec)

        self.checkBox_videoResize = QCheckBox(self.widget)
        self.checkBox_videoResize.setObjectName(u"checkBox_videoResize")

        self.horizontalLayout_2.addWidget(self.checkBox_videoResize)

        self.spinBox_videoResolutionWidth = QSpinBox(self.widget)
        self.spinBox_videoResolutionWidth.setObjectName(u"spinBox_videoResolutionWidth")
        sizePolicy5 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.spinBox_videoResolutionWidth.sizePolicy().hasHeightForWidth())
        self.spinBox_videoResolutionWidth.setSizePolicy(sizePolicy5)
        self.spinBox_videoResolutionWidth.setMinimum(1)
        self.spinBox_videoResolutionWidth.setMaximum(10000)
        self.spinBox_videoResolutionWidth.setValue(1920)

        self.horizontalLayout_2.addWidget(self.spinBox_videoResolutionWidth)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_4)

        self.spinBox_2 = QSpinBox(self.widget)
        self.spinBox_2.setObjectName(u"spinBox_2")
        sizePolicy5.setHeightForWidth(self.spinBox_2.sizePolicy().hasHeightForWidth())
        self.spinBox_2.setSizePolicy(sizePolicy5)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(10000)
        self.spinBox_2.setValue(1080)

        self.horizontalLayout_2.addWidget(self.spinBox_2)

        self.checkBox_2 = QCheckBox(self.widget)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_2.addWidget(self.checkBox_2)


        self.verticalLayout_3.addWidget(self.widget)

        self.widget_3 = QWidget(self.groupBox_basic)
        self.widget_3.setObjectName(u"widget_3")
        self.formLayout = QFormLayout(self.widget_3)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_4 = QVBoxLayout(self.widget_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 3, 0, -1)
        self.label_VideoQualityVal = QLabel(self.widget_4)
        self.label_VideoQualityVal.setObjectName(u"label_VideoQualityVal")
        self.label_VideoQualityVal.setText(u"12")

        self.verticalLayout_4.addWidget(self.label_VideoQualityVal)

        self.horizontalSlider_VideoQuality = QSlider(self.widget_4)
        self.horizontalSlider_VideoQuality.setObjectName(u"horizontalSlider_VideoQuality")
        self.horizontalSlider_VideoQuality.setMaximum(500)
        self.horizontalSlider_VideoQuality.setValue(242)
        self.horizontalSlider_VideoQuality.setOrientation(Qt.Horizontal)

        self.verticalLayout_4.addWidget(self.horizontalSlider_VideoQuality)


        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.widget_4)

        self.radioButton = QRadioButton(self.widget_3)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setChecked(True)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.radioButton)

        self.radioButton_2 = QRadioButton(self.widget_3)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setEnabled(False)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.radioButton_2)

        self.widget_5 = QWidget(self.widget_3)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, -1)
        self.spinBox = QSpinBox(self.widget_5)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(100000)
        self.spinBox.setValue(5000)

        self.horizontalLayout_4.addWidget(self.spinBox)


        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.widget_5)


        self.verticalLayout_3.addWidget(self.widget_3)

        self.widget_8 = QWidget(self.groupBox_basic)
        self.widget_8.setObjectName(u"widget_8")
        sizePolicy.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.widget_8)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit_2 = QLineEdit(self.widget_8)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setText(u"main")

        self.gridLayout.addWidget(self.lineEdit_2, 0, 1, 1, 1)

        self.label_10 = QLabel(self.widget_8)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 0, 4, 1, 1)

        self.lineEdit_4 = QLineEdit(self.widget_8)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setText(u"yuv420p")

        self.gridLayout.addWidget(self.lineEdit_4, 0, 5, 1, 1)

        self.label_9 = QLabel(self.widget_8)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 0, 2, 1, 1)

        self.label_8 = QLabel(self.widget_8)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)

        self.lineEdit_3 = QLineEdit(self.widget_8)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setText(u"slow")

        self.gridLayout.addWidget(self.lineEdit_3, 0, 3, 1, 1)


        self.verticalLayout_3.addWidget(self.widget_8)

        self.line_3 = QFrame(self.groupBox_basic)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_3)

        self.widget_10 = QWidget(self.groupBox_basic)
        self.widget_10.setObjectName(u"widget_10")
        self.verticalLayout_7 = QVBoxLayout(self.widget_10)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_15 = QLabel(self.widget_10)
        self.label_15.setObjectName(u"label_15")

        self.verticalLayout_7.addWidget(self.label_15)


        self.verticalLayout_3.addWidget(self.widget_10)


        self.verticalLayout_2.addWidget(self.groupBox_basic)

        self.groupBox_moreParams = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_moreParams.setObjectName(u"groupBox_moreParams")
        sizePolicy2.setHeightForWidth(self.groupBox_moreParams.sizePolicy().hasHeightForWidth())
        self.groupBox_moreParams.setSizePolicy(sizePolicy2)
        self.horizontalLayout = QHBoxLayout(self.groupBox_moreParams)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.plainTextEdit_2 = QPlainTextEdit(self.groupBox_moreParams)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")

        self.horizontalLayout.addWidget(self.plainTextEdit_2)


        self.verticalLayout_2.addWidget(self.groupBox_moreParams)

        self.widget_7 = QWidget(self.scrollAreaWidgetContents)
        self.widget_7.setObjectName(u"widget_7")
        self.verticalLayout_6 = QVBoxLayout(self.widget_7)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.widget_7)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_6.addWidget(self.label_7)

        self.plainTextEdit = QPlainTextEdit(self.widget_7)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setPlainText(u"")

        self.verticalLayout_6.addWidget(self.plainTextEdit)


        self.verticalLayout_2.addWidget(self.widget_7)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(Form_EncoderSettings)

        QMetaObject.connectSlotsByName(Form_EncoderSettings)
    # setupUi

    def retranslateUi(self, Form_EncoderSettings):
        Form_EncoderSettings.setWindowTitle(QCoreApplication.translate("Form_EncoderSettings", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form_EncoderSettings", u"Presets", None))
        self.comboBox_PresetList.setItemText(0, QCoreApplication.translate("Form_EncoderSettings", u"*Don't use preset", None))

        self.label.setText(QCoreApplication.translate("Form_EncoderSettings", u"Selected preset:", None))
        self.label_presetModifiedMark.setText(QCoreApplication.translate("Form_EncoderSettings", u"Modified", None))
        self.pushButton_ReloadPreset.setText(QCoreApplication.translate("Form_EncoderSettings", u"Reload", None))
        self.pushButton_SavePresetAs.setText(QCoreApplication.translate("Form_EncoderSettings", u"Save As", None))
        self.groupBox_basic.setTitle(QCoreApplication.translate("Form_EncoderSettings", u"Basic", None))
        self.label_16.setText(QCoreApplication.translate("Form_EncoderSettings", u"Container", None))
        self.comboBox_containerSelection.setItemText(0, QCoreApplication.translate("Form_EncoderSettings", u"Dummy text (.dummy)", None))

        self.checkBox_enableHwaccel.setText(QCoreApplication.translate("Form_EncoderSettings", u"Enable Hardware Accleration", None))
        self.checkBox_copyAttachment.setText(QCoreApplication.translate("Form_EncoderSettings", u"Copy attachments", None))
        self.checkBox_keepChapters.setText(QCoreApplication.translate("Form_EncoderSettings", u"Keep Chapters", None))
        self.label_2.setText(QCoreApplication.translate("Form_EncoderSettings", u"Audio Codec", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form_EncoderSettings", u"copy", None))

        self.radioButton_3.setText(QCoreApplication.translate("Form_EncoderSettings", u"Audio Bitrate", None))
        self.spinBox_4.setSuffix(QCoreApplication.translate("Form_EncoderSettings", u"kbps", None))
        self.label_3.setText(QCoreApplication.translate("Form_EncoderSettings", u"Video Codec", None))
        self.comboBox_videoCodec.setItemText(0, QCoreApplication.translate("Form_EncoderSettings", u"copy", None))

        self.checkBox_videoResize.setText(QCoreApplication.translate("Form_EncoderSettings", u"Resize", None))
        self.label_4.setText(QCoreApplication.translate("Form_EncoderSettings", u"x", None))
        self.checkBox_2.setText(QCoreApplication.translate("Form_EncoderSettings", u"Keep Aspect Ratio", None))
        self.radioButton.setText(QCoreApplication.translate("Form_EncoderSettings", u"Constant Quality", None))
        self.radioButton_2.setText(QCoreApplication.translate("Form_EncoderSettings", u"Bitrate (kbps)", None))
        self.spinBox.setSuffix(QCoreApplication.translate("Form_EncoderSettings", u"kbps", None))
        self.label_10.setText(QCoreApplication.translate("Form_EncoderSettings", u"Pixel Format", None))
        self.label_9.setText(QCoreApplication.translate("Form_EncoderSettings", u"Preset", None))
        self.label_8.setText(QCoreApplication.translate("Form_EncoderSettings", u"Profile", None))
        self.label_15.setText(QCoreApplication.translate("Form_EncoderSettings", u"[todo] Subtitle Codec (if it's mp4 encode then it will be needed)", None))
        self.groupBox_moreParams.setTitle(QCoreApplication.translate("Form_EncoderSettings", u"Advanced Options", None))
        self.plainTextEdit_2.setDocumentTitle("")
        self.plainTextEdit_2.setPlainText("")
        self.plainTextEdit_2.setPlaceholderText(QCoreApplication.translate("Form_EncoderSettings", u"FFmpeg command line optons, for emample: -sws_flags spline+accurate_rnd+full_chroma_int -x265-params me=2:rd=4:subme=7:aq-mode=3:aq-strength=1:deblock=1,1:psy-rd=1:psy-rdoq=1:rdoq-level=2:merange=57:bframes=8:b-adapt=2:limit-sao=1:no-info=1", None))
        self.label_7.setText(QCoreApplication.translate("Form_EncoderSettings", u"ffmpeg command preview", None))
    # retranslateUi

