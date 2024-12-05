import tkinter as tk
import subprocess

from tkinter import messagebox
from api_depth import Controller_API  # 기존의 ControllerAPI 클래스 임포트

class Depth_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PWM Controller")

        # controller_api  인스턴스 생성
        self.controller_api = Controller_API(pwm_pin=33, relay_pin=29)

        # Main Frame: 두 섹션을 나눌 컨테이너
        main_frame = tk.Frame(root)
        main_frame.pack(pady=10, padx=10)

        # Left Frame: Duty Cycle 섹션
        duty_frame = tk.Frame(main_frame)
        duty_frame.grid(row=0, column=0, padx=20)

        self.camera_process = None
        self.click_py_process = None

        # Duty Cycle 섹션
        duty_label = tk.Label(duty_frame, text="Duty Cycle:")
        duty_label.pack()

        self.duty_entry = tk.Entry(duty_frame, state='normal')
        self.duty_entry.pack(pady=5)


        self.set_duty_button = tk.Button(duty_frame, text="Set Duty Cycle", command=self.set_duty_cycle, state='normal')
        self.set_duty_button.pack(pady=5)


        # Reset 버튼 추가 (Duty Cycle 0으로 설정 및 버튼 초기화)
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_program)
        self.reset_button.pack(pady=10)

        # ZED Depth Viewer 실행 버튼 추가
        self.zed_button = tk.Button(root, text="Run ZED Depth Viewer", command=self.run_zed_viewer)
        self.zed_button.pack(pady=10)

        # Python 실행 버튼 추가
        self.click_py_button = tk.Button(root, text="Run Click to Depth Python", command=self.run_click_py)
        self.click_py_button.pack(pady=10)

        # Relay 리셋 버튼 추가
        self.reset_relay_button = tk.Button(root, text="Reset Relay", command=self.reset_relay)
        self.reset_relay_button.pack(pady=10)

        # 종료 버튼
        self.exit_button = tk.Button(root, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=10)

    def set_duty_cycle(self):
        """ 듀티 사이클 설정 """

        try:
            duty_value = int(self.duty_entry.get())
            if 0 <= duty_value <= 100:
                self.controller_api.change_duty_cycle(duty_value)
            else:
                raise ValueError("Duty cycle must be between 0 and 100")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid duty cycle between 0 and 100.")

    def reset_program(self):
        """ 프로그램 초기화 (Duty Cycle 0으로 설정 및 버튼 초기화) """
        self.controller_api.change_duty_cycle(0)  # Duty Cycle을 0으로 설정

    def run_zed_viewer(self):
        """ ZED Depth Viewer 실행 """
        try:
            # 버튼 비활성화
            # self.zed_button.config(state='disabled')

            # /usr/local/zed/tools 경로로 이동 후 ZED Depth Viewer 실행 (비동기 실행)
            self.camera_process = subprocess.Popen(['./ZED_Depth_Viewer'], cwd='/usr/local/zed/tools')

            # 다시 버튼 활성화
            self.click_py_button.config(state='normal')

        except FileNotFoundError:
            messagebox.showerror("Error", "Depth Camera 실행에 실패했습니다.")
            self.click_py_button.config(state='normal')  # 실패 시 버튼 다시 활성화


    def run_click_py(self):
        """ Click to Depth Python 실행 """
        try:
            # 버튼 비활성화
            # self.zed_button.config(state='disabled')

            # /usr/local/zed/tools 경로로 이동 후 Click to Depth Python 실행 (비동기 실행)
            self.click_py_process = subprocess.Popen(['python3', 'camera_only.py'], cwd='/home/tidepool/2024_depth_camera')

            # 다시 버튼 활성화
            self.zed_button.config(state='normal')

        except FileNotFoundError:
            messagebox.showerror("Error", "Click to Depth Python 실행에 실패했습니다.")
            self.zed_button.config(state='normal')  # 실패 시 버튼 다시 활성화


    def reset_relay(self):
        """ Relay를 껐다가 다시 켜는 함수 """
        self.controller_api.relay_off()
        print("Relay Off for reset")
        
        # 1초(1000밀리초) 후에 다시 켜기
        self.root.after(1000, lambda: [self.controller_api.relay_on(), print("Relay reset completed")])


    def exit_program(self):
        """ 프로그램 종료 (Duty Cycle 0으로 설정 후 종료) """
        self.controller_api.stop_and_cleanup()  # PWM 중지 및 GPIO 해제
        self.root.quit()  # 프로그램 종료

if __name__ == "__main__":
    root = tk.Tk()
    app = Depth_GUI(root)
    root.mainloop()

