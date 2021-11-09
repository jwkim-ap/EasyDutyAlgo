# Nurse_Duty_Algo

import heapq


def get_priority(duty):
    '''
    duty가 주어지면, 해당 duty가 다음 날 shift 탐색을 위해 힙에 더해질 때의 우선순위를 계산
    우선순위는 조건 적합성을 수치화한 것으로, 낮을수록 조건에 부합하는 (우선순위가 높은) duty임을 의미함
    '''
    d = duty[2:].count("T")
    e = duty[2:].count("E")
    n = duty[2:].count("N")

    max_shift = max(d, e, n)
    rest_percent = (len(duty[2:]) - sum([d, e, n])) / len(duty[2:]) 
    
    # DAY, EVENING, NIGHT 근무 수의 편차가 클수록 우선순위가 낮아짐
    # 누적 OFF가 0에서 떨어질수록 우선순위가 낮아짐
    if duty[2:].count("N") == 8:  # NIGHT 근무 8일으로 RECOVERY OFF 필요
        # NIGHT 근무가 8일인 경우 우선순위가 비교적 낮아짐 (+20)
        priority = ((3 * max_shift) - (d + e + n) + abs(rest_percent - off_percent) * 100 + 20)
    else:
        priority = ((3 * max_shift) - (d + e + n) + abs(rest_percent - off_percent) * 100)

    return priority


def get_final_duty(nurse_idx=0, final_duties=[]):
    if nurse_idx == 5:
        print(team_duties)
        return

    queue = []  # duty 찾기 위한 우선순위 큐
    # final_duties = []  # 최종으로 가능한 duty 저장

    heapq.heappush(queue, (0, days_left, prev_month_duties[nurse_idx]))

    while queue:
        now = heapq.heappop(queue)
        now_priority, now_days_left, now_duty = now[0], now[1], now[2]  # 현재까지 짠 duty

        # 조건을 만족하는 duty 찾음
        if now_days_left == 0:
            team_duties.append(now_duty[2:])
            final_duties.append(now_duty[2:])

            # 일단 한 명의 간호사의 duty를 찾았을 때 team_shift에 기록
            for idx, day in enumerate(now_duty[2:]):
                if day == 'T':
                    team_shifts[idx] += 4
                elif day == 'E':
                    team_shifts[idx] += 2
                elif day == 'N':
                    team_shifts[idx] += 1

            get_final_duty(nurse_idx + 1)
            
            # 백트래킹시 복원
            team_duties.pop()
            for idx, day in enumerate(now_duty[2:]):
                if day == 'T':
                    team_shifts[idx] -= 4
                elif day == 'E':
                    team_shifts[idx] -= 2
                elif day == 'N':
                    team_shifts[idx] -= 1

            continue
                 
        # 조건을 만족하는 duty 충분히 찾음
        if len(final_duties) >= 10000:
            # print(nurse_idx, team_duties)
            return

        # 월 NIGHT 횟수에 따른 가지치기
        if now_duty[2:].count("N") >= 9:
            continue

        for next_shift in ['T', 'E', 'N', 'O']:
            # 전일 근무에 따른 가지치기
            # if now_duty[-2] == now_duty[-1] == next_shift:
            #     continue
            if now_duty[-1] == 'E' and next_shift == 'T':
                continue
            
            if now_duty[-1] == 'N':  # 전날이 NIGHT
                if now_duty[-2] == 'N':  # 전전날도 NIGHT
                    if next_shift != 'O':  # 다음은 무조건 OFF
                        continue
                else:
                    if next_shift != 'N':
                        continue
            
            day_nurse_count = 0  # 해당 일에 배정된 간호사 수
            for idx in range(3):
                if team_shifts[month_days[month] - now_days_left] & (1 << idx):
                    day_nurse_count += 1

            if team_shifts[month_days[month] - now_days_left] & (1 << 2) and next_shift == 'T':
                continue 
            if team_shifts[month_days[month] - now_days_left] & (1 << 1) and next_shift == 'E':
                continue 
            if team_shifts[month_days[month] - now_days_left] & (1 << 0) and next_shift == 'N':
                continue

            if (5 - nurse_idx) + day_nurse_count <= 3 and next_shift == 'O':
                continue
            
            if 'O' not in now_duty[-5:] and next_shift != 'O':
                continue

            if now_duty[-2] == 'N' and now_duty[-1] == 'O' and next_shift == 'T':
                continue

            combined_duty = now_duty + next_shift  # 다음날 shift를 추가한 새 duty

            next_priority = get_priority(combined_duty)  # 전체 duty의 우선순위 (조건 적합성) 계산

            heapq.heappush(queue, (next_priority, now_days_left - 1, combined_duty))


year, month = map(int, input('작성할 연도와 월을 입력하세요: ').split())

# 월에 따라 며칠의 duty를 짜야하는지 확인
month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

days_left = month_days[month]  # duty를 짤 남은 일수를 해당 월의 일수로 초기화
team_shifts = [0] * days_left  # 한 팀의 일별 간호사 배치 현황, 예를 들어 team_shifts[0]은 1일의 배치 현황
off_percent = (days_left - ((days_left * 3)/6))/days_left

prev_month_duties = list(input('첫 2일의 duty를 입력하세요: ').split())  # 각 간호사의 전달 마지막 2일의 DUTY를 띄어쓰기를 포함하여 입력받음

team_duties = []  # 모든 간호사 duty 저장할 리스트

get_final_duty()  # 한 간호사의 duty 찾기

# print("Nurse #{}: {}".format(nurse+1, team_duties[nurse][1]))
# print("{} up to nurse #{}".format(team_shifts, nurse+1))
