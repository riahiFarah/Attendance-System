import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from subprocess import run

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import shutil
class FirstMenu(QDialog):
    def __init__(self):
        super(FirstMenu,self).__init__()
        loadUi("firstPage.ui",self)
        self.admin.clicked.connect(self.goAdminInterface)
        self.user.clicked.connect(self.goUserInterface)
        
    def goAdminInterface(self):
        login =Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def goUserInterface(self):
        run([sys.executable, 'app.py'])
        
class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginButton.clicked.connect(self.loginFunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.returnMenu.clicked.connect(self.goFirstMenu)
    
    def loginFunction(self):
        username=self.username.text()
        password=self.password.text()
        if(username=="admin" and password=="admin"):
            mainMenu =Menu()
            widget.addWidget(mainMenu)
            widget.setCurrentIndex(widget.currentIndex()+1)
        if len(username)==0 or len(password)==0 :
            self.error.setText("please entre your username and password")
        if len(username)==0 :
            self.error.setText("please entre your username ")
        if len(password)==0 :
            self.error.setText("please entre your password")
        else:
            self.error.setText("username or password is incorrect ")
            
    def goFirstMenu(self):
        firstPage =FirstMenu()
        widget.addWidget(firstPage)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Menu(QDialog):
    def __init__(self):
        super(Menu,self).__init__()
        loadUi("mainMenu.ui",self)
        self.addProfile.clicked.connect(self.goAddProfile)
        self.updateProfile.clicked.connect(self.goUpdateProfile)
        self.deleteProfile.clicked.connect(self.goDeleteProfile)
        self.returnMenu.clicked.connect(self.goFirstMenu)
        
    def goAddProfile(self):
        addProfile =AddProfile()
        widget.addWidget(addProfile)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def goUpdateProfile(self):
        updateProfile =UpdateProfile()
        widget.addWidget(updateProfile)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def goDeleteProfile(self):
        deleteProfile =DeleteProfile()
        widget.addWidget(deleteProfile)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goFirstMenu(self):
        firstPage =FirstMenu()
        widget.addWidget(firstPage)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    
        
##################### Menu content ###############################

#add profile
#ui functionalities
class AddProfile(QDialog):
    def __init__(self):
        super(AddProfile,self).__init__()
        loadUi("addProfile.ui",self)
        self.returnMenu.clicked.connect(self.goMainMenu)
        self.addButton.clicked.connect(self.addNewProfile)
        
    def goMainMenu(self):
        mainMenu =Menu()
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def addNewProfile(self):
        cred = credentials.Certificate("serviceAccountKey.json")
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {
                'databaseURL': "https://faceattendancertdb-default-rtdb.firebaseio.com/"
            })

        ref = db.reference('Students')

        name = self.name.text()
        year = self.year.text()
        syear = self.startingYear.text()
        occ = self.Occupation.text()
        imgpath = self.imgPath.text()

        data = {}
        f = open('newId.txt', 'r')
        newID = int(f.readline())
        f.close()

        new_entry = {
            "name": name,
            "major": occ,
            "starting_year": syear,
            "total_attendance": 0,
            "standing": "N",
            "year": year,
            "last_attendance_time": "2022-12-11 00:54:34"
        }

        data[str(newID)] = new_entry

        for key, value in data.items():
            ref.child(key).set(value)

        newID = newID + 1
        f = open('newId.txt', 'w')
        f.write(str(newID))
        f.close()

        destinationfile = "./images/" + str(newID) + ".jpg"
        shutil.copyfile(imgpath, destinationfile)

        run([sys.executable, 'EncodeGenerator.py'])

        mainMenu = Menu()
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    #ui functionalities
        
#delete profile
#ui functionalities
class DeleteProfile(QDialog):
    def __init__(self):
        super(DeleteProfile,self).__init__()
        loadUi("deleteProfile.ui",self)
        self.addButton.clicked.connect(self.deleteExistingProfile)
        self.returnMenu.clicked.connect(self.goMainMenu)

    def goMainMenu(self):
        mainMenu =Menu()
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def deleteExistingProfile(self):
        try:
            cred = credentials.Certificate("serviceAccountKey.json")
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred, {
                    'databaseURL': "https://faceattendancertdb-default-rtdb.firebaseio.com/"
                })

            ref = db.reference('Students')

            newID = self.profileID.text()
            ref.child(newID).delete()  # Use delete() instead of set(None)

            print(f"Student with ID {newID} deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

#app functionalities

#update profile
#ui functionalities
class UpdateProfile(QDialog):
    def __init__(self):
        super(UpdateProfile,self).__init__()
        loadUi("updateProfile.ui",self)
        self.addButton.clicked.connect(self.updateExistingProfile)
        self.returnMenu.clicked.connect(self.goMainMenu)

        
    def goMainMenu(self):
        mainMenu =Menu()
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def updateExistingProfile(self):
        cred = credentials.Certificate("serviceAccountKey.json")
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {
                'databaseURL': "https://faceattendancertdb-default-rtdb.firebaseio.com/"
            })

        ref = db.reference('Students')

        name = self.name.text()
        year = self.year.text()
        syear = self.startingYear.text()
        occ = self.Occupation.text()
        imgpath = self.imgPath.text()
        newID = self.profileID.text()

        data = {}

        new_entry = {
            "name": name,
            "major": occ,
            "starting_year": syear,
            "total_attendance": 0,
            "standing": "N",
            "year": year,
            "last_attendance_time": "2022-12-11 00:54:34"
        }

        data[newID] = new_entry

        for key, value in data.items():
            ref.child(key).set(value)

        mainMenu = Menu()
        widget.addWidget(mainMenu)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
#app functionalities







        
##################### Main ###############################
app=QApplication(sys.argv)
mainwindow=FirstMenu()           
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(900)
widget.setFixedHeight(700)
widget.show()
app.exec_()
