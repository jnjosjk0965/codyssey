import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
from datetime import datetime

FOLDER_NAME = "10/records"

def record_audio(duration=5, fs=44100):
    """
    마이크에서 지정된 시간 동안 오디오를 녹음하고 저장합니다.

    Args:
        duration (int): 녹음 시간 (초).
        fs (int): 샘플 레이트 (초당 샘플 수).
    """
    # Create 'records' directory if it doesn't exist
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)

    print(f"Recording for {duration} seconds...")

    try:
        # Record audio
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished

        # Generate filename with current date and time
        now = datetime.now()
        filename = now.strftime("%Y%m%d-%H%M%S.wav")
        filepath = os.path.join(FOLDER_NAME, filename)

        # Save the recorded audio
        write(filepath, fs, myrecording)
        print(f"Recording saved to {filepath}")

    except Exception as e:
        print(f"An error occurred during recording: {e}")

def list_recordings_by_date():
    """
    사용자로부터 날짜 범위를 입력받아 해당 범위 내의 녹음 파일 목록을 출력합니다.
    """
    if not os.path.exists(FOLDER_NAME) or not os.listdir(FOLDER_NAME):
        print(f"'{FOLDER_NAME}' 폴더가 없거나 녹음 파일이 없습니다.")
        return

    while True:
        try:
            start_date_str = input("시작 날짜를 입력하세요 (예: 20230101): ")
            start_date = datetime.strptime(start_date_str, "%Y%m%d")
            break
        except ValueError:
            print("잘못된 날짜 형식입니다. YYYYMMDD 형식으로 다시 입력해주세요.")

    while True:
        try:
            end_date_str = input("종료 날짜를 입력하세요 (예: 20231231): ")
            end_date = datetime.strptime(end_date_str, "%Y%m%d")
            break
        except ValueError:
            print("잘못된 날짜 형식입니다. YYYYMMDD 형식으로 다시 입력해주세요.")

    # 시작 날짜가 종료 날짜보다 늦으면 스왑
    if start_date > end_date:
        start_date, end_date = end_date, start_date
        print("시작 날짜가 종료 날짜보다 늦어 날짜 순서가 변경되었습니다.")

    print(f"\n{start_date.strftime('%Y년 %m월 %d일')}부터 {end_date.strftime('%Y년 %m월 %d일')}까지의 녹음 파일:")
    found_files = []

    for filename in os.listdir(FOLDER_NAME):
        if filename.endswith(".wav"):
            try:
                # 파일 이름에서 날짜 부분 파싱 (예: 20230101-123456.wav -> 20230101)
                file_date_str = filename.split('-')[0]
                file_date = datetime.strptime(file_date_str, "%Y%m%d")

                # 날짜 범위 안에 있는지 확인
                if start_date <= file_date <= end_date:
                    found_files.append(filename)
            except ValueError:
                # 날짜 형식이 아닌 파일은 건너뜁니다.
                continue

    if found_files:
        for f in sorted(found_files): # 파일 이름을 정렬하여 출력
            print(f"- {f}")
    else:
        print("해당 날짜 범위에 해당하는 녹음 파일이 없습니다.")

if __name__ == "__main__":
    print("어떤 작업을 하시겠습니까?")
    print("1. 음성 녹음 시작")
    print("2. 특정 날짜 범위의 녹음 파일 목록 보기")
    choice = input("선택 (1 또는 2): ")

    if choice == '1':
        record_audio()
    elif choice == '2':
        list_recordings_by_date()
    else:
        print("잘못된 선택입니다. 프로그램을 종료합니다.")