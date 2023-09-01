import ufirebase as firebase
from machine import Pin
import time, network
from pprint import pprint

_SSID = "YOUR_WIFI_SSID"
_KEY = "YOUR_WIFI_PASSWORD"
_FIREBASE_URL = "YOUR_FIREBASE_URL"
_MAX_ATTEMPT_LIMIT = 15
_led = Pin(2, Pin.OUT)


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
    print("Attempting connection to " + _ssid + "...")
    wlan.connect(_ssid, _key)
    counter = time.time()
    while not wlan.isconnected() and time.time() - counter < _max_attempt_limit:
        pass
    if wlan.isconnected():
        print("Connected to " + _ssid + " successfully")
        led.on()
        return True
    else:
        print("Connection to " + _ssid + " failed: Maximum attempt limit reached.")
        led.off()
        return False


def _disconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()
    wlan.active(False)


def _set_firebase_connection(_path):
    try:
        firebase.setURL(_path)
    except:
        raise OSError("Connection to Firebase failed")


def get_data(_path):
    try:
        firebase.get(_path, "res")
        return firebase.res
    except:
        raise OSError("Connection to Firebase failed")


def get_data_shallow(_path):
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
                print("Exiting...")
                exit(0)
    _set_firebase_connection(_FIREBASE_URL)
    pprint(get_data_shallow("devices"))
    if str(input("Disconnect from WiFi? (y/n) ")) == "y":
        _disconnect()
    # pprint(get_data("devices"))
