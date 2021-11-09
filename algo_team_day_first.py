# Nurse_Duty_Algo (day first, combined module)

import heapq

# 하루에 가능한 120가지 팀 duty 조합을 만드는 함수
def make_day_combinations():
    for day_nurse in range(6):
        for evening_nurse in range(6):
            for night_nurse in range(6):
                if (day_nurse != evening_nurse)\
                and (day_nurse != night_nurse)\
                and (evening_nurse != night_nurse):
                    temp_combination = ['O'] * 6
                    temp_combination[day_nurse] = 'T'
                    temp_combination[evening_nurse] = 'E'
                    temp_combination[night_nurse] = 'N'
                    day_combinations.append(temp_combination)


# 유효성 검사용 함수
def check_validity(combination, days, nurses, nurses_years):
    global teams_recorded

    # 각 간호사에 대하여 유효성 검사
    for nurse in range(6):
        # [필수] NIGHT - OFF - DAY 설 수 없음
        if nurses[nurse][days] == 'N' and nurses[nurse][days+1] == 'O' and combination[nurse] == 'T':
            return False

        # [필수] NIGHT - DAY, NIGHT - EVENING 설 수 없음
        if nurses[nurse][days+1] == 'N' and (combination[nurse] == 'T' or combination[nurse] == 'E'):
            return False
    
        # [필수] EVENING - DAY 설 수 없음
        if nurses[nurse][days+1] == 'E' and (combination[nurse] == 'T'):
            return False

        # [필수] 너무 연속으로 근무하게 됨
        if 'O' not in nurses[nurse][-5:] and (combination[nurse] != 'O'):
            return False

        # [권장] 한 달에 N은 9개 미만
        if nurses[nurse].count('N') == 8 and combination[nurse] == 'N':
            return False

        # 팀 연차에 관련된 유효성 검사
        if teams_recorded > 0:
            if combination[nurse] == 'T':
                if team_years_total[days][0] + nurses_years[nurse] <= (teams_recorded + 1) * 3:
                    return False

            if combination[nurse] == 'E':
                if team_years_total[days][1] + nurses_years[nurse] <= (teams_recorded + 1) * 3:
                    return False

            if combination[nurse] == 'N':
                if team_years_total[days][2] + nurses_years[nurse] <= (teams_recorded + 1) * 3:
                    return False

    return True


# 우선순위 계산용 함수
def check_priority(nurses, combination):
    points = 0  # 우선순위를 정할 점수, 높을 수록 바람직한 duty
    recommended_work_percent = 0.5

    for nurse_idx in range(len(nurses)):

        ### 각 간호사에 대하여 현재까지의 DAY, EVENING, NIGHT, OFF 일 수 계산 ###
        day_shifts = evening_shifts = night_shifts = offs = 0

        if combination[nurse_idx] == 'T':
            day_shifts += 1
        elif combination[nurse_idx] == 'E':
            evening_shifts += 1
        elif combination[nurse_idx] == 'N':
            night_shifts += 1
        else:
            offs += 1
    
        for day in nurses[nurse_idx][2:]:
            if day == 'T':
                day_shifts += 1
            elif day == 'E':
                evening_shifts += 1
            elif day == 'N':
                night_shifts += 1
            else:
                offs += 1
        
        # 근무 일수에 따른 점수 부여 (50% 근무보다 작아질수록 점수 차감)
        work_days = day_shifts + evening_shifts + night_shifts
        work_percent = work_days / (len(nurses[nurse_idx][2:]) + 1)
        points -= max(0, round(( (recommended_work_percent - work_percent)*100)**2 ))
        
        if nurses[nurse_idx][-1] == combination[nurse_idx]:
            # [권장] 세 개 근무 연속으로 오면 좋지 않음
            if nurses[nurse_idx][-2] == nurses[nurse_idx][-1]:
                points -= 50
            # [권장] 두 개 근무 연속으로 오면 좋음
            else:
                points += 25

        # DAY, EVENING, NIGHT중 어느 하나에 너무 치중되게 근무한 경우 점수 감소
        min_shifts = min(day_shifts, evening_shifts, night_shifts)  # DAY, EVENING, NIGHT 중 근무 수가 가장 적은 shift의 근무일수
        
        if day_shifts - min_shifts > 2 and combination[nurse_idx] == 'T':
                points -= 5 * (day_shifts - min_shifts) ** 2
        elif evening_shifts - min_shifts > 2 and combination[nurse_idx] == 'E':
                points -= 5 * (evening_shifts - min_shifts) ** 2
        elif night_shifts - min_shifts > 2 and combination[nurse_idx] == 'N':
                points -= 5 * (night_shifts - min_shifts) ** 2

    return points


# 특정 일자의 특정 듀티에 근무하는 간호사의 연차 기록하는 함수
# 한 팀의 듀티를 찾았을 때 호출되므로 함수 내에서 찾은 팀의 개수 갱신
def record_team_years(nurse_duties, nurses_years):
    global team_years_total, teams_recorded

    for date in range(len(nurse_duties[0])):
        for nurse_idx in range(len(nurse_duties)):
            if nurse_duties[nurse_idx][date] == 'T':
                team_years_total[date][0] += nurses_years[nurse_idx]
            elif nurse_duties[nurse_idx][date] == 'E':
                team_years_total[date][1] += nurses_years[nurse_idx]
            elif nurse_duties[nurse_idx][date] == 'N':
                team_years_total[date][2] += nurses_years[nurse_idx]

    teams_recorded += 1


# duty를 짜는 함수
def make_schedule(nurses, nurses_years, year, month, days=0):  # 인자는 duty를 짠 일 수
    global found_duty, team_years, result

    possible_combinations = []  # 가능한 근무 조합을 담을 리스트

    if found_duty:
        return

    if days == month_days[month]:
        found_duty = True
        for nurse_idx in range(6):
            result.append(nurses[nurse_idx][2:])
        record_team_years(result, nurses_years)
        # print(team_years_total)
        return

    # 모든 근무 조합 확인
    # combination은 DAY, EVENING, NIGHT의 배치를 담은 1차원 리스트
    # 예를 들어 ['T', 'E', 'N', 'O', 'O', 'O']는 1번 간호사가 DAY, 2번 간호사가 EVENING, 3번 간호사가 NIGHT근무임을 의미
    for combination in day_combinations:
        if check_validity(combination, days, nurses, nurses_years):  
            # check_priority 함수는 더 좋은 duty일수록 더 높은 값 반환
            # 최소 힙 사용을 위해 -1을 곱해줌 
            combination_priority = -1 * check_priority(nurses, combination)
            heapq.heappush(possible_combinations, (combination_priority, combination))

    for (priority, possible_combination) in possible_combinations:

        for idx in range(6):
            nurses[idx] += possible_combination[idx]
        
        make_schedule(nurses, nurses_years, year, month, days + 1)

        for idx in range(6):
            nurses[idx] = nurses[idx][:-1]


# 실제 값을 반환받기 위한 함수
def get_schedule(nurses, nurses_years, year, month):
    '''
    nurses: 각 간호사의 전 달 2일 duty가 저장된 1차원 리스트
    nurses_years: 각 간호사의 연차가 저장된 1차원 리스트
    year: 연도 (int)
    month: 월 (int)
    return: 각 간호사의 duty가 저장된 2차원 리스트
    '''
    global found_duty, result

    # 윤년 처리 및 탐색을 위한 초기 작업
    if (month == 2) and (((year % 4 == 0) and (year % 100 != 0)) or year % 400 == 0):
        month_days[2] = 29
    found_duty = False
    result = []

    make_day_combinations()
    make_schedule(nurses, nurses_years, year, month)

    if len(result) != 0:
        return result
    else:
        return "유효한 DUTY를 찾지 못했습니다. 팀을 다시 배정해주세요"


# 월에 따라 며칠의 duty를 짜야하는지 확인
month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

### 각 일자에 가능한 duty 조합 (make_day_combinations() 함수가 호출되며 생성됨) ###
day_combinations = []

result = []

# 팀 연차 관련 변수
teams_recorded = 0  # 듀티를 짠 팀의 수 (0~3)
team_years_total = [[0, 0, 0] for _ in range(32)]  # 특정 일자의 특정 듀티에 근무하는 세 간호사의 연차의 합
