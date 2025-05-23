# ──────────────────────────────────────────────────────────────
#  src/retriever/meds_rag.py
#  Build + query a TF–IDF + sklearn NearestNeighbors index
# ──────────────────────────────────────────────────────────────

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import List

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# ─── Paths ────────────────────────────────────────────────────
ROOT         = Path(__file__).parent          # src/retriever
MEDS_DIR     = Path("/mnt/ssd1/saumia/data/meds")
VECT_PATH    = ROOT / "meds_tfidf.joblib"
MATRIX_PATH  = ROOT / "meds_matrix.joblib"
DOC_MAP_PATH = ROOT / "doc_map.json"
SIG_PATH     = ROOT / "build.sig"

# ─── Helper: load & combine openFDA pages ─────────────────────
def load_meds() -> List[str]:
    docs, seen = [], set()
    for f in sorted(MEDS_DIR.glob("drug_label_*.json")):
        try:
            page = json.loads(f.read_text(encoding="utf-8"))["results"]
        except Exception:
            continue
        for rec in page:
            ind  = rec.get("indications_and_usage", "") or ""
            warn= rec.get("warnings_and_precautions", "") or ""
            # if lists, join, else cast
            if isinstance(ind, list): ind = " ".join(ind)
            if isinstance(warn, list): warn = " ".join(warn)
            combined = (str(ind).strip() + "\n" + str(warn).strip()).strip()
            if not combined:
                continue
            h = hashlib.sha1(combined.encode("utf-8")).hexdigest()
            if h in seen:
                continue
            seen.add(h)
            docs.append(combined)
    return docs

# ─── Build TF–IDF + NearestNeighbors index ────────────────────
def build_index(force: bool = False):
    # signature over JSON files
    hasher = hashlib.sha1()
    for f in sorted(MEDS_DIR.glob("drug_label_*.json")):
        hasher.update(str(f).encode())
        hasher.update(f.stat().st_mtime_ns.to_bytes(8, "little"))
    sig = hasher.hexdigest()

    if SIG_PATH.exists() and SIG_PATH.read_text() == sig \
       and VECT_PATH.exists() and MATRIX_PATH.exists() and DOC_MAP_PATH.exists() \
       and not force:
        print("⇨ Meds index up-to-date; skipping rebuild.")
        return

    print("⇨ Loading documents from openFDA …")
    docs = load_meds()
    if not docs:
        raise RuntimeError("No docs found in /data/meds/ – check your JSON files.")

    print(f"    {len(docs)} unique docs")

    print("⇨ Fitting TF–IDF vectorizer …")
    vect = TfidfVectorizer(max_features=5000, stop_words="english")
    X    = vect.fit_transform(docs).astype(np.float32).toarray()

    print("⇨ Saving vectorizer →", VECT_PATH)
    joblib.dump(vect, VECT_PATH)

    print("⇨ Saving document matrix →", MATRIX_PATH)
    joblib.dump(X, MATRIX_PATH)

    print("⇨ Saving doc map →", DOC_MAP_PATH)
    DOC_MAP_PATH.write_text(json.dumps({"docs": docs}, ensure_ascii=False, indent=2))

    print("⇨ Writing signature →", SIG_PATH)
    SIG_PATH.write_text(sig)

    print("✅ Build complete.\n")

# ─── Query helper ─────────────────────────────────────────────
def retrieve(query: str, k: int = 5) -> List[str]:
    """Return top-k document snippets for a natural-language query."""
    if not (VECT_PATH.exists() and MATRIX_PATH.exists() and DOC_MAP_PATH.exists()):
        raise RuntimeError("Index not found; run `python -m src.retriever.meds_rag build` first.")

    vect = joblib.load(VECT_PATH)
    X    = joblib.load(MATRIX_PATH)
    docs = json.loads(DOC_MAP_PATH.read_text(encoding="utf-8"))["docs"]

    # vectorize the query
    qv = vect.transform([query]).astype(np.float32).toarray()

    # use Euclidean nearest neighbors
    nn = NearestNeighbors(n_neighbors=k, metric="l2")
    nn.fit(X)
    distances, indices = nn.kneighbors(qv, n_neighbors=k)

    return [docs[i] for i in indices[0]]

# ─── Convenience alias ────────────────────────────────────────
def retrieve_meds(query: str, k: int = 3) -> List[str]:
    return retrieve(query, k)

# ─── CLI interface ────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build or query the meds TF–IDF index")
    sub = parser.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="(re)build the index")
    b.add_argument("--force", action="store_true",
                   help="force rebuild even if nothing changed")

    q = sub.add_parser("query", help="retrieve top-k docs for a query")
    q.add_argument("text", type=str, help="query text")
    q.add_argument("-k", type=int, default=5, help="number of results")

    args = parser.parse_args()
    if args.cmd == "build":
        build_index(force=args.force)
    else:
        for i, doc in enumerate(retrieve(args.text, args.k), 1):
            print(f"\n--- Result #{i} ---\n{doc}\n")
