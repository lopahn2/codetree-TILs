import sys
input = sys.stdin.readline

N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
gun = [[[] for _ in range(N)] for _ in range(N)]
for i in range(N):
    for j in range(N):
        if arr[i][j]>0:
            gun[i][j].append(arr[i][j])

arr = [[0]*N for _ in range(N)]
# [0]:i, [1]:j, [2]:dir, [3]:power,[4]:gun,[5]:score  방향 0,1,2,3 (↑, →, ↓, ←)
players = {}            # 1~M 플레이어
for m in range(1,M+1):
    i,j,d,p = map(int, input().split())
    players[m]=[i-1,j-1,d,p,0,0]
    arr[i-1][j-1]=m

opp = {0:2, 1:3, 2:0, 3:1}
#방향 상,우,하,좌
di = [-1, 0, 1, 0]
dj = [ 0, 1, 0,-1]

def leave(num,ci, cj, cd, cp, cg, cs):
    for k in range(4):      # 현재방향부터 시계방향 90도씩 빈칸 찾기 (최소한 내가온(상대방이 온)칸은 비어있음)
        ni,nj=ci+di[(cd+k)%4], cj+dj[(cd+k)%4]
        if 0<=ni<N and 0<=nj<N and arr[ni][nj]==0:
            # 총이 있다면 가장 강한총 획득
            if len(gun[ni][nj])>0:
                cg = max(gun[ni][nj])
                gun[ni][nj].remove(cg)
            arr[ni][nj]=num # 내 정보 갱신 후 리턴
            players[num]=[ni,nj,(cd+k)%4,cp,cg,cs]
            return

for _ in range(K):      # K라운드 동안 경기진행
    # 1번~M번까지 전체 플레이어 번호순대로 처리
    for i in players:
        # [1] 한 칸 이동(격자 벗어나면 반대방향)
        ci,cj,cd,cp,cg,cs = players[i]
        ni,nj=ci+di[cd], cj+dj[cd]
        if ni<0 or N<=ni or nj<0 or N<=nj:  # 범위를 벗어남
            cd = opp[cd]                    # 방향 반대로
            ni,nj=ci+di[cd], cj+dj[cd]      # 한 칸 이동
        arr[ci][cj]=0                       # 이전위치에서 플레이어 표시 제거

        # [2-1] 이동한 위치가 빈칸인 경우 => 강한총 획득
        if arr[ni][nj]==0:
            if len(gun[ni][nj])>0:          # 총이 있는 경우
                mx = max(gun[ni][nj])
                if cg<mx:                   # 더 강한총이면 교체
                    if cg>0:                # 총이 있는 경우
                        gun[ni][nj].append(cg)  # 내총을 바닥에..반납
                    gun[ni][nj].remove(mx)
                    cg=mx
            arr[ni][nj]=i                   # 위치이동
            players[i]=[ni,nj,cd,cp,cg,cs]  # 정보갱신
        # [2-2] 빈칸아닌경우 => 싸울 상대방이 있는 경우
        else:
            enemy=arr[ni][nj]               # 상대방 번호 확인
            ei,ej,ed,ep,eg,es = players[enemy]
            if cp+cg>ep+eg or (cp+cg==ep+eg and cp>ep): # 내가 이기는 경우
                cs+=(cp+cg)-(ep+eg)         # 공격력 차이만큼 점수 획득
                leave(enemy,ni,nj,ed,ep,0,es)   # 상대방은 총을 놓고 떠남

                # 이긴 플레이어는 가장 강한 총 얻기: 상대방총 vs 내총
                if cg<eg:
                    if cg>0:
                        gun[ni][nj].append(cg)
                    cg=eg
                else:
                    if eg>0:
                        gun[ni][nj].append(eg)
                arr[ni][nj]=i
                players[i]=[ni,nj,cd,cp,cg,cs]
            else:                                       # 지는 경우
                es+=(ep+eg)-(cp+cg)         # 공격력 차이만큼 점수 획득
                leave(i,ni,nj,cd,cp,0,cs)   # 내가 총 놓고 떠남

                # 이긴 플레이어는 가장 강한 총 얻기: 상대방총 vs 내총
                if eg<cg:
                    if eg>0:
                        gun[ni][nj].append(eg)
                    eg=cg
                else:
                    if cg>0:
                        gun[ni][nj].append(cg)
                arr[ni][nj]=enemy
                players[enemy]=[ni,nj,ed,ep,eg,es]

for i in players:
    print(players[i][5],end=' ')    # 각 플레이어 점수출력