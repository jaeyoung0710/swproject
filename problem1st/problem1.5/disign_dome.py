import numpy as np
import os

file_paths = [
    "problem1st\\problem1.5\\1-5-mars_base_main_parts-001.csv",
    "problem1st\\problem1.5\\1-5-mars_base_main_parts-002.csv",
    "problem1st\\problem1.5\\1-5-mars_base_main_parts-003.csv"
]

file_data = []

for path in file_paths:
    part_strength = {}
    with open(path, 'r', encoding='utf-8') as f:
        next(f)  
        for line in f:
            items = line.strip().split(',')
            if len(items) == 2:
                part = items[0].strip()
                try:
                    strength = float(items[1])
                    part_strength[part] = strength
                except ValueError:
                    continue
    file_data.append(part_strength)

common_parts = set(file_data[0].keys()) & set(file_data[1].keys()) & set(file_data[2].keys())

parts_to_save = []
for part in common_parts:
    values = [file_data[i][part] for i in range(3)]
    avg = np.mean(values)
    if avg < 50:
        parts_to_save.append((part, avg))

output_folder = "problem1st\\problem1.5"
output_file = os.path.join(output_folder, "parts_to_work_on.csv")

os.makedirs(output_folder, exist_ok=True)

try:
    with open(output_file, "w", encoding='utf-8') as out:
        out.write("parts,strength\n")
        for part, avg_strength in sorted(parts_to_save):
            out.write(f"{part},{avg_strength:.3f}\n")
    print(f"✅ 저장 완료: {len(parts_to_save)}개 항목 → {output_file}")
except Exception as e:
    print("[파일 저장 오류]", str(e))
