# Nurse_Duty_Algo

import heapq
from datetime import datetime

def get_priority(duty):
    '''
    duty가 주어지면, 해당 duty가 다음 날 shift 탐색을 위해 힙에 더해질 때의 우선순위를 계산
    우선순위는 조건 적합성을 수치화한 것으로, 낮을수록 조건에 부합하는 (우선순위가 높은) duty임을 의미함
    '''
    total_off = 0  # 누적 OFF 기록
    d, e, n = (0, 0, 0)  # day, evening, night 근무 수 초기화
    weekday_idx = initial_weekday  # 확인하는 날짜의 요일 (토: 5, 일: 6)

    for shift in duty[2:]:  # 현재까지 짠 해당 월의 duty에 대해
        if (weekday_idx == 5 or weekday_idx == 6) and shift != "O":
            total_off += 1  # 주말 근무의 경우 누적 OFF +1
        if (0 <= weekday_idx <= 4) and shift == "O":
            total_off -= 1  # 평일 OFF의 경우 누적 OFF -1
        if shift == 'D':
            d += 1
        elif shift == "E":
            e += 1
        elif shift == "N":
            n += 1
        weekday_idx = (weekday_idx + 1) % 7

    max_shift = max(d, e, n)
    
    # DAY, EVENING, NIGHT 근무 수의 편차가 클수록 우선순위가 낮아짐
    # 누적 OFF가 0에서 떨어질수록 우선순위가 낮아짐
    if duty.count("N") == 8:  # NIGHT 근무 8일으로 RECOVERY OFF 필요
        # NIGHT 근무가 8일인 경우 우선순위가 비교적 낮아짐 (+20)
        priority = ((3 * max_shift) - (d + e + n) + (5 * abs(total_off + 1)) + 20)
    else:
        priority = ((3 * max_shift) - (d + e + n) + (5 * abs(total_off)))

    return priority


def get_final_duty():
    while queue:
        now = heapq.heappop(queue)
        now_days_left, now_priority, now_duty = now[0], now[1], now[2]  # 현재까지 짠 duty
        now_day_of_week = (initial_weekday + len(now_duty) - 2) % 7  # 마지막으로 짠 날의 요일

        if now_days_left < 15 and now_duty.count('D') < 4:
            continue
        
        # 조건을 만족하는 duty 충분히 찾음
        if len(final_duties) >= 1000:
            return

        # 조건을 만족하는 duty 찾음
        if now_days_left == 0:
            heapq.heappush(final_duties, (now_priority, now_duty[2:]))
            continue

        # 주간 OFF 횟수에 따른 가지치기
        # if len(now_duty) >= 7:
        #     if now_day_of_week == 5 and now_duty[-now_day_of_week:].count('O') < 1\
        #     or now_day_of_week == 6 and now_duty[-now_day_of_week:].count('O') < 2:
        #         continue

        # 월 NIGHT 횟수에 따른 가지치기
        if len(now_duty) >= 11:
            if now_duty[2:].count("N") >= 9:
                continue

        for next_shift in ['D', 'E', 'N', 'O']:
            # 전일 근무에 따른 가지치기
            if now_duty[-2] == now_duty[-1] == next_shift:
                continue
            if now_duty[-1] == 'E' and next_shift == 'D':
                continue
            if now_duty[-1] == 'N' and next_shift != 'O':
                continue
            if now_duty[-2] == 'N' and now_duty[-1] == 'O' and next_shift == 'D':
                continue

            combined_duty = now_duty + next_shift  # 다음날 shift를 추가한 새 duty

            next_priority = get_priority(combined_duty)  # 전체 duty의 우선순위 (조건 적합성) 계산

            heapq.heappush(queue, (now_days_left - 1, next_priority, combined_duty))


prev_month_duty = input('첫 2일의 duty를 입력하세요: ')
year, month = map(int, input('작성할 연도와 월을 입력하세요: ').split())

queue = []  # duty 찾기 위한 우선순위 큐
best = dict()  # 각 듀티 순서 중 가장 좋은 경우 저장
final_duties = []  # 최종으로 가능한 duty 저장
initial_weekday = datetime(year, month, 1).weekday()  # 해당 월의 1일의 요일 반환 (월:0 ~ 일:6)

# 월에 따라 며칠의 duty를 짜야하는지 확인
thirty_one = [1, 3, 5, 7, 8, 10, 12]
thirty = [4, 6, 9, 11]

if month in thirty_one:
    days_left = 31
elif month in thirty:
    days_left = 30
else:
    days_left = 28

heapq.heappush(queue, (days_left, 0, prev_month_duty))
get_final_duty()

for i, duty in enumerate(final_duties):
    day = duty[1].count('D')
    evening = duty[1].count('E')
    night = duty[1].count('N')
    print("#{} {} day: {} / evening: {} / night: {}".format(i+1, duty, day, evening, night))
