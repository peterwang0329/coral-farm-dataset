import os
import numpy as np
from ultralytics import YOLO
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib
import time
matplotlib.use('Agg')  # 非互動式後端，避免在無GUI環境下出錯

class Validate_model:
    def __init__(self, log_file="validation_log.txt"):
        """初始化日誌系統"""
        self.log_file = log_file
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("\n\n" + "="*80 + "\n")
            f.write(f"=== YOLOv8 珊瑚檢測驗證日誌 - {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")

    def logger(self, message):
        """記錄消息到控制台和日誌文件"""
        print(message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {message}\n")

    def validate(self, model_path, val_img_dir):
        """
        驗證YOLOv8模型在珊瑚辨識任務上的性能
        
        Args:
            model_path: 模型路徑
            val_img_dir: 驗證圖片目錄
        """
        self.model_path = model_path
        model_best_path = os.path.join(model_path,'runs','train','weights', 'best.pt') if os.path.isdir(model_path) else model_path

        # 檢查模型文件是否存在
        if not os.path.exists(model_best_path):
            self.logger(f"模型文件不存在: {model_best_path}")
            return
        
        # 檢查驗證目錄是否存在
        if not os.path.exists(val_img_dir):
            self.logger(f"驗證圖片目錄不存在: {val_img_dir}")
            self.logger(f"嘗試創建目錄: {val_img_dir}")
            os.makedirs(val_img_dir, exist_ok=True)
            self.logger(f"已創建空驗證目錄，請添加驗證數據到: {val_img_dir}")
            return
        
        # 修正 model_files 未定義的問題
        model_files = [model_best_path] if os.path.isfile(model_best_path) else []
        if not model_files:
            self.logger(f"模型文件不存在: {model_best_path}")
            return
        
        # 優先使用 best.pt
        model_best_path = next((f for f in model_files if f.endswith('best.pt')), model_files[0])
        self.logger(f"使用模型: {model_best_path}")

        try:
            # 載入訓練好的模型
            model = YOLO(model_best_path)

            # 獲取驗證集中的類別（資料夾名稱）
            classes = [d for d in os.listdir(val_img_dir) if os.path.isdir(os.path.join(val_img_dir, d))]
            self.logger(f"驗證集包含以下類別: {classes}")
            
            total_images = 0
            all_class_metrics = {}
            
            # 分別驗證每個類別
            for cls in classes:
                self.logger(f"\n=== 驗證類別: {cls} ===")
                
                # 初始化當前類別的混淆矩陣統計
                cls_stats = defaultdict(lambda: {'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0})
                
                # 獲取當前類別的圖片
                cls_dir = os.path.join(val_img_dir, cls)
                cls_images = [f for f in os.listdir(cls_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
                total_images += len(cls_images)
                
                # 提取出實際類別名（移除中文部分）
                actual_class = cls.split(' ')[0] if ' ' in cls else cls
                
                self.logger(f"處理類別 '{cls}' (標籤: {actual_class})，共 {len(cls_images)} 張圖片")
                
                for img_file in cls_images:
                    img_path = os.path.join(cls_dir, img_file)
                    
                    # 使用模型預測
                    results = model(img_path, conf=0.25)  # 可調整置信度閾值
                    
                    # 獲取檢測結果
                    detected_classes = []
                    for r in results:
                        for c, conf in zip(r.boxes.cls, r.boxes.conf):
                            detected_class = model.names[int(c)]
                            detected_classes.append(detected_class)
                    
                    # 更新當前類別的TP、FN
                    if actual_class in detected_classes:
                        cls_stats[actual_class]['TP'] += 1
                    else:
                        cls_stats[actual_class]['FN'] += 1
                    
                    # 更新其他類別的FP、TN
                    for other_cls in classes:
                        if other_cls == cls:
                            continue
                        
                        other_actual_class = other_cls.split(' ')[0] if ' ' in other_cls else other_cls
                        
                        if other_actual_class in detected_classes:
                            cls_stats[other_actual_class]['FP'] += 1
                        else:
                            cls_stats[other_actual_class]['TN'] += 1
                
                # 計算當前類別的評估指標
                self.logger(f"\n--- {cls} 類別評估結果 ---")
                
                metrics = cls_stats[actual_class]
                TP = metrics['TP']
                FP = metrics['FP']
                FN = metrics['FN']
                TN = metrics['TN']
                
                # 避免除零錯誤
                accuracy = (TP + TN) / (TP + FP + FN + TN) if (TP + FP + FN + TN) > 0 else 0
                precision = TP / (TP + FP) if (TP + FP) > 0 else 0
                recall = TP / (TP + FN) if (TP + FN) > 0 else 0
                f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
                # f1 = 2 * TP / (2 * TP + FP + FN)

                self.logger(f"  TP: {TP}, FP: {FP}, FN: {FN}, TN: {TN}")
                self.logger(f"  Accuracy: {accuracy:.4f}")
                self.logger(f"  Precision: {precision:.4f}")
                self.logger(f"  Recall: {recall:.4f}")
                self.logger(f"  F1-Measure: {f1:.4f}")
                
                # 保存該類別的指標用於計算總體平均
                all_class_metrics[cls] = {
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1': f1,
                    'samples': TP + FN,  # 該類別的總樣本數
                    'confusion_matrix': {
                        'TP': TP, 'FP': FP, 'FN': FN, 'TN': TN
                    }
                }
            
            # 計算所有類別的平均指標
            valid_classes = len([cls for cls, metrics in all_class_metrics.items() if metrics['samples'] > 0])
            
            if valid_classes > 0:
                avg_metrics = {
                    'accuracy': sum(m['accuracy'] for m in all_class_metrics.values() if m['samples'] > 0) / valid_classes,
                    'precision': sum(m['precision'] for m in all_class_metrics.values() if m['samples'] > 0) / valid_classes,
                    'recall': sum(m['recall'] for m in all_class_metrics.values() if m['samples'] > 0) / valid_classes,
                    'f1': sum(m['f1'] for m in all_class_metrics.values() if m['samples'] > 0) / valid_classes
                }
                
                self.logger("\n=== 總體評估指標（平均） ===")
                self.logger(f"驗證圖像總數: {total_images}")
                self.logger(f"有效類別數: {valid_classes}")
                self.logger(f"平均 Accuracy: {avg_metrics['accuracy']:.4f}")
                self.logger(f"平均 Precision: {avg_metrics['precision']:.4f}")
                self.logger(f"平均 Recall: {avg_metrics['recall']:.4f}")
                self.logger(f"平均 F1-Measure: {avg_metrics['f1']:.4f}")
                
                # 創建各指標的可視化圖表
                self.create_metric_visualizations(all_class_metrics, avg_metrics)
            else:
                self.logger("沒有有效的類別用於計算平均指標")
            
        except Exception as e:
            self.logger(f"驗證過程中出現錯誤: {str(e)}")
            import traceback
            self.logger(traceback.format_exc())

    def create_metric_visualizations(self, class_metrics, avg_metrics):
        """
        創建各類別指標的可視化圖表
        
        Args:
            class_metrics: 各類別的評估指標字典
            avg_metrics: 平均指標字典
        """
        try:
            # 確保輸出目錄存在
            output_dir = os.path.join(self.model_path, 'evaluation_results')
            os.makedirs(output_dir, exist_ok=True)
            
            # 修正字體設置，避免無法加載的問題
            try:
                plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用常見中文字體
                plt.rcParams['axes.unicode_minus'] = False
            except Exception:
                self.logger("警告: 字體設置失敗，可能導致中文無法顯示")
            
            # 1. 繪製各類別的四個指標比較圖
            valid_classes = [cls for cls, m in class_metrics.items() if m['samples'] > 0]
            metrics_names = ['accuracy', 'precision', 'recall', 'f1']
            metrics_labels = ['準確率', '精確率', '召回率', 'F1值']
            
            fig, axs = plt.subplots(2, 2, figsize=(15, 12))
            axs = axs.flatten()
            
            for i, (metric_name, metric_label) in enumerate(zip(metrics_names, metrics_labels)):
                # 提取各類別的指標值
                values = [class_metrics[cls][metric_name] for cls in valid_classes]
                
                # 繪製條形圖
                bars = axs[i].bar(valid_classes, values)
                
                # 添加平均線
                axs[i].axhline(y=avg_metrics[metric_name], color='r', linestyle='--', label='平均值')
                
                # 在條形上標示數值
                for bar, value in zip(bars, values):
                    height = bar.get_height()
                    axs[i].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                            f'{value:.2f}', ha='center', va='bottom', rotation=0)
                
                axs[i].set_title(f'各類別{metric_label}比較')
                axs[i].set_ylim(0, 1.1)
                axs[i].set_xlabel('類別')
                axs[i].set_ylabel(metric_label)
                axs[i].legend()
                
                # 設置x軸標籤旋轉，避免重疊
                axs[i].set_xticks(range(len(valid_classes)))
                axs[i].set_xticklabels(valid_classes, rotation=45, ha='right')
            
            plt.tight_layout()
            metrics_chart_path = os.path.join(output_dir, 'class_metrics_comparison.png')
            plt.savefig(metrics_chart_path, dpi=300)
            plt.close(fig)
            self.logger(f"類別指標比較圖已保存至: {metrics_chart_path}")
            
            # 2. 繪製混淆矩陣可視化（針對樣本數較多的前幾個類別）
            top_classes = sorted(valid_classes, 
                                key=lambda x: class_metrics[x]['samples'], 
                                reverse=True)[:min(5, len(valid_classes))]
            
            if top_classes:
                fig, axs = plt.subplots(1, len(top_classes), figsize=(5*len(top_classes), 5))
                if len(top_classes) == 1:
                    axs = [axs]  # 確保axs是列表
                    
                for i, cls in enumerate(top_classes):
                    cm = class_metrics[cls]['confusion_matrix']
                    cm_display = np.array([[cm['TP'], cm['FP']], 
                                        [cm['FN'], cm['TN']]])
                    
                    im = axs[i].imshow(cm_display, cmap='Blues')
                    
                    # 添加數值標籤
                    for x in range(2):
                        for y in range(2):
                            axs[i].text(y, x, f"{cm_display[x, y]}", ha='center', va='center')
                    
                    axs[i].set_title(f"{cls} 混淆矩陣")
                    axs[i].set_xticks([0, 1])
                    axs[i].set_yticks([0, 1])
                    axs[i].set_xticklabels(['預測為正', '預測為負'])
                    axs[i].set_yticklabels(['實際為正', '實際為負'])
                    fig.colorbar(im, ax=axs[i])
                
                plt.tight_layout()
                cm_chart_path = os.path.join(output_dir, 'confusion_matrices.png')
                plt.savefig(cm_chart_path, dpi=300)
                plt.close(fig)
                self.logger(f"混淆矩陣可視化已保存至: {cm_chart_path}")
            
            # 3. 繪製雷達圖顯示各類別在不同指標上的表現
            if len(valid_classes) > 1:
                # 創建雷達圖
                fig = plt.figure(figsize=(10, 10))
                ax = fig.add_subplot(111, polar=True)
                
                # 設置雷達圖的角度和標籤
                angles = np.linspace(0, 2*np.pi, len(metrics_names), endpoint=False).tolist()
                angles += angles[:1]  # 閉合雷達圖
                
                ax.set_theta_offset(np.pi / 2)  # 從頂部開始
                ax.set_theta_direction(-1)  # 順時針
                
                # 設置雷達圖刻度標籤
                plt.xticks(angles[:-1], metrics_labels)
                
                # 設置y軸範圍
                ax.set_ylim(0, 1)
                
                # 繪製每個類別的雷達圖
                for cls in valid_classes:
                    values = [class_metrics[cls][metric] for metric in metrics_names]
                    values += values[:1]  # 閉合雷達圖
                    ax.plot(angles, values, linewidth=2, label=cls)
                    ax.fill(angles, values, alpha=0.1)
                
                # 添加圖例
                plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
                
                plt.title('各類別指標雷達圖比較', size=15)
                radar_chart_path = os.path.join(output_dir, 'metrics_radar_chart.png')
                plt.savefig(radar_chart_path, dpi=300)
                plt.close(fig)
                self.logger(f"指標雷達圖已保存至: {radar_chart_path}")
            
            # 4. 繪製總體平均指標柱狀圖
            fig, ax = plt.subplots(figsize=(10, 6))
            metrics_values = [avg_metrics[m] for m in metrics_names]
            bars = ax.bar(metrics_labels, metrics_values, color='skyblue')
            
            # 在條形上標示數值
            for bar, value in zip(bars, metrics_values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                        f'{value:.2f}', ha='center', va='bottom')
            
            ax.set_ylim(0, 1.1)
            ax.set_title('模型總體評估指標')
            ax.set_ylabel('指標值')
            
            avg_chart_path = os.path.join(output_dir, 'average_metrics.png')
            plt.savefig(avg_chart_path, dpi=300)
            plt.close(fig)
            self.logger(f"總體評估指標圖已保存至: {avg_chart_path}")
            
        except Exception as e:
            self.logger(f"創建指標可視化時出現錯誤: {str(e)}")
            import traceback
            self.logger(traceback.format_exc())
            avg_chart_path = os.path.join(output_dir, 'average_metrics.png')
            plt.savefig(avg_chart_path, dpi=300)
            plt.close(fig)
            self.logger(f"總體評估指標圖已保存至: {avg_chart_path}")
