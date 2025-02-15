import os 
import sys
import subprocess

# 英語の表情ラベルを日本語に変換するための辞書
"""emotion_translation = {
    "happiness": "幸せ",
    "sadness": "悲しみ",
    "anger": "怒り",
    "surprise": "驚き",
    "fear": "恐れ",
    "disgust": "嫌悪",
    "neutral": "中立",
    "nan" : "顔認識なし"
}
"""

emotion_translation = {
    "happiness": "幸せ",
    "sadness": "その他",
    "anger": "その他",
    "surprise": "その他",
    "fear": "その他",
    "disgust": "その他",
    "neutral": "中立",
    "nan" : "顔認識なし"
}

# 物体検出のラベルを日本語に変換するための辞書
object_detection_translations = {
    "aaa" : "映っている人数",
    "ninn" : "人",
    "buttai" : "物体検出結果",
    "person": "人",
    "car": "車",
    "dog": "犬",
    "cat": "猫",
    "chair": "椅子",
    "table": "テーブル",
    "bicycle": "自転車",
    "tree": "木",
    "book": "本",
    "cup": "カップ",
    "airplane": "飛行機",
    "apple": "りんご",
    "bag": "バッグ",
    "banana": "バナナ",
    "bed": "ベッド",
    "bench": "ベンチ",
    "bird": "鳥",
    "boat": "ボート",
    "bottle": "ボトル",
    "bowl": "ボウル",
    "bus": "バス",
    "cake": "ケーキ",
    "camera": "カメラ",
    "carrot": "にんじん",
    "clock": "時計",
    "cow": "牛",
    "cupcake": "カップケーキ",
    "tv" : "テレビ",
    "dining":"ダイニング",
    "desk": "机",
    "elephant": "象",
    "fan": "扇風機",
    "fish": "魚",
    "flower": "花",
    "fork": "フォーク",
    "glass": "グラス",
    "hat": "帽子",
    "house": "家",
    "ice": "氷",
    "jacket": "ジャケット",
    "key": "鍵",
    "knife": "ナイフ",
    "lamp": "ランプ",
    "leaf": "葉",
    "lion": "ライオン",
    "luggage": "荷物",
    "mirror": "鏡",
    "monkey": "猿",
    "motorcycle": "オートバイ",
    "mouse": "ネズミ",
    "orange": "オレンジ",
    "panda": "パンダ",
    "pen": "ペン",
    "pencil": "鉛筆",
    "phone": "電話",
    "pillow": "枕",
    "plate": "皿",
    "rabbit": "ウサギ",
    "refrigerator": "冷蔵庫",
    "remote": "リモコン",
    "rice": "ご飯",
    "ring": "指輪",
    "scissors": "ハサミ",
    "shoes": "靴",
    "sink": "シンク",
    "sofa": "ソファ",
    "spoon": "スプーン",
    "star": "星",
    "strawberry": "いちご",
    "suitcase": "スーツケース",
    "sun": "太陽",
    "tablecloth": "テーブルクロス",
    "tie": "ネクタイ",
    "tiger": "虎",
    "toaster": "トースター",
    "toilet": "トイレ",
    "tomato": "トマト",
    "toothbrush": "歯ブラシ",
    "towel": "タオル",
    "train": "電車",
    "treehouse": "ツリーハウス",
    "truck": "トラック",
    "umbrella": "傘",
    "van": "バン",
    "vase": "花瓶",
    "watch": "腕時計",
    "watermelon": "スイカ",
    "whale": "クジラ",
    "window": "窓",
    "wolf": "オオカミ",
    "zebra": "シマウマ",
    "candle": "ろうそく",
    "pizza": "ピザ",
    "burger": "バーガー",
    "cloud": "雲",
    "door": "ドア",
    "egg": "卵",
    "fence": "フェンス",
    "guitar": "ギター",
    "helicopter": "ヘリコプター",
    "kite": "凧",
    "ladder": "はしご",
    "laptop" : "パソコン",
    "notebook": "ノート",
    "oven": "オーブン",
    "piano": "ピアノ",
    "rocket": "ロケット",
    "rug": "敷物",
    "snowman": "雪だるま",
    "stool": "スツール",
    "telescope": "望遠鏡",
    "television": "テレビ",
    "wagon": "ワゴン",
    "zoo": "動物園"

    # 必要に応じて他の物体の翻訳を追加
}

# 画像パスを受け取り、様々なスクリプトを実行する関数
def file_path(image_path):
    # 各スクリプトを実行して結果を取得
    emotion_result = run_emotion_detection(image_path)
    head_direction_result = run_head_direction(image_path)
    mtcnn_result = run_mctnn(image_path)
    object_detection_result = run_object_detection(image_path)

    # 結果を指定のフォーマットで表示
    print("結果")
    print(f"表情認識結果\n{emotion_result}")
    print(f"{head_direction_result}")
    print(f"{mtcnn_result}")
    print(f"{object_detection_result}")

# 汎用的なスクリプト実行関数
def execute_script(script_path, image_path):
    try:
        result = subprocess.run(['python', script_path, image_path], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"エラー: {e.stderr}"

# 表情認識スクリプトを実行
def run_emotion_detection(image_path):
    result = subprocess.run(['python', 'C:/Users/Honda/.vscode/facial_expression_system/matplot_sample.py', image_path], capture_output=True, text=True)
    if result.returncode != 0:
        return f"エラー: {result.stderr}"

    emotion_result = result.stdout.strip()

    # 複数の英語の表情名を日本語に置き換え
    for english, japanese in emotion_translation.items():
        emotion_result = emotion_result.replace(english, japanese)

    return emotion_result

# 顔の向き検出スクリプトを実行
def run_head_direction(image_path):
    return f"\n顔の向き\n{execute_script('C:/Users/Honda/.vscode/facial_expression_system/face_direction.py', image_path)}"

# 視線の向き検出（MTCNN）スクリプトを実行
def run_mctnn(image_path):
    return f"視線の向き\n{execute_script('C:/Users/Honda/.vscode/facial_expression_system/dlib_eye.py', image_path)}"

# オブジェクト検出スクリプトを実行
def run_object_detection(image_path):
    # 引数に画像パスを正しく渡すための修正
    result = subprocess.run(['python', 'C:/Users/Honda/.vscode/facial_expression_system/yolov5-master/detect.py', image_path], capture_output=True, text=True)

    if result.returncode != 0:
        return f"エラー: {result.stderr}"

    # オブジェクト検出の結果を整理
    object_detection_result = result.stdout.strip()

    # 物体ラベルの英語から日本語への置き換え
    for english, japanese in object_detection_translations.items():
        object_detection_result = object_detection_result.replace(english, japanese)
    
    #return f"{object_detection_result}"
    return f"{object_detection_result}"


# コマンドライン引数から画像パスを取得し、スクリプトを実行
if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]  # コマンドライン引数から画像パスを取得
        file_path(image_path)  # 画像パスを引数にしてファイルパス関数を実行
    else:
        print("画像パスを引数として指定してください。")

