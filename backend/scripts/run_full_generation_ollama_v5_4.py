#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re,subprocess,sys,urllib.request
from pathlib import Path

OLLAMA="http://127.0.0.1:11434/api/generate"
FIELDS={"learn":("title","explanation"),"practice":("question",),"assess":("question",),"revise":("point",),"resources":("title",)}
BAD=[r"which source section",r"what source section",r"refer to the source",r"according to the source",r"source chapter text",r"comprehension check",r"placeholder",r"dummy content",r"sample question",r"test question",r"lorem ipsum",r"what did you learn"]

def rj(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def wj(p,o):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def clean(x): return re.sub(r"\s+"," ",str(x or "")).strip()
def bad(x): return any(re.search(q,x,re.I) for q in BAD)
def moj(x): return any(q in x for q in ("Ã","Â","â€","ðŸ","à¤","à¦","ï»¿"))

def extract(s):
    s=re.sub(r"^```(?:json)?\s*","",s.strip(),flags=re.I);s=re.sub(r"\s*```$","",s)
    try:return json.loads(s)
    except Exception:pass
    for op,cl in (("[","]"),("{","}")):
        st=s.find(op)
        if st<0:continue
        d=0;q=False;e=False
        for i in range(st,len(s)):
            c=s[i]
            if q:
                if e:e=False
                elif c=="\\":e=True
                elif c=='"':q=False
            else:
                if c=='"':q=True
                elif c==op:d+=1
                elif c==cl:
                    d-=1
                    if d==0:return json.loads(s[st:i+1])
    raise ValueError("no valid JSON")

def source(repo,job,cap):
    cp=Path(job["chapter"]["path"]);cp=cp if cp.is_absolute() else repo/cp
    fs=[]
    for p in cp.rglob("*"):
        if not p.is_file():continue
        z=str(p).lower()
        if any(q in z for q in ("90_generated","runtime","generation_staging")):continue
        if p.name.upper() in ("JOB.JSON","RAW_GENERATED.JSON"):continue
        if p.suffix.lower() in (".txt",".md",".json",".csv"):fs.append(p)
    fs.sort(key=lambda p:(0 if any(q in p.name.lower() for q in ("source","chapter","text","content")) else 1,str(p).lower()))
    out=[];left=cap
    for p in fs:
        if left<=0:break
        try:t=json.dumps(rj(p),ensure_ascii=False,separators=(",",":")) if p.suffix.lower()==".json" else p.read_text(encoding="utf-8-sig",errors="replace")
        except Exception:continue
        t=t.strip()
        if not t:continue
        t=t if len(t)<=left else t[:max(800,left-300)]+"\n[EXCERPT TRUNCATED]"
        out.append("SOURCE: "+p.name+"\n"+t);left-=len(t)+20
    return "\n".join(out)

def call(model,p,timeout):
    body={"model":model,"prompt":p,"stream":False,"format":"json","think":False,
          "options":{"temperature":0.1,"top_p":0.8,"num_ctx":4096,"num_predict":900}}
    req=urllib.request.Request(OLLAMA,data=json.dumps(body,ensure_ascii=False,separators=(",",":")).encode(),headers={"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=timeout) as x:return json.loads(x.read().decode()).get("response","")

def prompt(ch,ps,src):
    shapes=[]
    for p in ps:
        if p=="learn":shapes.append('"learn":[{"title":"...","explanation":"..."}]')
        elif p in ("practice","assess"):shapes.append(f'"{p}":[{{"question":"..."}}]')
        elif p=="revise":shapes.append('"revise":[{"point":"..."}]')
        else:shapes.append('"resources":[{"title":"..."}]')
    return f"""Generate high-quality educational content for GURUKUL AI.
Class: {ch["class_name"]}
Subject: {ch["subject_name"]}
Chapter: {ch["chapter_id"]} - {ch["chapter_title"]}
Requested pillars: {", ".join(ps)}

Return ONE JSON object with these pillar keys only:
{{{", ".join(shapes)}}}

Use ONLY information supported by SOURCE. No outside facts.
Every item must be chapter-specific, useful, and age-appropriate.
learn: title + explanation.
practice/assess: question.
revise: point.
resources: title only when supported by SOURCE.
No filler, meta questions, placeholders, citations, URLs, invented facts, or commentary.
Prefer a few strong items. Return JSON only.

SOURCE:
{src}"""

def norm(v,p):
    if isinstance(v,dict):v=v.get("items",v.get("records",v.get("data",[])))
    if not isinstance(v,list):return []
    req=FIELDS[p];out=[]
    for x in v:
        if isinstance(x,str):
            if len(req)!=1:continue
            x={req[0]:x}
        if not isinstance(x,dict):continue
        z={}
        good=True
        for f in req:
            q=clean(x.get(f))
            if not q or bad(q) or moj(q):good=False;break
            z[f]=q
        if good:out.append(z)
    return out

def build(job,d):
    ch=job["chapter"];out={"chapter_id":ch["chapter_id"],"chapter_title":ch["chapter_title"],"source_bundle_sha256":job["source_bundle_sha256"],"pillars":{}};errs=[]
    for p in job.get("missing_pillars",[]):
        arr=norm(d.get(p),p)
        if not arr:errs.append(p+": no valid items");continue
        final=[]
        for i,x in enumerate(arr,1):
            x=dict(x);x.update(id=f'{ch["chapter_id"]}_{p}_{i:03d}',content_origin="GENERATED",source_ref=x.get("source_ref"),chapter_id=ch["chapter_id"],source_bundle_sha256=job["source_bundle_sha256"]);final.append(x)
        out["pillars"][p]={"items":final,"gap":None}
    return out,errs

def usable(raw,job):
    if not isinstance(raw,dict) or raw.get("chapter_id")!=job["chapter"]["chapter_id"] or raw.get("source_bundle_sha256")!=job["source_bundle_sha256"]:return False
    for p in job.get("missing_pillars",[]):
        q=raw.get("pillars",{}).get(p)
        if not isinstance(q,dict) or not q.get("items"):return False
        for x in q["items"]:
            if not all(clean(x.get(f)) and not bad(clean(x.get(f))) and not moj(clean(x.get(f))) for f in FIELDS[p]):return False
    return True

def official(repo,run,promote):
    cmd=[sys.executable,str(repo/"backend/scripts/generate_all_valid_contents.py"),"--repo-root",str(repo),"--run-id",run,"--fail-on-gaps"]
    if promote:cmd.append("--promote")
    x=subprocess.run(cmd,cwd=repo,text=True,capture_output=True);return x.returncode,x.stdout+"\n"+x.stderr

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--repo-root",default=".");a.add_argument("--input-run",required=True)
    a.add_argument("--model",default="qwen3.5:2b-q4_K_M");a.add_argument("--max-source-chars",type=int,default=7000)
    a.add_argument("--attempts",type=int,default=2);a.add_argument("--timeout",type=int,default=90);a.add_argument("--promote",action="store_true")
    a=a.parse_args();repo=Path(a.repo_root).resolve();st=Path(a.input_run).resolve();jr=st/"jobs"
    jobs=sorted(x for x in jr.iterdir() if x.is_dir() and (x/"JOB.json").exists())
    print(f"GURUKUL AI V5.4 FAST | Jobs={len(jobs)} | Model={a.model} | Context={a.max_source_chars}")
    passed=failed=0;failures=[]
    for n,jd in enumerate(jobs,1):
        job=rj(jd/"JOB.json");ch=job["chapter"];rp=jd/"RAW_GENERATED.json"
        print(f"[{n}/{len(jobs)}] {ch['chapter_id']} - {ch['chapter_title']}")
        try:
            if rp.exists() and usable(rj(rp),job):print("  KEEP existing valid");passed+=1;continue
        except Exception:pass
        src=source(repo,job,a.max_source_chars)
        if not src:failed+=1;failures.append((ch["chapter_id"],"no source"));print("  FAIL: no source");continue
        ps=list(job.get("missing_pillars",[]));ok=False;last=""
        for k in range(1,a.attempts+1):
            print(f"  all missing pillars: attempt {k}/{a.attempts}")
            try:
                d=extract(call(a.model,prompt(ch,ps,src),a.timeout))
                if not isinstance(d,dict):raise ValueError("model output is not object")
                out,errs=build(job,d)
                if errs:raise ValueError("; ".join(errs))
                if set(out["pillars"])!=set(ps):raise ValueError("missing requested pillar")
                wj(rp,out);ok=True;print("  PASS");break
            except Exception as e:last=str(e);print("    rejected:",last)
        if ok:passed+=1
        else:failed+=1;failures.append((ch["chapter_id"],last));print("  FAIL:",last)
    report={"version":"V5.4","model":a.model,"jobs":len(jobs),"passed":passed,"failed":failed,"failures":[{"chapter_id":x,"reason":y} for x,y in failures]}
    wj(st/"V5_4_FULL_PACKAGE_REPORT.json",report)
    print(f"V5.4 COMPLETE | Passed={passed} | Failed={failed}")
    if failed:print("SAFETY STOP - no promotion.");return 1
    print("Running official repository validator...")
    code,out=official(repo,st.name,a.promote);print(out)
    return code

if __name__=="__main__":raise SystemExit(main())
