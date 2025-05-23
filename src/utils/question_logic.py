# ────────────────────────────────────────────────────────────
#  src/utils/question_logic.py
#  Rule-based follow-up engine for AllerGenie
# ────────────────────────────────────────────────────────────

from typing import Optional

SYMPTOM_KEYS = {
    "skin": [
        "rash", "itch", "hives", "eczema", "peeling", "scaly", "flaky", "blisters", "bumps", "dry", "red patches"
    ],
    "respiratory": [
        "sneeze", "wheeze", "cough", "shortness", "asthma", "breath", "tight chest", "runny nose"
    ],
    "digestive": [
        "nausea", "vomit", "stomach", "diarrhea", "ulcer", "pain", "bloating", "constipation", "abdomen"
    ],
}

FOLLOWUP_BANK = {
    "skin": "Have you recently used any new skincare products, detergents, or soaps?",
    "respiratory": "Have you been around pets, dust, mold, or pollen recently?",
    "digestive": "Did you eat anything unusual or new in the last 24 hours?",
}

# Fine label → symptom bucket mapping (used post-classification)
LABEL_TO_BUCKET = {
    # Skin
    "Psoriasis": "skin",
    "Fungal infection": "skin",
    "Impetigo": "skin",
    "allergy": "skin",
    "Acne": "skin",

    # Respiratory
    "Bronchial Asthma": "respiratory",
    "Pneumonia": "respiratory",
    "Common Cold": "respiratory",

    # Digestive / systemic
    "peptic ulcer disease": "digestive",
    "Typhoid": "digestive",
    "gastroesophageal reflux disease": "digestive",
    "Dengue": "digestive",
    "Malaria": "digestive",

    # Reasonable fallback guesses for remaining labels:
    "Hypertension": "respiratory",
    "Migraine": "digestive",  # GI triggers often linked
    "diabetes": "digestive",
    "drug reaction": "skin",
    "Dimorphic Hemorrhoids": "digestive",
    "urinary tract infection": "digestive",
    "Jaundice": "digestive",
    "Cervical spondylosis": "respiratory",
    "Varicose Veins": "skin",
    "Arthritis": "skin",
    "Chicken pox": "skin",
}

def detect_category(text: str) -> Optional[str]:
    """
    Fallback NLP: keyword scan to guess symptom bucket.
    """
    text = text.lower()
    for cat, kws in SYMPTOM_KEYS.items():
        if any(k in text for k in kws):
            return cat
    return None

def get_followup(raw_text: str, predicted_label: Optional[str] = None) -> str:
    """
    Decide which follow-up question to ask next.
    1) Use model label if present.
    2) Fallback to keyword-based symptom detection.
    """
    bucket = LABEL_TO_BUCKET.get(predicted_label) if predicted_label else None
    if bucket is None:
        bucket = detect_category(raw_text)

    return FOLLOWUP_BANK.get(bucket, "Could you tell me when the symptoms started?")
