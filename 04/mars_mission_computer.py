from dummy_sensor import DummySensor
import time

class MissionComputer:
    def __init__(self):
        self.env_values = {}
        self.ds = DummySensor()
        self.count = 0

    def get_sensor_data(self):
        """
        1. 센서의 값을 가져와서 env_values에 저장
        2. env_values의 값을 출력 -> json 형식으로 출력
        3. 1,2번을 5초마다 반복
        """
        while True:
            try:
                self.env_values = self.ds.get_env()
                print(self.env_values)

                self.ds.set_env()
                self.count += 5
                time.sleep(5)
            except KeyboardInterrupt:
                print("System stopped...")
                break
        

if __name__ == "__main__":
    runComputer = MissionComputer()
    runComputer.get_sensor_data()


