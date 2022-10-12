import time
from os import path
import sys
import tkinter
import threading
import math
from tkinter import ttk, BOTH, TRUE

from virtual_picar.speed_rpm_gui import iSTEP_SPEED
from virtual_picar.speed_rpm_gui import iSTEP_RPM
from virtual_picar.speed_rpm_gui import iMAX_RPM
from virtual_picar.speed_rpm_gui import iMIN_RPM
from virtual_picar.speed_rpm_gui import iMIN_SPEED
from virtual_picar.speed_rpm_gui import iMAX_SPEED
from virtual_picar.speed_rpm_gui import set_up_meter

from virtual_picar.speed_rpm_gui import Speedometer
from virtual_picar.control_gui import ControlGUI


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
        self.iThrottle_Value = 0
        self.iBrake_Value = 0
        self.iSteering_Value = 0
        self.iSelected_Clamp_15 = 0
        self.iSelected_Clamp_30 = 1
        self.iDrive_State = 0
        self.fSpeed = 0
        self.fRpm = 0
        self.fAcceleration = 0.5    # 1 = Normal
        self.fCool_Down_Acceleration = 0    # 1 = Normal
        self.iTimer = 0
        self.bProgram_terminated = False

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
        ControlGUI.create_throttle(self.throttle_window, self.iThrottle_Value)

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
        ControlGUI.create_drive(self.gear_window, self.iDrive_State)

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
        ControlGUI.create_plot(frame1, self.iThrottle_Value)
        ControlGUI.create_plot_throttle(frame2, self.iBrake_Value)

    def build_steering_window(self):
        self.steering_window = tkinter.Toplevel(self.main_window)
        self.steering_window.geometry('280x200')
        self.steering_window.title("Steering Window")
        self.steering_window.wm_transient(self.main_window)
        self.steering_window.geometry("+%d+%d" % (self.x + 860, self.y + 400))
        ControlGUI.create_steering(self.steering_window, self.iSteering_Value)

    def build_brake_window(self):
        self.brake_window = tkinter.Toplevel(self.main_window)
        self.brake_window.geometry('200x300')
        self.brake_window.title("Brake Window")
        self.brake_window.wm_transient(self.main_window)
        self.brake_window.geometry("+%d+%d" % (self.x + 1600, self.y + 400))
        ControlGUI.create_brake(self.brake_window, self.iBrake_Value)

    def build_clamps_window(self):
        self.clamps_window = tkinter.Toplevel(self.main_window)
        self.clamps_window.geometry('190x50')
        self.clamps_window.title("Clamps 15/30 Window")
        self.clamps_window.wm_transient(self.main_window)
        self.clamps_window.geometry("+%d+%d" % (self.x + 1600, self.y + 750))
        ControlGUI.create_clamps(self.clamps_window, self.iSelected_Clamp_15, self.iSelected_Clamp_30)

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
        self.bProgram_terminated = True
        self.main_window.quit()
        self.main_window.destroy()

    def rpm_acceleration(self, iThrottle, fVelocity):
        fAcceleration_Factor = self.fAcceleration / 1000
        time.sleep(0.05)
        return fVelocity + (fAcceleration_Factor * iThrottle)

    def speed_acceleration(self, iThrottle, fVelocity):
        fAcceleration_Factor = self.fAcceleration / 142.8571
        time.sleep(0.05)
        return fVelocity + (fAcceleration_Factor * iThrottle)

    def get_temperature(self, fMinutes):
        # Temperature curve
        return -(38 * (pow(math.e, -((1 / 4) * fMinutes)))) + 60

    def get_steering_angle(self):
        iSTEERING_AND_WHEEL_RATIO = 4
        return (ControlGUI.get_steering_value(self.steering_window) / iSTEERING_AND_WHEEL_RATIO)

    def current_drive_state(self):
        iState = ControlGUI.get_drive_state(self.gear_window)
        if iState == 0:
            return "P"
        if iState == 2:
            return "D"
        if iState == 1:
            return "N"
        if iState == 3:
            return "R"

    def cool_down_rpm(self, fVelocity):
        fCool_Down_Factor = self.fCool_Down_Acceleration / 200
        iBrake = ControlGUI.get_brake_value(self.brake_window)
        if iBrake == 0:
            iBrake = 1
        fVelocity = fVelocity - (fCool_Down_Factor * iBrake)
        if fVelocity <= 0:
            time.sleep(0.05)
            return 0
        time.sleep(0.05)
        return fVelocity

    def cool_down_speed(self, fVelocity):
        fCool_Down_Factor = self.fCool_Down_Acceleration / 27.8
        iBrake = ControlGUI.get_brake_value(self.brake_window)
        if iBrake == 0:
            iBrake = 1
        fVelocity = fVelocity - (fCool_Down_Factor * iBrake)
        if fVelocity <= 0:
            time.sleep(0.05)
            return 0
        time.sleep(0.05)
        return fVelocity

    def increase_speed(self, fVelocity):
        MAX_SPEED = 50
        iThrottle = ControlGUI.get_throttle_value(self.throttle_window)
        if iThrottle == 0:
            return self.cool_down_speed(fVelocity)
        while fVelocity <= MAX_SPEED:
            return self.speed_acceleration(iThrottle, fVelocity)
        return MAX_SPEED

    def increase_rpm(self, fVelocity):
        MAX_RPM = 7  # 7 * 1000 = 7000 fRpm
        iThrottle = ControlGUI.get_throttle_value(self.throttle_window)
        if iThrottle == 0:
            return self.cool_down_rpm(fVelocity)
        while fVelocity <= MAX_RPM:
            return self.rpm_acceleration(iThrottle, fVelocity)
        return MAX_RPM

    def update_speed_and_rpm_gui(self):
        rpm_needle = self.increase_rpm(self.fRpm)
        self.fRpm = rpm_needle
        speed_needle = self.increase_speed(self.fSpeed)
        self.fSpeed = speed_needle
        self.rpm_gauge.draw_needle(self.fRpm)
        self.speed_gauge.draw_needle(speed_needle)

    def update_signal_list_outputs(self):
        self.edit_signal_list(0, "Speed", self.fSpeed * 4, "m/s")
        self.edit_signal_list(1, "RPM", self.fRpm * 1000 * 2, "Rpm")
        self.edit_signal_list(2, "Steering angle", self.get_steering_angle(), "degrees")
        self.edit_signal_list(3, "Drive State", self.current_drive_state(), "state")
        self.edit_signal_list(4, "Temperature", self.get_temperature(self.get_time_minutes()) - 1000, "Celsius")

    def start_timer_thread(self):
        timer_thread = threading.Thread(target=self.iterate_time)
        timer_thread.start()

    def iterate_time(self):
        while not self.bProgram_terminated:
            time.sleep(1)
            self.iTimer += 1

    def get_time_minutes(self):
        return self.iTimer / 60

    def update_throttle_window(self):
        ControlGUI.get_throttle_scale(self.throttle_window).set(self.iThrottle_Value)

    def update_brake_window(self):
        ControlGUI.get_brake_scale(self.brake_window).set(self.iBrake_Value)

    def update_steering_window(self):
        ControlGUI.get_steering_scale(self.steering_window).set(self.iSteering_Value)

    def update_gear_window(self):
        ControlGUI.get_drive_state_scale(self.gear_window).set(self.iDrive_State)

    def update_clamp_window(self):
        if self.iSelected_Clamp_15 == 1:
            ControlGUI.get_clamp_15(self.clamps_window).select()
        if self.iSelected_Clamp_15 == 0:
            ControlGUI.get_clamp_15(self.clamps_window).deselect()
        if self.iSelected_Clamp_30 == 1:
            ControlGUI.get_clamp_30(self.clamps_window).select()
        if self.iSelected_Clamp_30 == 0:
            ControlGUI.get_clamp_30(self.clamps_window).deselect()

    def set_throttle(self, value):
        self.iThrottle_Value = value / 2

    def set_brake(self, value):
        self.iBrake_Value = value * 5

    def set_steering(self, value):
        self.iSteering_Value = -value

    def select_clamp_15(self):
        self.iSelected_Clamp_30 = 1

    def deselect_clamp_15(self):
        self.iSelected_Clamp_30 = 0

    def select_clamp_30(self):
        self.iSelected_Clamp_15 = 1

    def deselect_clamp_30(self):
        self.iSelected_Clamp_15 = 0

    def set_drive_state(self, mode):
        self.iDrive_State = mode

    def get_speed(self):
        return self.fSpeed

    def get_rpm(self):
        return self.fRpm

    def get_throttle(self):
        return self.iThrottle_Value

    def get_brake(self):
        return self.iBrake_Value

    def get_steering(self):
        return self.iSteering_Value

    def get_drive_state(self):
        return self.iDrive_State

    def get_clamp_15(self):
        return self.iSelected_Clamp_15

    def get_clamp_30(self):
        return self.iSelected_Clamp_30

    def quit_model(self):
        self.bProgram_terminated = True

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
        self.build_plot_window()
        self.build_signal_list_window()

    def quit_program(self):
        quit_button = tkinter.Button(master=self.main_window, text="Quit",
                                     command=self.quit_button)
        quit_button.pack(side=tkinter.BOTTOM)

    def run_gui(self):
        self.start_timer_thread()
        while not self.bProgram_terminated:
            try:
                self.update_speed_and_rpm_gui()
                self.update_signal_list_outputs()
                self.program_update()
            except:
                pass
