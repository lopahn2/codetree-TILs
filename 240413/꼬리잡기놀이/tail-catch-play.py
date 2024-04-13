import sys
input = sys.stdin.readline
N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
teams = {}

from collections import deque
def bfs(si, sj, team_n):
    team = deque()
    q = deque()
    team.append((si,sj))
    q.append((si,sj))
    arr[si][sj] = team_n
    v[si][sj] = 1
    while q:
        ci, cj = q.popleft()
        for ni, nj in ((ci + 1, cj),(ci - 1, cj),(ci, cj + 1),(ci, cj - 1)):
            if 0 <= ni < N and 0 <= nj < N and v[ni][nj] == 0 and arr[ni][nj] != 0:
                if arr[ni][nj] == 2 or (arr[ni][nj] == 3 and (ni, nj) != (si, sj)):
                    team.append((ni,nj))
                    q.append((ni,nj))
                    v[ni][nj] = 1
                    arr[ni][nj] = team_n
    teams[team_n] = team


v = [[0] * N for _ in range(N)]
team_n = 5
for i in range(N):
    for j in range(N):
        if v[i][j] == 0 and arr[i][j] == 1:
            bfs(i,j,team_n)
            team_n += 1


ans = 0
for k in range(K):
    # [1] 꼬리 이동
    for tn, team in teams.items():
        ti, tj = team.pop()
        arr[ti][tj] = 4
        hi, hj = team[0]
        for ni, nj in ((hi + 1, hj),(hi - 1, hj),(hi, hj + 1),(hi, hj - 1)):
            if 0 <= ni < N and 0 <= nj < N and arr[ni][nj] == 4:
                team.appendleft((ni,nj))
                arr[ni][nj] = tn
                break
        teams[tn] = team
    # [2] 공 던지기
    bdr = [(0,1), (-1,0), (0,-1),(1,0)]
    bdri = ( k // N ) % 4

    ci = cj = -1
    if bdri == 0:
        ci, cj = k % N, 0
    elif bdri == 1:
        ci, cj = N - 1, k % N
    elif bdri == 2:
        ci, cj = N - 1 - ( k % N ), N - 1
    else:
        ci, cj = 0, N - 1 - ( k % N )
    
    # [3] 공 맞기 처리
    
    for _ in range(N):
        if 0 <= ci < N and 0 <= cj < N and arr[ci][cj] > 4:
          team_n = arr[ci][cj]
          ans += (teams[team_n].index((ci,cj)) + 1) ** 2
          teams[team_n].reverse()
          break
        ci, cj = ci + bdr[bdri][0], cj + bdr[bdri][1]
print(ans)