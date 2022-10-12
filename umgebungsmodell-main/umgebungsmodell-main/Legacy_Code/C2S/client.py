import socket
from main import App
import json
import threading
import time


class Client:
    def __init__(self):
        self.HOST = "127.0.0.1"      # The servers hostname or IP address
        self.PORT = 65432            # The port used by the server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Disconnect_msg = "!Disconnect"
        self.FORMAT = "utf-8"
        self.s.connect((self.HOST, self.PORT))

    def stop(self):
        print("[Connection stopped!] The client is disconnecting!")
        self.s.close()


    def recieve(self):
        data = self.s.recv(1024).decode(self.FORMAT)
        if data != self.Disconnect_msg:
            print(f"Received {data}")
            return
        else:
            self.stop()

    def send(self, msg):
        msg = str(msg)
        message = msg.encode(self.FORMAT)
        self.s.send(message)
        line_break = "\n"
        line_break = line_break.encode(self.FORMAT)
        self.s.send(line_break)


def get_input_parameters():
    config_file = open("config.json", "r")
    config_data = config_file.read()
    parameters = json.loads(config_data)
    return parameters['parameters']


def set_input_parameters():
    app.set_throttle(parameters['throttle'])
    app.set_brake(parameters['brake'])
    app.set_steering(parameters['steering'])
    app.set_drive_state(parameters['drive_state'])
    app.set_clamp(parameters['clamps'])

def send_input_parameters(client, parameters):
    app.set_throttle(parameters['throttle'])
    app.set_brake(parameters['brake'])
    app.set_steering(parameters['steering'])
    app.set_drive_state(parameters['drive_state'])
    app.set_clamp(parameters['clamps'])
    client.send("Throttle: " + str(parameters['throttle']))
    client.send("Brake: " + str(parameters['brake']))
    client.send("Steering: " + str(parameters['steering']))
    client.send("Drive State: " + str(parameters['drive_state']))
    client.send("Clamps: " + str(parameters['clamps']))


if __name__ == '__main__':
    app = App()
    cl = Client()
    send_input_parameters(cl, get_input_parameters())
    # TODO: Read output and send it to server
    # client.send(app.get_rpm())
    app.set_up_windows()
    app.quit_program()
    app.run_gui()


