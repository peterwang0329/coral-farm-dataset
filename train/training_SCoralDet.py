import os
import torch
import numpy as np
import cv2
from torch.utils.data import Dataset, DataLoader
import albumentations as A
from albumentations.pytorch import ToTensorV2
import json
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import shutil

# SCoralDet模型和配置
class CoralDataset(Dataset):
    def __init__(self, img_dir, annotations, transform=None):
        self.img_dir = img_dir
        self.transform = transform
        self.annotations = annotations
        self.images = list(annotations.keys())
        
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_name = self.images[idx]
        img_path = os.path.join(self.img_dir, img_name)
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        anno = self.annotations[img_name]
        boxes = anno["boxes"]
        labels = anno["labels"]
        
        # 轉換為tensor格式
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        labels = torch.as_tensor(labels, dtype=torch.int64)
        
        target = {
            "boxes": boxes,
            "labels": labels,
            "image_id": torch.tensor([idx])
        }
        
        if self.transform:
            transformed = self.transform(image=image, bboxes=boxes, labels=labels)
            image = transformed["image"]
            target["boxes"] = torch.as_tensor(transformed["bboxes"], dtype=torch.float32)
        
        return image, target

# 資料預處理和增強
def get_transform(train):
    if train:
        return A.Compose([
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.5),
            A.RandomBrightnessContrast(p=0.2),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ToTensorV2()
        ], bbox_params=A.BboxParams(format='pascal_voc', label_fields=['labels']))
    else:
        return A.Compose([
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ToTensorV2()
        ], bbox_params=A.BboxParams(format='pascal_voc', label_fields=['labels']))

# 解析JSON標籤檔案
def parse_labelme_json(json_dir):
    annotations = {}
    coral_classes = {}
    class_id = 1
    
    for json_file in tqdm(os.listdir(json_dir), desc="解析標籤檔案"):
        if not json_file.endswith('.json'):
            continue
        
        with open(os.path.join(json_dir, json_file), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        image_path = os.path.basename(data['imagePath'])
        if image_path.startswith('..\\'):
            image_path = image_path.split('\\')[-1]
        
        height, width = data['imageHeight'], data['imageWidth']
        boxes = []
        labels = []
        
        for shape in data['shapes']:
            label = shape['label']
            if label not in coral_classes:
                coral_classes[label] = class_id
                class_id += 1
            
            # 取得標籤框座標
            points = shape['points']
            if shape['shape_type'] == 'rectangle':
                x1, y1 = points[0]
                x2, y2 = points[1]
                xmin, ymin = min(x1, x2), min(y1, y2)
                xmax, ymax = max(x1, x2), max(y1, y2)
                
                # 確保座標在圖像範圍內
                xmin, ymin = max(0, xmin), max(0, ymin)
                xmax, ymax = min(width, xmax), min(height, ymax)
                
                boxes.append([xmin, ymin, xmax, ymax])
                labels.append(coral_classes[label])
        
        if boxes:  # 如果有有效的邊界框
            annotations[image_path] = {
                "boxes": boxes,
                "labels": labels,
                "width": width,
                "height": height
            }
    
    return annotations, coral_classes

# 準備訓練資料
def prepare_dataset(data_dir, output_dir):
    # 建立所需的資料夾
    os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'annotations'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'train'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'val'), exist_ok=True)
    
    # 找到所有珊瑚類別資料夾
    coral_dirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    
    all_annotations = {}
    for coral_dir in coral_dirs:
        coral_path = os.path.join(data_dir, coral_dir)
        label_dir = os.path.join(coral_path, 'label')
        
        if not os.path.exists(label_dir):
            continue
        
        print(f"處理 {coral_dir} 資料...")
        anno, classes = parse_labelme_json(label_dir)
        
        # 複製圖片到輸出目錄
        for img_name in anno.keys():
            src_img = os.path.join(coral_path, img_name)
            dst_img = os.path.join(output_dir, 'images', img_name)
            if os.path.exists(src_img):
                shutil.copy2(src_img, dst_img)
        
        all_annotations.update(anno)
    
    # 將類別資訊保存到檔案
    with open(os.path.join(output_dir, 'coral_classes.json'), 'w', encoding='utf-8') as f:
        json.dump(classes, f, ensure_ascii=False, indent=4)
    
    # 儲存所有標註資訊
    with open(os.path.join(output_dir, 'annotations', 'instances.json'), 'w', encoding='utf-8') as f:
        json.dump(all_annotations, f, ensure_ascii=False, indent=4)
    
    # 分割訓練集和驗證集
    image_names = list(all_annotations.keys())
    train_imgs, val_imgs = train_test_split(image_names, test_size=0.2, random_state=42)
    
    with open(os.path.join(output_dir, 'train', 'instances.json'), 'w', encoding='utf-8') as f:
        train_annos = {img: all_annotations[img] for img in train_imgs}
        json.dump(train_annos, f, ensure_ascii=False, indent=4)
    
    with open(os.path.join(output_dir, 'val', 'instances.json'), 'w', encoding='utf-8') as f:
        val_annos = {img: all_annotations[img] for img in val_imgs}
        json.dump(val_annos, f, ensure_ascii=False, indent=4)
    
    return len(image_names), len(train_imgs), len(val_imgs), classes

# 訓練模型
def train_model(data_dir, output_dir, num_epochs=50, batch_size=4):
    # 載入資料
    with open(os.path.join(data_dir, 'train', 'instances.json'), 'r', encoding='utf-8') as f:
        train_annotations = json.load(f)
    
    with open(os.path.join(data_dir, 'val', 'instances.json'), 'r', encoding='utf-8') as f:
        val_annotations = json.load(f)
    
    with open(os.path.join(data_dir, 'coral_classes.json'), 'r', encoding='utf-8') as f:
        classes = json.load(f)
    
    # 創建資料集
    train_dataset = CoralDataset(
        img_dir=os.path.join(data_dir, 'images'),
        annotations=train_annotations,
        transform=get_transform(train=True)
    )
    
    val_dataset = CoralDataset(
        img_dir=os.path.join(data_dir, 'images'),
        annotations=val_annotations,
        transform=get_transform(train=False)
    )
    
    # 創建資料載入器
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=lambda x: tuple(zip(*x))
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        collate_fn=lambda x: tuple(zip(*x))
    )
    
    # 建立SCoralDet模型 (此處使用替代方案，實際應使用SCoralDet框架)
    # 這裡假設使用Faster R-CNN作為基礎模型
    num_classes = len(classes) + 1  # +1 表示背景類
    
    # 導入Faster R-CNN模型 (實際應替換為SCoralDet)
    from torchvision.models.detection import fasterrcnn_resnet50_fpn
    from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
    
    model = fasterrcnn_resnet50_fpn(pretrained=True)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    
    # 將模型移至GPU (如果可用)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    # 定義優化器
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)
    
    # 學習率調度器
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.1)
    
    # 訓練模型
    print("開始訓練模型...")
    for epoch in range(num_epochs):
        # 訓練模式
        model.train()
        train_loss = 0
        
        progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}")
        for images, targets in progress_bar:
            images = list(image.to(device) for image in images)
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]
            
            # 前向傳播
            loss_dict = model(images, targets)
            losses = sum(loss for loss in loss_dict.values())
            
            # 反向傳播
            optimizer.zero_grad()
            losses.backward()
            optimizer.step()
            
            train_loss += losses.item()
            progress_bar.set_postfix({"loss": losses.item()})
        
        # 更新學習率
        lr_scheduler.step()
        
        # 計算平均訓練損失
        train_loss /= len(train_loader)
        print(f"Epoch {epoch+1}, 訓練損失: {train_loss:.4f}")
        
        # 每10個epoch保存一次模型
        if (epoch + 1) % 10 == 0:
            torch.save(model.state_dict(), os.path.join(output_dir, f'model_epoch_{epoch+1}.pth'))
    
    # 保存最終模型
    torch.save(model.state_dict(), os.path.join(output_dir, 'model_final.pth'))
    print("模型訓練完成！")
    return model

# 模型評估
def evaluate_model(model, data_dir, output_dir, batch_size=4):
    print("開始評估模型...")
    
    # 載入驗證資料
    with open(os.path.join(data_dir, 'val', 'instances.json'), 'r', encoding='utf-8') as f:
        val_annotations = json.load(f)
    
    with open(os.path.join(data_dir, 'coral_classes.json'), 'r', encoding='utf-8') as f:
        classes = json.load(f)
    
    # 建立反向類別對應
    rev_classes = {v: k for k, v in classes.items()}
    
    # 創建驗證資料集
    val_dataset = CoralDataset(
        img_dir=os.path.join(data_dir, 'images'),
        annotations=val_annotations,
        transform=get_transform(train=False)
    )
    
    # 創建資料載入器
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        collate_fn=lambda x: tuple(zip(*x))
    )
    
    # 準備評估
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()
    
    # 設定評估結果資料夾
    eval_output_dir = os.path.join(output_dir, 'evaluation')
    os.makedirs(eval_output_dir, exist_ok=True)
    
    with torch.no_grad():
        for i, (images, targets) in enumerate(tqdm(val_loader, desc="評估進度")):
            images = list(img.to(device) for img in images)
            
            # 執行推理
            outputs = model(images)
            
            # 視覺化結果 (每個批次只顯示第一張圖片)
            if i < 10:  # 只處理前10個批次以節省時間
                image = images[0].cpu().permute(1, 2, 0).numpy()
                # 還原標準化
                mean = np.array([0.485, 0.456, 0.406])
                std = np.array([0.229, 0.224, 0.225])
                image = std * image + mean
                image = np.clip(image, 0, 1)
                
                # 繪製預測框
                plt.figure(figsize=(10, 10))
                plt.imshow(image)
                
                output = outputs[0]
                boxes = output['boxes'].cpu().numpy().astype(int)
                scores = output['scores'].cpu().numpy()
                labels = output['labels'].cpu().numpy()
                
                # 只顯示得分較高的預測結果
                for box, score, label in zip(boxes, scores, labels):
                    if score > 0.5:  # 設定閾值
                        x1, y1, x2, y2 = box
                        class_name = rev_classes.get(label.item(), "未知")
                        plt.gca().add_patch(plt.Rectangle((x1, y1), x2-x1, y2-y1, 
                                                        fill=False, edgecolor='red', linewidth=2))
                        plt.text(x1, y1, f'{class_name}: {score:.2f}', 
                                bbox=dict(facecolor='yellow', alpha=0.5))
                
                plt.axis('off')
                plt.savefig(os.path.join(eval_output_dir, f'result_{i}.png'))
                plt.close()
    
    print("模型評估完成！")

# 主函數
def main():
    # 設定資料目錄
    base_dir = r"c:\Users\peter\Desktop\program\爬蟲"
    data_dir = os.path.join(base_dir, "images", "test")
    output_dir = os.path.join(base_dir, "SCoralDet_output")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 準備資料集
    print("準備資料集...")
    total_imgs, train_imgs, val_imgs, classes = prepare_dataset(data_dir, output_dir)
    print(f"總共有 {total_imgs} 張圖片，訓練集: {train_imgs}，驗證集: {val_imgs}")
    print(f"檢測到的珊瑚類別: {classes}")
    
    # 訓練模型
    model = train_model(output_dir, output_dir, num_epochs=50)
    
    # 評估模型
    evaluate_model(model, output_dir, output_dir)
    
    print("全部流程完成!")

if __name__ == "__main__":
    main()
