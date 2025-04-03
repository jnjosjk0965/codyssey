from dummy_sensor import DummySensor
import time

class MissionComputer:
    def __init__(self):
        self.env_values = {}
        self.ds = DummySensor()
        self.count = 0

    def format_json(self, dic: dict):
        """
        dictionary를 json 형식으로 출력
        """
        lines = ["{"]
        for i, (key, value) in enumerate(dic.items()):
            # 값이 튜플이면 (값, 단위) 결합, 아니면 그대로
            if isinstance(value, tuple):
                val_str = f"{value[0]}{value[1]}"
            else:
                val_str = f"{value:.2f}"  # 평균 값은 소수점 2자리
            comma = "," if i < len(dic) - 1 else ""  # 마지막 항목엔 쉼표 없음
            lines.append(f'  "{key}": "{val_str}"{comma}')
        lines.append("}")
        return "\n".join(lines)

    def get_sensor_data(self):
        """
        1. 센서의 값을 가져와서 env_values에 저장
        2. env_values의 값을 출력 -> json 형식으로 출력
        3. 1,2번을 5초마다 반복
        """
        log = []
        while True:
            try:
                self.env_values = self.ds.get_env()
                if self.count >= 20:
                    print("5 minutes passed")
                    keys = list(self.env_values.keys())
                    avg = {}
                    for i in range(len(keys)):
                        sum = 0
                        for j in range(len(log)):
                            sum += log[j][i]
                        avg[keys[i]] = round(sum / len(log), 2)
                    print(f"5min average: {self.format_json(avg)}")
                    print("\n" + "="*50 + "\n")
                    log = []
                    self.count = 0
                else:
                    # 값과 단위의 튜플에서 값만 추출
                    temp = [ v for (v, _) in list(self.env_values.values())]
                    log.append(temp)
                
                print(self.format_json(self.env_values))

                self.ds.set_env()
                time.sleep(1)
                self.count += 5
                
            except KeyboardInterrupt:
                print("System stopped...")
                break
        

if __name__ == "__main__":
    runComputer = MissionComputer()
    runComputer.get_sensor_data()


