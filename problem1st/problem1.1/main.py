print("Hello Mars")

def display_log_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)

    except FileNotFoundError:
        print(f"[에러] 파일이 존재하지 않습니다.")

    except Exception as e:
        print(f"[에러] 알 수 없는 문제가 발생했습니다: {e}")

if __name__ == "__main__":
    log_file = "C:\\swproject\\swproject\\problem1st\\problem1.1\\1-1-mission_computer_main.log"
    display_log_file(log_file)