"""Small synthetic exam-group network; only listed ties are drawn."""
from pathlib import Path
import pandas as pd

here = Path(__file__).resolve().parent
nodes = []
for g, people in {"Exam A": ["A1", "A2", "A3", "A4", "A5"],
                  "Exam B": ["B1", "B2", "B3", "B4", "B5"],
                  "Exam C": ["C1", "C2", "C3", "C4", "C5"]}.items():
    for i, person in enumerate(people):
        nodes.append({"id": person, "label": f"Person {person}",
                      "region": "Hunan" if i % 3 == 0 else "Other",
                      "exam_group": g, "label_show": int(i == 0)})
pd.DataFrame(nodes).to_csv(here / "demo_nodes.csv", index=False)
pd.DataFrame([
    ["A1", "B1", "national_exam", 0], ["A1", "C1", "blood", 0],
    ["B1", "C1", "provincial_exam", 0], ["A2", "A3", "provincial_exam", 0],
    ["B2", "C2", "blood", 0], ["C1", "A4", "national_exam", 1],
], columns=["source", "target", "type", "directed"]).to_csv(here / "demo_edges.csv", index=False)
print("SYNTHETIC_NETWORK_OK")
