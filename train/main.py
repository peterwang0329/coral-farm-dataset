import os
import sys
from training import YoloCoralDetection
from predict import Validate_model


def main():
    try:
        print("=== 珊瑚辨識系統 - YOLOv8模型訓練與驗證 ===")
        print("1. 準備初始化訓練與驗證環境")

        model_name = "yolov8_Coral"

        # 定義兩個路徑變數
        base_dir = os.path.dirname(os.path.abspath(__file__))
        imagedir_path = os.path.join(base_dir, "images")
        train_path = os.path.join(imagedir_path, "train")
        val_path = os.path.join(imagedir_path, "valid")
        modeldir_path = os.path.join(base_dir, "models", model_name)

        # 確保目錄存在
        os.makedirs(train_path, exist_ok=True)
        os.makedirs(val_path, exist_ok=True)
        os.makedirs(modeldir_path, exist_ok=True)
        
        print(f"訓練圖片目錄: {train_path}")
        print(f"測試圖片目錄: {val_path}")
        print(f"模型輸出目錄: {modeldir_path}")

        # 1. 呼叫 training.py 進行訓練
        train = YoloCoralDetection(train_path, val_path, modeldir_path)
        train.prepare_dataset()
        train.training()

        # 2. 計算模型的準確率
        test = Validate_model()
        # test.validate(modeldir_path, val_path)
        print("程序執行完畢")
    
    except Exception as e:
        print(f"程序執行過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()