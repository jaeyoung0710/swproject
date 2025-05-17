import numpy as np

arr1 = np.genfromtxt("C:\\swproject\\swproject\\problem1st\\problem1.5\\1-5-mars_base_main_parts-001.csv", delimiter=",", skip_header=1)
arr2 = np.genfromtxt("C:\\swproject\\swproject\\problem1st\\problem1.5\\1-5-mars_base_main_parts-002.csv", delimiter=",", skip_header=1)
arr3 = np.genfromtxt("C:\\swproject\\swproject\\problem1st\\problem1.5\\1-5-mars_base_main_parts-003.csv", delimiter=",", skip_header=1)

parts = np.vstack((arr1, arr2, arr3))

print(parts)

averages = np.mean(parts, axis=1)

parts_to_work_on = parts[averages < 50]

try:
    np.savetxt("parts_to_work_on.csv", parts_to_work_on, delimiter=",", fmt="%.3f")
    print("결과 파일이 성공적으로 저장되었습니다.")
except Exception as e:
    print("[파일 저장 오류]", str(e))
