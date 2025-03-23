FILE_PATH = '02/Mars_Base_Inventory_List.csv'
DANGER_SUBS = '02/Mars_Base_Inventory_danger.csv'
BINARY_FILE = '02/Mars_Base_Inventory_List.bin'

def readFile(file_name: str):
    try:
        data = []
        # 파일 읽기
        with open('02/Mars_Base_Inventory_List.csv', 'r', encoding="utf-8") as file:
            while True:
                line = file.readline().strip()
                if not line:
                    break
                print (line)
                data.append(line.split(','))
        return data

    except FileNotFoundError as e:
        print(f"{file_name}을 찾을 수 없음. 파일명 또는 경로 확인 필요: {e}")
    except PermissionError as e:
        print(f"{file_name}에 대한 권한이 없음 : {e}")
    except Exception as e:
        print(f"에러 발생 : {e}")

def sortByFlammability(data: list):
    # 헤더 분리
    header = data[0]
    data = data[1:]

    # 인화성 높은 순으로 정렬
    data.sort(key=lambda x: x[4], reverse=True)

    return [header] + data

def classifyDangerSub(file_name: str,data: list):
    try:
        if not data: return
        # 헤더 분리
        header = data[0]
        data = data[1:]

        # 인화성 0.7 이상인 물품 목록 작성
        print("=" * 20 + "Flammability over 0.7" + "=" *20)
        with open(file_name, 'w', encoding="utf-8") as file:
            header_str = ",".join(header)
            print(header_str)
            file.write(header_str + "\n")
            for sub in data:
                if float(sub[4]) >= 0.7:
                    print(",".join(sub))
                    file.write(",".join(sub) + "\n") 

    except FileNotFoundError as e:
        print(f"{file_name}을 찾을 수 없음. 파일명 또는 경로 확인 필요: {e}")
    except PermissionError as e:
        print(f"{file_name}에 대한 권한이 없음 : {e}")
    except Exception as e:
        print(f"에러 발생 : {e}")

def processBinary(file_name: str, data: list):
    try:
        if not data: return
        # 헤더 분리
        header = data[0]
        data = data[1:]

        # 이진 파일로 저장
        with open(file_name, 'wb') as file:
            header_str = ",".join(header)
            file.write(header_str.encode("utf-8") + b"\n")
            for sub in data:
                file.write(",".join(sub).encode("utf-8") + b"\n")

        # 이진 파일 읽기
        print("=" * 20 + "Read binary file" + "=" *20)
        with open(file_name, 'rb') as file:
            byteData = file.read().split(b"\n")
        
        strData = [byte.decode("utf-8") for byte in byteData]
        for line in strData:
            print(line)

    except FileNotFoundError as e:
        print(f"{file_name}을 찾을 수 없음. 파일명 또는 경로 확인 필요: {e}")
    except PermissionError as e:
        print(f"{file_name}에 대한 권한이 없음 : {e}")
    except Exception as e:
        print(f"에러 발생 : {e}")

data = readFile(FILE_PATH)
sortedData = sortByFlammability(data)
classifyDangerSub(DANGER_SUBS, sortedData)
processBinary(BINARY_FILE, sortedData)