#!/usr/bin/python3

# Import all necessary modules
import sys
import PyQt5.QtGui as qgui
import PyQt5.QtCore as qcore
import PyQt5.QtWidgets as qwid

################################## MAIN WINDOW ##################################

class mainWindow(qwid.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set style sheets for all widgets used
        self.setStyleSheet(".QPushButton { font-size: 11pt;}"
                           ".QTabBar { font-size: 10pt;}"
                           ".QLabel { font-size: 10pt;}"
                           ".QCheckBox { font-size: 10pt;}"
                           ".QRadioButton { font-size: 10pt;}"
                           ".QSpinBox { font-size: 10pt;}"
                           ".QLineEdit { font-size: 10pt;}"
                           ".QComboBox { font-size: 10pt;}")

        self.setFixedSize(550, 650)
        self.initUI()

    def initUI(self):
        # Initialize tab screen
        self.tabs = qwid.QTabWidget(self)
        self.tabs.resize(530, 590)
        self.tabs.move(10, 10)

        # Four widgets for four tabs
        self.tabProg = qwid.QWidget()
        self.tabDomain = qwid.QWidget()
        self.tabSolver = qwid.QWidget()
        self.tabMG = qwid.QWidget()

        self.tabs.addTab(self.tabProg, "Program")
        self.tabs.addTab(self.tabDomain, "Domain")
        self.tabs.addTab(self.tabSolver, "Solver")
        self.tabs.addTab(self.tabMG, "Multigrid")

        self.fillProgTab()
        self.fillDomainTab()
        self.fillSolverTab()
        self.fillMGTab()

        # Generate button - to generate the YAML
        startButton = qwid.QPushButton('Generate', self)
        startButton.clicked.connect(self.startSolver)
        startButton.resize(startButton.sizeHint())
        startButton.move(350, 610)

        # Quit button - to quit the program :(
        quitButton = qwid.QPushButton('Quit', self)
        quitButton.clicked.connect(self.close)
        quitButton.resize(quitButton.sizeHint())
        quitButton.move(450, 610)

        # Window title and icon
        self.setWindowTitle('SARAS')
        self.setWindowIcon(qgui.QIcon('icon.png'))

        # Reveal thyself
        self.show()


    # This function fills the widgets in the Program tab
    def fillProgTab(self):
        ########### HBox Layout for Solver Variables ###########
        pTypLayout = qwid.QHBoxLayout()
        pTypLayout.setContentsMargins(10,8,10,8)
        pTypLayout.setSpacing(5)

        pTypLayout.addWidget(qwid.QLabel("Problem Type", self.tabProg), 1)
        pTypRButGroup = qwid.QButtonGroup(self)

        self.pTypHydRadBut = qwid.QRadioButton("Hydro", self.tabProg)
        self.pTypTheRadBut = qwid.QRadioButton("Thermal", self.tabProg)
        self.pTypHydRadBut.setChecked(True)

        pTypRButGroup.addButton(self.pTypHydRadBut)
        pTypRButGroup.addButton(self.pTypTheRadBut)

        pTypLayout.addStretch(1)
        pTypLayout.addWidget(self.pTypHydRadBut, 1)
        pTypLayout.addWidget(self.pTypTheRadBut, 1)

        ########### Grid Layout for five line edits ###########
        gLayout = qwid.QGridLayout()
        gLayout.setColumnStretch(0, 3)
        gLayout.setColumnStretch(1, 1)
        gLayout.setContentsMargins(10,8,10,8)

        # Widgets to get non-dimensional constants
        gLayout.addWidget(qwid.QLabel("Reynolds Number", self.tabProg), 0, 0)
        self.reLEdit = qwid.QLineEdit(self.tabProg)
        gLayout.addWidget(self.reLEdit, 0, 1)

        gLayout.addWidget(qwid.QLabel("Rayleigh Number", self.tabProg), 1, 0)
        self.raLEdit = qwid.QLineEdit(self.tabProg)
        gLayout.addWidget(self.raLEdit, 1, 1)

        gLayout.addWidget(qwid.QLabel("Prandtl Number", self.tabProg), 2, 0)
        self.prLEdit = qwid.QLineEdit(self.tabProg)
        gLayout.addWidget(self.prLEdit, 2, 1)

        gLayout.addWidget(qwid.QLabel("Rossby Number", self.tabProg), 3, 0)
        self.roLEdit = qwid.QLineEdit(self.tabProg)
        gLayout.addWidget(self.roLEdit, 3, 1)

        gLayout.addWidget(qwid.QLabel("Taylor Number", self.tabProg), 4, 0)
        self.taLEdit = qwid.QLineEdit(self.tabProg)
        gLayout.addWidget(self.taLEdit, 4, 1)

        ########### Add everything to the main Layout ###########
        vbLayout = qwid.QVBoxLayout()
        vbLayout.setContentsMargins(15,22,15,150)
        vbLayout.setSpacing(22)

        vbLayout.addLayout(pTypLayout)
        vbLayout.addLayout(gLayout)

        self.tabProg.setLayout(vbLayout)


    # This function fills the widgets in the Domain tab
    def fillDomainTab(self):
        ########### Grid Layout for first three Spin Boxes ###########
        gLayout = qwid.QGridLayout()
        gLayout.setColumnStretch(0, 1)
        gLayout.setColumnStretch(1, 3)
        gLayout.setColumnStretch(2, 3)
        gLayout.setColumnStretch(3, 2)
        gLayout.setColumnStretch(4, 2)
        gLayout.setColumnStretch(5, 2)
        gLayout.setColumnStretch(6, 2)

        gLayout.setRowStretch(0, 1)
        gLayout.setRowStretch(1, 1)
        gLayout.setRowStretch(2, 1)
        gLayout.setRowStretch(3, 1)

        gLayout.addWidget(qwid.QLabel("X", self.tabDomain), 1, 0)
        gLayout.addWidget(qwid.QLabel("Y", self.tabDomain), 2, 0)
        gLayout.addWidget(qwid.QLabel("Z", self.tabDomain), 3, 0)

        gLayout.addWidget(qwid.QLabel("Length", self.tabDomain), 0, 1)
        self.xLenLEdit = qwid.QLineEdit("1.0", self.tabDomain)
        self.yLenLEdit = qwid.QLineEdit("1.0", self.tabDomain)
        self.zLenLEdit = qwid.QLineEdit("1.0", self.tabDomain)
        gLayout.addWidget(self.xLenLEdit, 1, 1)
        gLayout.addWidget(self.yLenLEdit, 2, 1)
        gLayout.addWidget(self.zLenLEdit, 3, 1)

        gLayout.addWidget(qwid.QLabel("Points", self.tabDomain), 0, 2)
        self.xPtsSBox = qwid.QSpinBox(self.tabDomain)
        self.yPtsSBox = qwid.QSpinBox(self.tabDomain)
        self.zPtsSBox = qwid.QSpinBox(self.tabDomain)
        self.xPtsSBox.setMinimum(2);    self.xPtsSBox.setMaximum(16384)
        self.yPtsSBox.setMinimum(2);    self.yPtsSBox.setMaximum(16384)
        self.zPtsSBox.setMinimum(2);    self.zPtsSBox.setMaximum(16384)
        gLayout.addWidget(self.xPtsSBox, 1, 2)
        gLayout.addWidget(self.yPtsSBox, 2, 2)
        gLayout.addWidget(self.zPtsSBox, 3, 2)

        gLayout.addWidget(qwid.QLabel("Periodic", self.tabDomain), 0, 3)
        self.xPerChBox = qwid.QCheckBox(self.tabDomain)
        self.yPerChBox = qwid.QCheckBox(self.tabDomain)
        self.zPerChBox = qwid.QCheckBox(self.tabDomain)
        self.xPerChBox.setStyleSheet("margin-left:15%; margin-right:5%;")
        self.yPerChBox.setStyleSheet("margin-left:15%; margin-right:5%;")
        self.zPerChBox.setStyleSheet("margin-left:15%; margin-right:5%;")
        gLayout.addWidget(self.xPerChBox, 1, 3)
        gLayout.addWidget(self.yPerChBox, 2, 3)
        gLayout.addWidget(self.zPerChBox, 3, 3)

        gLayout.addWidget(qwid.QLabel("Uniform", self.tabDomain), 0, 4)
        self.xUnifChBox = qwid.QCheckBox(self.tabDomain)
        self.yUnifChBox = qwid.QCheckBox(self.tabDomain)
        self.zUnifChBox = qwid.QCheckBox(self.tabDomain)
        self.xUnifChBox.setStyleSheet("margin-left:15%; margin-right:5%;")
        self.yUnifChBox.setStyleSheet("margin-left:15%; margin-right:5%;")
        self.zUnifChBox.setStyleSheet("margin-left:15%; margin-right:5%;")
        gLayout.addWidget(self.xUnifChBox, 1, 4)
        gLayout.addWidget(self.yUnifChBox, 2, 4)
        gLayout.addWidget(self.zUnifChBox, 3, 4)

        gLayout.addWidget(qwid.QLabel("Beta", self.tabDomain), 0, 5)
        self.xBetaLEdit = qwid.QLineEdit("1.0", self.tabDomain)
        self.yBetaLEdit = qwid.QLineEdit("1.0", self.tabDomain)
        self.zBetaLEdit = qwid.QLineEdit("1.0", self.tabDomain)
        gLayout.addWidget(self.xBetaLEdit, 1, 5)
        gLayout.addWidget(self.yBetaLEdit, 2, 5)
        gLayout.addWidget(self.zBetaLEdit, 3, 5)

        gLayout.addWidget(qwid.QLabel("Processors", self.tabDomain), 0, 6)
        self.xProcsSBox = qwid.QSpinBox(self.tabDomain)
        self.yProcsSBox = qwid.QSpinBox(self.tabDomain)
        self.zProcsSBox = qwid.QSpinBox(self.tabDomain)
        self.xProcsSBox.setMinimum(1);    self.xProcsSBox.setMaximum(2048)
        self.yProcsSBox.setMinimum(1);    self.yProcsSBox.setMaximum(2048)
        self.zProcsSBox.setMinimum(1);    self.zProcsSBox.setMaximum(2048)
        gLayout.addWidget(self.xProcsSBox, 1, 6)
        gLayout.addWidget(self.yProcsSBox, 2, 6)
        gLayout.addWidget(self.zProcsSBox, 3, 6)

        ########### HBox Layout for OpenMP Threads ###########
        ompLayout = qwid.QHBoxLayout()
        ompLayout.setContentsMargins(15,18,15,18)

        # Widgets to set Successive Over Relaxation parameter
        ompLayout.addWidget(qwid.QLabel("Number of OpenMP Threads", self.tabDomain), 3)

        self.openMPSBox = qwid.QSpinBox(self.tabDomain)
        self.openMPSBox.setAlignment(qcore.Qt.AlignRight)
        self.openMPSBox.setMinimum(1);    self.openMPSBox.setMaximum(128)
        ompLayout.addWidget(self.openMPSBox, 1)

        ########### Add everything to the main Layout ###########
        vbLayout = qwid.QVBoxLayout()
        vbLayout.setContentsMargins(15,22,15,340)
        vbLayout.setSpacing(15)

        vbLayout.addLayout(gLayout)
        vbLayout.addLayout(ompLayout)

        self.tabDomain.setLayout(vbLayout)


    # This function fills the widgets in the Solver tab
    def fillSolverTab(self):
        ########### HBox Layout for Differentiation Order ###########
        ordLayout = qwid.QHBoxLayout()
        ordLayout.setContentsMargins(10,5,10,5)
        ordLayout.setSpacing(3)

        ordLayout.addWidget(qwid.QLabel("Order of Differentiation", self.tabSolver), 1)
        ordRButLayout = qwid.QVBoxLayout()
        ordRButGroup = qwid.QButtonGroup(self)

        self.ord2ndRadBut = qwid.QRadioButton("2nd Order", self.tabSolver)
        self.ord4thRadBut = qwid.QRadioButton("4th Order", self.tabSolver)
        self.ord2ndRadBut.setChecked(True)

        ordRButGroup.addButton(self.ord2ndRadBut)
        ordRButLayout.addWidget(self.ord2ndRadBut, 1)

        ordRButGroup.addButton(self.ord4thRadBut)
        ordRButLayout.addWidget(self.ord4thRadBut, 1)

        ordLayout.addLayout(ordRButLayout, 1)

        ########### HBox Layout for Integration Scheme ###########
        intLayout = qwid.QHBoxLayout()
        intLayout.setContentsMargins(10,5,10,5)
        intLayout.setSpacing(3)

        intLayout.addWidget(qwid.QLabel("Integration Scheme", self.tabSolver), 1)
        intRButLayout = qwid.QVBoxLayout()
        intRButGroup = qwid.QButtonGroup(self)

        self.intCNRadBut = qwid.QRadioButton("Euler-Crank-Nicholson", self.tabSolver)
        self.intRKRadBut = qwid.QRadioButton("Low-Storage Runge-Kutta", self.tabSolver)
        self.intCNRadBut.setChecked(True)

        intRButGroup.addButton(self.intCNRadBut)
        intRButLayout.addWidget(self.intCNRadBut, 1)

        intRButGroup.addButton(self.intRKRadBut)
        intRButLayout.addWidget(self.intRKRadBut, 1)

        intLayout.addLayout(intRButLayout, 1)

        ########### HBox Layout for Non-Linear Term ###########
        nltLayout = qwid.QHBoxLayout()
        nltLayout.setContentsMargins(10,5,10,5)
        nltLayout.setSpacing(3)

        nltLayout.addWidget(qwid.QLabel("Non-Linear Term", self.tabSolver), 1)
        nltRButLayout = qwid.QVBoxLayout()
        nltRButGroup = qwid.QButtonGroup(self)

        self.nltCDiffRadBut = qwid.QRadioButton("Central Difference", self.tabSolver)
        self.nltHUpwdRadBut = qwid.QRadioButton("Hybrid Upwinding", self.tabSolver)
        self.nltMorinRadBut = qwid.QRadioButton("Morinishi Scheme", self.tabSolver)
        self.nltCDiffRadBut.setChecked(True)

        self.nltHUpwdRadBut.toggled.connect(self.upwindCheck)

        nltRButGroup.addButton(self.nltCDiffRadBut)
        nltRButLayout.addWidget(self.nltCDiffRadBut, 1)

        nltRButGroup.addButton(self.nltHUpwdRadBut)
        nltRButLayout.addWidget(self.nltHUpwdRadBut, 1)

        nltRButGroup.addButton(self.nltMorinRadBut)
        nltRButLayout.addWidget(self.nltMorinRadBut, 1)

        nltLayout.addLayout(nltRButLayout, 1)

        ########### HBox Layout for Tuning Upwinding ###########
        upwLayout = qwid.QHBoxLayout()
        upwLayout.setContentsMargins(10,8,10,8)

        self.upPeLabel = qwid.QLabel("Peclet Limit", self.tabSolver)
        self.upPeLEdit = qwid.QLineEdit("2.0", self.tabSolver)
        upwLayout.addWidget(self.upPeLabel, 1)
        upwLayout.addWidget(self.upPeLEdit, 1)

        upwLayout.addStretch(1)

        self.upCBLabel = qwid.QLabel("Central Bias", self.tabSolver)
        self.upCBLEdit = qwid.QLineEdit("0.8", self.tabSolver)
        upwLayout.addWidget(self.upCBLabel, 1)
        upwLayout.addWidget(self.upCBLEdit, 1)

        self.upPeLabel.setEnabled(False)
        self.upPeLEdit.setEnabled(False)
        self.upCBLabel.setEnabled(False)
        self.upCBLEdit.setEnabled(False)

        ########### HBox Layout for Iterative Solver Tolerance ###########
        rbgsLayout = qwid.QHBoxLayout()
        rbgsLayout.setContentsMargins(10,8,10,8)

        rbgsLayout.addWidget(qwid.QLabel("Tolerance in iterative solvers of predictors", self.tabSolver), 3)

        self.rbgstLEdit = qwid.QLineEdit("1e-5", self.tabSolver)
        self.rbgstLEdit.setAlignment(qcore.Qt.AlignRight)
        rbgsLayout.addWidget(self.rbgstLEdit, 1)

        ########### HBox Layout for CFL Condition ###########
        cflLayout = qwid.QHBoxLayout()
        cflLayout.setContentsMargins(10,5,10,5)

        # A Frame widget containing widgets to enable or disable CFL condition
        cflFrame = qwid.QFrame(self.tabSolver)
        cflFrame.setFrameStyle(qwid.QFrame.StyledPanel)
        cflFrame.setLayout(cflLayout)

        # Check box to enable CFL condition
        self.cflCondChBox = qwid.QCheckBox("Enable CFL Condition", self.tabSolver)
        self.cflCondChBox.setToolTip("<p>If enabled,the solver will use given CFL number to adjust time-step<\p>")
        cflLayout.addWidget(self.cflCondChBox, 3)
        self.cflCondChBox.stateChanged.connect(self.cflCondCheck)

        # Widgets to get the CFL number
        self.cflLabel = qwid.QLabel("Courant Number", self.tabSolver)
        self.cflLabel.setEnabled(False)
        cflLayout.addWidget(self.cflLabel, 1)

        self.cflLEdit = qwid.QLineEdit("0.5", self.tabSolver)
        self.cflLEdit.setToolTip("<p>Ideally Courant number should be less than 1<\p>")
        self.cflLEdit.setAlignment(qcore.Qt.AlignRight)
        self.cflLEdit.setEnabled(False)
        cflLayout.addWidget(self.cflLEdit, 1)

        ########### HBox Layout for Time-Step Details ###########
        tStpLayout = qwid.QHBoxLayout()
        tStpLayout.setContentsMargins(10,10,10,5)

        tStpLayout.addWidget(qwid.QLabel("Time-Step", self.tabSolver), 1)
        self.tStpLEdit = qwid.QLineEdit("1e-3", self.tabSolver)
        tStpLayout.addWidget(self.tStpLEdit, 1)

        tStpLayout.addStretch(1)

        tStpLayout.addWidget(qwid.QLabel("Final Time", self.tabSolver), 1)
        self.tMaxLEdit = qwid.QLineEdit("10.0", self.tabSolver)
        tStpLayout.addWidget(self.tMaxLEdit, 1)

        tStpLayout.addStretch(1)

        tStpLayout.addWidget(qwid.QLabel("I/O Count", self.tabSolver), 1)
        self.iCntSBox = qwid.QSpinBox(self.tabSolver)
        self.iCntSBox.setMinimum(1)
        tStpLayout.addWidget(self.iCntSBox, 1)

        ########### HBox Layout for File I/O Intervals ###########
        fIOLayout = qwid.QHBoxLayout()
        fIOLayout.setContentsMargins(10,10,10,5)

        fIOLayout.addWidget(qwid.QLabel("Solution Write Interval", self.tabSolver), 1)
        self.swIntLEdit = qwid.QLineEdit("1e-3", self.tabSolver)
        fIOLayout.addWidget(self.swIntLEdit, 1)

        fIOLayout.addStretch(1)

        fIOLayout.addWidget(qwid.QLabel("Restart Write Interval", self.tabSolver), 1)
        self.rwIntLEdit = qwid.QLineEdit("1e-3", self.tabSolver)
        fIOLayout.addWidget(self.rwIntLEdit, 1)

        ########### HBox Layout for Solution Format ###########
        fFormLayout = qwid.QHBoxLayout()
        fFormLayout.setContentsMargins(10,10,10,5)

        fFormLayout.addWidget(qwid.QLabel("Solution Format", self.tabSolver), 1)
        fFormRButGroup = qwid.QButtonGroup(self)

        self.fSarRadBut = qwid.QRadioButton("SARAS", self.tabSolver)
        self.fTarRadBut = qwid.QRadioButton("TARANG", self.tabSolver)
        self.fSarRadBut.setChecked(True)

        fFormRButGroup.addButton(self.fSarRadBut)
        fFormRButGroup.addButton(self.fTarRadBut)

        fFormLayout.addStretch(1)
        fFormLayout.addWidget(self.fSarRadBut, 1)
        fFormLayout.addWidget(self.fTarRadBut, 1)

        ########### HBox Layout for Probe Details ###########
        probeLayout = qwid.QHBoxLayout()
        probeLayout.setContentsMargins(10,5,10,5)

        # A Frame widget containing widgets to enable or disable probes
        probeFrame = qwid.QFrame(self.tabSolver)
        probeFrame.setFrameStyle(qwid.QFrame.StyledPanel)
        probeFrame.setLayout(probeLayout)

        # Check box to enable probes
        self.probeCondChBox = qwid.QCheckBox("Record Probes", self.tabSolver)
        probeLayout.addWidget(self.probeCondChBox, 3)
        self.probeCondChBox.stateChanged.connect(self.probeCondCheck)

        # Widgets to get probe interval
        self.probeLabel = qwid.QLabel("Probe Interval", self.tabSolver)
        self.probeLabel.setEnabled(False)
        probeLayout.addWidget(self.probeLabel, 1)

        self.probeLEdit = qwid.QLineEdit("0.5", self.tabSolver)
        self.probeLEdit.setAlignment(qcore.Qt.AlignRight)
        self.probeLEdit.setEnabled(False)
        probeLayout.addWidget(self.probeLEdit, 1)

        ########### Add everything to the main Layout ###########
        vbLayout = qwid.QVBoxLayout()
        vbLayout.setContentsMargins(15,22,15,15)
        vbLayout.setSpacing(7)

        vbLayout.addLayout(ordLayout, 2)
        vbLayout.addLayout(intLayout, 2)
        vbLayout.addLayout(nltLayout, 3)
        vbLayout.addLayout(upwLayout, 1)
        vbLayout.addLayout(rbgsLayout, 1)
        vbLayout.addWidget(cflFrame, 1)
        vbLayout.addLayout(tStpLayout, 1)
        vbLayout.addLayout(fIOLayout, 1)
        vbLayout.addLayout(fFormLayout, 1)
        vbLayout.addWidget(probeFrame, 1)

        self.tabSolver.setLayout(vbLayout)


    # This function fills the widgets in the Multigrid tab
    def fillMGTab(self):
        ########### Grid Layout for first three Spin Boxes ###########
        gLayout = qwid.QGridLayout()
        gLayout.setColumnStretch(0, 3)
        gLayout.setColumnStretch(1, 1)

        # Widgets to get number of V-Cycles
        gLayout.addWidget(qwid.QLabel("Number of V-Cycles to be computed", self.tabMG), 0, 0)

        self.vcSBox = qwid.QSpinBox(self.tabMG)
        self.vcSBox.setMinimum(1)
        self.vcSBox.setMaximum(32)
        gLayout.addWidget(self.vcSBox, 0, 1)

        # Widgets to get number of pre-smoothing iterations
        gLayout.addWidget(qwid.QLabel("Number of pre-smoothing iterations", self.tabMG), 1, 0)

        self.preSBox = qwid.QSpinBox(self.tabMG)
        self.preSBox.setMinimum(1)
        self.preSBox.setMaximum(16)
        gLayout.addWidget(self.preSBox, 1, 1)

        # Widgets to get number of post-smoothing iterations
        gLayout.addWidget(qwid.QLabel("Number of post-smoothing iterations", self.tabMG), 2, 0)

        self.pstSBox = qwid.QSpinBox(self.tabMG)
        self.pstSBox.setMinimum(1)
        self.pstSBox.setMaximum(16)
        gLayout.addWidget(self.pstSBox, 2, 1)

        ########### HBox Layout for Frame regarding solving ###########
        tLayout = qwid.QHBoxLayout()

        # A Frame widget containing widgets to enable or disable solving at coarsest level
        mgSFrame = qwid.QFrame(self.tabMG)
        mgSFrame.setFrameStyle(qwid.QFrame.StyledPanel)
        mgSFrame.setLayout(tLayout)

        # Check box to enable solving at coarsest grid
        self.mgSolveChBox = qwid.QCheckBox("Solve at coarsest grid", self.tabMG)
        self.mgSolveChBox.setToolTip("<p>If enabled,the solver will use Red-Black Gauss Seidel solver at the coarsest multigrid level<\p>")
        tLayout.addWidget(self.mgSolveChBox, 3)
        self.mgSolveChBox.stateChanged.connect(self.mgSolveCheck)

        # Widgets to get the tolerance for solving at coarsest V-Cycle level
        self.mgTolLabel = qwid.QLabel("Tolerance", self.tabMG)
        self.mgTolLabel.setEnabled(False)
        tLayout.addWidget(self.mgTolLabel, 1)

        self.mgTolLEdit = qwid.QLineEdit("1e-4", self.tabMG)
        self.mgTolLEdit.setToolTip("<p>It is best to enter tolerance in scientific notion as shown<\p>")
        self.mgTolLEdit.setAlignment(qcore.Qt.AlignRight)
        self.mgTolLEdit.setEnabled(False)
        tLayout.addWidget(self.mgTolLEdit, 1)

        ########### HBox Layout for Successive Over-Relaxation ###########
        sorLayout = qwid.QHBoxLayout()

        # Widgets to set Successive Over Relaxation parameter
        sorLayout.addWidget(qwid.QLabel("Successive Over Relaxation parameter", self.tabMG), 3)

        self.mgSORLEdit = qwid.QLineEdit("1.2", self.tabMG)
        self.mgSORLEdit.setToolTip("<p>Parameter for Successive Over-Relaxation (SOR) in iterative solver - setting to 1 disables SOR<\p>")
        self.mgSORLEdit.setAlignment(qcore.Qt.AlignRight)
        sorLayout.addWidget(self.mgSORLEdit, 1)

        ########### HBox Layout for Frame regarding residual ###########
        rLayout = qwid.QVBoxLayout()
        rLayout.setContentsMargins(15,18,15,18)
        rLayout.setSpacing(18)

        # A Frame widget containing widgets adjust residual calculation
        mgRFrame = qwid.QFrame(self.tabMG)
        mgRFrame.setFrameStyle(qwid.QFrame.StyledPanel)
        mgRFrame.setLayout(rLayout)

        rTypeLayout = qwid.QHBoxLayout()
        rTypeRButGroup = qwid.QButtonGroup(self)

        self.rtMaxRadBut = qwid.QRadioButton("Max", self.tabMG)
        self.rtAvgRadBut = qwid.QRadioButton("Mean", self.tabMG)
        self.rtRMSRadBut = qwid.QRadioButton("RMS", self.tabMG)
        self.rtMaxRadBut.setChecked(True)

        rTypeLayout.addWidget(qwid.QLabel("Residual Type", self.tabMG), 2)
        rTypeLayout.addWidget(self.rtMaxRadBut, 1)
        rTypeLayout.addWidget(self.rtAvgRadBut, 1)
        rTypeLayout.addWidget(self.rtRMSRadBut, 1)

        rTypeRButGroup.addButton(self.rtMaxRadBut)
        rTypeRButGroup.addButton(self.rtAvgRadBut)
        rTypeRButGroup.addButton(self.rtRMSRadBut)

        rLayout.addLayout(rTypeLayout)

        rValLayout = qwid.QHBoxLayout()
        rValLayout.addWidget(qwid.QLabel("Tolerance value for residual", self.tabMG), 2)
        rValLayout.addWidget(qwid.QLineEdit("1e-4", self.tabMG), 1)

        rLayout.addLayout(rValLayout)

        # Check box to enable printing of residual
        pResLayout = qwid.QHBoxLayout()
        self.mgPRChBox = qwid.QCheckBox("Print Residual", self.tabMG)
        self.mgPRChBox.setToolTip("<p>If enabled,the solver will print the residual at each V-Cycle. Used only for debugging<\p>")
        pResLayout.addWidget(self.mgPRChBox)

        rLayout.addLayout(pResLayout)

        vbLayout = qwid.QVBoxLayout()
        vbLayout.setContentsMargins(15,22,15,150)
        vbLayout.setSpacing(22)

        vbLayout.addLayout(gLayout)
        vbLayout.addWidget(mgSFrame)
        vbLayout.addLayout(sorLayout)
        vbLayout.addWidget(mgRFrame)

        self.tabMG.setLayout(vbLayout)


    # This function enables or disables the widgets used for fine-tuning
    # upwinding scheme when it is enabled for non-linear term calculations
    def upwindCheck(self):
        if self.nltHUpwdRadBut.isChecked() == True:
            self.upPeLabel.setEnabled(True)
            self.upPeLEdit.setEnabled(True)
            self.upCBLabel.setEnabled(True)
            self.upCBLEdit.setEnabled(True)
        else:
            self.upPeLabel.setEnabled(False)
            self.upPeLEdit.setEnabled(False)
            self.upCBLabel.setEnabled(False)
            self.upCBLEdit.setEnabled(False)

    # This function enables or disables the widgets used to get probe details
    def probeCondCheck(self):
        if self.probeCondChBox.isChecked() == True:
            self.probeLabel.setEnabled(True)
            self.probeLEdit.setEnabled(True)
        else:
            self.probeLabel.setEnabled(False)
            self.probeLEdit.setEnabled(False)

    # This function enables or disables the widgets used to get Courant number
    def cflCondCheck(self):
        if self.cflCondChBox.isChecked() == True:
            self.cflLabel.setEnabled(True)
            self.cflLEdit.setEnabled(True)
        else:
            self.cflLabel.setEnabled(False)
            self.cflLEdit.setEnabled(False)

    # This function enables or disables the LineEdit used to enter the tolerance
    # for Red-Black Gauss-Seidel solver in the multigrid solver
    # This decision is based on the state of the CheckBox for solving at coarses level.
    def mgSolveCheck(self):
        if self.mgSolveChBox.isChecked() == True:
            self.mgTolLabel.setEnabled(True)
            self.mgTolLEdit.setEnabled(True)
        else:
            self.mgTolLabel.setEnabled(False)
            self.mgTolLEdit.setEnabled(False)

    # This function enables or disables the LineEdit used to enter the tangent-hyperbolic
    # grid stretching parameter, beta.
    # This decision is based on the state of the CheckBox for non-uniform grid.
    def nuGridCheck(self):
        if self.nugChBox.isChecked() == True:
            self.betLabel.setEnabled(True)
            self.betLEdit.setEnabled(True)
        else:
            self.betLabel.setEnabled(False)
            self.betLEdit.setEnabled(False)

    # This function interfaces with the multi-grid solver and sets its parameters.
    # These parameters are read from the inputs given in the window.
    # It then opens the console window and hands the baton to it.
    def startSolver(self):
        tolValue = 0.0
        # Check if tolerance specified is valid
        try:
            tolValue = float(self.tolLEdit.text())
        except:
            errDialog = qwid.QMessageBox.critical(self, 'Invalid Tolerance', "The specified tolerance is not a valid floating point number! :(", qwid.QMessageBox.Ok)
            return 1

        # Open console window and run the solver
        self.cWindow = consoleWindow()
        self.cWindow.runSolver()

    # Clingy function for a clingy app - makes sure that the user wants to quit the app
    def closeEvent(self, event):
        reply = qwid.QMessageBox.question(self, 'Close Window', "Are you sure?", qwid.QMessageBox.Yes | qwid.QMessageBox.No, qwid.QMessageBox.No)

        if reply == qwid.QMessageBox.Yes:
            try:
                self.cWindow.close()
            except:
                pass

            event.accept()
        else:
            event.ignore()

############################### CONSOLE WINDOW ##################################

class consoleWindow(qwid.QMainWindow):
    def __init__(self):
        super().__init__()

        # Three boolean flags for the three check boxes in the main window for plots
        # Set to true since the elements have been removed
        self.sPlot = True
        self.ePlot = True
        self.rPlot = True

        self.setFixedSize(400, 400)
        self.initUI()

    def initUI(self):
        # Text box to output console stream
        self.conTEdit = qwid.QTextEdit(self)
        self.conTEdit.resize(340, 300)
        self.conTEdit.move(30, 30)

        # Plot button
        plotButton = qwid.QPushButton('Plot', self)
        plotButton.resize(plotButton.sizeHint())
        plotButton.move(165, 350)

        # The plot button will be disabled if none of the check boxes in main window are checked
        if (self.sPlot or self.ePlot or self.rPlot):
            plotButton.setEnabled(True)
        else:
            plotButton.setEnabled(False)

        # Close button
        closeButton = qwid.QPushButton('Close', self)
        closeButton.clicked.connect(self.close)
        closeButton.resize(closeButton.sizeHint())
        closeButton.move(275, 350)

        # Window title and icon
        self.setWindowTitle('MG-Lite Console Output')
        self.setWindowIcon(qgui.QIcon('icon.png'))

        # Reveal thyself
        self.show()

    # As the function name says, it calls the main() of the MG solver
    def runSolver(self):
        #mgSolver.main(self)
        qwid.QApplication.processEvents()

    # This function is called by the MG solver at all places where it normally uses the print()
    # command. The string passed to the print command is instead passed to this function,
    # which sends it to the text box of the console window.
    def updateTEdit(self, cOutString):
        self.conTEdit.append(cOutString)
        qwid.QApplication.processEvents()


############################## THAT'S IT, FOLKS!! ###############################

if __name__ == '__main__':
    app = qwid.QApplication(sys.argv)
    welWindow = mainWindow()

    sys.exit(app.exec_())
