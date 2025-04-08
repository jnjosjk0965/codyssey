# 기술적 설명

## 스토리

별다른 코딩을 한 것도 아닌데 미션 컴퓨터가 중간 중간 다운되는 현상이 일어나기 시작했다. 아직 생명유지와 관련된 기능까지 연결되어 있다면 문제가 심각해 질 것 같다. 컴퓨터의 상태를 좀 알고 싶긴한데 우주 기지에 설치된 컴퓨터라 완전히 밀봉되어 있어서 뜯어 보지도 못할 것 같다. 미션 컴퓨터의 지금 상태는 뭐가 문제인지 알 수가 없다.

지금 미션 컴퓨터의 상태를 알아보고 문제를 파악해 봐야겠는데 일단은 미션 컴퓨터 정보를 가져오는 코드를 좀 작성해서 상태를 파악해 보야겠다.

## 수행과제

- 파이썬 코드를 사용해서 다음과 같은 미션 컴퓨터의 정보를 알아보는 메소드를 get_mission_computer_info() 라는 이름으로 만들고 문제 7에서 완성한 MissionComputer 클래스에 추가한다.

  - 필요한 미션 컴퓨터의 시스템 정보
    - 운영체계
    - 운영체계 버전
    - CPU의 타입
    - CPU의 코어 수
    - 메모리의 크기

- get_mission_computer_info()에 가져온 시스템 정보를 JSON 형식으로 출력하는 코드를 포함한다.
- 미션 컴퓨터의 부하를 가져오는 코드를 get_mission_computer_load() 메소드로 만들고 MissionComputer 클래스에 추가한다
- get_mission_computer_load() 메소드의 경우 다음과 같은 정보들을 가져 올 수 있게한다.
  - CPU 실시간 사용량
  - 메모리 실시간 사용량
- get_mission_computer_load()에 해당 결과를 JSON 형식으로 출력하는 코드를 추가한다.
- get_mission_computer_info(), get_mission_computer_load()를 호출해서 출력이 잘되는지 확인한다.
- MissionComputer 클래스를 runComputer 라는 이름으로 인스턴스화 한다.
- runComputer 인스턴스의 get_mission_computer_info(), get_mission_computer_load() 메소드를 호출해서 시스템 정보에 대한 값을 출력 할 수 있도록 한다.
- 최종적으로 결과를 mars_mission_computer.py 에 저장한다.

# 제약 조건

## 제약 사항

- python에서 기본 제공되는 명령어 이외의 별도의 라이브러리나 패키지를 사용해서는 안된다.
- 단 시스템 정보를 가져오는 부분은 별도의 라이브러리를 사용 할 수 있다.
- 시스템 정보를 가져오는 부분은 예외처리가 되어 있어야 한다.
- 모든 라이브러리는 안정된 마지막 버전을 사용해야 한다.

## 보너스 과제

- setting.txt 파일을 만들어서 출력되는 정보의 항목을 셋팅 할 수 있도록 코드를 수정한다.

# psutil

psutil은 Process and System Utilities의 약자로
파이썬에서 시스템 모니터링, 프로파일링, 프로세스 리소스 제한 및 실행중인 프로세스 관리에 유용한 모듈이다.

## 시스템 관련 (CPU)

```python
''' cpu 시간을 튜플로 리턴. percpu가 True인 경우 각 cpu에 대해 튜플로 리스트를 리턴함 '''
psutil.cpi_times()
# scputimes(user=182305.26, nice=0.0, system=114865.72, idle=2466723.85)

''' cpu 사용률을 백분율로 리턴함.  '''
for x in range(3):
  psutil.cpu_percent(interval = 1)
# 8.1 5.5 7.9

''' cpu 코어 수를 리턴 logical가 False 라면 물리적 코어수를 리턴함. '''
psutil.cpu_count()
# 11
```

## 메모리 관련

```python
'''
시스템 메모리 사용량을 바이트 단위로 튜플로 반환
total : 총 메모리
available : 시스템을 스왑하지 않고 프로세스에 즉시 제공 가능한 메모리
percent : 메모리 사용량 백분율
used : 사용되는 메모리
free : 실제 메모리 여유량 (total - used == free)가 반드시 성립하지 않음
active : 현재 사용중이거나 최근에 사용된 메모리
inactive : 사용중이 아닌 메모리
buffers : 파일 시스템, 메타 데이터와 같은 것들을 위한 캐시
shared : 여러 프로세스에서 동시에 액세스 가능한 메모리
wired : 항상 ram에 남아있는 것으로 표시되는 메모리
'''
psutil.virtual_memory()
# svmem(total=19327352832, available=4029939712, percent=79.1, used=7132069888, free=76890112, active=3963748352, inactive=3747577856, wired=3168321536)
```
