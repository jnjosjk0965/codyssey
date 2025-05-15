import pyzipper
import itertools
import string
import time
import os
import io
import multiprocessing
import logging

# 설정
zip_file_path = '08/emergency_storage_key-2.zip'
password_file_path = '08/password.txt'
charset = string.ascii_lowercase + string.digits
password_length = 6
prefix_length = 2
num_workers = multiprocessing.cpu_count()
log_interval = 100_000  # 진행 상황 로그 간격

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# 자음과 모음 정의
consonants = 'bcdfghjklmnpqrstvwxyz'
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

def worker(prefixes, zip_data_bytes, charset, password_length, result_queue, stop_event, worker_id):
    start_time = time.time()
    with pyzipper.AESZipFile(io.BytesIO(zip_data_bytes)) as zf:
        file_list = zf.namelist()
        if not file_list:
            return
        first_file = file_list[0]

        attempts = 0
        for prefix in prefixes:
            if stop_event.is_set():
                return
            suffix_length = password_length - len(prefix)
            for suffix_tuple in itertools.product(charset, repeat=suffix_length):
                if stop_event.is_set():
                    return
                password = prefix + ''.join(suffix_tuple)
                try:
                    zf.pwd = password.encode()
                    zf.read(first_file)
                    result_queue.put(password)
                    stop_event.set()
                    return
                except Exception:
                    pass

                attempts += 1
                if attempts % log_interval == 0:
                    elapsed = time.time() - start_time
                    logging.info(f"[Worker {worker_id}] {attempts:,}개 시도 중 (prefix='{prefix}', 최근='{password}', 경과: {elapsed:.1f}s)")

def unlock_zip_with_prefixes(zip_data_bytes, prefix_list):
    chunk_size = len(prefix_list) // num_workers
    prefix_chunks = [prefix_list[i:i + chunk_size] for i in range(0, len(prefix_list), chunk_size)]

    manager = multiprocessing.Manager()
    result_queue = manager.Queue()
    stop_event = manager.Event()

    processes = []
    for i, chunk in enumerate(prefix_chunks):
        p = multiprocessing.Process(
            target=worker,
            args=(chunk, zip_data_bytes, charset, password_length, result_queue, stop_event, i)
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    if not result_queue.empty():
        return result_queue.get()
    else:
        return None

def unlock_zip_parallel(zip_path):
    try:
        with open(zip_path, 'rb') as f:
            zip_data_bytes = f.read()
    except FileNotFoundError:
        logging.error(f"[!] 파일을 찾을 수 없습니다: {zip_path}")
        return None

    logging.info(f"[*] 멀티프로세싱 시작 ({num_workers} 프로세스 사용)")

    start_time = time.time()

    # 1단계: 우선순위 prefix 시도
    priority_prefixes = generate_prioritized_prefixes()
    logging.info("[1단계] 우선순위 prefix 시도 중...")
    result = unlock_zip_with_prefixes(zip_data_bytes, priority_prefixes)

    if result:
        elapsed = time.time() - start_time
        logging.info(f"[✓] 비밀번호 찾음 (우선순위): {result}")
        logging.info(f"[i] 소요 시간: {elapsed:.2f}초")
    else:
        # 2단계: 나머지 prefix 시도
        logging.info("[2단계] 나머지 prefix 시도 중...")
        remaining_prefixes = generate_remaining_prefixes()
        result = unlock_zip_with_prefixes(zip_data_bytes, remaining_prefixes)
        elapsed = time.time() - start_time
        if result:
            logging.info(f"[✓] 비밀번호 찾음 (나머지): {result}")
            logging.info(f"[i] 소요 시간: {elapsed:.2f}초")
        else:
            logging.warning("[-] 비밀번호를 찾지 못했습니다.")
            return None

    os.makedirs(os.path.dirname(password_file_path), exist_ok=True)
    with open(password_file_path, 'w') as f:
        f.write(result + '\n')
    return result

if __name__ == '__main__':
    unlock_zip_parallel(zip_file_path)
