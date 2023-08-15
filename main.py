import ufirebase as firebase
from machine import Pin
import time, network
from pprint import pprint

_SSID = "e21 5g"
_KEY = "a1b2c3d4e5f6"
_FIREBASE_URL = "https://dash-24-default-rtdb.asia-southeast1.firebasedatabase.app/"
_MAX_ATTEMPT_LIMIT = 15
_led = Pin(2, Pin.OUT)

def _connect(_ssid: str, _key: str, _max_attempt_limit: int = _MAX_ATTEMPT_LIMIT, led = _led) -> bool:
    led.on()
    time.sleep(0.5)
    wlan = network.WLAN(network.STA_IF)
    led.off()
    wlan.active(True)
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
                pass
            else:
                print("Exiting...")
                SystemExit()
    _set_firebase_connection(_FIREBASE_URL)
    pprint(get_data_shallow("devices"))
    # pprint(get_data("devices"))
