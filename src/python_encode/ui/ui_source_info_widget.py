# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'source_info_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QHBoxLayout, QLabel, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_source_info_widget(object):
    def setupUi(self, source_info_widget):
        if not source_info_widget.objectName():
            source_info_widget.setObjectName(u"source_info_widget")
        source_info_widget.resize(512, 381)
        self.verticalLayout = QVBoxLayout(source_info_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.comboBox_inputSourcesList = QComboBox(source_info_widget)
        self.comboBox_inputSourcesList.setObjectName(u"comboBox_inputSourcesList")

        self.verticalLayout.addWidget(self.comboBox_inputSourcesList)

        self.frame = QFrame(source_info_widget)
        self.frame.setObjectName(u"frame")
        self.formLayout = QFormLayout(self.frame)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_fullPathTitle = QLabel(self.frame)
        self.label_fullPathTitle.setObjectName(u"label_fullPathTitle")
        font = QFont()
        font.setBold(True)
        self.label_fullPathTitle.setFont(font)
        self.label_fullPathTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_fullPathTitle)

        self.label_fullPathContent = QLabel(self.frame)
        self.label_fullPathContent.setObjectName(u"label_fullPathContent")
        self.label_fullPathContent.setText(u"lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem lorem ")
        self.label_fullPathContent.setTextFormat(Qt.PlainText)
        self.label_fullPathContent.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_fullPathContent.setWordWrap(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label_fullPathContent)

        self.label_animeNameTitle = QLabel(self.frame)
        self.label_animeNameTitle.setObjectName(u"label_animeNameTitle")
        self.label_animeNameTitle.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_animeNameTitle)

        self.label_animeNameContent = QLabel(self.frame)
        self.label_animeNameContent.setObjectName(u"label_animeNameContent")
        self.label_animeNameContent.setText(u"Some Anime Name - 01")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.label_animeNameContent)

        self.label_groupTitle = QLabel(self.frame)
        self.label_groupTitle.setObjectName(u"label_groupTitle")
        self.label_groupTitle.setFont(font)
        self.label_groupTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_groupTitle)

        self.label_groupContent = QLabel(self.frame)
        self.label_groupContent.setObjectName(u"label_groupContent")
        self.label_groupContent.setText(u"I like subsplease and erairaw")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.label_groupContent)

        self.label_CRC32Title = QLabel(self.frame)
        self.label_CRC32Title.setObjectName(u"label_CRC32Title")
        self.label_CRC32Title.setFont(font)
        self.label_CRC32Title.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_CRC32Title)

        self.frame_CRC32Content = QFrame(self.frame)
        self.frame_CRC32Content.setObjectName(u"frame_CRC32Content")
        self.frame_CRC32Content.setFrameShape(QFrame.NoFrame)
        self.frame_CRC32Content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_CRC32Content)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_CRC32FileT = QLabel(self.frame_CRC32Content)
        self.label_CRC32FileT.setObjectName(u"label_CRC32FileT")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_CRC32FileT.sizePolicy().hasHeightForWidth())
        self.label_CRC32FileT.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_CRC32FileT)

        self.label_CRC32FileC = QLabel(self.frame_CRC32Content)
        self.label_CRC32FileC.setObjectName(u"label_CRC32FileC")
        sizePolicy.setHeightForWidth(self.label_CRC32FileC.sizePolicy().hasHeightForWidth())
        self.label_CRC32FileC.setSizePolicy(sizePolicy)
        self.label_CRC32FileC.setText(u"12345678")

        self.horizontalLayout.addWidget(self.label_CRC32FileC)

        self.horizontalSpacer_2 = QSpacerItem(40, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.label_CRC32NameT = QLabel(self.frame_CRC32Content)
        self.label_CRC32NameT.setObjectName(u"label_CRC32NameT")
        sizePolicy.setHeightForWidth(self.label_CRC32NameT.sizePolicy().hasHeightForWidth())
        self.label_CRC32NameT.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_CRC32NameT)

        self.label_CRC32NameC = QLabel(self.frame_CRC32Content)
        self.label_CRC32NameC.setObjectName(u"label_CRC32NameC")
        sizePolicy.setHeightForWidth(self.label_CRC32NameC.sizePolicy().hasHeightForWidth())
        self.label_CRC32NameC.setSizePolicy(sizePolicy)
        self.label_CRC32NameC.setText(u"ABCDEFGH")

        self.horizontalLayout.addWidget(self.label_CRC32NameC)

        self.horizontalSpacer = QSpacerItem(40, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_CRC32CheckResult = QLabel(self.frame_CRC32Content)
        self.label_CRC32CheckResult.setObjectName(u"label_CRC32CheckResult")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_CRC32CheckResult.sizePolicy().hasHeightForWidth())
        self.label_CRC32CheckResult.setSizePolicy(sizePolicy1)
        self.label_CRC32CheckResult.setText(u"Match")

        self.horizontalLayout.addWidget(self.label_CRC32CheckResult)


        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.frame_CRC32Content)

        self.label_videoLengthT = QLabel(self.frame)
        self.label_videoLengthT.setObjectName(u"label_videoLengthT")
        self.label_videoLengthT.setFont(font)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_videoLengthT)

        self.label_videoLengthC = QLabel(self.frame)
        self.label_videoLengthC.setObjectName(u"label_videoLengthC")
        self.label_videoLengthC.setText(u"something seconds (something frames)")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.label_videoLengthC)

        self.label_resolutionT = QLabel(self.frame)
        self.label_resolutionT.setObjectName(u"label_resolutionT")
        self.label_resolutionT.setFont(font)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_resolutionT)

        self.label_resolutionC = QLabel(self.frame)
        self.label_resolutionC.setObjectName(u"label_resolutionC")
        self.label_resolutionC.setText(u"something by something")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.label_resolutionC)

        self.label_tagT = QLabel(self.frame)
        self.label_tagT.setObjectName(u"label_tagT")
        self.label_tagT.setFont(font)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_tagT)

        self.label_tagC = QLabel(self.frame)
        self.label_tagC.setObjectName(u"label_tagC")
        self.label_tagC.setText(u"[a], [b], [c]")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.label_tagC)

        self.label_ChaptersTitle = QLabel(self.frame)
        self.label_ChaptersTitle.setObjectName(u"label_ChaptersTitle")
        self.label_ChaptersTitle.setFont(font)

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_ChaptersTitle)

        self.label_ChaptersContent = QLabel(self.frame)
        self.label_ChaptersContent.setObjectName(u"label_ChaptersContent")
        self.label_ChaptersContent.setText(u"0:00 OP, 1:25 Part 1, 13:00 Part 2, 22:30 ED")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.label_ChaptersContent)

        self.label_StreamsT = QLabel(self.frame)
        self.label_StreamsT.setObjectName(u"label_StreamsT")
        self.label_StreamsT.setFont(font)
        self.label_StreamsT.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_StreamsT)

        self.label_StreamsC = QLabel(self.frame)
        self.label_StreamsC.setObjectName(u"label_StreamsC")
        self.label_StreamsC.setText(u"#0 HEVC frames-per-second\n"
"#1 AAC 2ch\n"
"(IDK What to put here)")
        self.label_StreamsC.setTextFormat(Qt.PlainText)
        self.label_StreamsC.setWordWrap(True)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.label_StreamsC)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(source_info_widget)

        QMetaObject.connectSlotsByName(source_info_widget)
    # setupUi

    def retranslateUi(self, source_info_widget):
        source_info_widget.setWindowTitle(QCoreApplication.translate("source_info_widget", u"Form", None))
        self.label_fullPathTitle.setText(QCoreApplication.translate("source_info_widget", u"Full Path", None))
        self.label_animeNameTitle.setText(QCoreApplication.translate("source_info_widget", u"Title", None))
        self.label_groupTitle.setText(QCoreApplication.translate("source_info_widget", u"Group", None))
        self.label_CRC32Title.setText(QCoreApplication.translate("source_info_widget", u"CRC32", None))
        self.label_CRC32FileT.setText(QCoreApplication.translate("source_info_widget", u"File", None))
        self.label_CRC32NameT.setText(QCoreApplication.translate("source_info_widget", u"Filename", None))
        self.label_videoLengthT.setText(QCoreApplication.translate("source_info_widget", u"Length", None))
        self.label_resolutionT.setText(QCoreApplication.translate("source_info_widget", u"Resolution", None))
        self.label_tagT.setText(QCoreApplication.translate("source_info_widget", u"Tags", None))
        self.label_ChaptersTitle.setText(QCoreApplication.translate("source_info_widget", u"Chapters", None))
        self.label_StreamsT.setText(QCoreApplication.translate("source_info_widget", u"Streams", None))
    # retranslateUi

