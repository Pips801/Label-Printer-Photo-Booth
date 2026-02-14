from __future__ import annotations

import base64
import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, PlainTextResponse
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_QZ_DIR = Path(os.getenv("USERPROFILE", str(Path.home()))) / "Desktop" / "QZ Tray Demo Cert"
CERT_PATH = Path(os.getenv("QZ_CERT_PATH", str(DEFAULT_QZ_DIR / "digital-certificate.txt")))
KEY_PATH = Path(os.getenv("QZ_KEY_PATH", str(DEFAULT_QZ_DIR / "private-key.pem")))
SIGN_ALG = os.getenv("QZ_SIGN_ALG", "SHA512").upper()

app = FastAPI()


def load_cert() -> str:
    try:
        return CERT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail="QZ cert not found") from exc


def load_private_key():
    try:
        key_bytes = KEY_PATH.read_bytes()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail="QZ private key not found") from exc
    return serialization.load_pem_private_key(key_bytes, password=None)


def get_hash_algorithm():
    if SIGN_ALG == "SHA1":
        return hashes.SHA1()
    if SIGN_ALG == "SHA512":
        return hashes.SHA512()
    return hashes.SHA256()


@app.get("/")
def index() -> FileResponse:
    return FileResponse(BASE_DIR / "index2.html")


@app.get("/index2.html")
def index_alias() -> FileResponse:
    return FileResponse(BASE_DIR / "index2.html")


@app.get("/qz/cert")
def qz_cert() -> PlainTextResponse:
    return PlainTextResponse(load_cert(), media_type="text/plain")


@app.post("/qz/sign")
async def qz_sign(request: Request) -> PlainTextResponse:
    raw = await request.body()
    if not raw:
        raise HTTPException(status_code=400, detail="Empty payload")

    text = None
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            payload = json.loads(raw.decode("utf-8"))
            if isinstance(payload, dict):
                text = payload.get("request") or payload.get("data")
        except json.JSONDecodeError:
            text = None

    if text is None:
        text = raw.decode("utf-8", errors="ignore")

    if not text:
        raise HTTPException(status_code=400, detail="Empty message")

    key = load_private_key()
    signature = key.sign(
        text.encode("utf-8"),
        padding.PKCS1v15(),
        get_hash_algorithm(),
    )
    return PlainTextResponse(base64.b64encode(signature).decode("ascii"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000)
