import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
from ultralytics import YOLO

# 設定路徑
model_name = "yolov8_Coral"
data_yaml_path = os.path.join("./models", model_name, "data.yaml")
model_path = os.path.join("./models", model_name, "runs/train/weights/best.pt")
log_dir = "./logs"
model_log_dir = os.path.join(log_dir, model_name)

def main():
    # 建立模型日誌資料夾
    try:
        os.makedirs(model_log_dir, exist_ok=True)
    except OSError as e:
        print(f"建立日誌資料夾 '{model_log_dir}' 時發生錯誤: {e}")
        sys.exit()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(model_log_dir, f"evaluation_log_{timestamp}.txt")

    # 開始評估與紀錄
    print(f"開始評估模型，日誌儲存於：{log_file_path}")

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        original_stdout = sys.stdout
        sys.stdout = log_file

        try:
            # 1. 載入訓練好的模型
            print("---1. 載入模型---")
            print(f"載入模型名稱: {model_name}")
            try:
                model = YOLO(model_path)
            except Exception as e:
                print(f"載入模型時發生錯誤: {e}")
                sys.exit()

            # 2. 執行驗證
            print("\n---2. 執行驗證---")
            try:
                metrics = model.val(data=data_yaml_path, save=False, plots=True, conf=0.25)
            except Exception as e:
                print(f"執行驗證時發生錯誤: {e}")
                sys.exit()
            print("驗證完成")

            # 3. 打印整體評估效果
            print("\n" + "="*60)
            print("整體模型評估結果".center(60))
            print("="*60)
            print(f"mAP50-95 (主要指標) : {metrics.box.map:.4f}")
            print(f"mAP50    (寬鬆標準) : {metrics.box.map50:.4f}")
            print(f"mAP75    (嚴格標準) : {metrics.box.map75:.4f}")
            print(f"精確率    (Precision): {metrics.box.p.mean():.4f}") 
            print(f"召回率    (Recall)   : {metrics.box.r.mean():.4f}")
            print(f"F1分數    (F1 Score): {metrics.box.f1.mean():.4f}")

            # 4. 計算並打印各類別詳細指標
            if hasattr(metrics, 'confusion_matrix') and metrics.confusion_matrix is not None:
                conf_matrix = metrics.confusion_matrix.matrix
                class_names = model.names
                
                print("\n" + "="*60)
                print("各類別詳細評估指標".center(60))
                print("="*60)

                for i, name in class_names.items():
                    tp = conf_matrix[i, i]
                    fp = conf_matrix[:, i].sum() - tp
                    fn = conf_matrix[i, :].sum() - tp
                    
                    precision = tp / (tp + fp + 1e-6)
                    recall = tp / (tp + fn + 1e-6)
                    f1_score = 2 * (precision * recall) / (precision + recall + 1e-6)

                    print(f"類別: {name} ({i})")
                    print(f"  - True Positives  (TP): {int(tp)}")
                    print(f"  - False Positives (FP): {int(fp)}")
                    print(f"  - False Negatives (FN): {int(fn)}")
                    print(f"  - Precision           : {precision:.4f}")
                    print(f"  - Recall              : {recall:.4f}")
                    print(f"  - F1-Score            : {f1_score:.4f}")
                    print("-"*60)
            else:
                print("\n警告：無法從驗證結果中獲取混淆矩陣")

            print("報告生成完畢")
        finally:
            # 還原標準輸出
            sys.stdout = original_stdout

    print(f"評估完成，所有結果都已儲存到 '{log_file_path}'！")

    # 刪除多餘的驗證資料夾
    val_dir = Path("runs/detect/val")
    if val_dir.exists():
        shutil.rmtree(val_dir)
        print(f"已刪除驗證資料夾: {val_dir}")


if __name__ == "__main__":
    main()