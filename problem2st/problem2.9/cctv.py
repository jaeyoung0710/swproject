import os
import zipfile
import cv2

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ZIP_PATH = os.path.join(BASE_PATH, 'CCTV.zip')
CCTV_DIR = os.path.join(BASE_PATH, 'CCTV')


def unzip_cctv():
    if not os.path.exists(CCTV_DIR):
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(CCTV_DIR)
        print('✅ CCTV.zip 압축 해제 완료')
    else:
        print('📂 CCTV 폴더가 이미 존재합니다')


def load_image_files(folder_path):
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    return sorted([
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(valid_extensions)
    ])


def view_images(images):
    if not images:
        print('❌ 이미지가 없습니다.')
        return

    index = 0
    total = len(images)

    while True:
        img = cv2.imread(images[index])
        if img is None:
            print(f'⚠️ 이미지를 불러올 수 없습니다: {images[index]}')
            break

        cv2.imshow('CCTV Viewer', img)

        key = cv2.waitKeyEx(0) 

        if key == 27:  
            break
        elif key == 2424832:  
            index = (index - 1) % total
        elif key == 2555904: 
            index = (index + 1) % total

    cv2.destroyAllWindows()


def main():
    unzip_cctv()
    image_files = load_image_files(CCTV_DIR)
    view_images(image_files)


if __name__ == '__main__':
    main()
