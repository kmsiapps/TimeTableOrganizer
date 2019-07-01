
# 시간표 배치 프로그램
# By kmsiapps@gmail.com
# Last edit: 2019.06.03

import os

class personTT:
    def __init__(self, name, avTime, avTimeLen):
        self.name = name
        self.availableTimeCount = avTimeLen
        self.availableTime = avTime #avTime은 가능한 시간을 (i, j) 형태의 인덱스로 표시한 리스트. (1, 1)부터 시작함에 유의
    
    def __gt__(self, other):
        return self.availableTimeCount > other.availableTimeCount

def getLayout(filename):
    # layout.csv 파일 파싱해 기본 레이아웃 결정
    with open(filename, "r", encoding="utf-8 sig" ) as f:
        lineList = f.readlines()
        for i in range(len(lineList)):
            lineList[i] = lineList[i].strip().split(",")
    
    return lineList


def getTTinfo(filename, xLen, yLen, timedict):
    # 각 사람별 시간표 파일 파싱해 가능한 시간 정보 저장
    # timedict도 계속 업데이트함
    # timedict는 (i, j)를 key로, (i, j)에 가능한 시간 사람 수를 value로 가지는 딕셔너리

    with open(filename, "r", encoding="utf-8 sig" ) as f:
        lineList = f.readlines()
        for i in range(len(lineList)):
            lineList[i] = lineList[i].strip().split(",")

    avTime = []
    for i in range(1, yLen+1):
        for j in range(1, xLen+1):
            if i>=len(lineList) or j>=len(lineList[0]) or lineList[i][j] != 'X':
                avTime.append((i, j))
                timedict[(i, j)] += 1

    return (avTime, timedict)


def readData(xLen, yLen):
    personTTdict = {}
    timedict = {}
    file_lst = [file for file in os.listdir("./src/") if file[len(file)-4:] == ".csv"]

    if len(file_lst) == 0:
        print("사람별 시간표 파일이 없습니다!")
        return None
    
    for i in range(1, yLen+1):
        for j in range(1, xLen+1):
            timedict[(i, j)] = 0 # initialize timedict

    for file in file_lst:
        (avTime, timedict) = getTTinfo("./src/" + file, xLen, yLen, timedict)
        personTTdict[file[:len(file)-4]] = personTT(file[:len(file)-4], avTime, len(avTime))
    
    return (timedict, personTTdict)
    
layoutLst = getLayout("layout.csv")
yLen = len(layoutLst)-1
xLen = len(layoutLst[0])-1

(timedict, personTTdict) = readData(xLen, yLen)
personLst = [v[0] for v in sorted(personTTdict.items(), key=lambda kv: (kv[1], kv[0]))] # 가능한 시간이 적은 순서대로 배열된 사람들 목록
timeLst = [v[0] for v in sorted(timedict.items(), key=lambda kv: (kv[1], kv[0]))] # 가능하다고 말한 사람이 적은 순서대로 배열된 시간 목록

# TODO: 사람당 N번 배치되도록 해야함

N = int(input("사람당 배치 횟수: "))

for person in personLst:
    count = 0
    for time in timeLst:
        try:
            index = personTTdict[person].availableTime.index(time)
        except ValueError:
            continue
        (i, j) = personTTdict[person].availableTime[index]
        if (layoutLst[i][j] == ''):
            layoutLst[i][j] = person
        else:
            continue
        count+=1
        if (count == N): break
    if count < N: print("{} 배치 실패: {}번 중 {}번밖에 배치하지 못했습니다.".format(person, N, count))

writeStr = ""
for i in layoutLst:
    writeStr += ",".join(i) + "\n"

with open("./result.csv", "w", encoding="utf-8 sig") as f:
    f.write(writeStr)

input("결과가 result.csv로 저장되었습니다. 엔터를 누르면 종료합니다.")