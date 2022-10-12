class MotorAcceleration:

    def __init__(self, aCommand_Values_Motors, fLeft_Motor_Speed, left_motor,
                 fRight_Motor_Speed, fMotor_Acceleration_Speed, right_motor,
                 fMotors_Max_Speed, fMotors_Min_Speed, iServo_Motor_Position):

        self.aCommand_Values_Motors = aCommand_Values_Motors
        self.fLeft_Motor_Speed = fLeft_Motor_Speed
        self.left_motor = left_motor
        self.fRight_Motor_Speed = fRight_Motor_Speed
        self.fMotor_Acceleration_Speed = fMotor_Acceleration_Speed
        self.right_motor = right_motor
        self.fMotors_Max_Speed = fMotors_Max_Speed
        self.fMotors_Min_Speed = fMotors_Min_Speed
        self.iServo_Motor_Position = iServo_Motor_Position

    def output_speed_servo(self):

        print("Left Motor: " + str(round(self.fLeft_Motor_Speed, 2)) + '\t' +
              'Right Motor: ' + str(round(self.fRight_Motor_Speed, 2)) + '\n'
              + 'Steering angle: ' + str(round(self.iServo_Motor_Position, 2)))

    def move_forward(self):

        if self.aCommand_Values_Motors['K_UP'] == 1:

            self.fLeft_Motor_Speed = self.fLeft_Motor_Speed \
                                     + self.fMotor_Acceleration_Speed
            self.fRight_Motor_Speed = self.fRight_Motor_Speed \
                                      + self.fMotor_Acceleration_Speed

            if self.fLeft_Motor_Speed >= self.fMotors_Max_Speed:
                self.fLeft_Motor_Speed = self.fMotors_Max_Speed

            if self.fRight_Motor_Speed >= self.fMotors_Max_Speed:
                self.fRight_Motor_Speed = self.fMotors_Max_Speed

            self.left_motor.throttle = self.fLeft_Motor_Speed
            self.right_motor.throttle = self.fRight_Motor_Speed

        return self.fLeft_Motor_Speed, self.fRight_Motor_Speed

    def move_backward(self):

        if self.aCommand_Values_Motors['K_DOWN'] == 1:

            self.fLeft_Motor_Speed = self.fLeft_Motor_Speed \
                                     - self.fMotor_Acceleration_Speed
            self.fRight_Motor_Speed = self.fRight_Motor_Speed \
                                      - self.fMotor_Acceleration_Speed

            if self.fLeft_Motor_Speed <= self.fMotors_Min_Speed:
                self.fLeft_Motor_Speed = self.fMotors_Min_Speed

            if self.fRight_Motor_Speed <= self.fMotors_Min_Speed:
                self.fRight_Motor_Speed = self.fMotors_Min_Speed

            self.left_motor.throttle = self.fLeft_Motor_Speed
            self.right_motor.throttle = self.fRight_Motor_Speed

        return self.fLeft_Motor_Speed, self.fRight_Motor_Speed
