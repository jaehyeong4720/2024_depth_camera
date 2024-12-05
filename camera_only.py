import sys
import cv2
import pyzed.sl as sl

# ZED 카메라 초기화
zed = sl.Camera()
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD720  # 해상도를 HD720으로 설정
init_params.camera_fps = 30  # 프레임 속도를 30FPS로 설정

status = zed.open(init_params)
if status != sl.ERROR_CODE.SUCCESS:
    print(f"카메라 초기화 실패: {status}")
    sys.exit(1)

runtime_parameters = sl.RuntimeParameters()
image = sl.Mat()

# 카메라 화면 출력 루프
while True:
    if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
        # 카메라 이미지 가져오기
        zed.retrieve_image(image, sl.VIEW.LEFT)  # 왼쪽 카메라 화면을 가져옴
        frame = image.get_data()
        
        # OpenCV를 이용한 화면 출력
        cv2.imshow("ZED Mini Camera View", frame)

        # ESC 키로 종료
        if cv2.waitKey(1) == 27:
            break

# 자원 해제
zed.close()
cv2.destroyAllWindows()
