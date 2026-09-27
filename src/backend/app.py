from fastapi import FastAPI
import json

from src.backend.services.correlation import run_correlation


app = FastAPI(
    title="Missing Person Case Coordination API",
    description="Backend for the IBM Bob Hackathon prototype",
    version="1.0.0"
)


# =========================================================
# DATA LOADERS
# =========================================================

def load_person_profile():
    with open(
        "src/data/person_profile.json",
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def load_tips():
    with open(
        "src/data/tips.json",
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def load_cctv():
    with open(
        "src/data/cctv.json",
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Missing Person Case Coordination API is running",
        "status": "ok"
    }


# =========================================================
# CASE DATA
# =========================================================

@app.get("/case")
def get_case():

    return load_person_profile()


@app.get("/tips")
def get_tips():

    return load_tips()


@app.get("/cctv")
def get_cctv():

    return load_cctv()


# =========================================================
# CORRELATION / ANALYSIS
# =========================================================

@app.get("/analyze")
def analyze_case():

    return run_correlation()