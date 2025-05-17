import os 

def main():
    try:
        # 파일 열기
        file = open("problem1st\\problem1.3\\1-3-Mars_Base_Inventory_List.csv", "r", encoding="utf-8")
        lines = file.readlines()
        file.close()

        # 고정 크기 배열 선언 (최대 200개 항목 저장)
        name_column = [""] * 200
        flammability_column = [0.0] * 200
        count = 0

        # 첫 줄은 헤더이므로 건너뜀
        for i in range(1, len(lines)):
            line = lines[i].strip()
            parts = line.split(",")
            
            if len(parts) < 5:
                continue  # 항목이 부족하면 무시

            flammability_str = parts[4].strip()
            try:
                flammability = float(flammability_str)
            except:
                continue  # 숫자 변환 불가 시 무시

            name_column[count] = parts[0]
            flammability_column[count] = flammability
            count += 1

        # 인화성 높은 순으로 정렬 (버블 정렬)
        for i in range(count):
            for j in range(i + 1, count):
                if flammability_column[i] < flammability_column[j]:
                    # 교환
                    tmp_f = flammability_column[i]
                    flammability_column[i] = flammability_column[j]
                    flammability_column[j] = tmp_f

                    tmp_n = name_column[i]
                    name_column[i] = name_column[j]
                    name_column[j] = tmp_n

        # 결과 출력
        print("[🔥 위험 물질 (인화성 ≥ 0.7)]")
        for i in range(count):
            if flammability_column[i] >= 0.7:
                print(name_column[i], flammability_column[i])

        # CSV 파일로 저장
                # CSV 파일로 저장
        try:
            output_folder = "problem1st\\problem1.3"
            output_file = os.path.join(output_folder, "Mars_Base_Inventory_danger.csv")
            os.makedirs(output_folder, exist_ok=True)

            out = open(output_file, "w", encoding="utf-8")
            out.write("name,flammability\n")
            for i in range(count):
                if flammability_column[i] >= 0.7:
                    out.write(name_column[i] + "," + str(flammability_column[i]) + "\n")
            out.close()
            print("\n✅ 파일 저장 완료:", output_file)
        except:
            print("[오류] 저장 중 오류 발생")


    except FileNotFoundError:
        print("[에러] Mars_Base_Inventory_List.csv 파일이 없습니다.")
    except Exception as e:
        print("[에러] 처리 중 문제 발생:", str(e))

output_folder = "problem1st\\problem1.3"
output_file = os.path.join(output_folder, "Mars_Base_Inventory_danger.csv")

# 폴더 없으면 생성
os.makedirs(output_folder, exist_ok=True)

# 실행
if __name__ == "__main__":
    main()
