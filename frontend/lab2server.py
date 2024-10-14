import socket
import time
from time import sleep
from threading import Thread
from json import dumps

from random import randint
from ultrasonic import measure_distance, gpio_clean_up

import SpiderG
from constants import Directions
HOST = '0.0.0.0'
PORT = 65432

SpiderG.move_init()

class Spider:
    def __init__(self):
        self.busy = False

        self.mapping = {
            "right": Directions.TURN_RIGHT.value,
            "left": Directions.TURN_LEFT.value,
            "forward": Directions.FORWARD.value,
            "backward": Directions.BACKWARD.value,
        }

    def is_busy(self):
        return self.busy

    def perform_action(self, action):
        resp = {"action": action, "result": None, "success": False}
        if action in ["right", "left", "forward", "backward"]:
            if not self.busy:
                resp.update({"result": self._move(action)})
        elif action == "distance":
            resp.update({"result": self._get_distance()})
        elif action == "busy":
            resp.update({"result": self.is_busy()})
        elif action == "random":
            resp.update({"result": self._random_data()})
        resp.update({"success": True})
        return resp

    def _move_handler(self, direction):
        try:
            self.busy = True
            SpiderG.walk(self.mapping[direction])
            time.sleep(2)
            SpiderG.servoStop()
        except Exception as e:
            print(e)
        self.busy = False

    def _move(self, direction):
        resp = "Bot is busy"
        if not self.busy:
            Thread(target=self._move_handler, args=(direction,)).start()
            resp = f"Moving f{direction}"
        return resp

    @staticmethod
    def _random_data():
        resp = randint(1, 100)
        print(f"Random Data: {resp}")
        return resp

    @staticmethod
    def _get_distance():
        return measure_distance()

    @staticmethod
    def clean_up():
        print("clean up")
        gpio_clean_up()
        SpiderG.servoStop()
        SpiderG.move_init()

spider = Spider()
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            break
                        command = data.decode().strip('\r').strip('\n')
                        reply = spider.perform_action(command)
                        conn.sendall(dumps(reply).encode('utf-8'))
                    except Exception as e:
                        print(e)
except KeyboardInterrupt:
    s.close()
    spider.clean_up()
finally:
    s.close()
    spider.clean_up()