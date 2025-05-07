import cv2
import PIL
import pytesseract

def is_valid(string_name: str)->bool:
    return (string_name.replace(' ', '').isalnum())

#robadita de stackoverflow
###########################################################
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
###########################################################

capture = cv2.VideoCapture(0)

def parse(info: str, code: str)->dict:
    if code=='':
        return None
    
    
    pre = {}
    if "Cl " in info:
        found="Cl "
    elif "CI " in info:
        found="CI "
    else:
        return None
    
    try:
        pre["cardcode"]=''.join([i for i in code if i.isalnum()])
        idx = info.index(found)
        pre["id"]=info[idx+2:idx+14].strip().replace(' ', '').replace("-", '').replace(".", '')
        pre["id"].strip()
        pre["name"]=info.split("ESTUDIANTE")[1].split(found)[0].splitlines()
        pre["name"]=[i for i in pre["name"] if i.isupper()]
        for i in pre["name"]:
            if not is_valid(i):
                return None
    
        pre["name"]=' '.join(pre["name"])
        print(pre)
        return pre
    except:
        return None


def get_code(image)->str:
    rotated90deg = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    rotated90deg = rotated90deg[0:250, 200:720] #<-----AJUSTAR SEGUN RESOLUCION DE CAMARA
    return pytesseract.image_to_string(PIL.Image.fromarray(rotated90deg), lang='spa')[0:8]

while (capture.isOpened()):
    ret, frame = capture.read()
    
    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    ret, thresh = cv2.threshold(imgray, 120, 200, 0)
    
    cv2.imshow("webcam", thresh)
    
    info = pytesseract.image_to_string(
        PIL.Image.fromarray(cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)),
        lang='spa')
    cardcode = get_code(thresh)
    
    print(parse(info, cardcode))
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break