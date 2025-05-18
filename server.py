from flask import Flask, request, jsonify
import base64
import easyocr as ocr
import cv2
import numpy as np

#CONST
CONFIDENCE=0.45
URL_PATH="api"
#bytes to MatLike
def bytes_to_image(data: bytes)->cv2.typing.MatLike:
    nparr: np.ndarray = np.frombuffer(data, np.uint8)
    img: cv2.typing.MatLike = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


app: Flask = Flask("Hola")

def get_ocr(img: cv2.typing.MatLike)->dict | int:
    result: list = reader.readtext(img)[0:4]
    person: dict = {}
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

@app.route(f"/{URL_PATH}", methods=["POST"])
def index():
    json_data = request.get_json()
    if not json_data or 'data' not in json_data:
        return "Parámetro 'data' no encontrado", 400
    base64_data=json_data['data']
    
    #decode base64
    decoded_data = base64.b64decode(base64_data)
    
    person: dict | int = get_ocr(bytes_to_image(decoded_data))
    if person==400:
        return "Bad request", 400
    return jsonify(person)
    
if __name__=='__main__':
    reader: ocr.Reader = ocr.Reader(["es"], gpu=False)
    app.run("localhost", 8000, True)