import cv2
import ipdb
import os
import signal
from Tensorflow_stream import tensorflow, dFrame_Rate_Calculation, dFrequency
from Picar_module_initalisation import DrivingModule
from Motor_acceleration import MotorAcceleration
from Motor_steering import MotorSteering


class Main:

    def __init__(self):
	
        self.user_information()
        self.raspberrypi()
        self.motors_initialisation()
        self.keypads_command()
        self.control_loop(dFrame_Rate_Calculation)

    def user_information(self):

        print("Ready")
        print("Press q to Quit")
        #intech cops

    def raspberrypi(self):

        [self.LEDpin_detection_ball, self.pca, self.pca.frequency,
         self.left_motor, self.right_motor, self.servo_motor,
         self.LEDpin_detection_ball.duty_cycle] \
            = DrivingModule.raspberrypi_configurations(self)

    def motors_initialisation(self):

        [self.iServo_Motor_Max_Position, self.iServo_Motor_Min_Position,
         self.fMotor_Acceleration_Speed, self.iServo_Motor_Steer_Range,
         self.iServo_Motor_Position, self.fLeft_Motor_Speed,
         self.fRight_Motor_Speed, self.fMotors_Max_Speed] \
            = DrivingModule.motors_initial_conditions(self)

    def keypads_command(self):

        self.aCommand_Values_Motors = {
            'K_UP': 0,
            'K_DOWN': 0,
            'K_LEFT': 0,
            'K_RIGHT': 0,
            'Break': 0
        }

    def control_loop(self, dFrame_Rate_Calculation):

        signal.signal(signal.SIGINT, self.signal_handler)

        while True:
            [self.aFrame, self.dTime1, self.fLeft_Motor_Speed_Detect,
             self.fRight_Motor_Speed_Detect, self.aVideo_Stream] \
                = tensorflow(self.LEDpin_detection_ball, self.fLeft_Motor_Speed,
                             self.fRight_Motor_Speed, self.left_motor,
                             self.right_motor)

            self.fLeft_Motor_Speed = self.fLeft_Motor_Speed_Detect
            self.fRight_Motor_Speed = self.fRight_Motor_Speed_Detect
            cv2.putText(
                self.aFrame, 'FPS: {0:.2f}'.format(dFrame_Rate_Calculation),
                (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2,
                cv2.LINE_AA)
            cv2.imshow('Object detector', self.aFrame)
            self.dTime2 = cv2.getTickCount()
            self.dTotal_Time = (self.dTime2 - self.dTime1) / dFrequency
            dFrame_Rate_Calculation = 1 / self.dTotal_Time

            MotorAcceleration1 = \
                MotorAcceleration(
                    self.aCommand_Values_Motors, self.fLeft_Motor_Speed,
                    self.left_motor, self.fRight_Motor_Speed,
                    self.fMotor_Acceleration_Speed, self.right_motor,
                    self.fMotors_Max_Speed, self.fMotors_Min_Speed,
                    self.iServo_Motor_Position)

            MotorSteering1 = MotorSteering(
                self.aCommand_Values_Motors, self.iServo_Motor_Position,
                self.iServo_Motor_Steer_Range, self.iServo_Motor_Max_Position,
                self.iServo_Motor_Min_Position, self.servo_motor)

            self.sKeybad = cv2.waitKey(1)

            if self.sKeybad == ord('w'):
                self.aCommand_Values_Motors['K_UP'] = 1
                [self.fLeft_Motor_Speed, self.fRight_Motor_Speed] \
                    = MotorAcceleration.move_forward(MotorAcceleration1)
                MotorAcceleration.output_speed_servo(MotorAcceleration1)

            elif self.sKeybad == ord('s'):
                self.aCommand_Values_Motors['K_DOWN'] = 1
                [self.fLeft_Motor_Speed, self.fRight_Motor_Speed] \
                    = MotorAcceleration.move_backward(MotorAcceleration1)
                MotorAcceleration.output_speed_servo(MotorAcceleration1)

            elif self.sKeybad == ord('d'):
                self.aCommand_Values_Motors['K_RIGHT'] = 1
                self.iServo_Motor_Position = MotorSteering.move_right(
                    MotorSteering1)
                MotorAcceleration.output_speed_servo(MotorAcceleration1)

            elif self.sKeybad == ord('a'):
                self.aCommand_Values_Motors['K_LEFT'] = 1
                self.iServo_Motor_Position = MotorSteering.move_left(
                    MotorSteering1)
                MotorAcceleration.output_speed_servo(MotorAcceleration1)

            elif self.sKeybad == ord('q'):
                break

        # Clean up
        self.post_action()
        

    

    def signal_handler(self, signum, frame):
        self.post_action()
        exit(1)

    def post_action(self):
        self.fLeft_Motor_Speed = 0.00001
        self.fRight_Motor_Speed = 0.00001
        self.left_motor.throttle = self.fLeft_Motor_Speed
        self.right_motor.throttle = self.fRight_Motor_Speed
        self.iServo_Motor_Position = 90
        self.servo_motor.angle = self.iServo_Motor_Position
        self.LEDpin_detection_ball.duty_cycle = 0x0000
        cv2.destroyAllWindows()
        self.aVideo_Stream.stop()
        


# run code
run_code = Main()
