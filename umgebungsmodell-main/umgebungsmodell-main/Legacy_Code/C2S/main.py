import time
from threading import Thread

import tkinter
from tkinter import ttk, BOTH, TRUE
from speed_rpm_gui import iSTEP_SPEED
from speed_rpm_gui import iSTEP_RPM
from speed_rpm_gui import iMAX_RPM
from speed_rpm_gui import iMIN_RPM
from speed_rpm_gui import iMIN_SPEED
from speed_rpm_gui import iMAX_SPEED
from speed_rpm_gui import set_up_meter

from speed_rpm_gui import Speedometer
from control_gui import ControlGUI
from test_control_gui import TestControlGUI

test_controls = TestControlGUI()
control_gui = ControlGUI()
speed_and_rpm = Speedometer()


class App:

    def __init__(self):
        self.main_window = None
        self.x = None
        self.y = None
        self.plot_window = None
        self.throttle_window = None
        self.speed_and_rpm_window = None
        self.gear_window = None
        self.steering_window = None
        self.brake_window = None
        self.clamps_window = None
        self.speed_gauge = None
        self.rpm_gauge = None
        self.throttle_value = 0
        self.brake_value = 0
        self.steering_value = 0
        self.selected_clamp = 2
        self.drive_state = 0
        self.speed = 0
        self.rpm = 0

    def build_main_window(self):
        self.main_window = tkinter.Tk()
        self.main_window.attributes('-fullscreen', True)
        self.main_window.title("Parent Window")
        self.x = self.main_window.winfo_x()
        self.y = self.main_window.winfo_y()

    def build_throttle_window(self):
        self.throttle_window = tkinter.Toplevel(self.main_window)
        self.throttle_window.geometry('200x300')
        self.throttle_window.title("Throttle Window")
        self.throttle_window.wm_transient(self.main_window)
        self.throttle_window.geometry("+%d+%d" % (self.x + 1350, self.y + 50))
        ControlGUI.create_throttle(self.throttle_window, self.throttle_value)

        # Doesn't work
        #control_gui.create_throttle(self.throttle_window, self.throttle_value)

    def build_speed_and_rpm_window(self):
        self.speed_and_rpm_window = tkinter.Toplevel(self.main_window)
        self.speed_and_rpm_window.geometry('600x300')
        self.speed_and_rpm_window.title("Speed and RPM Window")
        self.speed_and_rpm_window.wm_transient(self.main_window)
        self.speed_and_rpm_window.geometry("+%d+%d" % (self.x + 700, self.y + 50))
        speed_and_rpm.set_gauge_meters()

        self.speed_gauge = set_up_meter(self.speed_and_rpm_window, iMin_val=iMIN_SPEED, iMax_val=iMAX_SPEED,
                                        iStep_val=iSTEP_SPEED, sTitle='Speed', iunit='KMPH')
        self.rpm_gauge = set_up_meter(self.speed_and_rpm_window, iMin_val=iMIN_RPM, iMax_val=iMAX_RPM,
                                      iStep_val=iSTEP_RPM, sTitle='RPM', iunit='x1000')

    def build_gear_window(self):
        self.gear_window = tkinter.Toplevel(self.main_window)
        self.gear_window.geometry('200x300')
        self.gear_window.title("Gear Window")
        self.gear_window.wm_transient(self.main_window)
        self.gear_window.geometry("+%d+%d" % (self.x + 1600, self.y + 50))
        ControlGUI.create_drive(self.gear_window, self.drive_state)

    def build_plot_window(self):
        self.plot_window = tkinter.Toplevel(self.main_window)
        self.plot_window.geometry('600x300')
        self.plot_window.title("Plot Window")
        self.plot_window.wm_transient(self.main_window)
        self.plot_window.geometry("+%d+%d" % (self.x + 50, self.y + 50))
        # Tab Widget
        tabs = ttk.Notebook(self.plot_window)
        tabs.pack(fill=BOTH, expand=TRUE)
        frame1 = ttk.Frame(tabs)
        frame2 = ttk.Frame(tabs)
        tabs.add(frame1, text="Throttle")
        tabs.add(frame2, text="Brake")
        ControlGUI.create_plot(frame1, self.throttle_value)
        ControlGUI.create_plot_throttle(frame2, self.brake_value)

    def build_steering_window(self):
        self.steering_window = tkinter.Toplevel(self.main_window)
        self.steering_window.geometry('280x200')
        self.steering_window.title("Steering Window")
        self.steering_window.wm_transient(self.main_window)
        self.steering_window.geometry("+%d+%d" % (self.x + 860, self.y + 400))
        ControlGUI.create_steering(self.steering_window, self.steering_value)

    def build_brake_window(self):
        self.brake_window = tkinter.Toplevel(self.main_window)
        self.brake_window.geometry('200x300')
        self.brake_window.title("Brake Window")
        self.brake_window.wm_transient(self.main_window)
        self.brake_window.geometry("+%d+%d" % (self.x + 1600, self.y + 400))
        ControlGUI.create_brake(self.brake_window, self.brake_value)

    def build_clamps_window(self):
        self.clamps_window = tkinter.Toplevel(self.main_window)
        self.clamps_window.geometry('190x50')
        self.clamps_window.title("Clamps 15/30 Window")
        self.clamps_window.wm_transient(self.main_window)
        self.clamps_window.geometry("+%d+%d" % (self.x + 1600, self.y + 750))
        ControlGUI.create_clamps(self.clamps_window, self.selected_clamp)

    def quit_button(self):
        self.main_window.quit()
        self.main_window.destroy()

    def quit_program(self):
        quit_button = tkinter.Button(master=self.main_window, text="Quit",
                                     command=self.quit_button)
        quit_button.pack(side=tkinter.BOTTOM)

    def rpm_acceleration(self, throttle, v):
        v = v + (0.001 * throttle)
        time.sleep(0.05)
        return v

    def speed_acceleration(self, thr, velocity):
        time.sleep(0.05)
        return velocity + (0.007 * thr)

    def cool_down_rpm(self, v):
        brake_val = ControlGUI.get_brake_value(self.brake_window)
        if brake_val == 0:
            brake_val = 1
        brake_val = brake_val / 10
        v = v - (0.05 * brake_val)
        if v <= 0:
            return 0
        time.sleep(0.05)
        return v

    def cool_down_speed(self, v):
        brake_val = ControlGUI.get_brake_value(self.brake_window)
        if brake_val == 0:
            brake_val = 1
        brake_val = brake_val / 10
        v = v - (0.36 * brake_val)
        if v <= 0:
            return 0
        time.sleep(0.05)
        return v

    def move_speedometer_needle(self, velocity):
        throttle_val = ControlGUI.get_throttle_value(self.throttle_window)
        if throttle_val == 0:
            return self.cool_down_speed(velocity)
        while velocity <= 50:
            return self.speed_acceleration(throttle_val, velocity)
        return 50

    def move_rpm_needle(self, v):
        throttle_val = ControlGUI.get_throttle_value(self.throttle_window)
        if throttle_val == 0:
            return self.cool_down_rpm(v)
        while v <= 7:
            return self.rpm_acceleration(throttle_val, v)
        return 7

    def program_update(self):
        # TODO: Update all windows for setting parameters when the app is running
        # self.main_window.after(100, self.update_throttle_window)
        self.main_window.update_idletasks()
        self.main_window.update()

    def set_up_windows(self):
        self.build_main_window()
        self.build_throttle_window()
        self.build_speed_and_rpm_window()
        self.build_gear_window()
        self.build_steering_window()
        self.build_brake_window()
        self.build_clamps_window()
        self.build_plot_window()

    def run_gui(self):
        while True:
            rpm_needle = self.move_rpm_needle(self.rpm)
            self.rpm = rpm_needle
            speed_needle = self.move_speedometer_needle(self.speed)
            self.speed = speed_needle
            self.rpm_gauge.draw_needle(self.rpm)
            self.speed_gauge.draw_needle(speed_needle)
            # self.throttle_value += 1
            # self.build_throttle_window()
            # TODO: Get current throttle from slider and update the plot. This is a task for next sprint
            # throttle_val = self.get_updated_throttle_value()
            # self.set_throttle(throttle_val)
            # self.update_plot_window(self.throttle_value)
            self.program_update()

    def update_throttle_window(self):
        scale = ControlGUI.get_throttle_scale(self.throttle_window)
        scale.set(self.throttle_value)

    def set_throttle(self, value):
        self.throttle_value = value

    def set_brake(self, value):
        self.brake_value = value

    def set_steering(self, value):
        self.steering_value = value

    def set_clamp(self, value):
        if value == 30:
            self.selected_clamp = 2
        if value == 15:
            self.selected_clamp = 1

    def set_drive_state(self, mode):
        self.drive_state = mode

    def get_updated_throttle_value(self):
        return ControlGUI.get_throttle_value(self.throttle_window)

    def update_plot_window(self, new_value):
        ControlGUI.create_plot(self.plot_window, new_value)

    def get_speed(self):
        return self.speed

    def get_rpm(self):
        return self.rpm


"""
if __name__ == '__main__':
    app = App()
    # Setting values for UI elements
    app.set_throttle(0)
    app.set_brake(40)
    app.set_drive_state(0)
    app.set_steering(60)
    app.set_clamp(30)

    app.set_up_windows()
    app.quit_program()
    app.run_gui()
"""