import os

def read_csv_columnwise(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            header = file.readline().strip().split(',')
            columns = [[] for _ in header]

            for line in file:
                values = line.strip().split(',')
                if len(values) != len(columns):
                    continue
                for i in range(len(values)):
                    columns[i].append(values[i])
            return header, columns
    except FileNotFoundError:
        print(f"[오류] 파일이 존재하지 않습니다: {filename}")
        return [], []
    except Exception as e:
        print(f"[오류] 알 수 없는 문제 발생: {e}")
        return [], []

def combine_rows(header, columns):
    return [list(row) for row in zip(*columns)]

def sort_by_flammability(rows, header):
    if "flammability" in header:
        idx = header.index("flammability")
        rows.sort(key=lambda x: float(x[idx]), reverse=True)
    return rows

def filter_dangerous(rows, header):
    dangerous = []
    if "flammability" in header:
        idx = header.index("flammability")
        for row in rows:
            try:
                if float(row[idx]) >= 0.7:
                    dangerous.append(row)
            except ValueError:
                continue
    return dangerous

def save_to_csv(filename, header, rows):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(','.join(header) + '\n')
        for row in rows:
            file.write(','.join(row) + '\n')
    print(f"[완료] 위험 물품 목록 저장됨: {filename}")

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    input_file = os.path.join(current_dir, "1-3-Mars_Base_Inventory_List.csv")
    output_file = os.path.join(current_dir, "1-3-Mars_Base_Inventory_danger.csv")

    header, columns = read_csv_columnwise(input_file)

    if header:
        print("[📦 전체 데이터 출력]")
        all_rows = combine_rows(header, columns)
        for row in all_rows:
            print(row)

        sorted_rows = sort_by_flammability(all_rows, header)

        print("\n[🔥 인화성 순 정렬된 목록]")
        for row in sorted_rows:
            print(row)

        danger_rows = filter_dangerous(sorted_rows, header)

        print("\n[⚠️ 인화성 0.7 이상 위험 목록]")
        for row in danger_rows:
            print(row)

        save_to_csv(output_file, header, danger_rows)
