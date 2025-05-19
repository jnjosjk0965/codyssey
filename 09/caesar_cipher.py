
password_path = "password.txt"
result_path = "result.txt"

def caesar_cipher_decode(target_text: str):
    # 대문자였던 자리의 인덱스를 기억
    uppercase_indices = [i for i, c in enumerate(target_text) if c.isupper()]
    lower_text = target_text.lower()
    
    # 알파벳 목록
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    # 복호화 시도 리스트
    decoded_list = []

    for shift in range(1, 26):  # Caesar는 1~25 시프트
        shifted_text = ""
        for char in lower_text:
            if char in alphabet:
                new_index = (alphabet.index(char) + shift) % 26
                shifted_text += alphabet[new_index]
            else:
                shifted_text += char  # 알파벳이 아니면 그대로 둠

        # 대문자 복원
        shifted_text = ''.join(
            c.upper() if i in uppercase_indices else c
            for i, c in enumerate(shifted_text)
        )
        decoded_list.append(shifted_text)

    # 결과 출력
    print("\n--- 복호화 후보 리스트 ---")
    for idx, decoded in enumerate(decoded_list):
        print(f"{idx}: {decoded}")

    # 사용자 선택
    while (True):
        choice = int(input("\n선택할 인덱스를 입력하세요: "))
        if 0 <= choice < len(decoded_list):
            with open(result_path, 'w', encoding='utf-8') as f:
                f.write(decoded_list[choice])
            print("선택한 결과가 result.txt에 저장되었습니다.")
            break
        else:
            print("잘못된 인덱스입니다.")


if __name__ == "__main__":
    try:
        with open(password_path, 'r', encoding='utf-8') as f:
            encrypted_text = f.read().strip()
        caesar_cipher_decode(encrypted_text)
    except FileNotFoundError:
        print(f"{password_path} 파일이 존재하지 않습니다.")
