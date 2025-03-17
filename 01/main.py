'''
- 본격적으로 로그를 분석하기 위해서 mission_computer_main.log 파일을 열고 전체 내용을 화면에 출력해 본다. 이때 코드는 main.py 파일로 저장한다. (로그 데이터는 별도 제공)
- 파일을 처리 할 때에 발생할 수 있는 예외를 처리한다.
- mission_computer_main.log의 내용을 통해서 사고의 원인을 분석하고 정리해서 보고서(log_analysis.md)를 Markdown 형태로 를 작성해 놓는다.
- 보고서는 UTF8 형태의 encoding을 사용해서 저장한다.
- 수행 과제에 지시된 파일 이름을 준수한다.

보너스 과제
- 출력 결과를 시간의 역순으로 정렬해서 출력한다.
- 출력 결과 중 문제가 되는 부분만 따로 파일로 저장한다.
'''
# 보고서 작성
def make_log_report(file_name:str, logs:list, reverse=False):
    data = f'# 로그 분석 보고서\n## 로그 데이터 요약\n- **총 로그 수**: {len(logs)}개\n## 로그 데이터\n'
    write_file(file_name, data=data)
    header = '| ' + ' | '.join(logs[0]) + ' |\n' +  '| ' + ' | '.join(['---' for _ in logs[0]]) + ' |\n'
    add_file(file_name, header)
    
    # 로그 데이터 정렬
    logdata = sorted(logs[1:] ,key=lambda x: x[0], reverse=reverse)
    for log in logdata:
        print(",".join(log))
        if(len(log) >= 3):
            timestamp, event, msg = log[0], log[1], ','.join(log[2:]) # 로그 메시지에 ,가 들어 있을 경우
            add_file(file_name,f'| {timestamp} | {event} | {msg.strip()} |\n')

# 문제 로그 분류
def classified_log_report(file_name:str, logs:list):
    erorr_log = list(filter(lambda x: x[1] == 'ERROR', logs[1:]))

    data = f'# 에러 로그 보고서\n- **총 로그 수**: {len(erorr_log)}개\n## 로그 데이터\n'
    write_file(file_name, data=data)
    header = '| ' + ' | '.join(logs[0]) + ' |\n' +  '| ' + ' | '.join(['---' for _ in logs[0]]) + ' |\n'
    add_file(file_name, header)

    for log in erorr_log:
        if(len(log) >= 3):
            timestamp, event, msg = log[0], log[1], ','.join(log[2:]) # 로그 메시지에 ,가 들어 있을 경우
            add_file(file_name,f'| {timestamp} | {event} | {msg.strip()} |\n')

# 파일 작성
def write_file(file_name:str, data):
    try:
        with open(file_name, mode='w', encoding='utf-8') as file:
            file.write(data)
    except FileNotFoundError:
        print('파일을 찾을 수 없음. 파일명 또는 경로 확인 필요')
    except Exception as e:
        print("에러: ", e)

# 파일 내용 추가
def add_file(file_name:str, data):
    try:
        with open(file_name, mode='a', encoding='utf-8') as file:
            file.write(data)
    except FileNotFoundError:
        print('파일을 찾을 수 없음. 파일명 또는 경로 확인 필요')
    except Exception as e:
        print("에러: ", e)

# 파일 읽기
def read_file(file_path:str):
    try:
        data = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            while True:
                line = file.readline().strip()
                if not line:
                    break
                print (line)
                data.append(line.split(','))
        return data
    except FileNotFoundError:
        print('파일을 찾을 수 없음. 파일명 또는 경로 확인 필요')
    except Exception as e:
        print("에러: ", e)


# 실행
print('Hello Mars')
logs = read_file('01/mission_computer_main.log')
print("-" * 40 + " 역순 출력 " + "-" * 40)
make_log_report('01/log_analysis.md', logs=logs, reverse=True)
classified_log_report('01/error_log_report.md', logs=logs)
print('done')