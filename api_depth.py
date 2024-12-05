import Jetson.GPIO as GPIO
import time

class Controller_API:
    def __init__(self, pwm_pin, relay_pin, frequency=1000):
        """
        ControllerAPI 초기화 함수
        :param pwm_pin: 제어할 GPIO 핀 번호 (BOARD 모드 기준)
        :param relay_pin: 제어할 GPIO 핀 번호 (BOARD 모드 기준)
        :param frequency: PWM 신호의 주파수 (Hz)
        """
        GPIO.setwarnings(False)
        self.pwm_pin = pwm_pin
        self.relay_pin = relay_pin
        self.frequency = frequency
        self.pwm = None

        # GPIO 설정
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup([self.pwm_pin, self.relay_pin], GPIO.OUT)

        # PWM 객체 생성
        self.pwm = GPIO.PWM(self.pwm_pin, self.frequency)
        self.pwm.start(0)  # 초기 듀티 사이클 0%
        
        #릴레이 초기화
        GPIO.output(self.relay_pin, GPIO.HIGH)  # 릴레이 OFF 상태로 초기화

    def change_duty_cycle(self, duty_cycle):
        """
        듀티 사이클을 변경합니다.
        :param duty_cycle: 듀티 사이클 (0-100)
        """
        if self.pwm is not None:
            self.pwm.ChangeDutyCycle(duty_cycle)
            print(f"Duty Cycle: {duty_cycle}%")

    def relay_on(self):
        GPIO.output(self.relay_pin, GPIO.LOW) 
        print("Relay On")

    def relay_off(self):
        GPIO.output(self.relay_pin, GPIO.HIGH) 
        print("Relay Off")   
    
    def stop_and_cleanup(self):
        """
        PWM 신호를 중지하고 GPIO 설정을 해제합니다.
        """
        if self.pwm is not None:
            self.pwm.stop()
            print("PWM 중지")
        GPIO.output(self.relay_pin, GPIO.HIGH)     
        print("Relay 중지")           
        GPIO.cleanup()
        print("GPIO 해제 완료")
    


# 사용 예시
if __name__ == "__main__":
    pwm_pin = 33  # PWM 제어 핀 (예시: 33번 핀)
    relay_pin = 29  # Relay 제어 핀 (예시: 29번 핀)

    controller_api = Controller_API(pwm_pin, relay_pin, frequency=1000)  # 1kHz 주파수로 초기화

    # PWM 신호의 듀티 사이클을 50%로 변경
    controller_api.change_duty_cycle(50)
    time.sleep(2)  # 2초 동안 PWM이 50% 듀티 사이클로 동작

    # 릴레이를 켜고 끄기
    controller_api.relay_on()
    time.sleep(2)  # 2초 동안 Relay ON
    controller_api.relay_off()
    time.sleep(2)  # 2초 동안 Relay OFF

    # PWM 종료 및 GPIO 해제
    controller_api.stop_and_cleanup()
