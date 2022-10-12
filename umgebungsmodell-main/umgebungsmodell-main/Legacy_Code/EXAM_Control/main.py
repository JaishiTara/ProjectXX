import time
from os import path
import sys
import tkinter
import threading
import math
from tkinter import ttk, BOTH, TRUE

sys.path.append(path.abspath(r"S:\50_xProjects\Umgebungsmodell"))

from EXAM_Control.speed_rpm_gui import iSTEP_SPEED
from EXAM_Control.speed_rpm_gui import iSTEP_RPM
from EXAM_Control.speed_rpm_gui import iMAX_RPM
from EXAM_Control.speed_rpm_gui import iMIN_RPM
from EXAM_Control.speed_rpm_gui import iMIN_SPEED
from EXAM_Control.speed_rpm_gui import iMAX_SPEED
from EXAM_Control.speed_rpm_gui import set_up_meter

from EXAM_Control.speed_rpm_gui import Speedometer
from EXAM_Control.control_gui import ControlGUI


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
        self.signal_list_window = None
        self.speed_gauge = None
        self.rpm_gauge = None
        self.throttle_value = 0
        self.brake_value = 0
        self.steering_value = 0
        self.selected_clamp = 2
        self.drive_state = 0
        self.speed = 0
        self.rpm = 0
        self.car_wheel_angle = 0
        self.timer = 0
        self.program_terminated = False

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

    def build_speed_and_rpm_window(self):
        speed_and_rpm = Speedometer()
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

    def build_signal_list_window(self):
        self.signal_list_window = tkinter.Toplevel(self.main_window)
        self.signal_list_window.geometry('600x300')
        self.signal_list_window.title("Signal list")
        self.signal_list_window.wm_transient(self.main_window)
        self.signal_list_window.geometry("+%d+%d" % (self.x + 50, self.y + 400))
        ControlGUI.create_signal_list(self.signal_list_window)
        ControlGUI.insert_to_signal_list(self.signal_list_window, "Speed", 0, 0)
        ControlGUI.insert_to_signal_list(self.signal_list_window, "RPM", 0, 1)
        ControlGUI.insert_to_signal_list(self.signal_list_window, "Steering angle", 0, 2)
        ControlGUI.insert_to_signal_list(self.signal_list_window, "Drive State", 0, 3)
        ControlGUI.insert_to_signal_list(self.signal_list_window, "Chip Temperature", 0, 4)



    def edit_signal_list(self, list_index, signal_name, signal_value, unit):
        signal_list = ControlGUI.get_signal_list(self.signal_list_window)
        signal_list.item(list_index, text=unit, values=(signal_name, signal_value))

    def quit_button(self):
        self.program_terminated = True
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

    def get_temperature(self, minutes):
        # Temperature curve
        return -(38*(pow(math.e, -((1/4)*minutes))))+60

    def get_steering_angle(self):
        return ControlGUI.get_steering_value(self.steering_window) / 2

    def current_drive_state(self):
        state = ControlGUI.get_drive_state(self.gear_window)
        if state == 0:
            return "P"
        if state == 1:
            return "D"
        if state == 2:
            return "N"
        if state == 3:
            return "R"

    def cool_down_rpm(self, v):
        brake_val = ControlGUI.get_brake_value(self.brake_window)
        if brake_val == 0:
            brake_val = 1
        brake_val = brake_val / 10
        v = v - (0.05 * brake_val)
        if v <= 0:
            time.sleep(0.05)
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
            time.sleep(0.05)
            return 0
        time.sleep(0.05)
        return v

    def increase_speed(self, velocity):
        throttle_val = ControlGUI.get_throttle_value(self.throttle_window)
        if throttle_val == 0:
            return self.cool_down_speed(velocity)
        while velocity <= 50:
            return self.speed_acceleration(throttle_val, velocity)
        return 50

    def increase_rpm(self, v):
        throttle_val = ControlGUI.get_throttle_value(self.throttle_window)
        if throttle_val == 0:
            return self.cool_down_rpm(v)
        while v <= 7:
            return self.rpm_acceleration(throttle_val, v)
        return 7

    def program_update(self):
        self.main_window.after(100, self.update_throttle_window)
        self.main_window.after(100, self.update_brake_window)
        self.main_window.after(100, self.update_gear_window())
        self.main_window.after(100, self.update_clamp_window())
        self.main_window.after(100, self.update_steering_window())
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
        # self.build_plot_window()
        self.build_signal_list_window()

    def run_gui(self):
        self.start_timer_thread()
        while not self.program_terminated:
            try:
                rpm_needle = self.increase_rpm(self.rpm)
                self.rpm = rpm_needle
                speed_needle = self.increase_speed(self.speed)
                self.speed = speed_needle
                self.rpm_gauge.draw_needle(self.rpm)
                self.speed_gauge.draw_needle(speed_needle)
                self.edit_signal_list(0, "Speed", self.speed, "m/s")
                self.edit_signal_list(1, "RPM", self.rpm * 1000, "rpm")
                self.edit_signal_list(2, "Steering angle", self.get_steering_angle(), "degrees")
                self.edit_signal_list(3, "Drive State", self.current_drive_state(), "state")
                self.edit_signal_list(4, "Temperature", self.get_temperature(self.get_time_minutes()), "Celsius")

                self.program_update()
            except:
                pass

    def start_timer_thread(self):
        timer_thread = threading.Thread(target=self.iterate_time)
        timer_thread.start()

    def iterate_time(self):
        while not self.program_terminated:
            time.sleep(1)
            self.timer += 1

    def get_time_minutes(self):
        return self.timer / 60

    def update_throttle_window(self):
        scale = ControlGUI.get_throttle_scale(self.throttle_window)
        scale.set(self.throttle_value)

    def update_brake_window(self):
        ControlGUI.get_brake_scale(self.brake_window).set(self.brake_value)

    def update_steering_window(self):
        ControlGUI.get_steering_scale(self.steering_window).set(self.steering_value)

    def update_gear_window(self):
        ControlGUI.get_drive_state_scale(self.gear_window).set(self.drive_state)

    def update_clamp_window(self):
        if self.selected_clamp == 2:
            ControlGUI.get_clamp_30(self.clamps_window).select()
        if self.selected_clamp == 1:
            ControlGUI.get_clamp_15(self.clamps_window).select()

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

    def get_speed(self):
        return self.speed

    def get_rpm(self):
        return self.rpm

    def get_car_wheel_angle(self):
        return self.car_wheel_angle
