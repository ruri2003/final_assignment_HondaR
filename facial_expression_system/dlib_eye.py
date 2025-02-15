import dlib
import cv2
import numpy as np
import sys

detector = dlib.get_frontal_face_detector()
path = "C:/Users/Honda/.vscode/facial_expression_system/shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(path)

def is_close(y0, y1):
    return abs(y0 - y1) < 10

def get_center(gray_img):
    moments = cv2.moments(gray_img, False)
    try:
        return int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00'])
    except:
        return None

def get_eye_parts(parts, left=True):
    if left:
        return [parts[36], min(parts[37], parts[38], key=lambda x: x.y), max(parts[40], parts[41], key=lambda x: x.y), parts[39]]
    else:
        return [parts[42], min(parts[43], parts[44], key=lambda x: x.y), max(parts[46], parts[47], key=lambda x: x.y), parts[45]]

def get_pupil_location(img, parts, left=True):
    eyes = get_eye_parts(parts, left)
    org_x, org_y = eyes[0].x, eyes[1].y
    if is_close(org_y, eyes[2].y):
        return None
    eye_img = img[org_y:eyes[2].y, org_x:eyes[-1].x]
    _, threshold_eye = cv2.threshold(cv2.cvtColor(eye_img, cv2.COLOR_RGB2GRAY), 45, 255, cv2.THRESH_BINARY_INV)
    center = get_center(threshold_eye)
    if center:
        return center[0] + org_x, center[1] + org_y
    return None


def calculate_direction(parts, pupil_locate):
    if not pupil_locate:
        return None
    eyes = get_eye_parts(parts, True)
    #left_border = eyes[0].x + (eyes[3].x - eyes[0].x) / 3
    #right_border = eyes[0].x + (eyes[3].x - eyes[0].x) * 2 / 3
    left_border = eyes[0].x + (eyes[3].x - eyes[0].x) * 0.35
    right_border = eyes[0].x + (eyes[3].x - eyes[0].x) * 0.65
    up_border = eyes[1].y + (eyes[2].y - eyes[1].y) *0.35
    down_border = eyes[1].y + (eyes[2].y - eyes[1].y) *0.65

    #print(pupil_locate[0])
    #print(pupil_locate[1])
    #print(left_border)
    #print(right_border)
    

    # Determine horizontal direction
    if pupil_locate[0] < left_border:
        direction_x = "左"        
    elif pupil_locate[0] <= right_border:
        direction_x = "真ん中"
    else:
        direction_x = "右"

    # Determine vertical direction
    if pupil_locate[1] < up_border:
        direction_y = "上"
    elif pupil_locate[1] <= down_border:
        direction_y = "真ん中"
    else:
        direction_y = "下"

    # Combine directions into one label
    if direction_x == "真ん中" and direction_y == "真ん中":
        return "真ん中"
    elif direction_x == "真ん中":
        return direction_y
    elif direction_y == "真ん中":
        return direction_x
    else:
        return f"{direction_x}{direction_y}"




def process_image(image_path):
    img = cv2.imread(image_path)
    dets = detector(img)
    results = []

    # 顔の大きさを計算してソート
    face_areas = []
    for det in dets:
        width = det.width()
        height = det.height()
        area = width * height
        face_areas.append((det, area))

    # 面積が大きい順にソート
    face_areas.sort(key=lambda x: x[1], reverse=True)

    # ソートされた顔順で処理
    for i, (det, _) in enumerate(face_areas):
        parts = predictor(img, det).parts()
        left_pupil_location = get_pupil_location(img, parts, True)
        if left_pupil_location:
            direction = calculate_direction(parts, left_pupil_location)
            if direction:
                direction_y = direction
                results.append(f"顔{i+1}: {direction_y}")
            else:
                results.append(f"顔{i+1}: 瞳の位置が検出できませんでした")
        else:
            results.append(f"顔{i+1}: 瞳の位置が検出できませんでした")

    # 結果を出力
    for result in results:
        print(result)

# 画像を読み込み、結果を文字で出力
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("画像のパスを指定してください。")
        sys.exit(1)
    image_path = sys.argv[1]
    
    #image_path = "C:/Users/Honda/.vscode/test1/4.jfif"
    process_image(image_path)
