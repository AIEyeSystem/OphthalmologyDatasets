import csv
from pathlib import Path
from collections import defaultdict


# Find the repository root
ROOT = Path(__file__).resolve().parent.parent

CSV_FILE = ROOT / "datasets.csv"
OUTPUT_FILE = ROOT / "browse" / "disease.md"


# Store datasets by disease
diseases = defaultdict(list)


# Read datasets.csv
with CSV_FILE.open("r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        dataset_name = row["Dataset"].strip()
        disease_field = row["Disease / Condition"].strip()

        # One dataset may have multiple diseases separated by ";"
        for disease in disease_field.split(";"):
            disease = disease.strip()

            if disease:
                diseases[disease].append(row)


# Generate Markdown
lines = []

lines.append("# Browse by Disease")
lines.append("")
lines.append(
    "Browse ophthalmology datasets by disease or clinical condition."
)
lines.append("")

for disease in sorted(diseases):

    lines.append(f"## {disease}")
    lines.append("")
    lines.append("| Dataset | Modality | Task | Access |")
    lines.append("|---|---|---|---|")

    for dataset in sorted(
        diseases[disease],
        key=lambda x: x["Dataset"].lower()
    ):
        name = dataset["Dataset"]
        modality = dataset["Modality"]
        task = dataset["Task"]
        access = dataset["Access"]

        lines.append(
            f"| {name} | {modality} | {task} | {access} |"
        )

    lines.append("")


# Make sure the browse folder exists
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


# Write disease.md
OUTPUT_FILE.write_text(
    "\n".join(lines),
    encoding="utf-8"
)

print(f"Generated: {OUTPUT_FILE}")
