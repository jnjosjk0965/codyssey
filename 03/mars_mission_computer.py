import random

class MyTime:
    '''로그에 입력할 시간을 생성하는 클래스'''
    # 각 월별 일수를 저장한 리스트
    month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    def __init__(self):
        self.year = 2025
        self.month = 1
        self.day = 1
        self.hour = random.randint(0, 23)
        self.minute = random.randint(0, 59)
        self.second = random.randint(0, 59)

    def get_time(self):
        '''시간을 생성하는 메서드'''
        self.hour = random.randint(0, 23)
        self.minute = random.randint(0, 59)
        self.second = random.randint(0, 59)
        time_str = f"{self.year}-{self.month:02d}-{self.day:02d} {self.hour:02d}:{self.minute:02d}:{self.second:02d}"

        # 1~5일 사이의 날짜를 증가
        self.day += random.randint(1,5)
        month_day = MyTime.month_day[self.month-1]
        if self.day > month_day:
            self.day = self.day - month_day
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1
        return time_str

class DummySensor:
    '''센서 더미 데이터를 생성하는 클래스'''
    def __init__(self):
        self.time = MyTime()
        self.env_values = {
            # 화성 기지 내부 온도 (18~30도)
            "mars_base_internal_temperature": 0.0,
            # 화성 기지 외부 온도 (0~21도)
            "mars_base_external_temperature": 0.0,
            # 화성 기지 내부 습도 (50~60%)
            "mars_base_internal_humidity": 0.0,
            # 화성 기지 외부 광량 (500~715 W/m2) 
            "mars_base_external_illuminance": 0.0,
            # 화성 기지 내부 이산화탄소 농도 (0.02~0.1%)
            "mars_base_internal_co2": 0.0,
            # 화성 기지 내부 산소 농도 (4%~7%)
            "mars_base_internal_oxygen": 0.0     
        }
    
    def set_env(self):
        '''센서 더미 데이터를 생성하는 메서드'''
        self.env_values["mars_base_internal_temperature"] = random.uniform(18, 30)
        self.env_values["mars_base_external_temperature"] = random.uniform(0, 21)
        self.env_values["mars_base_internal_humidity"] = random.uniform(50, 60)
        self.env_values["mars_base_external_illuminance"] = random.uniform(500, 715)
        self.env_values["mars_base_internal_co2"] = random.uniform(0.02, 0.1)
        self.env_values["mars_base_internal_oxygen"] = random.uniform(4, 7)

    def get_env(self):
        '''센서 더미 데이터를 로그에 저장하는 메서드'''
        try:
            with open("03/mars_base_env.log", "a", encoding="utf-8") as file:
                file.write(f"{self.time.get_time()}\n")
                for key, value in self.env_values.items():
                    match key:
                        case "mars_base_internal_temperature" | "mars_base_external_temperature":
                            file.write(f"{key}: {value:.2f}°C\n")
                        case "mars_base_external_illuminance":
                            file.write(f"{key}: {value:.2f}W/m2\n")
                        case "mars_base_internal_humidity" | "mars_base_internal_co2" | "mars_base_internal_oxygen":
                            file.write(f"{key}: {value:.2f}%\n")
                file.write("\n")

        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")
        except PermissionError:
            print("파일을 열 권한이 없습니다.")
        except Exception as e:
            print(f"에러 발생: {e}")

        return self.env_values
    
ds = DummySensor()
with open("03/mars_base_env.log", "w", encoding="utf-8") as file:
    file.write("Mars Base Environment Log\n\n") 
    
ds.set_env()
env_data = ds.get_env()
for key, value in env_data.items():
    print(f"{key}: {value:.2f}") # : 포매팅 시작, .2 소수점 둘째자리 까지 f 실수형

for _ in range(150):
    ds.set_env()
    ds.get_env()

print("done")