import random
import time

import network
from machine import Pin

import ufirebase as firebase

_SSID = "YOUR_SSID_HERE"
_KEY = "YOUR_KEY_HERE"
_FIREBASE_URL = "YOUR_FIREBASE_RTDB_URL_HERE"
_MAX_ATTEMPT_LIMIT = 15
_led = Pin(2, Pin.OUT)
_ap_gen_pwd = "".join(random.choice('abcdefghijklmnopqrstuvwxyz1234567890') for _ in range(8))


def _connect(_ssid: str, _key: str, _max_attempt_limit: int = _MAX_ATTEMPT_LIMIT, led=_led) -> bool:
    led.on()
    time.sleep(0.5)
    wlan = network.WLAN(network.STA_IF)
    led.off()
    wlan.active(True)
    if wlan.isconnected():
        print("Already connected to " + _ssid)
        led.on()
        return True
    print("Attempting connection to '" + _ssid + "'...")
    wlan.connect(_ssid, _key)
    counter = time.time()
    while not wlan.isconnected() and time.time() - counter < _max_attempt_limit:
        pass
    if wlan.isconnected():
        print("Connected to '" + _ssid + "' successfully")
        led.on()
        return True
    else:
        print("Connection to '" + _ssid + "' failed: Maximum attempt limit reached.")
        led.off()
        return False


def _setup_access_point(led=_led, ap_gen_pwd=_ap_gen_pwd) -> None:
    led.on()
    time.sleep(0.5)
    led.off()
    wlan = network.WLAN(network.AP_IF)
    wlan.active(True)
    wlan.config(essid="DASH Server-Connect",
                password=ap_gen_pwd,
                authmode=3)
    while not wlan.active():
        pass
    led.on()
    print("Access point setup successfully.\nSSID: 'DASH Server-Connect', Password:", ap_gen_pwd)


def _disconnect() -> None:
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()
    wlan.active(False)


def _set_firebase_connection(_path: str):
    try:
        firebase.setURL(_path)
    except:
        raise OSError("Connection to Firebase failed")


def get_data(_path: str):
    try:
        firebase.get(_path, "res")
        return firebase.res
    except:
        raise OSError("Connection to Firebase failed")


def get_data_shallow(_path: str):
    try:
        firebase.get(_path, "res", limit=True)
        return firebase.res
    except:
        raise OSError("Connection to Firebase failed")


if __name__ == '__main__':
    while True:
        if _connect(_SSID, _KEY):
            break
        else:
            if str(input("Connect to WiFi? (y/n) ")) == "y":
                # setup personal hotspot on the esp32
                pass
            else:
                _setup_access_point()
                break
    try:
        _set_firebase_connection(_FIREBASE_URL)
        print(get_data_shallow("devices"))
    except OSError:
        print('Connection to Firebase failed.')
    if str(input("Disconnect from WiFi? (y/n) ")) == "y":
        _disconnect()
    # pprint(get_data("devices"))
