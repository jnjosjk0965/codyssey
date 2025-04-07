from dummy_sensor import DummySensor
import time

class MissionComputer:
    def __init__(self):
        self.ds = DummySensor()
        self.env_values = self.ds.get_env()
        self.data = { k : [] for k in self.env_values.keys() }
        self.count = 0

    def format_json(self, dic: dict):
        """
        dictionary를 json 형식으로 출력
        """
        lines = ["{"]
        for _, (key, value) in enumerate(dic.items()):
            # 값이 튜플이면 (값, 단위) 결합, 아니면 그대로
            if isinstance(value, tuple):
                val_str = f"{value[0]} {value[1]}"
            elif isinstance(value, float):
                val_str = f"{value:.2f}"  # 평균 값은 소수점 2자리
            else:
                val_str = f"{value}"
            lines.append(f'  "{key}": "{val_str}",')
        lines[-1] = lines[-1].rstrip(",")
        lines.append("}")
        return "\n".join(lines)
    
    def get_average(self):
        avg = {}
        for key, value in self.data.items():
            avg[key] = round(sum(value) / len(value), 2)
        # 평균값 계산 후 data 초기화
        self.data = { k : [] for k in self.env_values.keys() }
        return avg

    def get_sensor_data(self, interval = 5, avg_interval = 300):
        """
        1. 센서의 값을 가져와서 env_values에 저장
        2. env_values의 값을 출력 -> json 형식으로 출력
        3. 1,2번을 5초마다 반복
        """
        while True:
            try:
                if self.count >= avg_interval:
                    # 5분 경과 시
                    print("5 minutes passed")
                    avg = self.get_average()
                    print(f"5min average: {self.format_json(avg)}")
                    print("\n" + "="*50 + "\n")
                    self.count = 0
                else:
                    # 값과 단위의 튜플에서 값만 추출
                    for key, value in self.env_values.items():
                        self.data[key].append(value[0])
                
                print(self.format_json(self.env_values))

                self.ds.set_env()
                self.env_values = self.ds.get_env()
                time.sleep(interval)
                self.count += interval
                
            except KeyboardInterrupt:
                print("System stopped...")
                break
        

if __name__ == "__main__":
    runComputer = MissionComputer()
    runComputer.get_sensor_data(interval= 1, avg_interval= 10)


