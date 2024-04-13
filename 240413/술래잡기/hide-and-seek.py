import sys
input = sys.stdin.readline
N, MM, H, K = map(int, input().split())

M = N // 2

d = [(-1,0),(0,1),(1,0),(0,-1)]

# 도망자 좌표
arr = []
for _ in range(MM):
  i, j, dt = map(int, input().split())
  arr.append([i-1,j-1,dt])

tree = set()
for _ in range(H):
  i, j = map(int, input().split())
  tree.add((i-1,j-1))

drun = [(0,-1),(0,1),(1,0),(-1,0)]
opp = {0:1,1:0,2:3,3:2} # 반대방향 구하는 법

ei, ej = M, M

answer = dr = cnt = flag = 0
value = cnt_mx = 1
for k in range(1,K+1):
  # 도망자 이동
  for i in range(len(arr)):
    if abs(arr[i][0] - ei) + abs(arr[i][1] - ej) <= 3:
      ni, nj = arr[i][0] + drun[arr[i][2]][0], arr[i][1] + drun[arr[i][2]][1]
      if 0 <= ni < N and 0 <= nj < N:
        if (ni, nj) != (ei, ej): 
          arr[i][0], arr[i][1] = ni, nj
      else:
        nd = opp[arr[i][2]] # 반대 방향
        ni, nj = arr[i][0] + drun[nd][0], arr[i][1] + drun[nd][1]
        if (ni, nj) != (ei, ej):
          arr[i] = [ni, nj, nd] # 실제 이동 처리 / 방향 바뀜 
        else:
          arr[i][2] = nd       


  # 술래의 이동
  ei, ej = ei + d[dr][0], ej + d[dr][1]
  cnt += 1
  
  if (ei, ej) == (0,0):
    cnt_mx, cnt, flag, value = N, 1, 1, -1
    dr = 2
  elif (ei, ej) == (M, M):
    cnt_mx, cnt, flag, value = 1, 0, 0, 1
    dr = 0
  else:
    if cnt == cnt_mx:
      cnt = 0
      dr = (dr + value) % 4
      if flag == 0:
        flag = 1
      else:
        flag = 0
        cnt_mx += value
  
  # 도망자 잡기
  tset = set(((ei, ej), (ei+d[dr][0], ej+d[dr][1]), (ei+d[dr][0] * 2, ej+d[dr][1] * 2)))
  for i in range(len(arr) -1, -1, -1):
    if (arr[i][0], arr[i][1]) in tset and (arr[i][0], arr[i][1]) not in tree:
      arr.pop(i)
      answer += k
  # 도망자가 없으면 끝
  if len(arr) == 0:
    break
print(answer)