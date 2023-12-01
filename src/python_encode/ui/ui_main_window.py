# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QToolButton,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QSize(800, 600))
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, -1, 0)
        self.pushButton_selectFile = QPushButton(self.widget_2)
        self.pushButton_selectFile.setObjectName(u"pushButton_selectFile")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_selectFile.sizePolicy().hasHeightForWidth())
        self.pushButton_selectFile.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.pushButton_selectFile)

        self.pushButton_selectFolder = QPushButton(self.widget_2)
        self.pushButton_selectFolder.setObjectName(u"pushButton_selectFolder")
        sizePolicy1.setHeightForWidth(self.pushButton_selectFolder.sizePolicy().hasHeightForWidth())
        self.pushButton_selectFolder.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.pushButton_selectFolder)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButton_startStopEncode = QPushButton(self.widget_2)
        self.pushButton_startStopEncode.setObjectName(u"pushButton_startStopEncode")
        self.pushButton_startStopEncode.setText(u"Start/Stop Encode")

        self.horizontalLayout_3.addWidget(self.pushButton_startStopEncode)


        self.verticalLayout_3.addWidget(self.widget_2)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_sourceFilenameT = QLabel(self.widget)
        self.label_sourceFilenameT.setObjectName(u"label_sourceFilenameT")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_sourceFilenameT.sizePolicy().hasHeightForWidth())
        self.label_sourceFilenameT.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setBold(True)
        self.label_sourceFilenameT.setFont(font)

        self.horizontalLayout.addWidget(self.label_sourceFilenameT)

        self.label_sourceFilenameC = QLabel(self.widget)
        self.label_sourceFilenameC.setObjectName(u"label_sourceFilenameC")
        sizePolicy2.setHeightForWidth(self.label_sourceFilenameC.sizePolicy().hasHeightForWidth())
        self.label_sourceFilenameC.setSizePolicy(sizePolicy2)
        self.label_sourceFilenameC.setText(u"Open a file to continue... / LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG LONG / [group] Title - 01 [CRC32]")

        self.horizontalLayout.addWidget(self.label_sourceFilenameC)

        self.label_multipleInputCounter = QLabel(self.widget)
        self.label_multipleInputCounter.setObjectName(u"label_multipleInputCounter")
        self.label_multipleInputCounter.setText(u"and X more")

        self.horizontalLayout.addWidget(self.label_multipleInputCounter)

        self.toolButton = QToolButton(self.widget)
        self.toolButton.setObjectName(u"toolButton")

        self.horizontalLayout.addWidget(self.toolButton)


        self.verticalLayout_3.addWidget(self.widget)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidgetPageInputList = QWidget()
        self.tabWidgetPageInputList.setObjectName(u"tabWidgetPageInputList")
        sizePolicy.setHeightForWidth(self.tabWidgetPageInputList.sizePolicy().hasHeightForWidth())
        self.tabWidgetPageInputList.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.tabWidgetPageInputList)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget_tabWidgetPageInputList = QWidget(self.tabWidgetPageInputList)
        self.widget_tabWidgetPageInputList.setObjectName(u"widget_tabWidgetPageInputList")

        self.verticalLayout_2.addWidget(self.widget_tabWidgetPageInputList)

        self.tabWidget.addTab(self.tabWidgetPageInputList, "")
        self.tab_encoderSettings = QWidget()
        self.tab_encoderSettings.setObjectName(u"tab_encoderSettings")
        self.tabWidget.addTab(self.tab_encoderSettings, "")
        self.tab_appSettings = QWidget()
        self.tab_appSettings.setObjectName(u"tab_appSettings")
        self.tabWidget.addTab(self.tab_appSettings, "")
        self.widget_3 = QWidget()
        self.widget_3.setObjectName(u"widget_3")
        self.tabWidget.addTab(self.widget_3, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.label_statusTextGlobal = QLabel(self.centralwidget)
        self.label_statusTextGlobal.setObjectName(u"label_statusTextGlobal")
        self.label_statusTextGlobal.setText(u"Display status like \"Encoding example.mkv\" or \"Calculating CRC32 checksum for example.mkv\"")

        self.verticalLayout_3.addWidget(self.label_statusTextGlobal)

        self.widget_progressContainer = QWidget(self.centralwidget)
        self.widget_progressContainer.setObjectName(u"widget_progressContainer")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_progressContainer)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.progressBar_statusGlobal = QProgressBar(self.widget_progressContainer)
        self.progressBar_statusGlobal.setObjectName(u"progressBar_statusGlobal")
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.progressBar_statusGlobal.sizePolicy().hasHeightForWidth())
        self.progressBar_statusGlobal.setSizePolicy(sizePolicy3)
        self.progressBar_statusGlobal.setValue(24)
        self.progressBar_statusGlobal.setFormat(u"%p%")

        self.horizontalLayout_2.addWidget(self.progressBar_statusGlobal)

        self.label_progressTextForFFMPEG = QLabel(self.widget_progressContainer)
        self.label_progressTextForFFMPEG.setObjectName(u"label_progressTextForFFMPEG")
        self.label_progressTextForFFMPEG.setText(u"shows ffmpeg's progress output")

        self.horizontalLayout_2.addWidget(self.label_progressTextForFFMPEG)


        self.verticalLayout_3.addWidget(self.widget_progressContainer)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.pushButton_selectFile.clicked.connect(MainWindow.read_source_button_clicked)
        self.pushButton_startStopEncode.clicked.connect(MainWindow.encode_button_clicked)

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_selectFile.setText(QCoreApplication.translate("MainWindow", u"Select File", None))
        self.pushButton_selectFolder.setText(QCoreApplication.translate("MainWindow", u"Select Folder", None))
        self.label_sourceFilenameT.setText(QCoreApplication.translate("MainWindow", u"Source", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPageInputList), QCoreApplication.translate("MainWindow", u"Info", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_encoderSettings), QCoreApplication.translate("MainWindow", u"Encode Settings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_appSettings), QCoreApplication.translate("MainWindow", u"App Settings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget_3), QCoreApplication.translate("MainWindow", u"Page", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
    # retranslateUi

