import sys
input = sys.stdin.readline
N, M, K = map(int, input().split())

arr = [list(map(int, input().split())) for _ in range(N)]
guns = [[[] for _ in range(N)] for _ in range(N)]
for i in range(N):
    for j in range(N):
        if arr[i][j] > 0:
            guns[i][j].append(arr[i][j])
arr = [[0] * N for _ in range(N)]

players = {}

# i, j, direction, stat, gun, point
for n in range(1, 1+M):
    i, j, d, s = map(int, input().split())
    players[n] = [i-1, j-1, d, s, 0, 0]
    arr[i-1][j-1] = n

dr = [(-1,0),(0,1),(1,0),(0,-1)]
opp = {0:2, 1:3, 2:0, 3:1}

def leave(num, ci, cj, cd, cs, cg, cp):
    for k in range(4):
        ni, nj = ci + dr[(cd + k) % 4][0], cj + dr[(cd + k) % 4][1]
        if 0 <= ni < N and 0 <= nj < N and arr[ni][nj] == 0:
            if len(guns[ni][nj]) > 0:
                if cg > max(guns[ni][nj]):
                    guns[ni][nj].append(cg)
                    cg = max(guns[ni][nj])
                    guns[ni][nj].remove(cg)
                arr[ni][nj] = num
                players[num] = [ni, nj, (cd + k) % 4, cs, cg, cp]
                return

for _ in range(K):
    for i in range(1, M+1):
        ci, cj, cd, cs, cg, cp = players[i]
        ni, nj = ci + dr[cd][0], cj + dr[cd][1]
        if ni < 0 or ni >= N or nj < 0 or nj >= N:
            cd = opp[cd]
            ni, nj = ci + dr[cd][0], cj + dr[cd][1]
        arr[ci][cj] = 0
        if arr[ni][nj] == 0:
            if len(guns[ni][nj]) > 0:
                if cg < max(guns[ni][nj]):
                    if cg > 0:
                        guns[ni][nj].append(cg)
                    cg = max(guns[ni][nj])
                    guns[ni][nj].remove(cg)
            # 진짜 이동 (이동한 것 업데이트)
            arr[ni][nj] = i
            players[i] = [ni, nj, cd, cs, cg, cp]
        else:
            enemy = arr[ni][nj]
            ei, ej, ed, es, eg, ep = players[enemy]
            if (cs+cg > es+eg) or ((cs+cg == es+eg) and cs > es): # 내가 승리
                cp += abs(cs+cg - es - eg)
                leave(enemy, ni, nj, ed, ep, 0, es)
                if cg < eg:
                    if cg > 0:
                        guns[ni][nj].append(cg)
                    cg= eg
                else:
                    if eg > 0:
                        guns[ni][nj].append(eg)
                arr[ni][nj] = i
                players[i] = [ni, nj, cd,cp,cg,cs]
                
            else: # 내가 패배
                ep += abs(cs+cg - es - eg)
                leave(i, ni, nj, cd, cp, 0, cs)

                if eg < cg:
                    if eg > 0:
                        guns[ni][nj].append(eg)
                    eg= cg
                else:
                    if cg > 0:
                        guns[ni][nj].append(cg)
                arr[ni][nj] = enemy
                players[enemy] = [ni, nj, ed,ep,eg,es]
                

for i in players:
    print(players[i][5], end=' ')