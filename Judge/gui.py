import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap

from login_request import authenticate_judge


class App(QWidget):

    def __init__(self,channel,host):
        super().__init__()
        try:
            self.title = 'BitsOJ Judge'
            self.setWindowTitle(self.title)
            self.resize(700,600)
            self.setWindowIcon(QIcon('./Assets/logo.png'))

            # Frame Geometry
            qtRectangle = self.frameGeometry()
            centerPoint = QDesktopWidget().availableGeometry().center()
            qtRectangle.moveCenter(centerPoint)     
            self.move(qtRectangle.topLeft())


            # Title of login window
            self.title = QLabel("<<BitsOJ>>")
            self.title.setObjectName('header')
            self.title.setFixedWidth(400)
            self.title.setFixedHeight(150)


            # Creating input fields

            # Username field
            self.judge_id = QLineEdit(self)
            self.judge_id.setFixedWidth(400)
            self.judge_id.setFixedHeight(50)
            self.judge_id.setPlaceholderText('Judge ID')

            # Password field
            self.password = QLineEdit(self)
            self.password.setFixedWidth(400)
            self.password.setFixedHeight(50)
            self.password.setPlaceholderText('Password')
            self.password.setEchoMode(QLineEdit.Password)

            # Button to login
            self.login_button = QPushButton('Login', self)
            self.login_button.setFixedWidth(300)
            self.login_button.setFixedHeight(80)
            self.login_button.clicked.connect(self.login_handler(channel,host))
            self.login_button.setDefault(True)
            self.login_button.setObjectName('login')

            # Creating  Vertical layout 
            layout = QVBoxLayout(self)

            # Adding widget to Layout
            layout.addWidget(self.title)
            layout.addWidget(self.judge_id)
            layout.addWidget(self.password)
            layout.addWidget(self.login_button)

            layout.setContentsMargins(150, 0, 0, 50)


            self.setLayout(layout)
            self.setObjectName('loginwindow')
            self.show()

        except Exception as e:
            print(e)
        return 

    # def onClick(self):
    #     print("button clicked")


    def login_handler(self,channel,host):

        if self.judge_id.text() == '' or self.password.text() == '':
            authenticate_judge.login(channel,host)
            status = authenticate_judge.login_status

            if( status == 'VALID'):
                try:
                    QApplication.quit()
                except Exception as error:
                    print('[ ERROR ] Could not exit properly : ' + str(error) )

            # If server is not accepting login request then show an alert
            elif( status == 'LRJCT' ):
                # QMessageBox.warning(self, 'Error', 'Login Rejected by admin.')
                QMessageBox.warning(self, 'Error', 'Login Rejected.\n Please wait.')
            else:
                QMessageBox.warning(self, 'Error', 'Wrong credentials')


        elif (self.judge_id.text() == ''):
            QMessageBox.warning(self, 'Error', 'Username cannot be empty')

        # If password is empty then show an alert
        elif (self.password.text() == ''):
            QMessageBox.warning(self, 'Error', 'Password cannot be empty')

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open('Assets/login.qss', "r").read())
    ex = App()
    ex.show()
    sys.exit(app.exec_())