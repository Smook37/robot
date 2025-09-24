# rover_client_gui.py
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGroupBox, QPushButton, QLabel,
    QLineEdit, QSlider, QPlainTextEdit, QHBoxLayout, QVBoxLayout,
    QGridLayout, QSizePolicy, QSpacerItem
)


class RoverClientUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client pour le robot ROVER GEII")
        self.resize(1000, 640)

        cw = QWidget(self)
        self.setCentralWidget(cw)
        root = QGridLayout(cw)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(12)

        # === 1) GROUPE CLIENT =================================================
        self.grpClient = QGroupBox("Client")
        gClient = QGridLayout(self.grpClient)
        gClient.setHorizontalSpacing(10)
        gClient.setVerticalSpacing(8)

        self.lblIp = QLabel("IP du serveur :")
        self.edtIp = QLineEdit("127.0.0.1")
        self.edtIp.setPlaceholderText("ex: 192.168.1.20")

        self.lblPort = QLabel("Port :")
        self.edtPort = QLineEdit("2500")
        self.edtPort.setPlaceholderText("ex: 2500")
        self.edtPort.setMaximumWidth(120)

        self.btnConnect = QPushButton("Connexion")
        self.btnDisconnect = QPushButton("Déconnexion")
        self.btnDisconnect.setEnabled(False)

        # Ligne d’envoi de message manuel
        self.edtMsg = QLineEdit()
        self.edtMsg.setPlaceholderText("Mon message")
        self.btnSend = QPushButton("Envoi message")

        gClient.addWidget(self.lblIp,      0, 0)
        gClient.addWidget(self.edtIp,      0, 1, 1, 2)
        gClient.addWidget(self.lblPort,    1, 0)
        gClient.addWidget(self.edtPort,    1, 1)
        gClient.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 2)
        gClient.addWidget(self.btnConnect, 2, 0, 1, 2)
        gClient.addWidget(self.btnDisconnect, 2, 2)
        gClient.addWidget(self.edtMsg,     3, 0, 1, 2)
        gClient.addWidget(self.btnSend,    3, 2)

        # === 2) GROUPE RÉCEPTION / DEBUG ======================================
        self.grpDebug = QGroupBox("Réception des messages")
        gDebug = QVBoxLayout(self.grpDebug)
        self.txtLog = QPlainTextEdit()
        self.txtLog.setReadOnly(True)
        self.txtLog.setPlaceholderText("Messages reçus, traces et débogage…")
        self.txtLog.setMinimumHeight(180)
        gDebug.addWidget(self.txtLog)

        # === 3) GROUPE PILOTAGE DU ROBOT ======================================
        self.grpPilotage = QGroupBox("Pilotage du Robot")
        gCtrl = QGridLayout(self.grpPilotage)
        gCtrl.setHorizontalSpacing(14)
        gCtrl.setVerticalSpacing(12)

        self.btnLeft  = QPushButton("<-")
        self.btnAv    = QPushButton("Av")
        self.btnRight = QPushButton("->")
        self.btnStop  = QPushButton("STOP")
        self.btnArr   = QPushButton("Arr")

        self.lblVitesse = QLabel("Vitesse :")
        self.sldVitesse = QSlider(Qt.Horizontal)
        self.sldVitesse.setRange(0, 100)
        self.sldVitesse.setValue(50)
        self.lblPct = QLabel("50 %")
        self.lblPct.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lblPct.setMinimumWidth(50)

        # Placement façon “manette”
        gCtrl.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 0)
        gCtrl.addWidget(self.btnAv,    0, 1, 1, 1)
        gCtrl.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 2)

        gCtrl.addWidget(self.btnLeft,  1, 0)
        gCtrl.addWidget(self.btnStop,  1, 1)
        gCtrl.addWidget(self.btnRight, 1, 2)

        gCtrl.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum), 2, 0)
        gCtrl.addWidget(self.btnArr,   2, 1)
        gCtrl.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum), 2, 2)

        # Ligne slider vitesse
        gCtrl.addWidget(self.lblVitesse, 3, 0)
        gCtrl.addWidget(self.sldVitesse, 3, 1)
        gCtrl.addWidget(self.lblPct,     3, 2)

        # === 4) GROUPE CAPTEURS ===============================================
        self.grpCapteurs = QGroupBox("Capteurs")
        gCap = QGridLayout(self.grpCapteurs)
        gCap.setHorizontalSpacing(10)
        gCap.setVerticalSpacing(8)

        self.lblIR1 = QLabel("IR1 : —")
        self.lblIR2 = QLabel("IR2 : —")
        self.lblIR3 = QLabel("IR3 : —")
        self.lblUbat = QLabel("Ubat : —")
        self.lblAngle = QLabel("Angle : —")
        self.lblLRVB = QLabel("L,R,V,B : —")

        self.btnReqCapteurs = QPushButton("Requête Capteurs")

        gCap.addWidget(self.lblIR1,  0, 0)
        gCap.addWidget(self.lblIR2,  1, 0)
        gCap.addWidget(self.lblIR3,  2, 0)
        gCap.addWidget(self.lblUbat, 3, 0)
        gCap.addWidget(self.lblAngle,4, 0)
        gCap.addWidget(self.lblLRVB, 5, 0)
        gCap.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding), 0, 1, 6, 1)
        gCap.addWidget(self.btnReqCapteurs, 6, 0, 1, 2)

        # === Placement des 4 grandes parties en grille 2×2 ====================
        root.addWidget(self.grpClient,   0, 0)
        root.addWidget(self.grpDebug,    0, 1)
        root.addWidget(self.grpPilotage, 1, 0)
        root.addWidget(self.grpCapteurs, 1, 1)

        # Bouton Quitter dans la barre de statut (optionnel)
        self.btnQuit = QPushButton("Quitter")
        self.statusBar().addPermanentWidget(self.btnQuit)

        # === Connexions minimales (sans logique réseau pour l’instant) ========
        self.btnQuit.clicked.connect(self.close)
        self.sldVitesse.valueChanged.connect(self._update_pct)

        # Petites traces pour vérifier que tout marche
        for w in (self.btnConnect, self.btnDisconnect, self.btnSend, self.btnAv,
                  self.btnStop, self.btnArr, self.btnLeft, self.btnRight,
                  self.btnReqCapteurs):
            w.clicked.connect(lambda _, b=w: self._trace(f"[UI] Clic: {b.text()}"))

    # -------------------------- Helpers UI ------------------------------------
    def _update_pct(self, val: int):
        self.lblPct.setText(f"{val} %")

    def _trace(self, msg: str):
        self.txtLog.appendPlainText(msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = RoverClientUI()
    ui.show()
    sys.exit(app.exec_())
