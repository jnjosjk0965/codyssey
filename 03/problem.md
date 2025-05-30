# 기술적 설명

## 스토리

화성 기지에 돔을 새로 만들어 연결하고 기지를 보강하고 나니 드디어 우주복을 벗을 수 있었다.

우주복을 벗고나니 한결 마음의 여유가 생긴다. 하지만 여전히 가장 큰 문제가 남아 있다. 미션 컴퓨터가 여전히 지금 상태를 제대로 작동을 못하고 있다는 점이다. 한송희 박사는 미션 컴퓨터의 메뉴를 구성하고 앞으로 생존에 필요한 기능들을 하나씩 추가하면서 화성을 탈출 할 수 있는 실마리를 만달어야 가야 한다고 생각했다.

그러기 위해서는 먼저 화성 기지의 남은 센서들을 사용해서 환경 값을 읽어 들이고 출력하는 기능을 추가 해야했다. 그리고 실제 센서를 만들기 전에 더미 센서(dummy sensor) 부터 만들어서 테스트를 시작해야 했다.

## 수행과제

- 더미 센서에 해당하는 클래스를 생성한다. 클래스의 이름은 DummySensor로 정의한다.
- DummySensor의 멤버로 env_values라는 사전 객체를 추가한다. 사전 객체에는 다음과 같은 항목들이 추가 되어 있어야 한다.
  - 화성 기지 내부 온도 (mars_base_internal_temperature)
  - 화성 기지 외부 온도 (mars_base_external_temperature)
  - 화성 기지 내부 습도 (mars_base_internal_humidity)
  - 회성 기지 외부 광량 (mars_base_external_illuminance)
  - 화성 기지 내부 이산화탄소 농도 (mars_base_internal_co2)
  - 화성 기지 내부 산소 농도 (mars_base_internal_oxygen)
- DummySensor는 테스트를 위한 객체이므로 데이터를 램덤으로 생성한다.
- DummySensor 클래스에 set_env() 메소드를 추가한다. set_env() 메소드는 random으로 주어진 범위 안의 값을 생성해서 env_values 항목에 채워주는 역할을 한다. 각 항목의 값의 범위는 다음과 같다.
  - 화성 기지 내부 온도 (18~30도)
  - 화성 기지 외부 온도 (0~21도)
  - 화성 기지 내부 습도 (50~60%)
  - 화성 기지 외부 광량 (500~715 W/m2)
  - 화성 기지 내부 이산화탄소 농도 (0.02~0.1%)
  - 화성 기지 내부 산소 농도 (4%~7%)
- DummySensor 클래스는 get_env() 메소드를 추가하는데 get_env() 메소드는 env_values를 return 한다.
- DummySensor 클래스를 ds라는 이름으로 인스턴스(Instance)로 만든다.
- 인스턴스화 한 DummySensor 클래스에서 set_env()와 get_env()를 차례로 호출해서 값을 확인한다.
- 전체 코드를 mars_mission_computer.py 파일로 저장한다.

# 제약 조건

## 제약 사항

- Python에서 기본 제공되는 명령어만 사용해야 하며 별도의 라이브러리나 패키지를 사용해서는 안된다.
- 단 random을 다루는 라이브러리는 사용 가능하다.
- Python의 coding style guide를 확인하고 가이드를 준수해서 코딩한다.
- 경고 메시지 없이 모든 코드는 실행 되어야 한다.

## 보너스 과제

- 출력하는 내용을 날짜와시간, 화성 기지 내부 온도, 화성 기지 외부 온도, 화성 기지 내부 습도 ,화성 기지 외부 광량, 화성 기지 내부 이산화탄소 농도, 화성 기지 내부 산소 농도 와 같이 파일에 log를 남기는 부분을 get_env()에 추가 한다.
