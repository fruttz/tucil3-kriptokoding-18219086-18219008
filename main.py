import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDial, QDialog, QApplication, QStackedWidget, QFileDialog
from hashlib import sha1
import rsa_encrypt

class HomeScreen(QDialog):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi("UI/main.ui", self)

        self.Keygen.clicked.connect(self.to_keygen)
        self.sign.clicked.connect(self.to_sign)
        self.verify.clicked.connect(self.to_verify)
    
    def to_keygen(self):
        keygen = KeygenScreen()
        widget.addWidget(keygen)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def to_sign(self):
        sign = SignScreen()
        widget.addWidget(sign)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def to_verify(self):
        verify = VerifyScreen()
        widget.addWidget(verify)
        widget.setCurrentIndex(widget.currentIndex()+1)

class KeygenScreen(QDialog):
    def __init__(self):
        super(KeygenScreen, self).__init__()
        loadUi("UI/Keygen.ui", self)
        self.rsa = rsa_encrypt.RSA()

        self.generateKeyButton.clicked.connect(self.generate_key)
        self.saveKeyButton.clicked.connect(self.save_key)
        self.loadEKey.clicked.connect(self.load_public_key)
        self.loadDKey.clicked.connect(self.load_private_key)
        self.backButton.clicked.connect(back)
        
    def generate_key(self):
        self.rsa.generate_key()
        self.nKey.setText(str(self.rsa.n))
        self.eKey.setText(str(self.rsa.e))
        self.dKey.setText(str(self.rsa.d))
    
    def save_key(self):
        try:
            n = int(self.nKey.toPlainText())
            e = int(self.eKey.toPlainText())
            d = int(self.dKey.toPlainText())
            name = QFileDialog.getSaveFileName(self, 'Save File', "Key/")
            self.rsa.save_key(name[0], e, n, d)
        except:
            self.warning_msg("Wrong Key!", "Key must be integer")
    
    def load_public_key(self):
        fname = QFileDialog().getOpenFileName(None, "Load Public Key", "Key/", "PublicKey (*.pub)")
        if(fname[0] == ''):
            self.warning_msg("Error","Please choose key file!")
        else:
            with open(fname[0], "r") as file:
                key = file.read().split(" ")
            self.nKey.setText(key[1])
            self.eKey.setText(key[0])
    
    def load_private_key(self):
        fname = QFileDialog().getOpenFileName(None, "Load Private Key", "Key/", "PrivateKey (*.pri)")
        if(fname[0] == ''):
            self.warning_msg("Error","Please choose key file!")
        else:
            with open(fname[0], "r") as file:
                key = file.read().split(" ")
            self.nKey.setText(key[1])
            self.dKey.setText(key[0])
    
class SignScreen(QDialog):
    def __init__(self):
        super(SignScreen, self).__init__()
        loadUi("UI/Sign.ui", self)
        self.mode = "sign"
        self.message = ""
        self.outputPath = ""
        self.key = ""
        self.curve = ""
        self.keyboard = False
        self.infile = False
        self.rsa = rsa_encrypt.RSA() 

        self.fileRadio.toggled.connect(self.toggle_file_radio)
        self.keyboardRadio.toggled.connect(self.toggle_keyboard_radio)
        self.SeparateFile.toggled.connect(self.toggle_separate_file)
        self.InsideFile.toggled.connect(self.toggle_inside_file)
        self.messageFileButton.clicked.connect(self.browse_input)
        self.goButton.clicked.connect(self.sign_message)
        self.loadDKey.clicked.connect(self.load_private_key)
        self.backButton.clicked.connect(back)
        self.nKey.setReadOnly(False)
        self.dKey.setReadOnly(False)
    
    def browse_input(self):
        f = QFileDialog.getOpenFileName(
            self, 'Open File', 'Desktop'
        )
        self.inputFileField.setText(f[0])
    
    def load_private_key(self):
        fname = QFileDialog().getOpenFileName(None, "Load Private Key", "Key/", "PrivateKey (*.pri)")
        if(fname[0] == ''):
            self.warning_msg("Error","Please choose key file!")
        else:
            with open(fname[0], "r") as file:
                key = file.read().split(" ")
            self.nKey.setText(key[1])
            self.dKey.setText(key[0])
            self.nKey.setReadOnly(True)
            self.dKey.setReadOnly(True)
    
    def toggle_file_radio(self): 
        self.button_input_state(self.fileRadio)

    def toggle_keyboard_radio(self): 
        self.button_input_state(self.keyboardRadio)

    def toggle_separate_file(self): 
        self.button_input_state2(self.SeparateFile)

    def toggle_inside_file(self): 
        self.button_input_state2(self.InsideFile)
    
    def button_input_state(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(True)
                self.messageFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
                self.keyboard = False
                if self.infile == False:
                    self.outputFileField.setReadOnly(False)
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.messageFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")
                self.keyboard = True
                self.outputFileField.setReadOnly(False)
        
    def button_input_state2(self, b):
        if b.text() == "Separate File":
            if b.isChecked():
                self.signatureLocation = "Separate File"
                self.infile = False
                self.outputFileField.setReadOnly(False)
        elif b.text() == "Inside File":
            if b.isChecked():
                self.signatureLocation = "Inside File"
                self.infile = True
                if self.keyboard == False:
                    self.outputFileField.setReadOnly(True)
    
    def get_message(self):
        if (self.fileInputMethod == "File"):
            path = self.inputFileField.text()
            with open(path, "r") as file:
                self.message = file.read()
        else:
            self.message = self.inputKeyboardField.text()
        self.message = self.message.rstrip()
    
    def get_key(self):
        self.key = (
            int(self.nKey.text()),
            int(self.dKey.text())
        )
    
    def get_output_path(self):
        self.outputPath = "Output/" + self.outputFileField.text() + "_signed.txt"
        self.outputMsgPath = "Output/" + self.outputFileField.text() + "_message.txt"
    
    def sign_message(self):
        self.get_message()
        self.get_key()
        self.get_output_path()

        hash_message = int(sha1(self.message.encode()).hexdigest(), 16)
        sign = self.rsa.sign_rsa(hash_message, self.key[1], self.key[0])

        if self.fileInputMethod == 'Keyboard':
            with open(self.outputMsgPath, "w") as f:
                f.write(self.message + '\n')
            
            if self.signatureLocation == "Inside File":
                self.rsa.save_inside(sign, self.outputMsgPath)
            elif self.signatureLocation == "Separate File":
                self.rsa.save_newfile(sign, self.outputPath)
        else:
            if self.signatureLocation == "Inside File":
                self.rsa.save_inside(sign, self.inputFileField.text())
            elif self.signatureLocation == "Separate File":
                self.rsa.save_newfile(sign, self.outputPath)
        self.Status.setText('Signing Success!')

class VerifyScreen(QDialog):
    def __init__(self):
        super(VerifyScreen, self).__init__()
        loadUi("UI/Verify.ui", self)
        self.mode = "verify"
        self.message = ""
        self.outputPath = ""
        self.key = ""
        self.rsa = rsa_encrypt.RSA()

        self.SeparateFile.toggled.connect(self.toggle_separate_file)
        self.InsideFile.toggled.connect(self.toggle_inside_file)
        self.messageFileButton.clicked.connect(self.browse_input_message)
        self.signatureFileButton.clicked.connect(self.browse_input_signature)
        self.goButton.clicked.connect(self.verify_message)
        self.loadEKey.clicked.connect(self.load_public_key)
        self.backButton.clicked.connect(back)
        self.nKey.setReadOnly(False)
        self.eKey.setReadOnly(False)
    
    def toggle_separate_file(self):
        self.button_input_state(self.SeparateFile)
    
    def toggle_inside_file(self):
        self.button_input_state(self.InsideFile)
    
    def browse_input_message(self):
        m_file = QFileDialog.getOpenFileName(self, 'Open File', 'Output/')
        self.messageField.setText(m_file[0])
    
    def load_public_key(self):
        fname = QFileDialog().getOpenFileName(None, "Load Public Key", "Key/", "PublicKey (*.pub)")
        if(fname[0] == ''):
            self.warning_msg("Error","Please choose key file!")
        else:
            with open(fname[0], "r") as file:
                key = file.read().split(" ")
            self.nKey.setText(key[1])
            self.eKey.setText(key[0])
            self.nKey.setReadOnly(True)
            self.eKey.setReadOnly(True)
    
    def browse_input_signature(self):
        s_file = QFileDialog.getOpenFileName(self, "Open File", "Desktop")
        self.signatureFileField.setText(s_file[0])
    
    def button_input_state(self, b):
        if b.text() == "Separate File":
            if b.isChecked():
                self.messageFileButton.setEnabled(True)
                self.signatureFileButton.setEnabled(True)
                self.signatureLocation = "Separate File"
        elif b.text() == "Inside File":
            if b.isChecked():
                self.messageFileButton.setEnabled(True)
                self.signatureFileButton.setEnabled(False)
                self.signatureLocation = "Inside File"
                self.signatureFileField.setText("")
    
    def get_message(self):
        if self.signatureLocation == "Separate File":
            self.message, self.signature = self.rsa.read_newfile(self.messageField.text(), self.signatureFileField.text())
        elif self.signatureLocation == "Inside File":
            self.message, self.signature = self.rsa.read_inside(self.messageField.text())
    
    def get_key(self):
       self.key = (
            int(self.nKey.text()),
            int(self.eKey.text())
        )
    
    def verify_message(self):
        self.get_message()
        self.get_key()

        hash_message = int(sha1(self.message.encode()).hexdigest(), 16)

        if (self.nKey.text() != "" and self.eKey.text() != ""):
            verify = self.rsa.verify_rsa(self.signature, self.key[1], self.key[0], hash_message)

            if verify:
                self.Status.setText('Verification Success!')
            else:
                self.Status.setText('Verification Failed!')
        else:
            self.Status.setText('Signature not found!')

def back():
    widget.removeWidget(widget.currentWidget())

app = QApplication(sys.argv)
widget = QStackedWidget()

home = HomeScreen()

widget.addWidget(home)
widget.setFixedWidth(1000)
widget.setFixedHeight(720)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")


    



        

    

    

    






