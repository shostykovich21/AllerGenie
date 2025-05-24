# 🧬 AllerGenie: Multimodal Skin Condition Diagnosis Assistant

_AllerGenie is a lightweight, full-stack AI-powered web application that helps detect common skin conditions based on image, symptom description, and metadata (age, region, diameter, etc.)._

It supports real-time inference through a fusion model that combines:
- 📷 Image features via EfficientNet-B0  
- 💬 Symptom text via DistilBERT  
- 📊 Structured metadata (age, region, etc.)  

🔗 **Demo-ready FastAPI backend** + modern HTML/CSS/JS frontend + pretrained models.

---

## ✨ Features

- ✅ Multimodal fusion: Image + Text + Metadata
- 📦 FastAPI backend with `/api/infer` endpoint
- 📸 Image upload (lesion/affected region)
- 📝 Free-text symptom description
- 📍 Region and patient metadata entry
- 💡 Follow-up question generation
- 💊 Medication recommendations
- 📱 Responsive UI with modern CSS styling

---

## 📁 Directory Structure

```

AllerGenie/
├── app/
│   ├── main.py                 # FastAPI server
│   ├── templates/index.html    # Main HTML interface
│   └── static/
│       ├── script.js           # Client-side JS logic
│       └── style.css           # Styling
├── models/                     # Saved model weights (optional)
│   └── multimodal.weights.h5
├── notebooks/                  # Training code & exported assets
│   ├── models/                 # Alt path for weights
│   └── weights/                # Tokenizer and model config
├── src/                        # Source code for models & utils
│   ├── models/
│   │   ├── image_model.py
│   │   ├── text_model.py
│   │   └── multimodal_model.py
│   ├── utils/
│   │   ├── question_logic.py
│   │   └── geocode_utils.py
│   └── retriever/
│       └── meds_rag.py
└── README.md

````

---

## 🚀 Setup Instructions

> You need Python 3.9+ and Conda or virtualenv.

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/AllerGenie.git
cd AllerGenie
````

### 2. Install dependencies

```bash
conda create -n allergenie python=3.10
conda activate allergenie
pip install -r requirements.txt
```

### 3. Run the FastAPI backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open your browser at:
📍 [http://localhost:8000](http://localhost:8000)

---

## 🧠 Model Details

* **Image Backbone**: `EfficientNetB0` pretrained on ImageNet
* **Text Encoder**: `DistilBERT` pretrained from HuggingFace
* **Metadata Branch**: Two-layer dense + ReLU
* **Fusion**: `Concatenate([image_feats, text_feats, metadata])` → Dropout → Dense(Softmax)

Weights are saved using:

```python
mm_model.save_weights("models/multimodal.weights.h5")
```

---

## ⚠️ Important Notes

* 🔒 **This tool is not a substitute for medical advice**. It is a prototype intended for research, education, and demonstration.
* The backend relies on saved `.h5` weights and cannot load `.keras` model files unless Lambda layers are registered.

---

## 🧪 Future Improvements

* Add image segmentation for region-specific cropping
* Introduce multilingual support (Indian regional languages)
* Integrate patient history and geolocation-based allergy trends
* Dockerize deployment for cloud readiness
* Improve follow-up with dialog-based patient interaction

---

## 👨‍💻 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

```bash
# Format code
black .
# Run backend
uvicorn app.main:app --reload
```

---

## 🧾 License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.

---

## 🙌 Acknowledgments

* [HuggingFace Transformers](https://huggingface.co/transformers/)
* [TensorFlow & Keras](https://keras.io/)
* [FastAPI](https://fastapi.tiangolo.com/)
* \[Google Maps / Overpass APIs]\(used for allergist location if enabled)

---
