import os, random, cv2, torch
from pathlib import Path
from typing import List
from torchvision import transforms as T

IMG_EXT = {".png", ".jpg", ".jpeg", ".bmp"}

def list_images(directory: str) -> List[Path]:
    return [p for p in Path(directory).rglob('*') if p.suffix.lower() in IMG_EXT]

basic_tf = T.Compose([
    T.ToTensor(),
    T.Resize((224, 224)),
    T.Normalize([0.485, 0.456, 0.406],
                [0.229, 0.224, 0.225])
])

def load_image(path: str):
    img = cv2.cvtColor(cv2.imread(str(path)), cv2.COLOR_BGR2RGB)
    return basic_tf(img)

def seed_everything(seed: int = 42):
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)