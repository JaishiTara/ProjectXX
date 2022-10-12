import os
import argparse
import time
from threading import Thread
import importlib.util

import numpy as np
import cv2


class VideoStream:
    """Camera object that controls video streaming from the Picamera"""

    def __init__(self, aResolution=(640, 480), frame_rate=30):
        self.stream = cv2.VideoCapture(0)
        dCapture_Codec = cv2.VideoWriter_fourcc(*'MJPG')
        iProperty_Identfier_Fourcc = cv2.CAP_PROP_FOURCC
        self.stream.set(iProperty_Identfier_Fourcc, dCapture_Codec)
        iProperty_Identfier_Frame_Width = cv2.CAP_PROP_FRAME_WIDTH
        iProperty_Identfier_Frame_Height = cv2.CAP_PROP_FRAME_HEIGHT
        self.stream.set(iProperty_Identfier_Frame_Width, aResolution[0])
        self.stream.set(iProperty_Identfier_Frame_Height, aResolution[1])
        (self.bGrabbed, self.aFrame) = self.stream.read()
        self.bStopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.bStopped:
                self.stream.release()
                return

            (self.bGrabbed, self.aFrame) = self.stream.read()

    def read(self):
        return self.aFrame

    def stop(self):
        self.bStopped = True


parser = argparse.ArgumentParser()
parser.add_argument(
    '--modeldir',
    help='Folder the .tflite file is located in',
    required=True)
parser.add_argument(
    '--graph',
    help='Name of the .tflite file, if different than detect.tflite',
    default='detect.tflite')
parser.add_argument(
    '--labels',
    help='Name of the labelmap file, if different than labelmap.txt',
    default='labelmap.txt')
parser.add_argument(
    '--threshold',
    help='Minimum confidence threshold for displaying detected objects',
    default=0.5)
parser.add_argument(
    '--resolution',
    help='Desired webcam resolution in WxH. If the webcam does not support'
         ' the resolution entered, errors may occur.',
    default='1280x720')
parser.add_argument(
    '--edgetpu',
    help='Use Coral Edge TPU Accelerator to speed up detection',
    action='store_true')

args = parser.parse_args()
sModel_Name = args.modeldir
sGraph_Name = args.graph
sLabelmap_Name = args.labels
fMinimum_Configuration_Threshold = float(args.threshold)
dResolution_Width, dResolution_Height = args.resolution.split('x')
iResolution_Width, iResolution_Height = int(dResolution_Width), \
                                        int(dResolution_Height)
bUseTPU = args.edgetpu

pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter

    if bUseTPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter

    if bUseTPU:
        from tensorflow.lite.python.interpreter import load_delegate

if bUseTPU:

    if sGraph_Name == 'detect.tflite':
        sGraph_Name = 'edgetpu.tflite'

sCwd_Path = os.getcwd()

sPath_Object_Detection_Model = os.path.join(
    sCwd_Path, sModel_Name, sGraph_Name)

sPath_Label_Map = os.path.join(sCwd_Path, sModel_Name, sLabelmap_Name)

with open(sPath_Label_Map, 'r') as f:
    sLabels = [line.strip() for line in f.readlines()]

if sLabels[0] == '???':
    del (sLabels[0])

if bUseTPU:
    interpreter = Interpreter(
        model_path=sPath_Object_Detection_Model,
        experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print(sPath_Object_Detection_Model)
else:
    interpreter = Interpreter(model_path=sPath_Object_Detection_Model)

interpreter.allocate_tensors()
aInput_Details = interpreter.get_input_details()
aOutput_Details = interpreter.get_output_details()
iHeight = aInput_Details[0]['shape'][1]
iWidth = aInput_Details[0]['shape'][2]
bFloating_Model = (aInput_Details[0]['dtype'] == np.float32)
fInput_Mean = 127.5
fInput_Std = 127.5

sOutput_Name = aOutput_Details[0]['name']

if 'StatefulPartitionedCall' in sOutput_Name:
    iBoxes_Idx, iClasses_Idx, iScores_Idx = 1, 3, 0
else:
    iBoxes_Idx, iClasses_Idx, iScores_Idx = 0, 1, 2

dFrame_Rate_Calculation = 1
dFrequency = cv2.getTickFrequency()

aVideo_Stream = VideoStream(
    aResolution=(iResolution_Width, iResolution_Height), frame_rate=30).start()
time.sleep(1)

fLeft_Motor_Speed_Detect = 0.00001
fRight_Motor_Speed_Detect = 0.00001


def tensorflow(LEDpin_detection_ball, fLeft_Motor_Speed,
               fRight_Motor_Speed, left_motor, right_motor):
    global fLeft_Motor_Speed_Detect, fRight_Motor_Speed_Detect

    dTime1 = cv2.getTickCount()
    aFrame1 = aVideo_Stream.read()
    aFrame = aFrame1.copy()
    aFrame_Rgb = cv2.cvtColor(aFrame, cv2.COLOR_BGR2RGB)
    aFrame_Resized = cv2.resize(aFrame_Rgb, (iWidth, iHeight))
    aInput_Data = np.expand_dims(aFrame_Resized, axis=0)

    if bFloating_Model:
        aInput_Data = (np.float32(aInput_Data) - fInput_Mean) / fInput_Std
    interpreter.set_tensor(aInput_Details[0]['index'], aInput_Data)
    interpreter.invoke()
    aBoxes = interpreter.get_tensor(aOutput_Details[iBoxes_Idx]['index'])[0]
    aClasses = interpreter.get_tensor(aOutput_Details[iClasses_Idx]['index'])[
        0]
    aScores = interpreter.get_tensor(aOutput_Details[iScores_Idx]['index'])[0]

    for i in range(len(aScores)):
        if (aScores[i] > fMinimum_Configuration_Threshold) \
                and (aScores[i] <= 1.0):

            iY_Axis_Min = int(max(1, (aBoxes[i][0] * iResolution_Height)))
            iX_Axis_Min = int(max(1, (aBoxes[i][1] * iResolution_Width)))
            iY_Axis_Max = int(
                min(iResolution_Height, (aBoxes[i][2] * iResolution_Height)))
            iX_Axis_Max = int(
                min(iResolution_Width, (aBoxes[i][3] * iResolution_Width)))

            cv2.rectangle(
                aFrame, (iX_Axis_Min, iY_Axis_Min),
                (iX_Axis_Max, iY_Axis_Max), (10, 255, 0), 2)

            sObject_Name = sLabels[int(aClasses[i])]
            if sObject_Name == "sports ball":
                sObject_Name = "Tennis ball"
                left_motor.throttle = -1
                right_motor.throttle = -1
                LEDpin_detection_ball.duty_cycle = 0xffff
                [fLeft_Motor_Speed_Detect, fRight_Motor_Speed_Detect] \
                    = 0.00001, 0.00001
            else:
                fLeft_Motor_Speed_Detect = fLeft_Motor_Speed
                fRight_Motor_Speed_Detect = fRight_Motor_Speed
                left_motor.throttle = fLeft_Motor_Speed
                right_motor.throttle = fRight_Motor_Speed
                LEDpin_detection_ball.duty_cycle = 0x0000

            sLabel = '%s: %d%%' % (sObject_Name, int(aScores[i] * 100))
            aLabel_Size, iBase_Line = cv2.getTextSize(
                sLabel, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            iLabel_Y_Axis_Min = max(iY_Axis_Min, aLabel_Size[1] + 10)
            cv2.rectangle(
                aFrame, (iX_Axis_Min, iLabel_Y_Axis_Min - aLabel_Size[1] - 10),
                (iX_Axis_Min + aLabel_Size[0], iLabel_Y_Axis_Min + iBase_Line
                 - 10), (255, 255, 255), cv2.FILLED)
            cv2.putText(
                aFrame, sLabel, (iX_Axis_Min, iLabel_Y_Axis_Min - 7),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            if sObject_Name == "Tennis ball":
                cv2.imwrite("/home/pi/Desktop/TestPhoto.png", aFrame)

    return aFrame, dTime1, fLeft_Motor_Speed_Detect, fRight_Motor_Speed_Detect,\
           aVideo_Stream
