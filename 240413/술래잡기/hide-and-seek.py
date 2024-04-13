import sys

input = sys.stdin.readline

N, M, H, K = map(int, input().split())
m = N // 2

arr = [[0] * N for _ in range(N)]

runner = [] # i, j, direction
tree = set()
rdr = [(0,-1),(0,1),(1,0),(-1,0)]
opp = {0:1, 1:0, 2:3, 3:2}
for _ in range(M):
  i, j, rdi = map(int,input().split())
  runner.append([i-1,j-1,rdi])

for _ in range(H):
  i, j = map(int,input().split())
  tree.add((i-1, j-1))

ei = ej = m
cnt = flag = dri = answer = 0
val = cnt_mx = 1

dr = [(-1,0),(0,1),(1,0),(0,-1)]
for k in range(1,K + 1):
  # [1] 도망자 이동
  for i in range(len(runner)):
    si, sj, rdi = runner[i]
    if abs(si-ei) + abs(sj-ej) <= 3:
      ni, nj = si + rdr[rdi][0], sj + rdr[rdi][1]
      if 0 <= ni < N and 0 <= nj < N:
        if((ni, nj) != (ei, ej)):
          runner[i] = [ni, nj, rdi]
      else:
        nrdi = opp[rdi]
        ni, nj = si + rdr[nrdi][0], sj + rdr[nrdi][1]
        if((ni, nj) != (ei, ej)):
          runner[i] = [ni, nj, nrdi]
        else:
          runner[i][2] = nrdi
  # [2] 술래의 이동
  cnt += 1
  ei,ej = ei + dr[dri][0], ej + dr[dri][1]
  if (ei, ej) == (0,0):
    val, flag, cnt, dri = -1, 1, 1, 2
  elif (ei, ej) == (m, m):
    val, flag, cnt, dri = 1, 0, 0, 0
  if cnt == cnt_mx:
    cnt = 0
    dri = (dri + val) % 4
    if flag == 0:
      flag = 1
    else:
      flag = 0
      cnt_mx += val
  # [3] 도망자 탐색
  tset = set(((ei, ej), (ei+dr[dri][0], ej+dr[dri][1]), (ei+dr[dri][0] * 2, ej+dr[dri][1] * 2)))
  for i in range(len(runner) -1, -1, -1):
    if (runner[i][0], runner[i][1]) in tset and (runner[i][0], runner[i][1]) not in tree:
      runner.pop(i)
      answer += k
  # 도망자가 없으면 끝
  if len(arr) == 0:
    break
  # for i in range(3):
  #   ni, nj = ei + dr[dri][0] * i, ej + dr[dri][1] * i
  #   if 0 <= ni < N and 0 <= nj < N:
  #     if (ni, nj) in tree:
  #       continue
  #     for ridx in range(len(runner)-1, -1, -1):
  #       if (ni, nj) == (runner[ridx][0], runner[ridx][1]):
  #         runner.pop(ridx)
  #         catch += 1
  #   else:
  #     break
print(answer)