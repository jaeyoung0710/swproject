import json
from datetime import datetime
import os

def read_log_file(filename):
    log_list = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(',', 2)
                if len(parts) != 3:
                    continue

                timestamp_str, level, message = parts

                try:
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    continue

                log_entry = {
                    "timestamp": timestamp_str,
                    "level": level,
                    "message": message
                }
                log_list.append((timestamp, log_entry))

    except FileNotFoundError:
        print(f"[오류] 파일이 존재하지 않습니다: {filename}")
    except Exception as e:
        print(f"[오류] 알 수 없는 문제가 발생했습니다: {e}")
    return log_list


def save_as_json(log_entries, json_filename):
    log_dict = {entry['timestamp']: entry for _, entry in log_entries}

    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(log_dict, f, indent=4, ensure_ascii=False)

    print(f"[완료] JSON 파일 저장됨: {json_filename}")


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    
    log_path = os.path.join(current_dir, "..", "problem1.1", "1-1-mission_computer_main.log")
    json_path = os.path.join(current_dir, "mission_computer_main.json")

    logs = read_log_file(log_path)

    print("\n[로그 리스트]")
    for _, entry in logs:
        print(entry)

    logs.sort(reverse=True)

    print("\n[정렬된 로그 리스트]")
    for _, entry in logs:
        print(entry)

    save_as_json(logs, json_path)