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
        self.fillMGTab()

        ''' 

        # A Frame widget containing widgets to enable or disable non-uniform grid
        nuFrame = qwid.QFrame(self)
        nuFrame.setFrameStyle(qwid.QFrame.StyledPanel)
        nuFrame.resize(375, 46)
        nuFrame.move(25, 322)

        # Check box to enable non-uniform grid
        self.nugChBox = qwid.QCheckBox("Enable non-uniform grid", self)
        self.nugChBox.setToolTip("<p>Use a tangent-hyperbolic grid which is fine near the boundaries and coarse at the center of the domain<\p>")
        self.nugChBox.resize(self.nugChBox.sizeHint())
        self.nugChBox.move(40, 335)
        self.nugChBox.stateChanged.connect(self.nuGridCheck)

        # Widgets to get the tangent-hyperbolic grid stretching factor, beta
        self.betLabel = qwid.QLabel("Beta", self)
        self.betLabel.setToolTip("<nobr>Stretching parameter for <\nobr>tangent-hyperbolic grid")
        self.betLabel.resize(self.betLabel.sizeHint())
        self.betLabel.setEnabled(False)
        self.betLabel.move(275, 337)

        self.betLEdit = qwid.QLineEdit("0.5", self)
        self.betLEdit.setToolTip("<p>Must be a floating point number greater than 0, but not greater than 3<\p>")
        self.betLEdit.setAlignment(qcore.Qt.AlignRight)
        self.betLEdit.setEnabled(False)
        self.betLEdit.resize(70, 30)
        self.betLEdit.move(322, 330)

        # A few check boxes to decide what should be plotted
        self.solChBox = qwid.QCheckBox("Plot computed and analytical solution", self)
        self.solChBox.resize(self.solChBox.sizeHint())
        self.solChBox.move(30, 382)

        self.errChBox = qwid.QCheckBox("Plot error in computed solution", self)
        self.errChBox.resize(self.errChBox.sizeHint())
        self.errChBox.move(30, 412)

        ''' 

        # Start button - to start the simulation :)
        startButton = qwid.QPushButton('Start', self)
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
        # Widgets to get grid size
        gsLabel = qwid.QLabel("Number of points in the domain", self.tabProg)
        gsLabel.resize(gsLabel.sizeHint())
        gsLabel.move(32, 32)

        self.gsCBox = qwid.QComboBox(self.tabProg)
        self.gsCBox.setToolTip("<p>Grid should have 2^n + 1 points to enable restriction and prolongation during V-Cycles<\p>")
        for i in range(2, 15):
            n = 2**i + 1
            self.gsCBox.addItem(str(n))
        self.gsCBox.currentIndexChanged.connect(self.gsCBoxSelection)
        self.gsCBox.move(295, 25)


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

        vbLayout = qwid.QVBoxLayout()
        vbLayout.setContentsMargins(15,22,15,410)
        vbLayout.setSpacing(15)

        vbLayout.addLayout(gLayout)

        self.tabDomain.setLayout(vbLayout)


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
        rTypeLayout.addWidget(qwid.QLabel("Residual Type", self.tabMG), 2)
        rTypeLayout.addWidget(qwid.QRadioButton("Max", self.tabMG), 1)
        rTypeLayout.addWidget(qwid.QRadioButton("Mean", self.tabMG), 1)
        rTypeLayout.addWidget(qwid.QRadioButton("RMS", self.tabMG), 1)

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


    # This function restricts the maximum value of the SpinBox used to set V-Cycle depth.
    # This maximum value is obtained from the grid-size, passed as an index, i
    def gsCBoxSelection(self, i):
        maxDepth = i + 1
        self.vdSBox.setMaximum(i + 1)

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
        plotButton.clicked.connect(self.plotSolution)
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

    # This function is called by the 'Plot' button when clicked.
    # It merely calls the plotResult() function of the MG solver, with appropriate arguments.
    def plotSolution(self):
        pass
        '''
        if self.sPlot:
            mgSolver.plotResult(0)
        if self.ePlot:
            mgSolver.plotResult(1)
        if self.rPlot:
            mgSolver.plotResult(2)
        '''


############################## THAT'S IT, FOLKS!! ###############################

if __name__ == '__main__':
    app = qwid.QApplication(sys.argv)
    welWindow = mainWindow()

    sys.exit(app.exec_())
