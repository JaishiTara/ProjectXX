from main import App
import threading
import time


class Client:

    def set_input_parameters(self):
        # app.set_throttle(self.get_throttle_input())
        # app.set_brake(self.get_brake_input())
        # app.set_steering(self.get_steering_input())
        # app.set_drive_state(self.get_drive_state_input())
        # app.set_clamp(self.get_clamp_input())
        app.set_throttle(50)
        app.set_brake(0)
        app.set_steering(0)
        app.set_drive_state(1)
        #app.set_clamp(15)

    def get_throttle_input(self):
        while True:
            try:
                throttle = input(">>> [INPUT] Throttle (0 - 100): ")
                throttle = int(throttle)
                if 100 >= throttle >= 0:
                    return int(throttle)
                else:
                    self.print_input_error()
            except:
                self.print_input_error()

    def get_brake_input(self):
        while True:
            try:
                brake = input(">>> [INPUT] Brake (0 - 100): ")
                brake = int(brake)
                if 100 >= brake >= 0:
                    return int(brake)
                else:
                    self.print_input_error()
            except:
                self.print_input_error()

    def get_steering_input(self):
        while True:
            try:
                steering = input(">>> [INPUT] Steering (-90 - 90): ")
                steering = int(steering)
                if 90 >= steering >= -90:
                    return int(steering)
                else:
                    self.print_input_error()
            except:
                self.print_input_error()

    def get_drive_state_input(self):
        while True:
            try:
                drive_state = input(">>> [INPUT] Drive State (0 - 3): ")
                drive_state = int(drive_state)
                if 3 >= drive_state >= 0:
                    return drive_state
                else:
                    self.print_input_error()
            except:
                self.print_input_error()

    def get_clamp_input(self):
        while True:
            try:
                clamp = input(">>> [INPUT] Clamps (15 or 30): ")
                clamp = int(clamp)
                if clamp == 15 or clamp == 30:
                    return clamp
                else:
                    self.print_input_error()
            except:
                self.print_input_error()


    def print_input_error(self):
        print(">>> [ERROR] Wrong input. Make sure to input the allowed numbers! Don't input characters!")


def print_speed():
    while True:
        time.sleep(1)
        print(">>> [OUTPUT] Speed: " + str(app.get_speed()))


def print_rpm():
    while True:
        time.sleep(1)
        print(">>> [OUTPUT] RPM: " + str(app.get_rpm()))

def update_throttle():
    if app.program_terminated:
        return
    time.sleep(10)
    app.set_throttle(0)
    return

app = App()
cl = Client()
cl.set_input_parameters()

#update_speed_thread = threading.Thread(target=print_speed)
#update_rpm_thread = threading.Thread(target=print_rpm)
#update_speed_thread.start()
#update_rpm_thread.start()

t = threading.Thread(target=update_throttle)
t.start()

app.set_up_windows()
app.quit_program()
app.run_gui()
