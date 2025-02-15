import cv2 
import imutils
import numpy as np
import dlib
from imutils import face_utils
import sys

# 顔のIDを受け取る（省略可能）
face_id = sys.argv[2] if len(sys.argv) > 2 else None

# Dlibの顔検出器とランドマーク予測モデルを読み込む
detector = dlib.get_frontal_face_detector()  # 顔検出器
predictor = dlib.shape_predictor('C:/Users/Honda/.vscode/test1/shape_predictor_68_face_landmarks.dat')  # 68箇所の顔ランドマークモデルのパスを指定

def process_image(image_path):
    frame = cv2.imread(image_path)

    if frame is None:
        print("画像ファイルが開けませんでした")
        exit()

    frame = imutils.resize(frame, width=1000)  # frameの画像の表示サイズを整える
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # gray scaleに変換する
    rects = detector(gray, 0)  # grayから顔を検出

    # 顔の大きさ（面積）を計算し、ソートする
    face_areas = []
    for rect in rects:
        x, y, w, h = (rect.left(), rect.top(), rect.width(), rect.height())
        area = w * h  # 面積を計算
        face_areas.append((area, rect))

    # 面積が大きい順にソート
    sorted_faces = sorted(face_areas, key=lambda x: x[0], reverse=True)

    for idx, (_, rect) in enumerate(sorted_faces, start=1):  # 各顔に番号をつける
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        # 左右の目の横幅を計測
        left_eye_width = np.linalg.norm(shape[36] - shape[39])  # 左目の目頭と目尻
        right_eye_width = np.linalg.norm(shape[42] - shape[45])  # 右目の目頭と目尻
        eye_width = max(left_eye_width, right_eye_width)
        #print(f"顔{idx}: 左目の横幅={left_eye_width:.2f}, 右目の横幅={right_eye_width:.2f}, 使用する目の横幅={eye_width:.2f}")

        # 眉間と鼻の頂点の長さを計測し、目の横幅で割って比率を求める
        nose_bridge_length = np.linalg.norm(shape[27] - shape[30])  # 眉間と鼻先
        ratio = nose_bridge_length / eye_width
        #print(f"顔{idx}: 眉間から鼻の頂点までの長さ={nose_bridge_length:.2f}, 目の横幅={eye_width:.2f}, 比率={ratio:.2f}")

        # 顔の向き（Yaw方向）を計算
        image_points = np.array([
            tuple(shape[30]),  # 鼻頭
            tuple(shape[21]),
            tuple(shape[22]),
            tuple(shape[39]),
            tuple(shape[42]),
            tuple(shape[31]),
            tuple(shape[35]),
            tuple(shape[48]),
            tuple(shape[54]),
            tuple(shape[57]),
            tuple(shape[8]),
        ], dtype='double')

        # モデルポイントの定義
        model_points = np.array([
            (0.0, 0.0, 0.0),  # 鼻頭
            (-30.0, -125.0, -30.0),  # 左目
            (30.0, -125.0, -30.0),  # 右目
            (-60.0, -70.0, -60.0),  # 左口角
            (60.0, -70.0, -60.0),  # 右口角
            (-40.0, 40.0, -50.0),  # 左あご
            (40.0, 40.0, -50.0),  # 右あご
            (-70.0, 130.0, -100.0),  # 左耳
            (70.0, 130.0, -100.0),  # 右耳
            (0.0, 158.0, -10.0),  # 顔の中心
            (0.0, 250.0, -50.0)  # 顔の下
        ])

        size = frame.shape
        focal_length = size[1]
        center = (size[1] // 2, size[0] // 2)

        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype='double')

        dist_coeffs = np.zeros((4, 1))

        success, rotation_vector, translation_vector = cv2.solvePnP(
            model_points, image_points, camera_matrix,
            dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success:
            print(f"顔{idx}の姿勢推定が失敗しました。")
            continue

        rotation_matrix, jacobian = cv2.Rodrigues(rotation_vector)
        mat = np.hstack((rotation_matrix, translation_vector))

        _, _, _, _, _, _, eulerAngles = cv2.decomposeProjectionMatrix(mat)
        yaw = eulerAngles[1][0]

        # Yawの値によって顔の向きを表示し、それに対応する比率を出力
        if yaw < -20:
            if 1.2 < ratio < 1.3:
                print(f"顔{idx}: 左上")
            elif 1.5 < ratio < 1.7:
                print(f"顔{idx}: 左下")
            else:
                print(f"顔{idx}: 左")
        elif yaw > 20:
            if 1.2 < ratio < 1.4:
                print(f"顔{idx}: 右上")
            elif 1.5 < ratio < 1.8:
                print(f"顔{idx}: 右下")
            else:
                print(f"顔{idx}: 右")
        else:
            if 1.0 < ratio < 1.2:
                print(f"顔{idx}: 上")
            elif 1.65 < ratio < 1.9:
                print(f"顔{idx}: 下")
            else:
                print(f"顔{idx}: 正面")

# コマンドライン引数から画像パスを取得
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("画像のパスを指定してください。")
        sys.exit(1)
    image_path = sys.argv[1]  # コマンドラインから画像パスを取得
    
    process_image(image_path)  # 複数人の顔検出を実行
