import os
import cv2

# 현재 파일 기준 CCTV 폴더 경로
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CCTV_DIR = os.path.join(BASE_PATH, 'CCTV')

# 이미지 확장자
VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp')

# OpenCV 상반신 감지 Haar cascade 로드
cascade_path = cv2.data.haarcascades + 'haarcascade_upperbody.xml'
body_cascade = cv2.CascadeClassifier(cascade_path)


def load_image_files(folder_path):
    """유효한 이미지 파일 목록 반환"""
    return sorted([
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(VALID_EXTENSIONS)
    ])


def detect_human(image):
    """이미지에서 상반신(사람) 감지"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

    for (x, y, w, h) in bodies:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return len(bodies) > 0


def search_for_humans(images):
    """사람이 감지되면 출력, 엔터로 다음 탐색"""
    found = False

    for image_path in images:
        img = cv2.imread(image_path)
        if img is None:
            print(f'⚠️ 이미지 로드 실패: {image_path}')
            continue

        if detect_human(img):
            found = True
            print(f'🧍 사람 감지됨: {os.path.basename(image_path)}')
            cv2.imshow('Detected Human', img)

            key = cv2.waitKey(0)
            cv2.destroyAllWindows()

            if key == 13:  # Enter
                continue
            else:
                print('🛑 사용자 중단')
                return

    if found:
        print('✅ 모든 이미지 검색 완료')
    else:
        print('🔍 사람을 찾지 못했습니다.')


def main():
    if not os.path.exists(CCTV_DIR):
        print('❌ CCTV 폴더가 존재하지 않습니다.')
        return

    images = load_image_files(CCTV_DIR)
    if not images:
        print('❌ CCTV 폴더에 유효한 이미지가 없습니다.')
        return

    search_for_humans(images)



if __name__ == '__main__':
    main()
