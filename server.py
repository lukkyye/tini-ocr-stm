from PIL import Image
import io
from flask import Flask, request
import cv2.typing
import base64
import numpy as np
import easyocr as ocr

server = Flask("ocr-server")
CONFIDENCE=0.45

#data: b64
def to_ndarray(data)->np.ndarray:
    img_bytes = base64.b64decode(data)
    pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    return np.array(pil_img)

def get_ocr(img: cv2.typing.MatLike | np.ndarray)->dict:
    result: list = reader.readtext(img)[0:4]
    person: dict | int = {}
    prelist: list = [j for i, j, k in result if k>=CONFIDENCE]
    try:
        person["name"]=prelist[1]
        person["surname"]=prelist[2]
        person["id"]=prelist[3][3:]
        
        #cardid
        rotated90deg: cv2.typing.MatLike = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        result_cardcode: str = reader.readtext(rotated90deg)[0]
        person["card_id"]=result_cardcode[1]
    except:
        return 400
    return person
    
@server.route("/", methods=["POST"])
def main()-> tuple[str, int] | tuple[dict, int]:
    request_data = request.get_json(force=True)
    if 'data' not in request_data:
        return "bad request", 400
    
    try:
        #easyocr.readtext works with ndarray also
        ndarray= to_ndarray(request_data['data'])
        return get_ocr(ndarray), 200
    except Exception as error:
        return f"prolly bad request\nError: {error}", 400

if __name__ == '__main__':
    reader: ocr.Reader = ocr.Reader(["es"], gpu=False)
    server.run("0.0.0.0", 8000, True)