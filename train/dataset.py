import os
import json
import shutil
import time
from tqdm import tqdm
from PIL import Image

class YoloDatasetPreparation:
    def __init__(self, train_dir, valid_dir, output_dir):
        self.train_dir = train_dir
        self.valid_dir = valid_dir
        self.output_dir = output_dir
        self.train_img_dir = os.path.join(output_dir, 'images', 'train')
        self.train_label_dir = os.path.join(output_dir, 'labels', 'train')
        self.valid_img_dir = os.path.join(output_dir, 'images', 'val')
        self.valid_label_dir = os.path.join(output_dir, 'labels', 'val')

        # 固定的類別對照表
        self.coral_classes = {
            0: 'Acropora_hyacinthus',
            1: 'Acropora_pruinosa',
            2: 'Euphyllia_glabrescens',
            3: 'Fimbriaphyllia_ancora',
            4: 'Galaxea_astreata',
            5: 'Nephthea_sp',
            6: 'Pavona_decussata',
            7: 'Porites_lobata',
            8: 'Stylophora_pistillata',
            9: 'Turbinaria_reniformis'
        }

        # 反向字典：名字 → ID
        self.name_to_id = {v: k for k, v in self.coral_classes.items()}

        self.log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'debug_log.txt')

    def log(self, message):
        print(message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {message}\n")

    def prepare_dataset(self):
        self.log("開始準備YOLOv8數據集...")

        # 訓練集
        self.log(f"處理訓練集 ({self.train_dir})...")
        all_image_files = self.collect_image_files(self.train_dir)
        if not all_image_files:
            self.log("警告: 未找到有效的圖像文件!")
            return {}

        self.log(f"處理訓練集 ({len(all_image_files)} 圖像)...")
        self.process_files(all_image_files, self.train_img_dir, self.train_label_dir)

        # 驗證集
        self.log(f"處理測試集 ({self.valid_dir})...")
        all_image_files = self.collect_image_files(self.valid_dir)
        if not all_image_files:
            self.log("警告: 未找到有效的圖像文件!")
            return {}

        self.log(f"處理測試集 ({len(all_image_files)} 圖像)...")
        self.process_files(all_image_files, self.valid_img_dir, self.valid_label_dir)

        self.log(f"數據集準備完成！類別數: {len(self.coral_classes)}")
        return self.coral_classes

    def collect_image_files(self, input_dir):
        all_image_files = []
        coral_dirs = [d for d in os.listdir(input_dir)
                      if os.path.isdir(os.path.join(input_dir, d))]

        for coral_dir in coral_dirs:
            coral_path = os.path.join(input_dir, coral_dir)
            label_dir = os.path.join(coral_path, 'label')

            if not os.path.exists(label_dir):
                self.log(f"跳過 {coral_dir}: 沒有找到標籤目錄")
                continue

            self.log(f"處理 {coral_dir} 數據...")
            json_files = [f for f in os.listdir(label_dir) if f.endswith('.json')]

            for json_file in tqdm(json_files, desc=f"處理 {coral_dir} 標籤"):
                json_path = os.path.join(label_dir, json_file)

                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    image_path = data.get('imagePath', '')
                    if image_path.startswith('..\\'):
                        image_name = image_path.split('\\')[-1]
                    else:
                        image_name = os.path.basename(image_path)

                    img_path = os.path.join(coral_path, image_name)
                    if not os.path.exists(img_path):
                        self.log(f"跳過 {json_file}: 找不到圖像文件 {image_name}")
                        continue

                    all_image_files.append((img_path, json_path, image_name))
                except Exception as e:
                    self.log(f"處理 {json_file} 時出錯: {e}")

        return all_image_files

    def process_files(self, files, img_dir, label_dir):
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(label_dir, exist_ok=True)

        for img_path, json_path, image_name in tqdm(files):
            dst_img_path = os.path.join(img_dir, image_name)
            shutil.copy(img_path, dst_img_path)

            yolo_lines = self.labelme_to_yolo(json_path, img_path, image_name)
            if yolo_lines:
                label_name = os.path.splitext(image_name)[0] + '.txt'
                dst_label_path = os.path.join(label_dir, label_name)
                with open(dst_label_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(yolo_lines))

    def labelme_to_yolo(self, json_file, img_file, image_name):
        """只依照檔名比對類別，不看JSON內的label"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 獲取圖像尺寸
            if 'imageHeight' in data and 'imageWidth' in data:
                img_height, img_width = data['imageHeight'], data['imageWidth']
            else:
                img = Image.open(img_file)
                img_width, img_height = img.size

            # 依檔名比對類別
            normalized_name = image_name.lower().replace(" ", "_")

            matched_class_id = None
            for class_id, class_name in self.coral_classes.items():
                normalized_class = class_name.lower().replace(" ", "_")
                if normalized_class in normalized_name:
                    matched_class_id = class_id
                    break

            if matched_class_id is None:
                self.log(f"警告: {image_name} 無法匹配任何已知類別，跳過")
                return []

            yolo_lines = []
            for shape in data['shapes']:
                if shape['shape_type'] == 'rectangle':
                    x1, y1 = shape['points'][0]
                    x2, y2 = shape['points'][1]
                    x_min, y_min = min(x1, x2), min(y1, y2)
                    x_max, y_max = max(x1, x2), max(y1, y2)
                elif shape['shape_type'] == 'polygon':
                    x_coords = [p[0] for p in shape['points']]
                    y_coords = [p[1] for p in shape['points']]
                    x_min, y_min = min(x_coords), min(y_coords)
                    x_max, y_max = max(x_coords), max(y_coords)
                else:
                    continue

                x_center = ((x_min + x_max) / 2) / img_width
                y_center = ((y_min + y_max) / 2) / img_height
                width = (x_max - x_min) / img_width
                height = (y_max - y_min) / img_height

                yolo_line = f"{matched_class_id} {x_center} {y_center} {width} {height}"
                yolo_lines.append(yolo_line)

            return yolo_lines
        except Exception as e:
            self.log(f"處理 {json_file} 時出錯: {e}")
            return []
