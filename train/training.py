import os
import shutil
import random
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO
from dataset import YoloDatasetPreparation
import time


# 定義YOLOv8珊瑚檢測系統 - 優化重組後的結構
class YoloCoralDetection:
    """
    YOLOv8珊瑚檢測系統 - 包含數據準備、訓練、評估和預測等功能
    
    主要分區:
    1. 初始化和配置
    2. 日誌記錄功能
    3. 數據預處理
    4. 模型訓練
    """
    
    #------------------------------------------------------
    # 1. 初始化和配置
    #------------------------------------------------------
    def __init__(self, train_dir, valid_dir, output_dir):
        """初始化檢測系統"""
        # 基本路徑配置
        self.train_dir = train_dir
        self.valid_dir = valid_dir
        self.output_dir = output_dir
        self.dataset_yaml = os.path.join(output_dir, 'data.yaml')
        
        # 數據集目錄
        self.train_img_dir = os.path.join(output_dir, 'images', 'train')
        self.val_img_dir = os.path.join(output_dir, 'images', 'val')
        self.train_label_dir = os.path.join(output_dir, 'labels', 'train')
        self.val_label_dir = os.path.join(output_dir, 'labels', 'val')

        # 類別管理
        self.coral_classes = {}
        self.class_id = 0

        self.data_preparation = YoloDatasetPreparation(train_dir, valid_dir, output_dir)

        # 訓練參數
        self.epochs = 300
        self.save_period = 30
        self.batch_size = 8
        self.lr0 = 0.001

        # 創建必要的目錄
        for dir_path in [self.train_img_dir, self.val_img_dir, 
                         self.train_label_dir, self.val_label_dir]:
            os.makedirs(dir_path, exist_ok=True)
        
        # 初始化日誌系統
        self._init_logging()
        
        # 記錄初始化信息
        self.log(f"初始化珊瑚檢測系統")
        self.log(f"訓練目錄: {train_dir}")
        self.log(f"測試目錄: {valid_dir}")
        self.log(f"輸出目錄: {output_dir}")
    
    def _init_logging(self):
        """初始化日誌系統"""
        self.log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'debug_log.txt')
        
        # 以追加模式寫入日誌
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("\n\n" + "="*80 + "\n")
            f.write(f"=== YOLOv8 珊瑚檢測訓練日誌 - {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")

    #------------------------------------------------------
    # 2. 日誌記錄功能
    #------------------------------------------------------
    def log(self, message):
        """記錄消息到控制台和日誌文件"""
        print(message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {message}\n")
    
    # 用於進度條輸出的輔助類
    class TqdmToLogger:
        """將tqdm輸出重定向到日誌文件"""
        def __init__(self, log_file):
            self.log_file = log_file
            
        def write(self, buf):
            if buf.strip():  # 過濾空行
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(buf)
                    
        def flush(self):
            pass
    
    def _get_safe_value(self, value):
        """安全獲取指標值，處理各種類型的數據(張量、數組、標量)"""
        if hasattr(value, 'item'):  # PyTorch張量
            return value.item()
        elif hasattr(value, 'ndim') and value.ndim > 0:  # NumPy數組
            if value.size > 0:
                if value.ndim == 1:
                    return float(value.mean())
                else:
                    return float(value[0])
            else:
                return 0.0
        else:  # 標量值
            return float(value)
    #------------------------------------------------------
    # 3. 數據預處理
    #------------------------------------------------------
    def prepare_dataset(self):        
        self.coral_classes = self.data_preparation.prepare_dataset()
        self.log(f"檢測到的類別: {self.coral_classes}")
    #------------------------------------------------------
    # 4. 模型訓練
    #------------------------------------------------------
    def train(self, model_size='n', patience=30, resume=False, model_path=None):
        """使用YOLOv8訓練珊瑚檢測模型"""
        self.log(f"開始使用YOLOv8{model_size}模型訓練...")
        
        # 記錄訓練參數
        self.log(f"訓練參數配置:")
        self.log(f"  - 數據集: {self.dataset_yaml}")
        self.log(f"  - 模型大小: yolov8{model_size}")
        self.log(f"  - 任務類型: 物件偵測(Detection)")
        self.log(f"  - 訓練輪數: {self.epochs}")
        self.log(f"  - 批次大小: {self.batch_size}")
        self.log(f"  - 早停耐心值: {patience}")
        self.log(f"  - 設備: {'CUDA' if self._has_cuda() else 'CPU'}")
        self.log(f"  - 保存周期: {self.save_period}輪")

        # 初始化或加載模型
        if model_path and os.path.exists(model_path):
            self.log(f"加載已有模型: {model_path}")
            model = YOLO(model_path)
        else:
            self.log(f"使用預訓練模型 yolov8{model_size}.pt")
            model = YOLO(f'yolov8{model_size}.pt')

        # 執行訓練
        try:
            start_time = time.time()
            self.log("開始" + ("繼續" if resume else "新的") + "訓練...")
            
            results = model.train(
                data=self.dataset_yaml,
                epochs=self.epochs,
                imgsz=640,
                batch=self.batch_size,
                patience=patience,
                verbose=True,
                device='0' if self._has_cuda() else 'cpu',
                project=os.path.join(self.output_dir, 'runs'),
                name='train',
                exist_ok=True,
                pretrained=not resume,
                optimizer='auto',
                lr0=self.lr0,
                save_period=self.save_period,
                resume=resume,
                task='detect'
            )
            
            # 記錄訓練時間
            training_time = time.time() - start_time
            hours, remainder = divmod(training_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.log(f"模型訓練完成！總耗時: {int(hours)}小時 {int(minutes)}分鐘 {int(seconds)}秒")

            # 複製日誌到訓練結果目錄
            train_dir = os.path.join(self.output_dir, 'runs', 'train')
            if os.path.exists(train_dir):
                shutil.copy(self.log_file, os.path.join(train_dir, 'training_log.txt'))
            
            return model
            
        except Exception as e:
            self.log(f"訓練過程中出現錯誤: {e}")
            raise

    def _has_cuda(self):
        """檢查是否有CUDA設備可用"""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

    def training(self):
        # 檢查是否存在已訓練的模型
        model_path = os.path.join(self.output_dir, 'runs', 'train', 'weights', 'best.pt')
        if not os.path.exists(model_path):
            model_path = os.path.join(self.output_dir, 'runs', 'train', 'weights', 'last.pt')

        resume_training = os.path.exists(model_path)
        
        # 訓練模型（如果模型存在則嘗試繼續訓練，失敗則以該模型為基礎開始新訓練）
        if resume_training:
            self.log(f"發現已有模型: {model_path}")
            try:
                self.log("嘗試繼續上次的訓練...")
                model = self.train(model_size='n', resume=True, model_path=model_path)
            except AssertionError as e:
                # 捕獲特定的斷言錯誤（模型已完成訓練）
                error_message = str(e)
                self.log(f"無法繼續訓練: {error_message}")
        else:
            self.log("未找到已有模型，將開始新的訓練")
            model = self.train(model_size='n')

        self.log("YOLOv8 珊瑚檢測模型訓練完成！")
