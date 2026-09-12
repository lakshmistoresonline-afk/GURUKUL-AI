import json
import shutil
from pathlib import Path
from datetime import datetime, timezone


PROJECT_ROOT = Path(r"D:\GURUKUL-AI")
RUNTIME_ROOT = PROJECT_ROOT / "runtime-data"
CHAPTERS_ROOT = RUNTIME_ROOT / "chapters"
CATALOG_PATH = RUNTIME_ROOT / "catalog.json"
SEARCH_PATH = RUNTIME_ROOT / "search" / "index.json"

# Legacy runtime namespaces that must never be exposed
# as independent student-facing populations.
EXCLUDED_RUNTIME_NAMESPACES = {
    "Class 5",
}


def now():
    return datetime.now(timezone.utc).isoformat()


def read_json(path):
    raw = path.read_bytes()

    for enc in ("utf-8-sig", "utf-16", "utf-16-le", "utf-16-be"):
        try:
            return json.loads(raw.decode(enc))
        except Exception:
            pass

    raise RuntimeError(f"Cannot read JSON: {path}")


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def backup(path):
    if not path.exists():
        return

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    target = path.with_name(
        path.stem + f".BACKUP_{stamp}" + path.suffix
    )

    shutil.copy2(path, target)

    print(f"Backup: {target}")


def class_display(class_id):
    value = str(class_id or "")

    if value.startswith("class_"):
        return "Class " + value.replace("class_", "", 1)

    return value.replace("_", " ").title()


def subject_display(subject_id):
    value = str(subject_id or "")

    parts = value.split("_")

    if (
        len(parts) >= 4
        and parts[0] == "class"
    ):
        return "_".join(parts[3:]).replace(
            "_", " "
        ).title()

    return value.replace(
        "_", " "
    ).title()


def count_pillar(data, pillar):
    value = data.get(pillar, [])

    return len(value) if isinstance(value, list) else 0


def discover_chapters():
    result = []

    for namespace in sorted(
        CHAPTERS_ROOT.iterdir()
    ):
        if not namespace.is_dir():
            continue

        if namespace.name in EXCLUDED_RUNTIME_NAMESPACES:
            print(
                f"EXCLUDED legacy namespace: {namespace.name}"
            )
            continue

        for path in namespace.rglob("*.json"):
            try:
                data = read_json(path)
            except Exception as exc:
                print(
                    f"WARNING unreadable JSON: "
                    f"{path} :: {exc}"
                )
                continue

            if not isinstance(data, dict):
                continue

            chapter_id = (
                data.get("chapter_id")
                or data.get("chapterId")
                or data.get("id")
            )

            title = (
                data.get("chapter_title")
                or data.get("chapterTitle")
                or data.get("title")
            )

            class_id = (
                data.get("class_id")
                or data.get("classId")
            )

            subject_id = (
                data.get("subject_id")
                or data.get("subjectId")
            )

            if not chapter_id:
                print(
                    f"WARNING missing chapter ID: {path}"
                )
                continue

            if not class_id:
                print(
                    f"WARNING missing class ID: {path}"
                )
                continue

            if not subject_id:
                print(
                    f"WARNING missing subject ID: {path}"
                )
                continue

            result.append(
                {
                    "path": path,
                    "data": data,
                    "chapter_id": str(chapter_id),
                    "chapter_title": str(
                        title or chapter_id
                    ),
                    "class_id": str(class_id),
                    "subject_id": str(subject_id),
                }
            )

    return sorted(
        result,
        key=lambda x: (
            x["class_id"],
            x["subject_id"],
            x["chapter_id"],
        ),
    )


def chapter_entry(item):
    data = item["data"]

    learn = count_pillar(data, "learn")
    practice = count_pillar(data, "practice")
    assess = count_pillar(data, "assess")
    revise = count_pillar(data, "revise")
    resources = count_pillar(data, "resources")

    return {
        "id": item["chapter_id"],
        "chapterId": item["chapter_id"],

        "title": item["chapter_title"],
        "chapter_title": item["chapter_title"],

        "classId": item["class_id"],
        "subjectId": item["subject_id"],

        "learn": learn,
        "practice": practice,
        "assess": assess,
        "revise": revise,
        "resources": resources,

        "recordCount": (
            learn
            + practice
            + assess
            + revise
            + resources
        ),

        "accounting": data.get(
            "accounting",
            {},
        ),
    }


def build_catalog(chapters):
    classes = {}

    for item in chapters:
        class_id = item["class_id"]
        subject_id = item["subject_id"]

        cls = classes.setdefault(
            class_id,
            {
                "id": class_id,
                "classId": class_id,
                "name": class_display(
                    class_id
                ),
                "subjects": {},
            },
        )

        subject = cls["subjects"].setdefault(
            subject_id,
            {
                "id": subject_id,
                "subjectId": subject_id,
                "classId": class_id,
                "name": subject_display(
                    subject_id
                ),
                "chapters": [],
            },
        )

        subject["chapters"].append(
            chapter_entry(item)
        )

    output_classes = []

    for cls in classes.values():
        subjects = []

        for subject in cls["subjects"].values():
            subject["chapters"].sort(
                key=lambda x: str(
                    x["id"]
                )
            )

            subjects.append(subject)

        subjects.sort(
            key=lambda x: x["id"]
        )

        cls["subjects"] = subjects
        output_classes.append(cls)

    output_classes.sort(
        key=lambda x: x["id"]
    )

    return {
        "schema_version":
            "gurukul-runtime-catalog-v3",

        "generated_at": now(),

        "classes": output_classes,
    }


def build_search(chapters):
    records = []

    for item in chapters:
        data = item["data"]

        for pillar in (
            "learn",
            "practice",
            "assess",
            "revise",
            "resources",
        ):
            values = data.get(
                pillar,
                [],
            )

            if not isinstance(values, list):
                continue

            for record in values:
                if not isinstance(record, dict):
                    continue

                record_id = (
                    record.get("record_id")
                    or record.get("id")
                )

                if not record_id:
                    continue

                text = str(
                    record.get("text")
                    or record.get("content")
                    or record.get("question")
                    or record.get(
                        "question_text"
                    )
                    or ""
                ).strip()

                title = str(
                    record.get("title")
                    or record.get(
                        "item_title"
                    )
                    or item["chapter_title"]
                ).strip()

                records.append(
                    {
                        "record_id": record_id,
                        "id": record_id,

                        "chapter_id":
                            item["chapter_id"],
                        "chapterId":
                            item["chapter_id"],

                        "chapter_title":
                            item["chapter_title"],
                        "chapterTitle":
                            item["chapter_title"],

                        "class_id":
                            item["class_id"],
                        "classId":
                            item["class_id"],

                        "class":
                            class_display(
                                item["class_id"]
                            ),

                        "subject_id":
                            item["subject_id"],
                        "subjectId":
                            item["subject_id"],

                        "pillar": pillar,

                        "type": record.get(
                            "type",
                            "unknown",
                        ),

                        "title": title,
                        "text": text,

                        "source": record.get(
                            "source",
                            {},
                        ),
                    }
                )

    return {
        "schema_version":
            "gurukul-search-v3",

        "generated_at": now(),

        "record_count":
            len(records),

        "records": records,
    }


def main():
    print()
    print("=" * 72)
    print("GURUKUL AI — CANONICAL API PROJECTION REBUILD")
    print("=" * 72)
    print()

    chapters = discover_chapters()

    print()
    print(
        f"Public runtime chapters discovered: "
        f"{len(chapters)}"
    )

    if not chapters:
        raise RuntimeError(
            "No canonical runtime chapters found."
        )

    class_counts = {}

    for item in chapters:
        cid = item["class_id"]

        class_counts[cid] = (
            class_counts.get(cid, 0) + 1
        )

    print()
    print("Public class distribution:")

    for cid, count in sorted(
        class_counts.items()
    ):
        print(
            f"  {cid}: {count}"
        )

    # --------------------------------------------------------
    # Mandatory canonical Class 5 check
    # --------------------------------------------------------

    class5 = [
        x for x in chapters
        if x["class_id"] == "class_5"
    ]

    legacy_class5 = [
        x for x in chapters
        if x["class_id"] == "Class 5"
    ]

    if legacy_class5:
        raise RuntimeError(
            "Legacy Class 5 namespace leaked into "
            "public projection."
        )

    if len(class5) != 47:
        raise RuntimeError(
            f"Expected 47 canonical Class 5 chapters; "
            f"found {len(class5)}."
        )

    # --------------------------------------------------------
    # Backups
    # --------------------------------------------------------

    print()
    print("Backing up existing projections...")

    backup(CATALOG_PATH)
    backup(SEARCH_PATH)

    # --------------------------------------------------------
    # Build projections
    # --------------------------------------------------------

    catalog = build_catalog(
        chapters
    )

    search = build_search(
        chapters
    )

    write_json(
        CATALOG_PATH,
        catalog,
    )

    write_json(
        SEARCH_PATH,
        search,
    )

    # --------------------------------------------------------
    # Catalog identity verification
    # --------------------------------------------------------

    catalog_ids = []

    for cls in catalog["classes"]:
        for subject in cls["subjects"]:
            for chapter in subject["chapters"]:
                catalog_ids.append(
                    (
                        cls["id"],
                        subject["id"],
                        str(chapter["id"]),
                    )
                )

    runtime_ids = sorted(
        (
            x["class_id"],
            x["subject_id"],
            x["chapter_id"],
        )
        for x in chapters
    )

    catalog_ids = sorted(
        catalog_ids
    )

    if catalog_ids != runtime_ids:
        raise RuntimeError(
            "Catalog/runtime identity mismatch."
        )

    # --------------------------------------------------------
    # Chapter 101 canonical accounting
    # --------------------------------------------------------

    target = None

    for item in class5:
        if item["chapter_id"] == "101":
            target = item
            break

    if target is None:
        raise RuntimeError(
            "Canonical Class 5 chapter 101 not found."
        )

    data = target["data"]

    counts = {
        "learn":
            count_pillar(data, "learn"),
        "practice":
            count_pillar(data, "practice"),
        "assess":
            count_pillar(data, "assess"),
        "revise":
            count_pillar(data, "revise"),
        "resources":
            count_pillar(data, "resources"),
    }

    expected = {
        "learn": 9,
        "practice": 29,
        "assess": 12,
        "revise": 7,
        "resources": 3,
    }

    print()
    print(
        "Canonical Class 5 Chapter 101:"
    )

    for key in (
        "learn",
        "practice",
        "assess",
        "revise",
        "resources",
    ):
        print(
            f"  {key:<10}: {counts[key]}"
        )

    if counts != expected:
        raise RuntimeError(
            "Canonical Class 5 Chapter 101 "
            "accounting mismatch."
        )

    # --------------------------------------------------------
    # Search verification
    # --------------------------------------------------------

    search_records = search["records"]

    if not isinstance(
        search_records,
        list,
    ):
        raise RuntimeError(
            "Search records is not a list."
        )

    for record in search_records:
        if not isinstance(
            record,
            dict,
        ):
            raise RuntimeError(
                "Search index contains non-object record."
            )

        if "class" not in record:
            raise RuntimeError(
                "Search record missing class field."
            )

        if "title" not in record:
            raise RuntimeError(
                "Search record missing title."
            )

    # --------------------------------------------------------
    # Final report
    # --------------------------------------------------------

    print()
    print("=" * 72)
    print("CANONICAL API PROJECTION PASS")
    print("=" * 72)

    print(
        f"Public classes       : "
        f"{len(catalog['classes'])}"
    )

    print(
        f"Public chapters      : "
        f"{len(catalog_ids)}"
    )

    print(
        f"Canonical Class 5    : "
        f"{len(class5)} chapters"
    )

    print(
        f"Search records       : "
        f"{len(search_records)}"
    )

    print(
        "Legacy Class 5 API   : EXCLUDED"
    )

    print(
        "Chapter 101          : PASS"
    )

    print(
        "Catalog identity     : PASS"
    )

    print(
        "Search schema        : PASS"
    )

    print()
    print(
        "Educational content was NOT regenerated."
    )

    print(
        "Legacy runtime files were NOT deleted."
    )

    print()


if __name__ == "__main__":
    main()