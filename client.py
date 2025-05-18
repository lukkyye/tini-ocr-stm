import cv2
import base64
import requests

def cv2_to_base64(img):
    _, img_encoded = cv2.imencode('.jpg', img)
    img_bytes = img_encoded.tobytes()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    return img_base64

cam = cv2.VideoCapture(0)
ret, frame = cam.read()
print("Done! You can grab your card")
cam.release()

if ret:
    data = {
        "data": cv2_to_base64(frame)
    }
    response = requests.post("http://127.0.0.1:8000/api", json=data)
    if response.status_code == 200:
        print(f"{response.status_code}, {response.json()}")
    else:
        print(f"{response.content}, {response.status_code}")
else:
    print("Error, camera didnt took any frame")