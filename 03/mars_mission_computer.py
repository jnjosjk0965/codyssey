import random

MAX_DAY = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
class MyTime:
    '''로그에 입력할 시간을 생성하는 클래스'''
    # 각 월별 일수를 저장한 리스트
    def __init__(self):
        self.year = 2016
        self.month = 1
        self.day = 1
        self.hour = random.randint(0, 23)
        self.minute = random.randint(0, 59)
        self.second = random.randint(0, 59)

    def is_leap_year(self):
        '''윤년 여부를 확인하는 메서드'''
        year = self.year
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    def get_month_day(self):
            return 29 if self.month == 2 and self.is_leap_year() else MAX_DAY[self.month - 1]

    def get_time(self):
        '''시간을 생성하는 메서드'''
        time_str = f"{self.year}-{self.month:02d}-{self.day:02d} {self.hour:02d}:{self.minute:02d}:{self.second:02d}"

        # 다음 날짜를 3~7일 사이로 증가
        self.day += random.randint(3,7)

        month_day = self.get_month_day()

        # 날짜가 월별 일수를 넘으면 다음 달로 이동
        if self.day > month_day:
            self.day = self.day - month_day
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1

        # 다음 시간을 랜덤 생성        
        self.hour = random.randint(0, 23)
        self.minute = random.randint(0, 59)
        self.second = random.randint(0, 59)
        return time_str

class DummySensor:
    '''센서 더미 데이터를 생성하는 클래스'''
    def __init__(self, file: str):
        self.time = MyTime()
        self.file = file
        with open(self.file, "w", encoding="utf-8") as file:
            file.write("Mars Base Environment Log\n\n") 
        self.env_values = {
            # 화성 기지 내부 온도 (18~30도)
            "mars_base_internal_temperature": None,
            # 화성 기지 외부 온도 (0~21도)
            "mars_base_external_temperature": None,
            # 화성 기지 내부 습도 (50~60%)
            "mars_base_internal_humidity": None,
            # 화성 기지 외부 광량 (500~715 W/m2) 
            "mars_base_external_illuminance": None,
            # 화성 기지 내부 이산화탄소 농도 (0.02~0.1%)
            "mars_base_internal_co2": None,
            # 화성 기지 내부 산소 농도 (4%~7%)
            "mars_base_internal_oxygen": None     
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
        if self.env_values["mars_base_internal_temperature"] is None:
            self.set_env()
        return self.env_values
    
    def write_log(self):
        '''센서 더미 데이터를 로그에 저장하는 메서드'''
        self.set_env()
        try:
            with open(self.file, "a", encoding="utf-8") as file:
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

file_name = "03/mars_base_env.log"    
ds = DummySensor(file=file_name)
    
env_data = ds.get_env()
for key, value in env_data.items():
    print(f"{key}: {value:.2f}") # : 포매팅 시작, .2 소수점 둘째자리 까지 f 실수형

for _ in range(80):
    ds.write_log()

print("done")