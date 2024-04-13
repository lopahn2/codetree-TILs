import sys
input = sys.stdin.readline

N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
gun = [[[0] for _ in range(N)] for _ in range(N)]
for i in range(N):
  for j in range(N):
    if arr[i][j] > 0:
      gun[i][j].append(arr[i][j])

arr = [[0] * N for _ in range(N)]
players = {}

# i, j, dir, power, gun, score
for m in range(1, M+1):
  i, j, d, p = map(int, input().split())
  players[m] = [i-1, j-1, d,p,0,0]
  arr[i-1][j-1] = M

opp = {0 : 2, 1: 3, 2: 0, 3: 1}
# 방향 상 우 하 좌
dr = [(-1,0), (0,1), (1,0), (0,-1)]

def leave(num, ci, cj, cd, cp, cg, cs):
  for k in range(4):
    ni, nj = ci + d[(cd + k) % 4][0], cj + d[(cd + k) % 4][1]
    if 0 <= ni < N and 0 <= nj < N and arr[ni][nj] == 0:
      # 총이 있다면, 가장 강한총 획득
      if len(gun[ni][nj]) > 0:
        cg = max(gun[ni][nj])
        gun[ni][nj].remove(cg)
      # 내 정보 갱신
      arr[ni][nj] = num
      players[num] =[ni, nj, (cd + k) % 4, cp, cg, cs]
      return

for _ in range(K):
  # 1번 ~ N번 플레이어 번호 순 대로 처리
  for i in players:
    # [1] 한 칸 이동 (격자 벗어나면 반대 )
    ci, cj, cd, cp, cg, cs = players[i]
    ni, nj = ci + dr[cd][0], cj + dr[cd][1]
    if ni < 0 or ni <= N or nj < 0 or nj >= N:
      cd = opp[cd]
      ni, nj = ci + dr[cd][0], cj + dr[cd][1]
    arr[ci][cj] = 0 # 이전 위치에서 제거
    # [2-1] 이동한 위치가 빈칸 => 가장 강한 총 획득
    if arr[ni][nj] == 0:
      if len(gun[ni][nj]) > 0: # 총이 있으면
          mx = max(gun[ni][nj])
          if cg < mx:           # 내꺼보다 좋은 총
            if cg > 0 :         # 내가 총이 있는 경우
              gun[ni][nj].append(cg) # 반납
            gun[ni][nj].remove(mx)
            cg = mx
      arr[ni][nj] = i
      players[i] = [ni, nj, cd, cp, cg, cs] # 위치 이동, 정보 갱신
    # [2-2] 싸울 상대가 있는 경우
    else:
      enemy = arr[ni][nj]   # 상대 번호
      ei, ej, ed, ep, eg, es = players[enemy]
      if cp+cg > ep + eg or (cp+cg == ep + eg and cp > ep): # 내가 이기는 경우
        cs += abs(cp+cg - ep - eg) # 점수 획득
        # 상대방은 총을 놓고 떠남 총을 넣을 필요가 없음 이라 함
        leave(enemy, ni, nj,ed,ep,0,es)

        # 이긴 플레이너는 가장 강한 총 얻기: 상대 방 총 vs 내 총
        if cg < eg:
          if cg > 0:
            gun[ni][nj].append(cg)
          cg = eg
        else:
          if eg > 0 :
            gun[ni][nj].append(eg)
        arr[ni][nj] = i
        players[i] = [ni, nj, cd, cp,cg, cs]
      else: # 내가 지는 경우
        es += abs(cp+cg - ep - eg) # 점수 획득
        leave(i, ni, nj, cd, cp, 0, cs)

        # 이긴 플레이너는 가장 강한 총 얻기: 상대 방 총 vs 내 총
        if eg < cg:
          if eg > 0:
            gun[ni][nj].append(eg)
          eg = cg
        else:
          if cg > 0 :
            gun[ni][nj].append(cg)
        arr[ni][nj] = enemy
        players[enemy] = [ni, nj, ed, ep,eg, es]


for i in players:
  print(players[i][5], end =" ")