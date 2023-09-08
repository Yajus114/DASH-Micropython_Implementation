import random
import time

import network
from machine import Pin

import ufirebase as firebase


_SSID = 'YOUR_WIFI_SSID'
_KEY = 'YOUR_WIFI_KEY'
_FIREBASE_URL = 'YOUR_FIREBASE_URL'

_MAX_ATTEMPT_LIMIT = 15
_led = Pin(2, Pin.OUT)
_ap_gen_pwd = "".join(random.choice('abcdefghijklmnopqrstuvwxyz1234567890') for _ in
                      range(8))  # random.mpy doesn't have random.choices for some reason
_wlan_sta = network.WLAN(network.STA_IF)
_wlan_ap = network.WLAN(network.AP_IF)


def _connect(ssid: str, key: str, max_attempt_limit: int = _MAX_ATTEMPT_LIMIT, led=_led, wlan=_wlan_sta) -> bool:
    led.on()
    time.sleep(0.5)
    led.off()
    wlan.active(True)
    if wlan.isconnected():
        print("Already connected to " + ssid)
        led.on()
        return True
    print("Attempting connection to '" + ssid + "'...")
    wlan.connect(ssid, key)
    counter = time.time()
    while not wlan.isconnected() and time.time() - counter < max_attempt_limit:
        pass
    if wlan.isconnected():
        print("Connected to '" + ssid + "' successfully")
        led.on()
        return True
    else:
        print("Connection to '" + ssid + "' failed: Maximum attempt limit reached.")
        led.off()
        wlan.active(False)
        return False


def _setup_access_point(led=_led, ap_gen_pwd=_ap_gen_pwd, wlan=_wlan_ap) -> None:
    led.on()
    time.sleep(0.5)
    led.off()
    wlan.active(True)
    wlan.config(essid="DASH Server-Connect",
                password=ap_gen_pwd,
                authmode=3)
    while not wlan.active():
        pass
    led.on()
    print("Access point setup successfully.\nSSID: 'DASH Server-Connect', Password:", ap_gen_pwd)


def _disconnect(wlan, led=_led) -> None:
    try:
        wlan.disconnect()
        wlan.active(False)
        led.off()
    except Exception as e:
        print(f"An error occurred: Couldn't disconnect.\n{e}")


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
                continue
            else:
                _setup_access_point()
                break
    try:
        _set_firebase_connection(_FIREBASE_URL)
        print(get_data("devices"))
    except OSError:
        print('Connection to Firebase failed.')
    if str(input("Disconnect from WiFi? (y/n) ")) == "y":
        _disconnect(_wlan_sta if _wlan_sta.active() else _wlan_ap)
