# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QTabWidget,
    QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget)

from gui.FileChooserButton import FileChooserButton
from gui.HelpMenu import HelpMenu
from gui.RunParserButton import RunParserButton
from gui.actions.ActionsTable import ActionsTable
from gui.actions.AddRemoveActionButton import AddRemoveActionButton
from gui.actions.TreebankFormatComboBox import TreebankFormatComboBox

class Ui_gui_treebank_parser(object):
    def setupUi(self, gui_treebank_parser):
        if not gui_treebank_parser.objectName():
            gui_treebank_parser.setObjectName(u"gui_treebank_parser")
        gui_treebank_parser.resize(1139, 725)
        self.how_to = QAction(gui_treebank_parser)
        self.how_to.setObjectName(u"how_to")
        self.about = QAction(gui_treebank_parser)
        self.about.setObjectName(u"about")
        self.actionq1 = QAction(gui_treebank_parser)
        self.actionq1.setObjectName(u"actionq1")
        self.actionq2 = QAction(gui_treebank_parser)
        self.actionq2.setObjectName(u"actionq2")
        self.check_LAL_reachable = QAction(gui_treebank_parser)
        self.check_LAL_reachable.setObjectName(u"check_LAL_reachable")
        self.centralwidget = QWidget(gui_treebank_parser)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_7 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.inputTabSelector = QTabWidget(self.centralwidget)
        self.inputTabSelector.setObjectName(u"inputTabSelector")
        self.treebankTab = QWidget()
        self.treebankTab.setObjectName(u"treebankTab")
        self.verticalLayout_6 = QVBoxLayout(self.treebankTab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.treebankTab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(100, 0))
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_5)

        self.inputTreebankFile = QLineEdit(self.treebankTab)
        self.inputTreebankFile.setObjectName(u"inputTreebankFile")
        self.inputTreebankFile.setMinimumSize(QSize(350, 0))

        self.horizontalLayout.addWidget(self.inputTreebankFile)

        self.inputTreebankButton = FileChooserButton(self.treebankTab)
        self.inputTreebankButton.setObjectName(u"inputTreebankButton")

        self.horizontalLayout.addWidget(self.inputTreebankButton)


        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_6 = QLabel(self.treebankTab)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(100, 0))
        self.label_6.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_6)

        self.outputTreebankFile = QLineEdit(self.treebankTab)
        self.outputTreebankFile.setObjectName(u"outputTreebankFile")
        self.outputTreebankFile.setMinimumSize(QSize(350, 0))

        self.horizontalLayout_2.addWidget(self.outputTreebankFile)

        self.outputTreebankButton = FileChooserButton(self.treebankTab)
        self.outputTreebankButton.setObjectName(u"outputTreebankButton")

        self.horizontalLayout_2.addWidget(self.outputTreebankButton)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_3 = QSpacerItem(20, 65, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)

        self.inputTabSelector.addTab(self.treebankTab, "")
        self.treebankCollectionTab = QWidget()
        self.treebankCollectionTab.setObjectName(u"treebankCollectionTab")
        self.verticalLayout_8 = QVBoxLayout(self.treebankCollectionTab)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_9 = QLabel(self.treebankCollectionTab)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(140, 0))
        self.label_9.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_9)

        self.inputTreebankCollectionFile = QLineEdit(self.treebankCollectionTab)
        self.inputTreebankCollectionFile.setObjectName(u"inputTreebankCollectionFile")
        self.inputTreebankCollectionFile.setMinimumSize(QSize(350, 0))

        self.horizontalLayout_6.addWidget(self.inputTreebankCollectionFile)

        self.inputTreebankCollectionButton = FileChooserButton(self.treebankCollectionTab)
        self.inputTreebankCollectionButton.setObjectName(u"inputTreebankCollectionButton")

        self.horizontalLayout_6.addWidget(self.inputTreebankCollectionButton)


        self.verticalLayout_8.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_8 = QLabel(self.treebankCollectionTab)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(140, 0))
        self.label_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_8)

        self.outputTreebankCollectionDirectory = QLineEdit(self.treebankCollectionTab)
        self.outputTreebankCollectionDirectory.setObjectName(u"outputTreebankCollectionDirectory")
        self.outputTreebankCollectionDirectory.setMinimumSize(QSize(350, 0))

        self.horizontalLayout_7.addWidget(self.outputTreebankCollectionDirectory)

        self.outputTreebankCollectionButton = FileChooserButton(self.treebankCollectionTab)
        self.outputTreebankCollectionButton.setObjectName(u"outputTreebankCollectionButton")

        self.horizontalLayout_7.addWidget(self.outputTreebankCollectionButton)


        self.verticalLayout_8.addLayout(self.horizontalLayout_7)

        self.sentenceConsistencyCheckBox = QCheckBox(self.treebankCollectionTab)
        self.sentenceConsistencyCheckBox.setObjectName(u"sentenceConsistencyCheckBox")
        self.sentenceConsistencyCheckBox.setToolTipDuration(5000)
        self.sentenceConsistencyCheckBox.setChecked(True)

        self.verticalLayout_8.addWidget(self.sentenceConsistencyCheckBox)

        self.verticalSpacer_4 = QSpacerItem(20, 36, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_4)

        self.inputTabSelector.addTab(self.treebankCollectionTab, "")

        self.verticalLayout_7.addWidget(self.inputTabSelector)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.treebankFormatSelector = TreebankFormatComboBox(self.centralwidget)
        self.treebankFormatSelector.addItem("")
        self.treebankFormatSelector.setObjectName(u"treebankFormatSelector")

        self.verticalLayout.addWidget(self.treebankFormatSelector)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_5.addWidget(self.label_2)

        self.availableActionList = QListWidget(self.centralwidget)
        self.availableActionList.setObjectName(u"availableActionList")
        self.availableActionList.setMinimumSize(QSize(300, 0))
        self.availableActionList.setMaximumSize(QSize(300, 16777215))

        self.verticalLayout_5.addWidget(self.availableActionList)


        self.horizontalLayout_4.addLayout(self.verticalLayout_5)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.actionAddButton = AddRemoveActionButton(self.centralwidget)
        self.actionAddButton.setObjectName(u"actionAddButton")

        self.verticalLayout_3.addWidget(self.actionAddButton)

        self.actionRemoveButton = AddRemoveActionButton(self.centralwidget)
        self.actionRemoveButton.setObjectName(u"actionRemoveButton")

        self.verticalLayout_3.addWidget(self.actionRemoveButton)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_4.addWidget(self.label_3)

        self.chosenActionTable = ActionsTable(self.centralwidget)
        if (self.chosenActionTable.columnCount() < 3):
            self.chosenActionTable.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.chosenActionTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.chosenActionTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.chosenActionTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.chosenActionTable.setObjectName(u"chosenActionTable")
        self.chosenActionTable.setMinimumSize(QSize(600, 0))

        self.verticalLayout_4.addWidget(self.chosenActionTable)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)


        self.verticalLayout_7.addLayout(self.horizontalLayout_4)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.runTreebankParser = RunParserButton(self.centralwidget)
        self.runTreebankParser.setObjectName(u"runTreebankParser")

        self.horizontalLayout_3.addWidget(self.runTreebankParser)

        self.lalReleaseCheckBox = QCheckBox(self.centralwidget)
        self.lalReleaseCheckBox.setObjectName(u"lalReleaseCheckBox")
        self.lalReleaseCheckBox.setEnabled(False)

        self.horizontalLayout_3.addWidget(self.lalReleaseCheckBox)

        self.lalDebugCheckBox = QCheckBox(self.centralwidget)
        self.lalDebugCheckBox.setObjectName(u"lalDebugCheckBox")
        self.lalDebugCheckBox.setEnabled(False)

        self.horizontalLayout_3.addWidget(self.lalDebugCheckBox)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_3.addWidget(self.label_7)

        self.loggingLevelSpinBox = QSpinBox(self.centralwidget)
        self.loggingLevelSpinBox.setObjectName(u"loggingLevelSpinBox")
        self.loggingLevelSpinBox.setMaximum(3)

        self.horizontalLayout_3.addWidget(self.loggingLevelSpinBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.msgLogger = QTextEdit(self.centralwidget)
        self.msgLogger.setObjectName(u"msgLogger")
        self.msgLogger.setSizeIncrement(QSize(0, 0))
        self.msgLogger.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.msgLogger)


        self.verticalLayout_7.addLayout(self.verticalLayout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_5.addWidget(self.pushButton)


        self.verticalLayout_7.addLayout(self.horizontalLayout_5)

        gui_treebank_parser.setCentralWidget(self.centralwidget)
        self.menu_bar = QMenuBar(gui_treebank_parser)
        self.menu_bar.setObjectName(u"menu_bar")
        self.menu_bar.setGeometry(QRect(0, 0, 1139, 22))
        self.only_menu = HelpMenu(self.menu_bar)
        self.only_menu.setObjectName(u"only_menu")
        gui_treebank_parser.setMenuBar(self.menu_bar)
        self.statusbar = QStatusBar(gui_treebank_parser)
        self.statusbar.setObjectName(u"statusbar")
        gui_treebank_parser.setStatusBar(self.statusbar)

        self.menu_bar.addAction(self.only_menu.menuAction())
        self.only_menu.addAction(self.how_to)
        self.only_menu.addAction(self.about)
        self.only_menu.addSeparator()

        self.retranslateUi(gui_treebank_parser)
        self.pushButton.clicked.connect(self.msgLogger.clear)

        self.inputTabSelector.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(gui_treebank_parser)
    # setupUi

    def retranslateUi(self, gui_treebank_parser):
        gui_treebank_parser.setWindowTitle(QCoreApplication.translate("gui_treebank_parser", u"gui_treebank_parser", None))
        self.how_to.setText(QCoreApplication.translate("gui_treebank_parser", u"How to", None))
        self.about.setText(QCoreApplication.translate("gui_treebank_parser", u"About", None))
        self.actionq1.setText(QCoreApplication.translate("gui_treebank_parser", u"q1", None))
        self.actionq2.setText(QCoreApplication.translate("gui_treebank_parser", u"q2", None))
        self.check_LAL_reachable.setText(QCoreApplication.translate("gui_treebank_parser", u"Is LAL reachable?", None))
#if QT_CONFIG(tooltip)
        self.inputTabSelector.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("gui_treebank_parser", u"Treebank File", None))
        self.inputTreebankButton.setText(QCoreApplication.translate("gui_treebank_parser", u"Select", None))
        self.label_6.setText(QCoreApplication.translate("gui_treebank_parser", u"Heads File", None))
        self.outputTreebankButton.setText(QCoreApplication.translate("gui_treebank_parser", u"Select", None))
        self.inputTabSelector.setTabText(self.inputTabSelector.indexOf(self.treebankTab), QCoreApplication.translate("gui_treebank_parser", u"Single treebank", None))
        self.label_9.setText(QCoreApplication.translate("gui_treebank_parser", u"Treebank collection", None))
        self.inputTreebankCollectionButton.setText(QCoreApplication.translate("gui_treebank_parser", u"Select", None))
        self.label_8.setText(QCoreApplication.translate("gui_treebank_parser", u"Output directory", None))
        self.outputTreebankCollectionButton.setText(QCoreApplication.translate("gui_treebank_parser", u"Select", None))
#if QT_CONFIG(tooltip)
        self.sentenceConsistencyCheckBox.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.sentenceConsistencyCheckBox.setText(QCoreApplication.translate("gui_treebank_parser", u"Keep consistency of sentences", None))
        self.inputTabSelector.setTabText(self.inputTabSelector.indexOf(self.treebankCollectionTab), QCoreApplication.translate("gui_treebank_parser", u"Treebank collection", None))
        self.label.setText(QCoreApplication.translate("gui_treebank_parser", u"Choose a format", None))
        self.treebankFormatSelector.setItemText(0, "")

        self.label_2.setText(QCoreApplication.translate("gui_treebank_parser", u"Actions available for format", None))
        self.label_4.setText("")
        self.actionAddButton.setText(QCoreApplication.translate("gui_treebank_parser", u"Add", None))
        self.actionRemoveButton.setText(QCoreApplication.translate("gui_treebank_parser", u"Remove", None))
        self.label_3.setText(QCoreApplication.translate("gui_treebank_parser", u"Actions to be applied", None))
        ___qtablewidgetitem = self.chosenActionTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("gui_treebank_parser", u"Option", None));
        ___qtablewidgetitem1 = self.chosenActionTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("gui_treebank_parser", u"Value", None));
        ___qtablewidgetitem2 = self.chosenActionTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("gui_treebank_parser", u"Value Type", None));
        self.runTreebankParser.setText(QCoreApplication.translate("gui_treebank_parser", u"Run", None))
        self.lalReleaseCheckBox.setText(QCoreApplication.translate("gui_treebank_parser", u"Use laloptimized", None))
        self.lalDebugCheckBox.setText(QCoreApplication.translate("gui_treebank_parser", u"Use lal", None))
#if QT_CONFIG(tooltip)
        self.label_7.setToolTip(QCoreApplication.translate("gui_treebank_parser", u"Output logging messages showing the progress of the script. The higher the debugging level the more messages will be displayed.\n"
"* 0: display only 'error' and 'critical' messages.\n"
"* 1: messages from 0 plus 'warning' messages.\n"
"* 2: messages from 1 plus 'info' messages.\n"
"* 3: messages from 2 plus 'debug' messages.", None))
#endif // QT_CONFIG(tooltip)
        self.label_7.setText(QCoreApplication.translate("gui_treebank_parser", u"        Logging messages level", None))
        self.pushButton.setText(QCoreApplication.translate("gui_treebank_parser", u"Clear log messages", None))
        self.only_menu.setTitle(QCoreApplication.translate("gui_treebank_parser", u"Help", None))
    # retranslateUi

