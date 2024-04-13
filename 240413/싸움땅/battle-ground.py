import sys
input = sys.stdin.readline
N, M, K = map(int, input().split())

arr = [list(map(int, input().split())) for _ in range(N)]
guns = [[[0] for _ in range(N)] for _ in range(N)]
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
                # 진 사람 행동
                guns[ni][nj].append(eg)
                eg = 0 # 총 버리기

                for edi in range(4):
                    eni, enj = ei + dr[(ed + edi) % 4][0], ej + dr[(ed + edi) % 4][1]
                    if 0 <= eni < N and 0 <= enj < N and arr[eni][enj] == 0:
                        # arr[ei][ej] = 0
                        arr[eni][enj] = enemy
                        new_gun = 0
                        if len(guns[eni][enj]) > 0:
                            new_gun = max(guns[eni][enj])
                            guns[eni][enj].remove(new_gun)
                        players[enemy] = [eni, enj, (ed + edi) % 4, es, new_gun, ep]
                        break
                # 이긴 사람 행동
                if cg < max(guns[ni][nj]):
                    guns[ni][nj].append(cg)
                    cg = max(guns[ni][nj])
                    guns[ni][nj].remove(cg)
                players[i] = [ni, nj, cd, cs, cg, cp]
            else: # 내가 패배
                ep += abs(cs+cg - es - eg)

                # 진 사람 행동
                guns[ni][nj].append(cg)
                cg = 0 # 총 버리기

                for cdi in range(4):
                    cni, cnj = ni + dr[(cd + cdi) % 4][0], nj + dr[(cd + cdi) % 4][1]
                    if 0 <= cni < N and 0 <= cnj < N and arr[cni][cnj] == 0:
                        arr[cni][cnj] = i
                        new_gun = 0
                        if len(guns[cni][cnj]) > 0:
                            new_gun = max(guns[cni][cnj])
                            guns[cni][cnj].remove(new_gun)
                        players[i] = [cni, cnj, (cd + cdi) % 4, cs, new_gun, cp]
                        break
                # 이긴 사람 행동
                if eg < max(guns[ni][nj]):
                    guns[ni][nj].append(eg)
                    eg = max(guns[ni][nj])
                    guns[ni][nj].remove(eg)
                players[enemy] = [ni, nj, ed, es, eg, ep]

for i in players:
    print(players[i][5], end=' ')