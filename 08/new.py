import time
import itertools
import string
import zipfile
import io
import os
from multiprocessing import Pool, current_process

# 전역 변수 설정
charset = 'abcdefghijklmnopqrstuvwxyz0123456789'
zip_file = '08/emergency_storage_key-2.zip'
password_length = 6
prefix_length = 2

# 자음과 모음 정의
consonants = 'tscpbdmfglnrwkvj'
vowels = 'aeiou'

def generate_cv_vc_prefixes():
    cv = [c + v for c in consonants for v in vowels]
    vc = [v + c for v in vowels for c in consonants]
    return cv + vc

def generate_digit_prefixes():
    return [a + b for a in string.digits for b in string.digits]

def generate_prioritized_prefixes():
    return generate_cv_vc_prefixes() + generate_digit_prefixes()

def generate_remaining_prefixes():
    all_prefixes = set(''.join(p) for p in itertools.product(charset, repeat=prefix_length))
    priority_prefixes = set(generate_prioritized_prefixes())
    return sorted(all_prefixes - priority_prefixes)

def try_password(args):
    """각 프로세스가 시도할 비밀번호 조합"""
    c1, start_time = args

    # 현재 process ID 출력
    print(f'process({current_process().pid}) start with {c1}')

    # ZIP 파일을 메모리로 로딩
    with open(zip_file, 'rb') as f:
        zip_data = io.BytesIO(f.read())

    # ZIP 파일 열기
    zf = zipfile.ZipFile(zip_data, 'r')

    # 압축 파일 이름 목록(첫 번째 파일 이름) 
    fname = zf.namelist()[0]

    # 6자리 비밀번호 시도
    for c2 in charset:
        for c3 in charset:
            for c4 in charset:
                for c5 in charset:
                    password = f"{c1}{c2}{c3}{c4}{c5}"
                    try:
                        # 파일 열기 시도
                        with zf.open(fname, 'r', pwd=password.encode()) as file:
                            file.read(1)  # 파일이 정상인지 최소 1바이트 읽기
                            print(f"정답 찾음: {password}")

                            # 찾은 password를 password.txt에 저장
                            with open("password.txt", "w") as f:
                                f.write(password)

                            print(f"총 소요 시간: {time.time() - start_time}")
                            os._exit(0)  # 프로세스 종료
                            return password
                    except:
                        continue
    return None

def unlock_zip():
    # 시작 시간 측정
    start_time = time.time()
    print('시작 시간:', start_time)

    priority_prefixes = generate_prioritized_prefixes()
    print(priority_prefixes)
    # 멀티프로세싱 Pool 생성, 시스템 CPU 코어 수 만큼 프로세스 생성
    with Pool() as pool:
        # charset의 첫 번째 문자 기준으로 멀티프로세싱 분배
        tasks = [(c, start_time) for c in priority_prefixes]
        results = pool.map(try_password, tasks)

    print('최종 종료 시간:', time.time())
    print('총 소요 시간:', time.time() - start_time)
    return None

if __name__ == "__main__":
    try:
        unlock_zip()
    except KeyboardInterrupt:
        print("\n프로그램이 사용자에 의해 종료되었습니다 (Ctrl+C).")
        os._exit(0)
