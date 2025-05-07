import easyocr as ocr
import cv2
import time

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)


reader = ocr.Reader(["es"], gpu=False)
capture = cv2.VideoCapture(0)

#triggerear con rfid
rfid=True

cards = []
while capture.isOpened():
    if rfid:
        ret, frame = capture.read()
        frame = ResizeWithAspectRatio(frame, 640)
        result = reader.readtext(frame)[0:4]
        
        person = {}
        prelist = [j for i, j, k in result if k>=0.45]
        try:
            person["name"]=prelist[1]
            person["surname"]=prelist[2]
            person["id"]=prelist[3][3:]

            #cardcode
            rotated90deg = cv2.rotate(frame[100:400, 400:640], cv2.ROTATE_90_COUNTERCLOCKWISE)
            result_cardcode= reader.readtext(rotated90deg)[0]
            person["card_code"]=result_cardcode[1]
            
            
            print(person)
            cards.append(person)
            time.sleep(1)
        except:
            print("Retrying...")
            continue

capture.release()
cv2.destroyAllWindows()