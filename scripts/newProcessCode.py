#!/usr/bin/python

import rospy
import sys
import time
import serial
import hashlib
from std_msgs.msg import String
import glob


serialList = []
ports = glob.glob('/dev/ttyACM[0-9]*')
#print(ports)

for i in ports:
	try:
		serialList.append(serial.Serial(i, 115200,timeout = 1))
		#pub.publish("Flag 1")
	except:
		pass



arduino = serialList[0]
time.sleep(2)

cm = 391
Delay = "G07\n"
Home = "M11\nM18\n"
Up = "G05\n"
Down = "G06\n"
Length = 3*cm

def Length3Digit(Length):
    if Length > 100:
        return (str(Length))
    elif Length > 10:
        return ('0' + str(Length))
    elif Length > 0:
        return ('00' + str(Length))

def createMessage(messageList):
    targetNodeType    = str(messageList[0])
    targetNodeID      = str(messageList[1])
    sourceNodeType    = str(messageList[2])
    sourceNodeID      = str(messageList[3])
    commandType       = str(messageList[4])
    commandData       = str(messageList[5])
    commandDataLength = Length3Digit(len(commandData))
    dataToCheckSum = targetNodeType + targetNodeID + sourceNodeType + sourceNodeID + commandType + commandDataLength + commandData
    m = hashlib.sha256()
    m.update(dataToCheckSum.encode("utf-8"))
    checksum = str(m.hexdigest())
    dataToCheckSum += checksum
    return dataToCheckSum


def Centre(pos):
    if pos == '1':
        Command =  "G00 " + "X"+str(1*cm) + " Y"+str(-9*cm) +"\n"+Delay
    elif pos == '2':
        Command =  "G00 " + "X"+str(1*cm) + " Y"+str(-13*cm) +"\n"+ Delay
    elif pos == '3':
        Command =  "G00 " + "X"+str(6*cm) + " Y"+str(-9*cm) +"\n"+ Delay
    elif pos == '4':
        Command =  "G00 " + "X"+str(6*cm) + " Y"+str(-13*cm) +"\n"+ Delay
    return(Command)

def  X(Size):
    return "G00 " + "X"+str(Size) + " Y"+str(0)+"\n"


def  Y(Size):
    Command =  "G00 " + "X"+str(0) + " Y"+str(Size)+"\n"
    return(Command)

def  DiagTL(Size):
    Command =  "G00 " + "X"+str(Size) + " Y"+str(-Size)+"\n"
    return(Command)
def  DiagTR(Size):
    Command =  "G00 " + "X"+str(-Size) + " Y"+str(-Size)+"\n"
    return(Command)
def  DiagBL(Size):
    Command =  "G00 " + "X"+str(Size) + " Y"+str(Size)+"\n"
    return(Command)
def  DiagBR(Size):
    Command =  "G00 " + "X"+str(-Size) + " Y"+str(Size)+"\n"
    return(Command)

def PlacePiece():
    push = -7*cm
    serialprint(Home)
    time.sleep(10)
    serialprint(X(20*cm))
    time.sleep(5)
    serialprint(Y(-8*cm))
    time.sleep(5)
    serialprint(X(-11*cm))
    time.sleep(5)

def DrawPentagon(pos):
    startpos = Centre(pos)

    serialprint(Home)
    time.sleep(10)
    serialprint(Up)
    serialprint(startpos)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(Y(-Length/2))
    serialprint(Up)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(DiagTL(Length/2))
    serialprint(Up)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(DiagBL(Length/2))
    serialprint(Up)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(Y(Length/2))
    serialprint(Up)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(X(-Length))
    serialprint(Up)
    time.sleep(5)

def DrawSquare(pos):
    startpos = Centre(pos)

    serialprint(Home)
    time.sleep(10)
    serialprint(Up)
    serialprint(startpos)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(X(Length))
    serialprint(Up)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(Y(-Length))
    serialprint(Up)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(X(-Length))
    serialprint(Up)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(Y(Length))
    serialprint(Up)
    time.sleep(5)

def DrawDiamond(pos):
    startpos = Centre(pos)

    serialprint(Home)
    time.sleep(10)
    serialprint(Up)
    serialprint(startpos)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(DiagTL(Length/2))
    serialprint(Up)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(DiagBL(Length/2))
    serialprint(Up)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(DiagBR(Length/2))
    serialprint(Up)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(DiagTR(Length/2))
    serialprint(Up)
    time.sleep(5)

def DrawTriangle(pos):
    startpos = Centre(pos)

    serialprint(Home)
    time.sleep(10)
    serialprint(Up)
    serialprint(startpos)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(DiagTL(Length/2))
    serialprint(Up)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(DiagBL(Length/2))
    serialprint(Up)
    time.sleep(5)
    serialprint(Down)
    time.sleep(1)
    serialprint(Delay+X(-Length))
    serialprint(Up)
    time.sleep(5)

def serialprint(data):
    print(data)
    arduino.write(data)

def Gcoder(shape,pos):
    if shape == 'P':
        DrawPentagon(pos)
    if shape == 'S':
        DrawSquare(pos)
    if shape == 'D':
        DrawDiamond(pos)
    if shape == 'T':
        DrawTriangle(pos)

def rosCallback(data):
    global pub
    global sub
    inputString = data.data
    targetNodeType = inputString[0]
    targetNodeID = inputString[1]
    sourceNodeType = inputString[2]
    sourceNodeID = inputString[3]
    commandType = inputString[4:7]
    commandDataLength = int(inputString[7:10])
    commandData = inputString[10:(10+commandDataLength)]
    dataToCheckSum = inputString[:(10+commandDataLength)]
    checksum = inputString[(10+commandDataLength):]
    # get data, validate
    m = hashlib.sha256()
    m.update(dataToCheckSum.encode("utf-8"))
    hashResult = str(m.hexdigest())
    if(hashResult == checksum and (targetNodeType=="1" or targetNodeType=="0")): # check the message is valid and for me
        if commandType == "042": # ie have we been told to do something
            PlacePiece()
            position=0
            for shape in commandData:
                if shape in "PSDT": # check a recognised shape has been sent
                    Gcoder(shape,str(1+position))
                    position += 1
            serialprint(Home)
            # ack
            messageString =  createMessage([5,1,1,1,"046"," "])
            pub.publish(messageString)
        #if commandType == "":

def killerCallback(data):
    inputString = data.data
    targetNodeType = inputString[0]
    targetNodeID = inputString[1]
    sourceNodeType = inputString[2]
    sourceNodeID = inputString[3]
    commandType = inputString[4:7]
    commandDataLength = int(inputString[7:10])
    commandData = inputString[10:(10+commandDataLength)]
    dataToCheckSum = inputString[:(10+commandDataLength)]
    checksum = inputString[(10+commandDataLength):]
    # get data, validate
    m = hashlib.sha256()
    m.update(dataToCheckSum.encode("utf-8"))
    hashResult = str(m.hexdigest())
    if(hashResult == checksum and (targetNodeType=="1" or targetNodeType=="0")): # check the message$
        if commandType == "036": # ie we should stop
            serialPrint("M10\n") # prehaps we should send some stop GCODE
            rospy.signal_shutdown("Exit time!")
            exit()




rospy.init_node('ProcessingNode' , anonymous=True)
rospy.Subscriber("/system",String,killerCallback)
sub = rospy.Subscriber("/process", String, rosCallback)
pub = rospy.Publisher("/process", String, queue_size=10)
sysSub = rospy.Subscriber("/system", String, rosCallback)
sysPub = rospy.Publisher("/system", String, queue_size=10)
rospy.spin()
#
# if __name__ == '__main__':
#     shape = list()
#     pos = list()
#     for x in range(0,4):
#         shape.append(raw_input("Shape (P,T,S,D)? "))
#         pos.append( raw_input("Position (1,2,3,4,0)? "))
#         Gcoder(shape[x],pos[x])
