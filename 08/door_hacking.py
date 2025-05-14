import pyzipper
import itertools
import string
import time
import os
import io

# 압축 파일 경로
zip_file_path = '08/emergency_storage_key.zip'

# 사용할 문자셋 (소문자 + 숫자)
charset = string.ascii_lowercase + string.digits

# 비밀번호 길이
password_length = 6

# 결과 저장 경로
password_file_path = '08/password.txt'

def unlock_zip(zip_path):
    try:
        # ZIP 파일을 메모리에 로드
        with open(zip_path, 'rb') as f:
            zip_data = io.BytesIO(f.read())
    except FileNotFoundError:
        print(f"[!] 파일을 찾을 수 없습니다: {zip_path}")
        return None

    attempts = 0
    start_time = time.time()

    print("[*] 비밀번호 추측 시작...")

    with pyzipper.AESZipFile(zip_data) as zf:
        file_list = zf.namelist()
        if not file_list:
            print("[!] ZIP 파일이 비어 있습니다.")
            return None

        first_file = file_list[0]

        for pwd_tuple in itertools.product(charset, repeat=password_length):
            password = ''.join(pwd_tuple)
            try:
                zf.pwd = password.encode()
                # 비밀번호 유효성만 검증 (파일 하나 읽어보기)
                zf.read(first_file)

                # 비밀번호 맞음
                elapsed = time.time() - start_time
                print(f"[✓] 비밀번호 찾음: {password}")
                print(f"[i] 총 시도 횟수: {attempts}")
                print(f"[i] 소요 시간: {elapsed:.2f}초")

                # 저장
                os.makedirs(os.path.dirname(password_file_path), exist_ok=True)
                with open(password_file_path, 'w') as f:
                    f.write(password + '\n')

                return password

            except Exception:
                pass

            attempts += 1
            if attempts % 100000 == 0:
                print(f"[-] {attempts}개 시도 중... (최근: {password})")

    print("[-] 비밀번호를 찾지 못했습니다.")
    return None

# 메인 실행
if __name__ == '__main__':
    unlock_zip(zip_file_path)
