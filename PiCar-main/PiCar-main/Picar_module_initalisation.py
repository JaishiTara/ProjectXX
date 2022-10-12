import busio

from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo, motor


class DrivingModule:

    def __init__(self):

        self.raspberrypi_configurations()
        self.motors_initial_conditions()

    def raspberrypi_configurations(self):

        self.inter_integrate_circuit = busio.I2C(SCL, SDA)
        self.pca = PCA9685(self.inter_integrate_circuit)
        self.pca.frequency = 60
        self.left_motor = motor.DCMotor(
            self.pca.channels[4], self.pca.channels[14])
        self.right_motor = motor.DCMotor(
            self.pca.channels[5], self.pca.channels[15])
        self.servo_motor = servo.Servo(self.pca.channels[0])
        self.LEDpin_detection_ball = self.pca.channels[12]
        self.LEDpin_detection_ball.duty_cycle = 0

        return self.LEDpin_detection_ball, self.pca, self.pca.frequency,\
               self.left_motor, self.right_motor, self.servo_motor,\
               self.LEDpin_detection_ball.duty_cycle

    def motors_initial_conditions(self):

        self.fLeft_Motor_Speed = 0.00001
        self.fRight_Motor_Speed = 0.00001

        self.iServo_Motor_Position = 90

        self.fMotors_Max_Speed = 1.0
        self.fMotors_Min_Speed = 0.00001

        self.iServo_Motor_Max_Position = 180
        self.iServo_Motor_Min_Position = 0.0

        self.fMotor_Acceleration_Speed = 0.2

        self.iServo_Motor_Steer_Range = 15

        return self.iServo_Motor_Max_Position, self.iServo_Motor_Min_Position,\
               self.fMotor_Acceleration_Speed, self.iServo_Motor_Steer_Range,\
               self.iServo_Motor_Position, self.fLeft_Motor_Speed,\
               self.fRight_Motor_Speed, self.fMotors_Max_Speed

