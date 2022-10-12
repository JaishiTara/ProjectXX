import math
import tkinter
from tkinter.font import Font


iWIDTH, iHEIGHT = 300, 300  # Dimensions of the canvas.
fLENGTH_1, fLENGTH_2 = 0.85, 0.3  # Dimensions of the needle, relative to the canvas iRADIUS.
iRADIUS = int(0.7 * iWIDTH / 2)  # Radius of the dial.
iX_POS_0, iY_POS_0 = iWIDTH / 2, iWIDTH / 2  # Position of the center of the circle.
iMIN_SPEED, iMAX_SPEED = 0, 250  # Max and min values on the dial.
iSTEP_SPEED = 20  # Smallest fSpeed division of the dial
iMIN_RPM, iMAX_RPM = 0, 8  # Max and min values on the dial.
iSTEP_RPM = 1  # Smallest division on the dial which has a text value displayed.


class Speedometer(tkinter.Canvas):

    def draw_widget(self, iVel_min, iVel_max, iStep):
        self.iVelocity_min = iVel_min
        self.iVelocity_max = iVel_max
        # self.vmax = vmax
        # x0 = iWIDTH / 2
        # y0 = iWIDTH / 2
        # rad = int(0.7 * iWIDTH / 2)  # dial radius
        self.sTitle = self.create_text(iWIDTH / 2, 12, fill="#000",
                                       font=Font(family="Tahoma", size=12))
        self.create_oval(iX_POS_0 - iRADIUS * 1.1, iY_POS_0 - iRADIUS * 1.1,
                         iX_POS_0 + iRADIUS * 1.1, iY_POS_0 + iRADIUS * 1.1,
                         fill="red")  # Outercircle
        self.create_oval(iX_POS_0 - iRADIUS, iY_POS_0 - iRADIUS,
                         iX_POS_0 + iRADIUS, iY_POS_0 + iRADIUS, fill="#000")  # inner dial
        self.create_oval(iX_POS_0 - iRADIUS * 0.1, iY_POS_0 - iRADIUS * 0.1,
                         iX_POS_0 + iRADIUS * 0.1, iY_POS_0 + iRADIUS * 0.1,
                         fill="white")  # Needle center

        # Fill values of each step and create ticks.
        iRange_val = 1 + int((iVel_max - iVel_min) / iStep)
        for i in range(iRange_val):
            iStep_display = iVel_min + iStep * i
            fAngle = (5 + 6 * ((iStep * i) / (iVel_max - iVel_min))) * math.pi / 4
            self.create_line(iX_POS_0 + iRADIUS * math.sin(fAngle) * 0.9,
                             iY_POS_0 - iRADIUS * math.cos(fAngle) * 0.9,
                             iX_POS_0 + iRADIUS * math.sin(fAngle) * 0.98,
                             iY_POS_0 - iRADIUS * math.cos(fAngle) * 0.98,
                             fill="#FFF", width=2)
            self.create_text(iX_POS_0 + iRADIUS * math.sin(fAngle) * 0.75,
                             iY_POS_0 - iRADIUS * math.cos(fAngle) * 0.75,
                             text=iStep_display, fill="#FFF",
                             font=Font(family="Tahoma", size=12))
            if i == int(iVel_max - iVel_min) / iStep:
                continue
            for iDv in range(1, 5):
                fAngle = (5 + 6 * ((iStep_display + iDv * (iStep / 5) - iVel_min) /
                                   (iVel_max - iVel_min))) * math.pi / 4
                self.create_line(iX_POS_0 + iRADIUS * math.sin(fAngle) * 0.94,
                                 iY_POS_0 - iRADIUS * math.cos(fAngle) * 0.94,
                                 iX_POS_0 + iRADIUS * math.sin(fAngle) * 0.98,
                                 iY_POS_0 - iRADIUS * math.cos(fAngle) * 0.98, fill="#FFF")
        self.unit = self.create_text(iWIDTH / 2, iY_POS_0 + 0.8 * iRADIUS, fill="#FFF",
                                     font=Font(family="Tahoma", size=12))
        self.needle = self.create_line(
                                       iX_POS_0 - iRADIUS * math.sin(5 * math.pi / 4) * fLENGTH_2,
                                       iY_POS_0 + iRADIUS * math.cos(5 * math.pi / 4) * fLENGTH_2,
                                       iX_POS_0 + iRADIUS * math.sin(5 * math.pi / 4) * fLENGTH_1,
                                       iY_POS_0 - iRADIUS * math.cos(5 * math.pi / 4) * fLENGTH_1,
                                       width=2, fill="#FFF")

    # Draws the needle based on the fSpeed.
    def draw_needle(self, fVelocity):
        fVelocity = max(fVelocity, self.iVelocity_min)  # If input is less than 0
        fVelocity = min(fVelocity, self.iVelocity_max)  # If input is greater than max
        fAngle = (5 + 6 * ((fVelocity - self.iVelocity_min) /
                           (self.iVelocity_max - self.iVelocity_min))) * math.pi / 4
        self.coords(self.needle,
                    iX_POS_0 - iRADIUS * math.sin(fAngle) * fLENGTH_2,
                    iY_POS_0 + iRADIUS * math.cos(fAngle) * fLENGTH_2,
                    iX_POS_0 + iRADIUS * math.sin(fAngle) * fLENGTH_1,
                    iY_POS_0 - iRADIUS * math.cos(fAngle) * fLENGTH_1)

    def set_gauge_meters(self):
        """
        set up fSpeed and fRpm gui
        :return:
        """
        self.speed_gauge = set_up_meter(self, iMin_val=iMIN_SPEED, iMax_val=iMAX_SPEED,
                                        iStep_val=iSTEP_SPEED, sTitle='Speed', iunit='KMPH')
        self.rpm_gauge = set_up_meter(self, iMin_val=iMIN_RPM, iMax_val=iMAX_RPM,
                                      iStep_val=iSTEP_RPM, sTitle='RPM', iunit='x1000')
        self.label = tkinter.Label(self.speed_gauge, text='0', fg="Red", anchor="center",
                           font=("Helvetica", 12))
        self.label.place(x=142, y=190)

def set_up_meter(root, iMin_val, iMax_val, iStep_val, sTitle, iunit):
    meters = tkinter.Frame(root, width=iWIDTH, height=iWIDTH, bg="white")
    meter_unit = Speedometer(meters, width=iWIDTH, height=iWIDTH)
    meter_unit.draw_widget(iMin_val, iMax_val, iStep_val)
    #meter_unit.pack(side=LEFT, anchor=N, fill=Y)
    if sTitle == 'Speed':
        meter_unit.grid(row=0, column=0, sticky="w")
        meters.grid(row=0, column=0, sticky="w")
    elif sTitle == 'RPM':
        meter_unit.grid(row=0, column=1, sticky="w")
        meters.grid(row=0, column=1, sticky="w")
    meter_unit.itemconfig(meter_unit.sTitle, text=sTitle)
    meter_unit.itemconfig(meter_unit.unit, text=iunit)
    #meters.pack(side=LEFT, anchor=N, fill=Y)
    return meter_unit
