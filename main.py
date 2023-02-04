from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys

app = QtWidgets.QApplication([])
ui = uic.loadUi("design.ui")
ui.setWindowTitle("SerialGUI")

serial = QSerialPort()
serial.setBaudRate(9600)
portList = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.portName())
ui.comL.addItems(portList)

posX = 200
posY = 100
listX = []
for x in range(100): listX.append(x)
listY = []
for x in range(100): listY.append(0)
####
posX2 = 200
posY2 = 100
listX2 = []
for x2 in range(100): listX2.append(x2)
listY2 = []
for x2 in range(100): listY2.append(0)


def onRead():
    if not serial.canReadLine(): return
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(',')
    ui.nivelCO.setStyleSheet("QProgressBar::chunk {background-color: green;}")
    ui.nivelLP.setStyleSheet("QProgressBar::chunk {background-color: green;}")
    ui.nivelTe.setStyleSheet("QProgressBar::chunk {background-color: green;}")
    ui.nivelHu.setStyleSheet("QProgressBar::chunk {background-color: green;}")
    ui.nivelCO.setFormat("")
    ui.nivelLP.setFormat("")
    ui.nivelTe.setFormat("")
    ui.nivelHu.setFormat("")

    if data[0] == '0':
        ui.lcdN.display(data[1])
        ui.nivelCO.setValue(int(float(data[3])))

        if int(float(data[3]) > 350):
            ui.nivelCO.setStyleSheet("QProgressBar::chunk {background-color: red;}")
        if int(float(data[3]) > 350):
            ui.nivelLP.setStyleSheet("QProgressBar::chunk {background-color: red;}")
        if int(float(data[3]) > 350):
            ui.nivelTe.setStyleSheet("QProgressBar::chunk {background-color: red;}")
        if int(float(data[3]) > 350):
            ui.nivelHu.setStyleSheet("QProgressBar::chunk {background-color: red;}")

        ui.nivelLP.setValue(int(float(data[3]))-20)
        ui.nivelTe.setValue(int(float(data[3]))-20)
        ui.nivelHu.setValue(int(float(data[3]))-20)

        ui.labCO2.setText(data[3])
        ui.labLP.setText(data[3])
        ui.labTe.setText(data[3])
        ui.labHu.setText(data[3])

        ui.textF.setText(data[3])

        global listX
        global listY
        listY = listY[1:]
        listY.append(int(data[2]))  
        ui.graph.clear()
        ui.graph.plot(listX, listY)

        ######
        global listX2
        global listY2
        listY2 = listY2[1:]
        listY2.append(int(data[2]) - 2)  
        ui.graphHum.clear()
        ui.graphHum.plot(listX2, listY2)
        ######

    if data[0] == '1':
        if data[1] == '0':
            ui.circle.setChecked(True)
        else:
            ui.circle.setChecked(False)

    if data[0] == '2':
        global posX
        global posY
        posX += int((int(data[1]) - 512) / 100)
        posY += int((int(data[2]) - 512) / 100)
        ui.circle.setGeometry(posX, posY, 20, 20)


def onOpen():
    print("abriendo puerto")
    ui.lcdN.display(5)
    serial.setPortName(ui.comL.currentText())
    serial.open(QIODevice.ReadWrite)
    
    


def serialSend(data):
    txs = str(data)
    """
    for val in data:
        txs += str(val)
        txs += ','
    txs = txs[:-1]
    txs += ';'
    """
    print(txs)
    serial.write(txs.encode('ascii'))


def onClose():
    serial.close()


def ledControl(val):
    if val == 2: val = 1;
    serialSend([0, val])


def fanControl(val):
    if val == 2: val = 1;
    serialSend([3, val])


def bulbControl(val):
    if val == 2: val = 1;
    serialSend([4, val])


def RGBcontrol():
    ui.labelR.setText(str(ui.RS.value()))
    serialSend([1, ui.RS.value(), ui.GS.value(), ui.BS.value()])


def servoControl(val):
    #serialSend(val)
    print("serv" + str(val))
    serialSend([2, val])


def sendText():
    txs = "5,"
    txs += ui.textF.displayText()
    txs += ';'
    serial.write(txs.encode())


serial.readyRead.connect(onRead)
ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)

#ui.ledC.stateChanged.connect(ledControl)
#ui.fanC.stateChanged.connect(fanControl)
#ui.bulbC.stateChanged.connect(bulbControl)
#ui.RS.valueChanged.connect(RGBcontrol)
#ui.GS.valueChanged.connect(RGBcontrol)
#ui.BS.valueChanged.connect(RGBcontrol)
ui.servoK.valueChanged.connect(servoControl)
ui.sendB.clicked.connect(sendText)

ui.show()
app.exec()