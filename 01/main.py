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
logs = []
print('hello mars')
try:
    file = open('/Users/amaoto/study/codyssey/01/mission_computer_main.log', mode='r',encoding='utf-8',)
    while True:
        line = file.readline().strip()
        if not line:
            break
        logs.append(line.split(','))
    print('logs : ',logs)

    new_file = open('01/log_analysis.md', mode='w', encoding='utf-8')
    data = f'# 로그 분석 보고서\n## 로그 데이터 요약\n- ** 총 로그 수: {len(logs)}개\n## 로그 데이터'
    new_file.write(data)
    for log in logs:
        log_data = ', '.join(log)
        new_file.write(f'- {log_data}\n')

except FileNotFoundError:
    print('파일을 찾을 수 없음. 파일명 또는 경로 확인 필요')
except Exception as e:
    print("에러: ", e)
finally:
    file.close()
    new_file.close()