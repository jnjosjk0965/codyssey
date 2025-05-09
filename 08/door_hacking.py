import zipfile
import itertools
import string
import time

# 압축 파일 경로
zip_file_path = '08/emergency_storage_key.zip'

# 사용할 문자셋 (소문자 + 숫자)
charset = string.ascii_lowercase + string.digits

# 비밀번호 길이
password_length = 6

def unlock_zip(zip_path):
    zf = zipfile.ZipFile(zip_path)

    attempts = 0
    start_time = time.time()

    # 모든 가능한 6자리 조합을 순회
    for pwd_tuple in itertools.product(charset, repeat=password_length):
        password = ''.join(pwd_tuple)
        try:
            zf.extractall(pwd=password.encode())
            print(f"[+] 비밀번호 찾음: {password}")
            print(f"[i] 총 시도 횟수: {attempts}")
            print(f"[i] 소요 시간: {time.time() - start_time:.2f}초")
            return password
        except:
            attempts += 1
            if attempts % 100000 == 0:
                print(f"[-] {attempts}개 시도 중... (최근: {password})")

    print("[-] 비밀번호를 찾지 못했습니다.")
    return None

# 실행
unlock_zip(zip_file_path)
