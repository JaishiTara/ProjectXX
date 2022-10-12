import time

from main import App
import sys
import threading


def put_outputs_on_stream():
    while True:
        try:
            if app.program_terminated:
                sys.stdout.writelines(["\n", ", ", "Finished"])
                return
            time.sleep(1)
            sys.stdout.writelines([str(app.get_speed()), ", ", str(app.get_rpm()), ", ", str(app.car_wheel_angle),
                                   ", ", str(app.get_temperature(app.get_time_minutes())), "\n"])
        except BaseException:
            pass


throttle = int(sys.argv[1])
brake = int(sys.argv[2])
steering = int(sys.argv[3])
drive_state = int(sys.argv[4])
clamp = int(sys.argv[5])


app = App()

app.set_throttle(throttle)
app.set_brake(brake)
app.set_steering(steering)
app.set_drive_state(drive_state)
app.set_clamp(clamp)

t = threading.Thread(target=put_outputs_on_stream)
t.start()

app.set_up_windows()
app.quit_program()
app.run_gui()
