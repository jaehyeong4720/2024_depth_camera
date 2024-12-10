import Jetson.GPIO as GPIO
import time

class Controller_API:
    def __init__(self, pwm_pin, relay_pin, frequency=10000):
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
        
        #릴레이 LED 초기화
        GPIO.output(self.pwm_pin, GPIO.LOW)  # LED OFF 상태로 초기화
        GPIO.output(self.relay_pin, GPIO.HIGH)  # 릴레이 OFF 상태로 초기화


    def led_on(self):
        """
        LED를 켭니다.
        """
        GPIO.output(self.pwm_pin, GPIO.HIGH)

    def led_off(self):
        """
        LED를 끕니다.
        """
        GPIO.output(self.pwm_pin, GPIO.LOW)

    def relay_on(self):
        GPIO.output(self.relay_pin, GPIO.LOW) 
        print("Relay On")

    def relay_off(self):
        GPIO.output(self.relay_pin, GPIO.HIGH) 
        print("Relay Off")   
    
    def stop_and_cleanup(self):
        """
        GPIO 설정을 해제합니다.
        """
        GPIO.output(self.relay_pin, GPIO.HIGH)     
        print("Relay 중지")           
        GPIO.cleanup()
        print("GPIO 해제 완료")
    


# 사용 예시
if __name__ == "__main__":
    pwm_pin = 33  # PWM 제어 핀 (예시: 33번 핀)
    relay_pin = 29  # Relay 제어 핀 (예시: 29번 핀)

    controller_api = Controller_API(pwm_pin, relay_pin, frequency=10000)  # 10kHz 주파수로 초기화

    # LED 켜고 끄기
    controller_api.led_on()
    time.sleep(2)  # 2초 동안 Led ON
    controller_api.led_off()
    time.sleep(2)  # 2초 동안 Led OFF    

    # 릴레이를 켜고 끄기
    controller_api.relay_on()
    time.sleep(2)  # 2초 동안 Relay ON
    controller_api.relay_off()
    time.sleep(2)  # 2초 동안 Relay OFF

    # PWM 종료 및 GPIO 해제
    controller_api.stop_and_cleanup()
