import tkinter
from tkinter import *
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler

class ControlGUI(Frame):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.throttle_scale = None
        self.brake_scale = None
        self.steering_scale = None
        self.drive_scale = None
        self.iDrive_State = None
        self.checkbox_clamp_15 = None
        self.checkbox_clamp_30 = None

    def create_drive(self, value):
        scale_labels = {
            0: "Park",
            1: "Drive",
            2: "Neutral",
            3: "Reverse"
        }
        self.drive_scale = Scale(self, length=250, from_=min(scale_labels),
                             to=max(scale_labels), orient=VERTICAL, troughcolor="black")
        self.drive_scale.set(value)

        box_park= Label(self, text="P", bg="green", fg="white")
        box_drive = Label(self, text="D", bg="green", fg="white")
        box_neutral = Label(self, text="N", bg="green", fg="white")
        box_reverse = Label(self, text="R", bg="green", fg="white")
        car_mode = Label(self, text="GEAR", fg="red",
                         font=("Arial", 12, 'bold'))

        self.drive_scale.place(x=80, y=35)
        car_mode.place(x=75, y=10)
        box_park.place(x=120, y=45)
        box_drive.place(x=120, y=117)
        box_neutral.place(x=120, y=190)
        box_reverse.place(x=120, y=260)

    def create_throttle(self, value, low=0, high=0):
        self.throttle_scale = Scale(self, length=250, from_=100, to=0,
                               orient=VERTICAL)

        self.throttle_label = Label(self, text="THROTTLE", fg="red",
                               font=("Arial", 12, 'bold'))
        self.throttle_scale.set(value)
        self.throttle_label.pack()
        self.throttle_scale.pack()

    def create_brake(self, value):
        self.brake_scale = Scale(self, length=250, from_=100, to=0,
                            orient=VERTICAL)
        brake_label = Label(self, text="BRAKE", fg="red",
                            font=("Arial", 12, 'bold'))
        self.brake_scale.set(value)
        brake_label.pack()
        self.brake_scale.pack()

    def create_steering(self, value, lmax=-90, rmax=90):
        self.steering_scale = Scale(self, length=200, from_=lmax, to=rmax,
                               orient=HORIZONTAL, troughcolor='black')
        self.steering_scale.set(value)
        steering = Label(self, text="STEERING WHEEL", fg="red",
                         font=("Arial", 12, 'bold'))
        vertical_left = Frame(self, bg='blue', height=40, width=10)
        vertical_right = Frame(self, bg='blue', height=40, width=10)

        self.steering_scale.place(x=32, y=110)
        steering.place(x=60, y=50)
        vertical_left.place(x=28, y=100)
        vertical_right.place(x=234, y=100)

    def create_plot(self, value):
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True
        # iSpeedometerOutput = 3
        Figure_Window = Figure(figsize=(5, 5), dpi=100)
        ax = Figure_Window.add_subplot()
        ax.set_xlabel('Time in s')
        ax.set_ylabel('Speed in Kmph')
        # ax.set_xlim(0, 2)
        # ax.set_ylim(-2, 2)
        v = 50

        x = np.linspace(0, v, 100)
        y = []
        for i in range(0, 100):
            y.append(value)

        # PLOT = ax.plot([], [], lw=7)
        Drawing_Area = FigureCanvasTkAgg(Figure_Window, master=self)
        Toolbar = NavigationToolbar2Tk(Drawing_Area, self)

        # def init():
        # PLOT.set_data([],[])
        # return PLOT,

        def animate(frame):
            # y = np.sin(np.pi * (x - 0.01 * i))
            # PLOT.set_data(x, y)
            # y=randint(1,10)
            ax.set_xlim(left=frame, right=frame + 5)
            ax.plot(x, y)

            # ax.set_ylim(-2, 2)
            # return PLOT

        ani = animation.FuncAnimation(Figure_Window, animate, frames=v)

        #########################################

        # Drawing_Area = FigureCanvasTkAgg(Figure_Window, master=self)
        Drawing_Area.draw()
        Drawing_Area.get_tk_widget().pack(side=tkinter.TOP,
                                          fill=tkinter.BOTH, expand=1)

        Toolbar.update()
        Drawing_Area.get_tk_widget().pack(side=tkinter.TOP,
                                          fill=tkinter.BOTH, expand=1)

    def create_plot_throttle(self, throttle_value):
        plt.rcParams["figure.figsize"] = [7.50, 3.50]
        plt.rcParams["figure.autolayout"] = True
        # iSpeedometerOutput = 3
        Figure_Window = Figure(figsize=(5, 5), dpi=100)
        ax = Figure_Window.add_subplot()
        ax.set_xlabel('Time in s')
        ax.set_ylabel('Speed in Kmph')
        # ax.set_xlim(0, 2)
        # ax.set_ylim(-2, 2)
        v = 10
        x = np.linspace(0, v, 10)
        y = []
        for i in range(0, 10):
            y.append(throttle_value)

        # PLOT = ax.plot([], [], lw=7)
        Drawing_Area = FigureCanvasTkAgg(Figure_Window, master=self)
        Toolbar = NavigationToolbar2Tk(Drawing_Area, self)

        # def init():
        # PLOT.set_data([],[])
        # return PLOT,

        def animate(frame):
            # y = np.sin(np.pi * (x - 0.01 * i))
            # PLOT.set_data(x, y)
            # y=randint(1,10)
            ax.set_xlim(left=frame, right=frame + 5)
            ax.plot(x, y)
            # ax.set_ylim(-2, 2)
            # return PLOT

        ani = animation.FuncAnimation(Figure_Window, animate, frames=v)

        #########################################

        # Drawing_Area = FigureCanvasTkAgg(Figure_Window, master=self)
        Drawing_Area.draw()
        Drawing_Area.get_tk_widget().pack(side=tkinter.TOP,
                                          fill=tkinter.BOTH, expand=1)

        Toolbar.update()
        Drawing_Area.get_tk_widget().pack(side=tkinter.TOP,
                                          fill=tkinter.BOTH, expand=1)


        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, Drawing_Area, Toolbar)

        Drawing_Area.mpl_connect("key_press_event", on_key_press)

    def create_clamps(self, value_15, value_30):
            clamp_30 = IntVar()
            clamp_15 = IntVar()
            self.checkbox_clamp_15 = Checkbutton(self, text="Clamp 15",
                                            variable=clamp_15)
            self.checkbox_clamp_30 = Checkbutton(self, text="Clamp 30",
                                            variable=clamp_30)
            self.checkbox_clamp_15.pack()
            self.checkbox_clamp_30.pack()
            if value_15 == 0:
                self.checkbox_clamp_15.deselect()
            if value_30 == 1:
                self.checkbox_clamp_30.select()
            if value_15 == 1:
                self.checkbox_clamp_15.select()
            if value_30 == 0:
                self.checkbox_clamp_30.deselect()

            self.clamp_15 = clamp_15
            self.clamp_30 = clamp_30

    def create_signal_list(self):
        self.signal_list = ttk.Treeview(self)
        self.signal_list['columns'] = ("Signal Name", "Value")
        self.signal_list.column("#0", width=120, minwidth=25)
        self.signal_list.column("Value", anchor=W, width=120)

        self.signal_list.heading("#0", text="Index", anchor=W)
        self.signal_list.heading("Signal Name", text="Signal Name", anchor=W)
        self.signal_list.heading("Value", text="Value", anchor=W)
        self.signal_list.pack(pady=20)

    def create_output_list(self):
        self.output_list = ttk.Treeview(self)

        self.output_list['columns'] = ("Output Name", "Value")
        self.output_list.column("#0", width=120, minwidth=25)
        self.output_list.column("Value", anchor=W, width=120)

        self.output_list.heading("#0", text="Unit", anchor=W)
        self.output_list.heading("Output Name", text="Output Name", anchor=W)
        self.output_list.heading("Value", text="Value", anchor=W)
        self.output_list.pack(pady=20)


    def insert_to_signal_list(self, signal_name, signal_value, list_index):
        self.signal_list.insert(parent='', index='end', iid=list_index, text="Signals", values=(signal_name, signal_value))

    def insert_to_output_list(self, output_name, output_value, list_index):
        self.output_list.insert(parent='', index='end', iid=list_index, text="Output", values=(output_name, output_value))

    def get_signal_list(self):
        return self.signal_list

    def get_output_list(self):
        return self.output_list

    def get_throttle_value(self):
        return self.throttle_scale.get()

   # def get_zero_throttle_value(self):
     #   return self.zero_throttle_scale.get()

    def get_brake_value(self):
        return self.brake_scale.get()

    def get_throttle_scale(self):
        return self.throttle_scale

   # def get_zero_throttle_scale(self):
    #    return self.zero_throttle_scale

    def get_brake_scale(self):
        return self.brake_scale

    def get_steering_scale(self):
        return self.steering_scale

    def get_drive_state_scale(self):
        return self.drive_scale

    def get_car_state(self):
        return self.iDrive_State

    def get_clamp_15(self):
        return self.checkbox_clamp_15.select()

    def get_clamp_30(self):
        return self.checkbox_clamp_30.select()

    def get_steering_value(self):
        return self.steering_scale.get()

    def get_drive_state(self):
        return self.drive_scale.get()

    def get_clamp_15_selection(self):
        return self.clamp_15.get()

    def get_clamp_30_selection(self):
        return self.clamp_30.get()
