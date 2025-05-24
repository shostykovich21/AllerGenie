# app/main.py

import json
import numpy as np
import tensorflow as tf
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
from io import BytesIO
from transformers import DistilBertTokenizerFast
from src.models.multimodal_model import build_multimodal_model

# ─── PATH SETUP ──────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent
NOTEBOOKS  = BASE_DIR / "notebooks"
MODELS_DIR = BASE_DIR / "models"
WEIGHTS_DIR= BASE_DIR / "weights"

# ─── FASTAPI BOILERPLATE ─────────────────────────────────────────────────
app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR/"app"/"static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR/"app"/"templates")

# ─── 1) LOAD LABEL‐MAPS & FEATURE‐COLS ────────────────────────────────────
def _pick_json(filename: str):
    for directory in (NOTEBOOKS / "models", NOTEBOOKS, BASE_DIR):
        candidate = directory / filename
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"Could not find {filename} under {NOTEBOOKS / 'models'}, {NOTEBOOKS}, or {BASE_DIR}"
    )

label_img_fp  = _pick_json("label_map_image.json")
feat_cols_fp  = _pick_json("feature_cols_image.json")
label_txt_fp  = _pick_json("label_map_text.json")

LABEL_MAP_IMG = json.loads(label_img_fp.read_text())
ID2LABEL_IMG  = {v: k for k, v in LABEL_MAP_IMG.items()}
FEATURE_COLS  = json.loads(feat_cols_fp.read_text())
LABEL_MAP_TXT = json.loads(label_txt_fp.read_text())
ID2LABEL_TXT  = {v: k for k, v in LABEL_MAP_TXT.items()}

# ─── 2) LOAD MULTIMODAL MODEL (HARD-CODED PATH) ──────────────────────────
MM_H5 = Path("/home/saumia/AllerGenie/notebooks/models/multimodal.weights.h5")
if not MM_H5.exists():
    raise FileNotFoundError(f"❌ Weights file not found at {MM_H5}")

print(f"🔄 Loading fusion model weights from {MM_H5}")
mm_model = build_multimodal_model(
    image_input_shape=(224, 224, 3),
    num_image_classes=len(LABEL_MAP_IMG),
    text_pretrained="distilbert-base-uncased",
    num_text_labels=len(LABEL_MAP_TXT),
    max_seq_len=256,
    metadata_dim=len(FEATURE_COLS),
    num_classes=len(LABEL_MAP_IMG),
    dropout=0.3
)
mm_model.load_weights(str(MM_H5))
print(f"✅ Loaded fusion model from {MM_H5}")

# ─── 3) LOAD TEXT TOKENIZER ───────────────────────────────────────────────
def _pick_tokenizer(dir_name: str):
    p1 = WEIGHTS_DIR / dir_name
    if p1.exists(): return p1
    p2 = NOTEBOOKS / "weights" / dir_name
    if p2.exists(): return p2
    raise FileNotFoundError(f"Tokenizer folder '{dir_name}' not found in {WEIGHTS_DIR} or {NOTEBOOKS/'weights'}")

tok_dir = _pick_tokenizer("text_tokenizer")
tokenizer = DistilBertTokenizerFast.from_pretrained(str(tok_dir))
print(f"✅ Loaded tokenizer from {tok_dir}")

# ─── ROUTES ────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/infer")
async def infer(
    image: UploadFile = File(...),
    symptom_text: str  = Form(""),
    metadata: str      = Form("{}"),
):
    img_bytes = await image.read()
    try:
        pil = Image.open(BytesIO(img_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(400, f"Invalid image upload: {e}")
    pil = pil.resize((224,224))
    arr = np.array(pil, dtype=np.float32)[None,...]
    arr = tf.keras.applications.efficientnet.preprocess_input(arr)

    toks = tokenizer(
        symptom_text,
        truncation=True,
        padding="max_length",
        max_length=256,
        return_tensors="np"
    )
    input_ids      = toks["input_ids"]
    attention_mask = toks["attention_mask"]

    try:
        meta_dict = json.loads(metadata)
    except json.JSONDecodeError:
        raise HTTPException(400, "Invalid metadata JSON")
    meta_vec = np.array([meta_dict.get(f,0.0) for f in FEATURE_COLS], dtype=np.float32)[None,:]

    preds = mm_model.predict([arr, input_ids, attention_mask, meta_vec])[0]
    idx       = int(np.argmax(preds))
    conf      = float(preds[idx])
    diagnosis = ID2LABEL_IMG.get(idx, "Unknown")

    from src.utils.question_logic import get_followup
    from src.retriever.meds_rag     import retrieve_meds

    followup = get_followup(symptom_text, diagnosis)
    meds     = retrieve_meds(diagnosis, k=3)

    return JSONResponse({
        "diagnosis":   diagnosis,
        "confidence":  conf,
        "followup":    followup,
        "medications": meds,
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
