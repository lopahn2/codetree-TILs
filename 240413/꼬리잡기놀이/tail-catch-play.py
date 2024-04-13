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
            if 0 <= ni < N and 0 <= nj < N and v[ni][nj] == 0:
                if arr[ni][nj] == 2 or (arr[ni][nj] == 3 and (ci, cj) != (si, sj)):
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
bdr = [(0,1), (-1,0), (0,-1),(1,0)]
for k in range(K):
    # [1] 꼬리 이동
    for team in teams.values():
        ei, ej = team.pop()
        arr[ei][ej] = 4
        si, sj = team[0]
        for ni,nj in ((si-1,sj),(si+1,sj),(si,sj-1),(si,sj+1)):
          if 0 <= ni < N and 0 <= nj < N and arr[ni][nj] == 4:
            team.appendleft((ni,nj))
            arr[ni][nj] = arr[si][sj]
            break
    # [2] 공 던지기
    
    bdri = ( k // N ) % 4
    offset = k%N
    if bdri==0:                           # 우
        ci,cj = offset, 0
    elif bdri==1:
        ci,cj = N-1, offset
    elif bdri==2:
        ci,cj = N-1-offset, N-1
    else:
        ci,cj = 0, N-1-offset
    
    # [3] 공 맞기 처리
    
    for _ in range(N):                              # 최대 N범위까지 탐색
        if 0<=ci<N and 0<=cj<N and arr[ci][cj]>4:   # 특정 팀이 공 받았음
            team_n = arr[ci][cj]
            # (해당 좌표 인덱스 +1 )**2
            ans += (teams[team_n].index((ci,cj))+1)**2
            # teams[team_n] = teams[team_n][::-1]
            teams[team_n].reverse()
            break
        ci, cj = ci + bdr[bdri][0], cj + bdr[bdri][1]
print(ans)