from dummy_sensor import DummySensor
import time
import psutil
import platform

class MissionComputer:
    def __init__(self, sensor: DummySensor):
        self.ds = sensor
        self.env_values = self.ds.get_env()
        self.data = { k : [] for k in self.env_values.keys() }
        self.count = 0

    def load_setting(self): 
        """ setting.txt 파일을 읽어 필터 설정 """
        try: 
            with open("05/setting.txt", "r") as f:
                return [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            print("setting.txt not found. Using default settings.")
            return None
        except Exception as e:
            print(f"Error occurred while reading setting.txt: {e}")
            return None


    def format_json(self, dic: dict):
        """ dictionary를 json 형식으로 출력 """
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
        """ 기록된 센서 값의 평균값을 계산"""
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

    def get_mission_computer_info(self):
        """ 운영체제 및 하드웨어 정보 가져오기 """
        os_info = {}

        # 운영체제 및 버전
        os_info["os_name"] = platform.system()
        os_info["os_version"] = platform.version()

        # CPU 타입
        os_info["cpu_type"] = platform.processor()

        # CPU 코어 수
        
        os_info["logical_cores"] = psutil.cpu_count(logical=True)
        os_info["physical_cores"] = psutil.cpu_count(logical=False)

        # 메모리 크기
        os_info["memory_size"] =(psutil.virtual_memory().total / (1024 ** 3), "GB")   # 바이트 -> GB 변환

        # setting에 적용된 필터 적용
        settings = self.load_setting()
        if settings:
            filtered_info = {k: v for k, v in os_info.items() if k in settings}
        else:
            filtered_info = os_info

        return filtered_info

    def get_mission_computer_load(self):
        """ CPU 및 메모리 실시간 사용량 가져오기 """
        computer_load = {}
        # CPU 사용량
        computer_load["cpu_usage"] = (psutil.cpu_percent(interval=1), "%")

        # 메모리 사용량
        memory_info = psutil.virtual_memory()
        used_memory = memory_info.used / (1024 ** 3)  # 바이트 -> GB
        memory_percent = memory_info.percent
        computer_load["memory_usage"] = (used_memory, "GB")
        computer_load["memory_percent"] = (memory_percent, "%")

        # setting에 적용된 필터 적용
        settings = self.load_setting()
        if settings:
            filtered_load = {k: v for k, v in computer_load.items() if k in settings}
        else:
            filtered_load = computer_load

        return filtered_load

if __name__ == "__main__":
    ds = DummySensor()
    runComputer = MissionComputer(sensor=ds)
    #runComputer.get_sensor_data(interval= 1, avg_interval= 10)

    my_os = runComputer.get_mission_computer_info()
    print(f"{'=' * 10} 시스템 정보 {'=' * 10}")
    print(runComputer.format_json(my_os))

    load = runComputer.get_mission_computer_load()
    print(f"{'=' * 10} 시스템 모니터링 {'=' * 10}")
    print(runComputer.format_json(load))

