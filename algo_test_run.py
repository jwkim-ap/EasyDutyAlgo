from algo_team_day_first import get_schedule

# 각 팀의 각 간호사 duty
teams = [
    ['OT', 'TN', 'NO', 'OO', 'EE', 'EO'],
    ['NN', 'OO', 'TE', 'OO', 'OO', 'OT'],
    ['TE', 'NO', 'EO', 'OT', 'OO', 'ON']
]

# 각 팀의 각 간호사 연차
nurses_years = [
    [1, 4, 9, 4, 4, 2],
    [1, 4, 2, 8, 3, 9],
    [6, 2, 10, 1, 1, 1]
]

year, month = 2021, 2

# 3팀의 duty를 찾기 위해 get_schedule() 함수를 총 3회 호출
for team_idx in range(len(teams)):
    ### 팀별 연차를 추가로 받는 구조
    schedule = get_schedule(teams[team_idx], nurses_years[team_idx], year, month)  # 반환값은 한 팀의 duty를 담은 1차원 리스트
    print(f"team #{team_idx + 1}: {schedule}")
    print("=========================")
