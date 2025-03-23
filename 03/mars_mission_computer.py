import random

class DummySensor:
    def __init__(self):
        self.env_values = {
            "mars_base_internal_temperature": 0.0, # 화성 기지 내부 온도 (18~30도)
            "mars_base_external_temperature": 0.0, # 화성 기지 외부 온도 (0~21도)
            "mars_base_internal_humidity": 0.0,    # 화성 기지 내부 습도 (50~60%)
            "mars_base_external_illuminance": 0.0, # 화성 기지 외부 광량 (500~715 W/m2)
            "mars_base_internal_co2": 0.0,         # 화성 기지 내부 이산화탄소 농도 (0.02~0.1%)
            "mars_base_internal_oxygen": 0.0       # 화성 기지 내부 산소 농도 (4%~7%)
        }
    
    def set_env(self):
        self.env_values["mars_base_internal_temperature"] = random.uniform(18, 30)
        self.env_values["mars_base_external_temperature"] = random.uniform(0, 21)
        self.env_values["mars_base_internal_humidity"] = random.uniform(50, 60)
        self.env_values["mars_base_external_illuminance"] = random.uniform(500, 715)
        self.env_values["mars_base_internal_co2"] = random.uniform(0.02, 0.1)
        self.env_values["mars_base_internal_oxygen"] = random.uniform(4, 7)

    def get_env(self):
        return self.env_values
    
ds = DummySensor()
ds.set_env()
env_data = ds.get_env()
for key, value in env_data.items():
    print(f"{key}: {value:.2f}") # : 포패팅 시작, .2 소수점 둘째자리 까지 f 실수형