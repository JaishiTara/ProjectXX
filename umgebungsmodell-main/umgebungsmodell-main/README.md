# Environmental model



## Overall description
The purpose of the environmental model is to simulate the [PiCar](https://team.in-tech.global/display/COC15/0.4.1.1+General+Information) behaviour. The model is represented by a graphical
interface where you can manipulate the essential parameters of the car. Depending on the parameters the GUI gives
feedback about the output. In addition the plot window shows the course of the input parameters.  
The environmental model is also able to be controlled from external tools like EXAM. There are some API functions for
the most important intends which you can find [here](https://team.in-tech.global/display/COC15/0.4.1.1.4+Umgebungsmodell+API).

## PiCar package

### Components
- **speed_rpm_gui.py** creates the widgets for the speedometer and the RPM indicator. This module is also responsible
for drawing and updating the needle position.
- **control_gui.py** is used to set up the scaling and look of all widgets except of the speedometer and RPM.
The model also includes some getter functions to get important variables to control and manipulate the widgets.
- **main.py** is the root of the application. Here are the windows built and the initial parameter of the widgets set.
Furthermore there are some functions to which have access to the speed and rpm needle to move them.

### Getting started
- All you have to do is to start the test suites i EXAM and run some tests. EXAM opens the application automatically.



## Legacy code (Don't use this fo EXAM)
This is a collection of old code which was used in the past. However, if you want test some functions in the model without
using EXAM (e.g. the EXAM server is down), use the EXAM_Control package to do so.

### Components
- For **speed_rpm_gui.py**, **control_gui.py** and **main.py** read the description above.
- **client.py** is a module which is representative as an EXAM client. It's used for testing some new functions to take 
over them to the real EXAM code, later on.

### Getting started
Run the `client.py` file in your IDE or start the client.ba file in your file explorer.

Now the environmental model should start and the input parameters should be set.


## More information about the Project
- Python Version: `3.9`
- The UI runs on the Tkinter framework
