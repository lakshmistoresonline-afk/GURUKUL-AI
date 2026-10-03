import json

with open(r"D:/GURUKUL/reports/production_qb_rebuild_v3_verification_corrected/source_index.json", "r", encoding="utf-8") as f:
    s_idx = json.load(f)

with open(r"D:/GURUKUL/reports/production_qb_rebuild_v3_verification_corrected/destination_index.json", "r", encoding="utf-8") as f:
    d_idx = json.load(f)

print("Sample source identity:", s_idx[0]["identity"])
print("Sample destination identity:", d_idx[0]["identity"])

s_idents = {o["identity"] for o in s_idx}
d_idents = {o["identity"] for o in d_idx}
print("Source unique ident count:", len(s_idents))
print("Dest unique ident count:", len(d_idents))
print("Intersection count:", len(s_idents.intersection(d_idents)))
