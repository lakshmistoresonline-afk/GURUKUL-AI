import json
import os

progress_path = "D:/GURUKUL-AI/OLLAMA_REGENERATION_PROGRESS.json"
with open(progress_path, 'r', encoding='utf-8') as f:
    progress = json.load(f)

# Units I know are done
done_ids = [
    # Class 5
    "eesa101", "eesa102", "eesa103", "eesa104", "eesa105", "eesa106", "eesa107", "eesa108", "eesa109", "eesa110",
    "eeev101", "eeev102", "eeev103", "eeev104", "eeev105", "eeev106", "eeev107", "eeev108", "eeev109", "eeev110",
    "ehve101", "ehve102", "ehve103", "ehve104", "ehve105", "ehve106", "ehve107", "ehve108", "ehve109", "ehve110", "ehve111", "ehve112",
    "eemm101", "eemm102", "eemm103", "eemm104", "eemm105", "eemm106", "eemm107", "eemm108", "eemm109", "eemm110", "eemm111", "eemm112", "eemm113", "eemm114", "eemm115",
    # Class 6
    "fepr101", "fepr102", "fepr103", "fepr104", "fepr105",
    "fhml101", "fhml102", "fhml103", "fhml104", "fhml105", "fhml106", "fhml107", "fhml108", "fhml109", "fhml110", "fhml111", "fhml112", "fhml113",
    "fegp101", "fegp102", "fegp103", "fegp104", "fegp105", "fegp106", "fegp107", "fegp108", "fegp109", "fegp110",
    "fecu101", "fecu102", "fecu103", "fecu104", "fecu105", "fecu106", "fecu107", "fecu108", "fecu109", "fecu110", "fecu111", "fecu112",
    "fees101", "fees102", "fees103", "fees104", "fees105", "fees106", "fees107", "fees108", "fees109", "fees110", "fees111", "fees112", "fees113", "fees114",
    # Class 7
    "gepr101", "gepr102", "gepr103", "gepr104", "gepr105",
    "ghml101", "ghml102", "ghml103", "ghml104", "ghml105", "ghml106", "ghml107", "ghml108", "ghml109", "ghml110",
    "gegp101", "gegp102", "gegp103", "gegp104"
]

skip_suffixes = ["ps", "gl"]

for entry in progress:
    uid = entry['unit_id']
    if uid in done_ids:
        entry['status'] = "COMPLETED"
        entry['validation_status'] = "PASS"
    elif any(uid.endswith(s) for s in skip_suffixes):
        entry['status'] = "SKIPPED"
        entry['validation_status'] = "NONE"

with open(progress_path, 'w', encoding='utf-8') as f:
    json.dump(progress, f, indent=2)

print(f"Marked {len(done_ids)} units as COMPLETED.")
