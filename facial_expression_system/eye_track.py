#今回は利用しない

import dlib 
import cv2
import numpy as np

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("C:/Users/Honda/.vscode/facial_expression_system/shape_predictor_68_face_landmarks.dat")

STRAIGHT = 0
LEFT = 1
RIGHT = 2

def mosaic(src, ratio=0.1):
    small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
    return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def get_center(gray_img):
    moments = cv2.moments(gray_img, False)
    try:
        return int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00'])
    except:
        return None

def matrix2line(arr):
    m, n = np.shape(arr)[:2]
    return arr.reshape(m * n, 1)

def calc_white_area(bw_image):
    image_size = bw_image.size
    white_pixels = cv2.countNonZero(bw_image)
    return (white_pixels / image_size) * 100  # [%]

def get_median_value_from_img(img):
    img_pixel_data = matrix2line(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY))
    return np.median(img_pixel_data)

def is_eye_close(y0, y1):
    return abs(y0 - y1) < 10

def get_eye_parts(parts, left):
    if left:
        eye_parts = [
            parts[36],
            min(parts[37], parts[38], key=lambda x: x.y),
            max(parts[40], parts[41], key=lambda x: x.y),
            parts[39],
        ]
    else:
        eye_parts = [
            parts[42],
            min(parts[43], parts[44], key=lambda x: x.y),
            max(parts[46], parts[47], key=lambda x: x.y),
            parts[45],
        ]
    return eye_parts if not is_eye_close(eye_parts[1].y, eye_parts[2].y) else None

def get_eye_image(img, parts, left=True):
    eye_parts = get_eye_parts(parts, left)
    if eye_parts is None:
        return None, None
    eye_img = img[eye_parts[1].y:eye_parts[2].y, eye_parts[0].x:eye_parts[3].x]
    eye_img = mosaic(eye_img, 0.4)
    return eye_parts, eye_img

def get_eye_center(img, parts, left=True):
    eye_parts = get_eye_parts(parts, left)
    if eye_parts is None:
        return None
    eye_img = img[eye_parts[1].y:eye_parts[2].y, eye_parts[0].x:eye_parts[3].x]
    _, eye_img = cv2.threshold(cv2.cvtColor(eye_img, cv2.COLOR_RGB2GRAY), get_median_value_from_img(eye_img), 255, cv2.THRESH_BINARY_INV)
    center = get_center(eye_img)
    return (center[0] + eye_parts[0].x, center[1] + eye_parts[1].y) if center else None

def eye_moving_direction(img, parts, left=True):
    eye_parts = get_eye_parts(parts, left)
    if eye_parts is None:
        return None
    eye_left_edge = eye_parts[3].x
    eye_right_edge = eye_parts[0].x
    eye_left_part = img[eye_parts[1].y:eye_parts[2].y, (2 * eye_left_edge + eye_right_edge) // 3:eye_left_edge]
    eye_right_part = img[eye_parts[1].y:eye_parts[2].y, eye_right_edge:(eye_left_edge + 2 * eye_right_edge) // 3]
    eye_img = img[eye_parts[1].y:eye_parts[2].y, eye_parts[0].x:eye_parts[3].x]
    _, eye_left_part = cv2.threshold(cv2.cvtColor(eye_left_part, cv2.COLOR_RGB2GRAY), get_median_value_from_img(eye_img), 255, cv2.THRESH_BINARY_INV)
    _, eye_right_part = cv2.threshold(cv2.cvtColor(eye_right_part, cv2.COLOR_RGB2GRAY), get_median_value_from_img(eye_img), 255, cv2.THRESH_BINARY_INV)
    black_eye_occupancy_rate_threshold = 80
    if calc_white_area(eye_left_part) > black_eye_occupancy_rate_threshold:
        return LEFT
    elif calc_white_area(eye_right_part) > black_eye_occupancy_rate_threshold:
        return RIGHT
    else:
        return STRAIGHT

def show_text(img, direction, pos):
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_arr = ['STRAIGHT', 'LEFT', 'RIGHT']
    cv2.putText(img, text_arr[direction], pos, font, 1, (0, 0, 0), 2, cv2.LINE_AA, False)

def show_image(img, parts, eye, direction):
    for i in range(2):
        if eye[i] is not None:
            cv2.circle(img, eye[i], 3, (255, 255, 0), -1)
    for i in parts:
        cv2.circle(img, (i.x, i.y), 3, (255, 0, 0), -1)
    show_text(img, direction, (parts[0].x, parts[0].y - 10))

# 画像を読み込む部分
img_path = "C:/Users/Honda/.vscode/test1/10.jfif"
img = cv2.imread(img_path)
if img is not None:
    img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    dets = detector(img)
    if len(dets) > 0:
        for det in dets:
            parts = predictor(img, det).parts()
            direction = eye_moving_direction(img, parts)
            left_eye = get_eye_center(img, parts)
            right_eye = get_eye_center(img, parts, False)
            show_image(img, parts, (left_eye, right_eye), direction)
        cv2.imshow("Gaze Direction", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
else:
    print("画像を読み込めませんでした。パスを確認してください。")










