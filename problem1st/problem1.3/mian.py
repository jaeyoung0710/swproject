import os 

def main():
    try:
        file = open("problem1st\\problem1.3\\1-3-Mars_Base_Inventory_List.csv", "r", encoding="utf-8")
        lines = file.readlines()
        file.close()

        name_column = [""] * 200
        flammability_column = [0.0] * 200
        count = 0

        for i in range(1, len(lines)):
            line = lines[i].strip()
            parts = line.split(",")
            
            if len(parts) < 5:
                continue  

            flammability_str = parts[4].strip()
            try:
                flammability = float(flammability_str)
            except:
                continue  

            name_column[count] = parts[0]
            flammability_column[count] = flammability
            count += 1

        for i in range(count):
            for j in range(i + 1, count):
                if flammability_column[i] < flammability_column[j]:
                    tmp_f = flammability_column[i]
                    flammability_column[i] = flammability_column[j]
                    flammability_column[j] = tmp_f

                    tmp_n = name_column[i]
                    name_column[i] = name_column[j]
                    name_column[j] = tmp_n

        print("[🔥 위험 물질 (인화성 ≥ 0.7)]")
        for i in range(count):
            if flammability_column[i] >= 0.7:
                print(name_column[i], flammability_column[i])

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

os.makedirs(output_folder, exist_ok=True)

if __name__ == "__main__":
    main()
