import re
import hashlib

def normalize_text(text: str) -> str:
    if not text:
        return ""
    t = str(text).lower()
    t = re.sub(r'[\u201c\u201d\u2018\u2019]', '"', t)
    t = re.sub(r'[^\w\s]', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def compute_content_fingerprint(q_text: str, options: list = None, answer: str = None) -> str:
    norm_q = normalize_text(q_text)
    norm_opts = sorted([normalize_text(o) for o in (options or [])])
    raw = f"{norm_q}::" + "||".join(norm_opts)
    return hashlib.md5(raw.encode('utf-8')).hexdigest()

def compute_context_fingerprint(cls: str, subj: str, part: str, ch_id: str, q_type: str, content_fp: str) -> str:
    raw = f"C{cls}::{subj}::{part}::{ch_id}::{q_type}::{content_fp}"
    return hashlib.md5(raw.encode('utf-8')).hexdigest()

def compute_physical_id(abs_path: str, filename: str, index: int, content_fp: str) -> str:
    raw = f"{abs_path}::{filename}::{index}::{content_fp}"
    return hashlib.md5(raw.encode('utf-8')).hexdigest()
