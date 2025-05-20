import math

result = {}

density_map = {
    "유리": 2.4,
    "알루미늄": 2.7,
    "탄소강": 7.85
}

gravity_ratio = 3.71 / 9.81 

def sphere_area(diameter, material="유리", thickness=1):
    global result

    radius = diameter / 2  
    area = 2 * math.pi * (radius ** 2)  
    
    area_cm2 = area * 10000     #면적 

    volume_cm3 = area_cm2 * thickness     #부피 

    density = density_map.get(material, 2.4)   #재질의 밀도  

    weight_g = volume_cm3 * density  #질량

    weight_kg_mars = (weight_g / 1000) * gravity_ratio 

    result = {
        "재질": material,
        "지름": diameter,
        "두께": thickness,
        "면적": round(area, 3),
        "무게": round(weight_kg_mars, 3)
    }

    print(f"재질 ⇒ {result['재질']}, 지름 ⇒ {result['지름']}, 두께 ⇒ {result['두께']}, 면적 ⇒ {result['면적']}, 무게⇒{result['무게']} kg")

if __name__ == "__main__":
    try:
        d = float(input("돔의 지름을 입력하세요 (단위: m): "))
        m = input("재질을 입력하세요 (유리 / 알루미늄 / 탄소강) [기본값: 유리]: ") or "유리"
        t = input("두께를 입력하세요 (단위: cm) [기본값: 1]: ") or "1"

        t = float(t)

        sphere_area(d, m, t)
    except ValueError:
        print("[오류] 숫자 형식이 잘못되었습니다.")