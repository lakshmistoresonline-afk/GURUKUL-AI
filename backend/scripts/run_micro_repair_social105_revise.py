import argparse, json, importlib.util, sys, time, urllib.request
from pathlib import Path

MODEL="qwen3.5:2b-q4_K_M"; URL="http://127.0.0.1:11434/api/generate"

def rj(p): return json.loads(Path(p).read_text(encoding="utf-8-sig"))
def wj(p,x): Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def load(root):
    p=root/"backend/scripts/generate_all_valid_contents.py"
    s=importlib.util.spec_from_file_location("gv_micro",p)
    m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m)
    return m

def find(run):
    for d in (run/"jobs").glob("*"):
        if not (d/"JOB.json").exists() or not (d/"RAW_GENERATED.json").exists(): continue
        try: j=rj(d/"JOB.json")
        except: continue
        c=j.get("chapter",{})
        if c.get("class_name")=="Class 7" and c.get("subject_name")=="03_SOCIAL_SCIENCE_GRADE7_PART2" and str(c.get("chapter_id"))=="105" and c.get("chapter_title")=="India, a Home to Many":
            return d,j
    raise RuntimeError("Target job not found")

def src(root):
    out=[]; n=0
    for p in sorted(Path(root).rglob("*")):
        if p.is_file() and p.suffix.lower() in {".txt",".md",".json",".csv"}:
            try: t=p.read_text(encoding="utf-8-sig",errors="replace").strip()
            except: continue
            if t:
                s=f"\n--- {p.name} ---\n{t[:3000]}"; out.append(s); n+=len(s)
                if n>=9000: break
    return "".join(out)[:9000]

def call(prompt):
    b={"model":MODEL,"prompt":prompt,"stream":False,"format":"json","think":False,"options":{"temperature":0.02,"num_ctx":3072,"num_predict":180}}
    q=urllib.request.Request(URL,data=json.dumps(b,ensure_ascii=False).encode(),headers={"Content-Type":"application/json; charset=utf-8"},method="POST")
    with urllib.request.urlopen(q,timeout=150) as x: o=json.loads(x.read().decode("utf-8",errors="replace"))
    return json.loads(o["response"])

def good(v):
    if not isinstance(v,str) or len(v.strip())<20 or not any(c.isalpha() for c in v): return False
    low=v.lower()
    return not any(x in low for x in ("placeholder","source section","source chapter text","as an ai","generation"))

def main():
    a=argparse.ArgumentParser(); a.add_argument("--repo-root",default="."); a.add_argument("--input-run",required=True); z=a.parse_args()
    root=Path(z.repo_root).resolve(); run=Path(z.input_run).resolve()
    print("FINAL MICRO REPAIR — Class 7 Social Science 105 revise[0].point")
    m=load(root); print("[OK] revise schema:",m.GENERATION_SCHEMA["revise"]["required_fields"])
    d,j=find(run); rp=d/"RAW_GENERATED.json"; raw=rj(rp); pillar=raw["pillars"]["revise"]
    if isinstance(pillar,list): raw["pillars"]["revise"]={"items":pillar,"gap":None}; pillar=raw["pillars"]["revise"]
    item=pillar["items"][0]; print("[INFO] Existing item:",json.dumps(item,ensure_ascii=False))
    prompt=f'''Repair ONLY the missing "point" field of this Class 7 Social Science revision item for the chapter "India, a Home to Many".
Existing item:
{json.dumps(item,ensure_ascii=False,indent=2)}
Relevant source:
{src(j["chapter"]["path"])}
Return ONLY {{"point":"..."}}.
The point must be a natural-language educational revision statement, at least 20 characters, not a number, ratio, equation, isolated word, placeholder, or meta-commentary. Preserve the meaning of the existing item and use only source-supported information.'''
    val=None; err=None
    for i in range(1,5):
        try:
            print(f"[OLLAMA] attempt {i}/4"); v=call(prompt).get("point")
            if not good(v): raise ValueError(f"rejected point: {v!r}")
            val=v.strip(); break
        except Exception as e: err=e; print(" REJECT:",e); time.sleep(1)
    if val is None: raise RuntimeError(f"Could not repair safely: {err}")
    item["point"]=val; wj(rp,raw); check=rj(rp)
    if not good(check["pillars"]["revise"]["items"][0]["point"]): raise RuntimeError("post-write validation failed")
    print("[PASS] repaired point:",check["pillars"]["revise"]["items"][0]["point"])
    print("Promotion: NOT performed")
if __name__=="__main__": main()
