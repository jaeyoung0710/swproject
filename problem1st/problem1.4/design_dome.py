import math

result = {}   #전역변수 초기화화

density_map = {
    "유리": 2.4,
    "알루미늄": 2.7,
    "탄소강": 7.85
}

gravity_ratio = 3.71 / 9.81  #지구 중력에 대한 화성 중력 비비

def sphere_area(diameter, material="유리", thickness=1):
    global result

    radius = diameter / 2   #반지름 = 지름 / 2
    area = 2 * math.pi * (radius ** 2)    #2 x pi x r^2
    
    area_cm2 = area * 10000     #면적  m^2를 cm^2으로 변경경

    volume_cm3 = area_cm2 * thickness     #부피 

    density = density_map.get(material, 2.4)   #재질의 밀도  

    weight_g = volume_cm3 * density  #질량

    weight_kg_mars = (weight_g / 1000) * gravity_ratio  #g을 kg으로 변환 x 중력비비

    result = {
        "재질": material,
        "지름": diameter,
        "두께": thickness,
        "면적": round(area, 3),
        "무게": round(weight_kg_mars, 3)
    }

    print(f"재질 ⇒ {result['재질']}, 지름 ⇒ {result['지름']}, 두께 ⇒ {result['두께']}, 면적 ⇒ {result['면적']}, 무게⇒{result['무게']} kg")

if __name__ == "__main__":
    while True:
        try:
            print("\n===== 반구 무게 계산기 =====")
            print("※ 종료하려면 'q' 입력")
            
            d_input = input("돔의 지름을 입력하세요 (단위: m): ")
            if d_input.lower() in ("q"):
                print("프로그램을 종료합니다.")
                break
            d = float(d_input)

            m = input("재질을 입력하세요 (유리 / 알루미늄 / 탄소강) [기본값: 유리]: ") or "유리"
            if m.lower() in ("q"):
                print("프로그램을 종료합니다.")
                break

            t_input = input("두께를 입력하세요 (단위: cm) [기본값: 1]: ") or "1"
            if t_input.lower() in ("q"):
                print("프로그램을 종료합니다.")
                break
            t = float(t_input)

            sphere_area(d, m, t)
        
        except ValueError:
            print("[오류] 숫자 형식이 잘못되었습니다. 다시 입력해주세요.")
