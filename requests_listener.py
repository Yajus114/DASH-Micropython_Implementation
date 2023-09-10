import urequests as res

data = res.get("YOUR_FIREBASE_RTDB_URL/PARENT_NAME.json").json()
while True:
  if data != res.get("YOUR_FIREBASE_RTDB_URL/PARENT_NAME.json").json():
    break
print("BROKEN")
