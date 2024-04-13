N, M, H, K = map(int, input().split())
m = N // 2
arr = []
tree = set()

for _ in range(M):
  i, j, dr = map(int, input().split())
  arr.append([i-1, j-1, dr])

for _ in range(H):
  i, j = map(int, input().split())
  tree.add((i-1, j-1))

ei = ej = m
answer = flag = cnt = dr =  0
val = cnt_mx = 1
tarr = [[0] * N for _ in range(N)]
d = [(-1,0),(0,1),(1,0),(0,-1)]
rd = [(0,-1),(0,1),(1,0),(-1,0)]
opp = {1:0, 0:1, 2:3, 3:2}
for k in range(1, K+1):
  # [1] 도망자 이동
  for i in range(len(arr)):
    si, sj, sdr = arr[i]
    if abs(si-ei) + abs(sj - ej) <= 3:
      ni, nj = si + rd[sdr][0], sj + rd[sdr][1]
      if 0 <= ni < N and 0 <= nj < N:
        if (ni, nj) != (ei, ej):
          arr[i][0], arr[i][1] = ni, nj
      else:
        sdr = opp[sdr]
        ni, nj = si + rd[sdr][0], sj + rd[sdr][1]
        if (ni, nj) != (ei, ej):
          arr[i] = [ni, nj, sdr]
        else:
          arr[i][2] = sdr
  # [2] 술래의 이동
  cnt += 1
  ei, ej = ei + d[dr][0], ej + d[dr][1]
  if (ei, ej) == (0,0):
    flag ,cnt , dr , val = 1, 1, 2, -1
  elif (ei, ej) == (m, m):
    flag ,cnt , dr , val = 0, 0, 0, 1
  if cnt == cnt_mx:
    cnt = 0
    dr = (dr + val) % 4
    if flag == 0:
      flag = 1
    else:
      flag = 0
      cnt_mx += val
  # [3] 도망자 잡기
  
  tset = set(((ei,ej), (ei + d[dr][0], ej + d[dr][1]), (ei + d[dr][0] * 2, ej + d[dr][1] * 2)))
  for i in range(len(arr) -1, -1, -1):
    if (arr[i][0], arr[i][1]) in tset and (arr[i][0], arr[i][1]) not in tree:
      arr.pop(i)
      answer += k
  if len(arr) == 0:
    break

print(answer)