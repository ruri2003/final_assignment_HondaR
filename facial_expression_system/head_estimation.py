#左右なら検出できそう ×

import os
import cv2
import mediapipe as mp
import numpy as np
from pathlib import Path

# mediapipeの顔ランドマークの初期化（max_num_facesを設定）
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# 複数顔を検出するためにmax_num_faces=2を設定
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=2)

def process_image(image_path):
    # 画像の絶対パスを取得
    abs_path = os.path.abspath(image_path)
    print("画像の絶対パス:", abs_path)

    # 画像を読み込み、RGB形式に変換
    image = cv2.imread(abs_path)
    if image is None:
        print(f"エラー: {image_path}の読み込みに失敗しました")
        return
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 顔ランドマークの検出を行い、結果を取得
    results = face_mesh.process(image_rgb)

    # 複数の顔に対応
    if results.multi_face_landmarks:
        print(f"検出された顔の数: {len(results.multi_face_landmarks)}")  # 顔の数を表示
        for face_idx, face_landmarks in enumerate(results.multi_face_landmarks):
            print(f"顔 {face_idx + 1} のランドマークを検出")

            # 左目の左端と右目の右端のランドマーク
            left_eye_left = tuple(map(int, [face_landmarks.landmark[33].x * image.shape[1], face_landmarks.landmark[33].y * image.shape[0]]))
            right_eye_right = tuple(map(int, [face_landmarks.landmark[263].x * image.shape[1], face_landmarks.landmark[263].y * image.shape[0]]))
            nose_top = tuple(map(int, [face_landmarks.landmark[4].x * image.shape[1], face_landmarks.landmark[4].y * image.shape[0]]))

            # 誤検出を確認し、ランドマーク6に切り替え
            if abs(nose_top[1] - (face_landmarks.landmark[33].y * image.shape[0])) < 20:
                nose_top = tuple(map(int, [face_landmarks.landmark[6].x * image.shape[1], face_landmarks.landmark[6].y * image.shape[0]]))

            # 鼻筋のランドマークを取得
            nose_bottom = tuple(map(int, [face_landmarks.landmark[168].x * image.shape[1], face_landmarks.landmark[168].y * image.shape[0]]))

            # 各ランドマークに円を描画
            cv2.circle(image, left_eye_left, 5, (0, 0, 255), -1)
            cv2.circle(image, right_eye_right, 5, (0, 0, 255), -1)
            cv2.circle(image, nose_top, 5, (0, 0, 255), -1)

            # 三角形を描画
            triangle_pts = np.array([left_eye_left, right_eye_right, nose_top])
            cv2.polylines(image, [triangle_pts], isClosed=True, color=(0, 255, 255), thickness=2)

            # 鼻筋の直線を描画
            cv2.line(image, nose_top, nose_bottom, (0, 255, 255), 2)

            # 顔の向きに応じた矢印を描画
            # 顔の中心（目と鼻の位置）を計算
            centroid = (
                (left_eye_left[0] + right_eye_right[0] + nose_top[0]) / 3,
                (left_eye_left[1] + right_eye_right[1] + nose_top[1]) / 3
            )
            
            # X方向、Y方向の差を計算
            distance_x = nose_top[0] - centroid[0]
            distance_y = nose_top[1] - centroid[1]

            # 矢印の長さを動的に計算する
            arrow_length = int(min(abs(distance_x), abs(distance_y)) * 1.5)  # 長さを調整

            # 各方向に矢印を描画
            if abs(distance_x) > 40:  # 水平方向に一定以上の差がある場合
                if distance_x < 0:
                    direction = "Left"
                    print(distance_x)
                    arrow_end = (nose_top[0] - arrow_length, nose_top[1])  # 左方向
                else:
                    direction = "Right"
                    print(distance_x)
                    arrow_end = (nose_top[0] + arrow_length, nose_top[1])  # 右方向
            
            
            else:  # 上下左右に大きな差がない場合
                direction = "Front"
                print(distance_x)
                arrow_end = (nose_top[0], nose_top[1])

            # 矢印を描画
            if arrow_end:
                cv2.arrowedLine(image, nose_top, arrow_end, (255, 0, 0), 2)

            # 向きの判定を表示
            print(f"顔 {face_idx + 1} の向き: {direction}")

    else:
        print("顔が検出されませんでした")

    # 画像サイズを縦0.5倍、横0.5倍にリサイズ
    image_resized = cv2.resize(image, (int(image.shape[1] * 0.5), int(image.shape[0] * 0.5)))

    # 画像を表示
    cv2.imshow("Output", image_resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# メイン処理
if __name__ == "__main__":
    # 画像ファイルのパスを直接指定
    image_path = "C:/Users/Honda/.vscode/test1/27.jfif"
    #image_path = "C:/Users/Honda/.vscode/photo/*.jpg"
    # 画像ファイルの処理
    process_image(image_path)

