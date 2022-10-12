from control_gui import ControlGUI

class TestControlGUI:

    def test_select_clamp_15(self):
        return 1

    def test_select_clamp_30(self):
        return 2

    def test_set_steering_degrees(self, value):
        return value

    def test_set_throttle(self, value):
        return value

    def test_set_drive_state(self, value):
        return value

    def test_set_brake(self, value):
        return value

    def test_get_throttle_value(self):
        return ControlGUI.get_throttle_value()
