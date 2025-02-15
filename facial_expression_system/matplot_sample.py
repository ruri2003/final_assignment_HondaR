from feat.detector import Detector
import os
import sys

# 画像から表情を検出する関数
def detect_emotion(image_path):
    # 検出器の定義
    detector = Detector()

    # 画像が存在するか確認
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")

    # 表情認識を実行
    result = detector.detect_image(image_path)

    # 表情認識の結果
    emotions = result.emotions  # 各顔の表情情報

    # 各顔ごとに最も高い表情スコアを取得
    for i in range(len(emotions)):
        # 各顔の表情スコアを取得
        face_emotions = emotions.iloc[i]
        # 最大スコアの表情を取得
        max_emotion = face_emotions.idxmax()
        max_score = face_emotions.max()
        print(f"顔 {i+1}: {max_emotion}")
        #print(f"顔 {i+1}: {max_emotion} (スコア: {max_score:.2f})")

# コマンドライン引数から画像パスを取得
if __name__ == "__main__":
    image_path = sys.argv[1]
    #image_path = "C:/Users/Honda/.vscode/test1/bbb.jpg"
    detect_emotion(image_path)


