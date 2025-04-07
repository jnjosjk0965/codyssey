import random

ENV_RANGES = {
    "mars_base_internal_temperature": (18.0, 30.0, "°C"),
    "mars_base_external_temperature": (0.0, 21.0, "°C"),
    "mars_base_internal_humidity": (50.0, 60.0, "%"),
    "mars_base_external_illuminance": (500.0, 715.0, "W/m2"),
    "mars_base_internal_co2": (0.02, 0.1, "%"),
    "mars_base_internal_oxygen": (4.0, 7.0, "%"),
}

class DummySensor:
    '''센서 더미 데이터를 생성하는 클래스'''
    def __init__(self):
        self.env_values = {}
    
    def set_env(self):
        '''센서 더미 데이터를 생성하는 메서드'''
        for key, value in ENV_RANGES.items():
            min, max, unit = value
            self.env_values[key] = (round(random.uniform(min, max), 2), unit)

    def get_env(self):
        if not self.env_values:
            self.set_env()
        return self.env_values
    
if __name__ == "__main__":
    ds = DummySensor()
    print(ds.get_env())