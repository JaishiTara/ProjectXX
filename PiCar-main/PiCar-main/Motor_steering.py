class MotorSteering:

    def __init__(self, aCommand_Values_Motors, iServo_Motor_Position,
                 iServo_Motor_Steer_Range, iServo_Motor_Max_Position,
                 iServo_Motor_Min_Position, servo_motor):

        self.aCommand_Values_Motors = aCommand_Values_Motors
        self.iServo_Motor_Position = iServo_Motor_Position
        self.iServo_Motor_Steer_Range = iServo_Motor_Steer_Range
        self.iServo_Motor_Max_Position = iServo_Motor_Max_Position
        self.servo_motor = servo_motor
        self.iServo_Motor_Min_Position = iServo_Motor_Min_Position

    def move_right(self):

        if self.aCommand_Values_Motors['K_RIGHT'] == 1:

            self.iServo_Motor_Position = self.iServo_Motor_Position \
                                         + self.iServo_Motor_Steer_Range

            if self.iServo_Motor_Position >= self.iServo_Motor_Max_Position:
                self.iServo_Motor_Position = self.iServo_Motor_Max_Position

            self.servo_motor.angle = self.iServo_Motor_Position

        return self.iServo_Motor_Position

    def move_left(self):

        if self.aCommand_Values_Motors['K_LEFT'] == 1:

            self.iServo_Motor_Position = self.iServo_Motor_Position \
                                         - self.iServo_Motor_Steer_Range

            if self.iServo_Motor_Position <= self.iServo_Motor_Min_Position:
                self.iServo_Motor_Position = self.iServo_Motor_Min_Position

            self.servo_motor.angle = self.iServo_Motor_Position

        return self.iServo_Motor_Position