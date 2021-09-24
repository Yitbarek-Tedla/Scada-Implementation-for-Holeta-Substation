from __future__ import print_function
from ui07 import Ui_MainWindow
from login_window import Ui_Form
from connection_window import Ui_Form as connection_Ui_Form
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtCore import left, pyqtSignal,QThread
from pymodbus.client.sync import ModbusSerialClient
import os, threading, time
import sqlite3
from paramData import Parameters

# result_=client.write_register(address=1,value=510,unit=1)
# print(result_)

class userInt(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setupUi(self)
        self.timerFunction()
        # self.modbusConnect()
        # self.readModbusThread = threading.Thread(name="readModbusThread",target=self.readModbus)
        # self.readModbusThread.start()
        # self.updateDscParamThread = threading.Thread(name="updateDscParamThread",target=self.updateDscParam)
        # self.updateDscParamThread.start()
        # QtWidgets.QTabWidget().setTabsClosable(True)
        # QTabWidget.setTabEnabled(1, false)
        # QtWidgets.QTabBar().tabButton(2,)
        # tabWidget->tabBar()->tabButton(i)->hide()
        # QtWidgets.QTabBar().setTabEnabled(1,True) 
        self.actionConnect.triggered.connect(self.connection_Window_fun)
        self.LoginPushButton.clicked.connect(self.checkAuthenticationStatus)
        self.LogoutPushButton.clicked.connect(self.logoutUser)
    
        # self.tabs.setEnabled(False)
        # self.Home.setEnabled(False)
        print(threading.active_count())
    def logoutUser(self):
        self.userMode="none"
        self.Home.setEnabled(False)
        self.Alarm.setEnabled(False)
        self.Events.setEnabled(False)
        self.Advanced.setEnabled(False)
        self.systemEventTab.setEnabled(False)
        self.operationRecordsTab.setEnabled(False)
        self.LoggedInLabel.setText('Logged Out!')
        self.LoggedInLabel.setStyleSheet("color:rgb(255, 0, 0)")
    def checkAuthenticationStatus(self):
        self.userName=self.UserNameInput.text()
        self.password=self.PasswordInput.text()
        #Input User name & Password and check
        if ((self.userName=='super') & (self.password == 'super123')):
            self.userMode = 'super'
        elif ((self.userName=='manager') & (self.password == 'manager123')):
            self.userMode = 'manager'
        elif ((self.userName=='operator') & (self.password == 'operator123')):
            self.userMode = 'operator'
        else:
            self.userMode = 'none'
        #Enable/Desable tabs as per the user mode
        if (self.userMode=='super'):
            self.Home.setEnabled(True)
            self.Alarm.setEnabled(True)
            self.Events.setEnabled(True)
            self.Advanced.setEnabled(True)
            self.systemEventTab.setEnabled(True)
            self.operationRecordsTab.setEnabled(True)
        elif (self.userMode == 'manager'):
            self.Home.setEnabled(True)
            self.Alarm.setEnabled(True)
            self.Events.setEnabled(True)
            self.Advanced.setEnabled(False)
            self.systemEventTab.setEnabled(True)
            self.operationRecordsTab.setEnabled(True)
        elif (self.userMode == 'operator'):
            self.Home.setEnabled(True)
            self.Alarm.setEnabled(True)
            self.Events.setEnabled(False)
            self.Advanced.setEnabled(False)
            self.systemEventTab.setEnabled(False)
            self.operationRecordsTab.setEnabled(False)
        else:
            self.Home.setEnabled(False)
            self.Alarm.setEnabled(False)
            self.Events.setEnabled(False)
            self.Advanced.setEnabled(False)
            self.systemEventTab.setEnabled(False)
            self.operationRecordsTab.setEnabled(False)
        #Login Status Display
        if ((self.userMode == 'operator') or (self.userMode == 'super') or (self.userMode == 'manager')):
            self.LoggedInLabel.setText('Logged_In!')
            self.LoggedInLabel.setStyleSheet("color:rgb(0, 255, 10)")
        else:
            self.LoggedInLabel.setText('Please Enter Correct Username or Password!')
            self.LoggedInLabel.setStyleSheet("color:rgb(255, 0, 0)")
        #Store in database
        self.initializeORDatabase()   
        self.storeORData('Sign In Attempt') 
    def connection_Window_fun(self):
        self.Form = QtWidgets.QWidget()
        self.ui = connection_Ui_Form()
        self.ui.setupUi(self.Form)
        self.Form.show()
        self.modbusConnect()
        self.readModbusThread = threading.Thread(name="readModbusThread",target=self.readModbus)
        self.readModbusThread.start()
        self.updateDscParamThread = threading.Thread(name="updateDscParamThread",target=self.updateDscParam)
        self.updateDscParamThread.start()
       
    def modbusConnect(self):
        self.client=ModbusSerialClient(method='rtu',port='COM2',stopbits=1,bytesize=8,parity='N',baudrate=19200)
        self.client.connect()
    def readModbus(self):
        while True:
            try:
                self.modbusData=self.client.read_holding_registers(address=1,count=6,unit=1)
                # print(self.modbusData.registers)
            except:
                print("Coudn't readModbus")
            
            time.sleep(1)
    def updateDscParam(self):
        while True:
            try:
                ###########Update DS1 Group##############
                self.DS1_Load.setText(str(self.modbusData.registers[0]))
                self.DS1_SysFreq.setText(str(self.modbusData.registers[1]))
                self.DS1_Voltage.setText(str(self.modbusData.registers[2]))
                self.DS1_ActiveP.setText(str(self.modbusData.registers[3]))
                self.DS1_ReactiveP.setText(str(self.modbusData.registers[4]))
                self.DS1_ApparentP.setText(str(self.modbusData.registers[5]))
                ###########Update DS2 Group##############
                self.DS2_Load.setText(str(self.modbusData.registers[0]))
                self.DS2_SysFreq.setText(str(self.modbusData.registers[1]))
                self.DS2_Voltage.setText(str(self.modbusData.registers[2]))
                self.DS2_ActiveP.setText(str(self.modbusData.registers[3]))
                self.DS2_ReactiveP.setText(str(self.modbusData.registers[4]))
                self.DS2_ApparentP.setText(str(self.modbusData.registers[5]))
                ###########Update DS3 Group##############
                self.DS3_Load.setText(str(self.modbusData.registers[0]))
                self.DS3_SysFreq.setText(str(self.modbusData.registers[1]))
                self.DS3_Voltage.setText(str(self.modbusData.registers[2]))
                self.DS3_ActiveP.setText(str(self.modbusData.registers[3]))
                self.DS3_ReactiveP.setText(str(self.modbusData.registers[4]))
                self.DS3_ApparentP.setText(str(self.modbusData.registers[5]))
            except:
                print("Coudn't update Disconnector Datas")
            time.sleep(1)
    def timerFunction(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateLCD)
        self.timer.start(1000)
    def updateLCD(self):
        self.currentTime = QtCore.QTime.currentTime()
        self.strCurrentTime= self.currentTime.toString('hh:mm:ss')
        self.lcdNumberHour.display(self.strCurrentTime)
        self.currentYear = QtCore.QDateTime.currentDateTime()
        self.strCurrentYear= self.currentYear.toString('yyyy:MM:dd')
        self.lcdNumberYear.display(self.strCurrentYear)
    def initializeSEDatabase(self):
        self.connSE=sqlite3.connect('systemEventData.db')
        self.cSE=self.connSE.cursor()
    def storeSEData(self):
        self.cSE.execute('INSERT INTO seInfo(em1, em2, em3) VALUES (?,?,?)',(1,2,3))
        self.connSE.commit()
    def initializeORDatabase(self):
        self.connOR=sqlite3.connect('operationalRecordData.db')
        self.cOR=self.connOR.cursor()
    def storeORData(self,logState):
        try:
            self.cOR.execute("CREATE TABLE orInfo(userMode, time, date, substation,oprDiscription)")
        except:
            pass
        self.cOR.execute("INSERT INTO orInfo VALUES (?,?,?,?,?)",(self.userMode,self.currentTime.toString('hh:mm:ss'),self.currentYear.toString('yyyy:MM:dd'),'Holeta',str(logState)))
        self.connOR.commit()
        queryOR="SELECT * FROM orInfo"
        resultOR = self.cOR.execute(queryOR)
        self.tableWidgetOR.setRowCount(0)
        for row_number, row_data in enumerate(resultOR):
            self.tableWidgetOR.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidgetOR.setItem(row_number,column_number,QtWidgets.QTableWidgetItem(str(data)))

        

if __name__ == '__main__':
    app=QtWidgets.QApplication([])
    widget = userInt()
    widget.show()
    app.exec()