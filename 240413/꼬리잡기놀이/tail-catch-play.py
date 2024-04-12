import sys

input = sys.stdin.readline

N, M, K = map(int, input().split())

arr = [list(map(int, input().split())) for _ in range(N)]
teams = {}
team_n = 5

from collections import deque
def bfs(si, sj, team_n):
    team = deque()
    q = deque()
    team.append((si, sj))
    q.append((si,sj))
    v[si][sj] = 1
    arr[si][sj] = team_n
    while q:
        ci, cj = q.popleft()
        for ni, nj in ((ci-1,cj),(ci+1,cj), (ci,cj-1), (ci,cj+1)):
            if 0<=ni<N and 0 <= nj < N and v[ni][nj] == 0:
                if arr[ni][nj] == 2 or (arr[ni][nj] == 3 and (ci,cj) != (si,sj)):
                    team.append((ni,nj))
                    v[ni][nj] = 1
                    q.append((ni,nj))
                    arr[ni][nj] = team_n
    teams[team_n] = team

v = [[0] * N for _ in range(N)]
for i in range(N):
    for j in range(N):
        if v[i][j] == 0 and arr[i][j] == 1:
            bfs(i,j,team_n)
            team_n += 1
ans = 0
for k in range(K):
    # [1] 머리 사람을 따라 한 칸 이동
    for tn, team in teams.items():
        ti, tj = team.pop()
        arr[ti][tj] = 4
        ci, cj = team[0]
        for ni, nj in ((ci-1,cj),(ci+1,cj), (ci,cj-1), (ci,cj+1)):
            if 0<=ni<N and 0 <= nj < N and arr[ni][nj] == 4:
                team.appendleft((ni,nj))
                arr[ni][nj] = tn
                break
        teams[tn] = team

    # [2] 공 발사 해서 맞는 사람 확인 및 방향 전환 및 점수 추가
    dr = ( k // N ) % 4
    ci = cj = -1
    d = [(0,1),(-1,0),(0,-1),(1,0)]
    if dr == 0:
        ci, cj = k % N , 0
    elif dr == 1:
        ci, cj = N - 1 , k % N
    elif dr == 2:
        ci, cj = N - 1 - ( k % N ), N - 1
    else:
        ci, cj = 0, N - 1 - ( k % N)
    for _ in range(N):
        if 0 <= ci < N and 0 <= cj < N and arr[ci][cj] > 4:
            team_n = arr[ci][cj]
            ans += (teams[team_n].index((ci,cj)) + 1) ** 2
            teams[team_n].reverse()
            break
        ci, cj = ci + d[dr][0], cj + d[dr][1]
print(ans)