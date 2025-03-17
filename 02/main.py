def classifyDangerSub():
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

        # 헤더 분리
        header = ",".join(data[0])
        data = data[1:]

        # 인화성 높은 순으로 정렬
        data.sort(key=lambda x: x[4], reverse=True)

        # 인화성 0.7 이상인 물품 목록 작성
        print("=" * 20 + "flammability over 0.7" + "=" *20)
        with open('02/Mars_Base_Inventory_danger.csv', 'w', encoding="utf-8") as file:
            print(header)
            file.write(header + "\n")
            for sub in data:
                if float(sub[4]) >= 0.7:
                    print(",".join(sub))
                    file.write(",".join(sub) + "\n")    

    except FileNotFoundError as e:
        print(f"파일을 찾을 수 없음. 파일명 또는 경로 확인 필요: {e}")
    except PermissionError as e:
        print(f"파일에 대한 권한이 없음 : {e}")
    except Exception as e:
        print(f"에러 발생 : {e}")
        

classifyDangerSub()