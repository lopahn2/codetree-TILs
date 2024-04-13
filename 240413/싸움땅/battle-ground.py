N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]

guns = [[[] for _ in range(N)] for _ in range(N)]

for i in range(N):
  for j in range(N):
    if arr[i][j] > 0:
      guns[i][j].append(arr[i][j])

arr = [[0] * N for _ in range(N)]
# i, j, d, power, gun, score
players = {}

for m in range(1, M+1):
  i, j, d, p = map(int ,input().split())
  players[m] = [i-1, j-1, d,p, 0, 0]
  arr[i-1][j-1] = m

pdr = [(-1,0),(0,1),(1,0),(0,-1)]
opp = {0:2, 1:3, 2:0, 3:1}


def leave(num, ci, cj, cd, cp, cg, cs):
  for di in range(4):
    ni, nj = ci + pdr[(cd + di) % 4][0], cj + pdr[(cd + di) % 4][1]
    if 0 <= ni < N and 0 <= nj < N and arr[ni][nj] == 0:
      if len(guns[ni][nj]) > 0:
         cg = max(guns[ni][nj])
         guns[ni][nj].remove(cg)
      players[num] = [ni, nj, (cd + di) % 4, cp ,cg, cs]
      arr[ni][nj] = num
      return
  



for k in range(1, K+1):
  for i in players:
    ci, cj, cd, cp, cg, cs = players[i]
    ni, nj = ci + pdr[cd][0], cj + pdr[cd][1]
    if ni < 0 or ni >= N or nj < 0 or nj >= N:
      cd = opp[cd]      
      ni, nj = ci + pdr[cd][0], cj + pdr[cd][1]
    arr[ci][cj] = 0

    if arr[ni][nj] == 0: # 플레이어가 없음
      if len(guns[ni][nj]) > 0:
        mx = max(guns[ni][nj])
        if cg < mx:
          if cg > 0:
            guns[ni][nj].append(cg)
          cg = mx
          guns[ni][nj].remove(mx)
      players[i] = [ni, nj, cd, cp, cg, cs]
      arr[ni][nj] = i
    else: # 플레이어가 있음
      enemy = arr[ni][nj]
      ei, ej, ed, ep, eg, es = players[enemy]

      if ((cp+cg) > (ep+eg)) or ((cp+cg) == (ep+eg) and cp > ep): # 내가 이기는 경우
        cs += abs((cp+cg) - (ep+eg))
        leave(enemy, ni, nj, ed, ep, 0, es)
        if cg < eg:
          if cg > 0:
            guns[ni][nj].append(cg)
          cg = eg
        else:
          if eg > 0:
            guns[ni][nj].append(eg)
        players[i] = [ni, nj, cd, cp, cg, cs]
        arr[ni][nj] = i
      else: # 상대방이 이기면
        es += abs((cp+cg) - (ep+eg))
        leave(i, ni, nj, cd, cp, 0, cs)
        if eg < cg:
          if eg > 0:
            guns[ni][nj].append(eg)
          eg = cg
        else:
          if cg > 0:
            guns[ni][nj].append(cg)
        players[enemy] = [ni, nj, ed, ep, eg, es]
        arr[ni][nj] = enemy

for i in players:
  print(players[i][5], end = ' ')