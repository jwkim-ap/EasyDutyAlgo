# Nurse_Duty_Algo

import heapq
import sys
sys.setrecursionlimit(10 ** 6)


def what_is_my_duty(now_duty, now_days_left, my_idx):
    # 듀티풀
    duty_pool = ['N', 'E', 'T', 'O']

    ### 내 팀과 비교 ###

    # [필수] 겹치는 근무 제외
    day_nurse_count = 0
    for my_team_today in range(2, -1, -1):
        if team_shifts[month_days[month] - now_days_left] & (1 << my_team_today):
            duty_pool.pop(my_team_today)
            day_nurse_count += 1

            # [필수] 이미 꽉 차게 일함
            if day_nurse_count >= 3:
                return ['O'] # 확정


    # [필수] 남은 팀원 수 + 그날 일하고 있는 팀원 수가 딱 3이면 난 OFF를 못 섬
    if (nurse_members - my_idx) + day_nurse_count == 3:
        duty_pool.remove('O')

    # [필수] 남은 팀원 수 + 그날 일하고 있는 팀원 수가 3보다 작으면 가망 없음
    if (nurse_members - my_idx) + day_nurse_count < 3:
        return  # 확정

    ### 내 전 근무와 비교 ###

    # [필수] N - O - D 는 설 수 없음
    if now_duty[-2] == 'N' and now_duty[-1] == 'O' and 'T' in duty_pool:
        duty_pool.remove('T')
        
    # [필수] N - D, N - E 는 설 수 없음
    if now_duty[-1] == 'N':
        if 'E' in duty_pool:
            duty_pool.remove('E')
        if 'T' in duty_pool:
            duty_pool.remove('T')

    # [필수] E - D 는 설 수 없음
    if now_duty[-1] == 'E' and 'T' in duty_pool:
        duty_pool.remove('T')

    # [필수] 너무 연속으로 근무했음
    if len(now_duty) >= 5 and 'O' not in now_duty[-5:]:
        return ['O']

    # [권장] 첫 번째 근무가 같으면 비슷한 패턴일 것이므로 뒤로
    if all_made_duties[my_idx] and all_made_duties[my_idx][-1][0] in duty_pool:
        duty_pool.remove(all_made_duties[my_idx][-1][0])
        duty_pool.append(all_made_duties[my_idx][-1][0])

    # [권장] 두 개의 근무가 연속으로 오는 것이 좋음
    if now_duty[-1] in duty_pool:
        duty_pool.remove(now_duty[-1])
        duty_pool = [now_duty[-1]] + duty_pool

    # [권장] 세 개의 근무가 연속으로 오면 안 좋음
    if now_duty[-1] == now_duty[-2] and now_duty[-1] in duty_pool:
        duty_pool.remove(now_duty[-1])
        duty_pool.append(now_duty[-1])
        # print(now_duty)
        # return 임시로 제외

    # [권장] 한 달에 N은 9개 미만
    if 'N' in duty_pool and now_duty[2:].count('N') == 8:
        duty_pool.remove('N')
        duty_pool.append('N')

    new_duty_pool = []
    for duty in duty_pool:
        new_duty_pool.append((duty, now_duty[2:].count(duty)))

    new_duty_pool.sort(key=lambda x: x[1])

    ##### 듀티 확정 #####
    # print('i will return it', duty_pool)
    return new_duty_pool


def update_scheduler(now_duty, flag=0):
    for idx, day in enumerate(now_duty[2:]):
        # 저장
        if not flag:
            if day == 'T':
                team_shifts[idx] += 4
            elif day == 'E':
                team_shifts[idx] += 2
            elif day == 'N':
                team_shifts[idx] += 1
        # 복원
        else:
            if day == 'T':
                team_shifts[idx] -= 4
            elif day == 'E':
                team_shifts[idx] -= 2
            elif day == 'N':
                team_shifts[idx] -= 1


def make_my_duty(now_duty, left_cnt, my_idx):
    ### 내 듀티 다 만들었음 ###
    if left_cnt == 0:
        # print(now_duty)
        save_my_duty(now_duty, my_idx)
        return now_duty

    ### 듀티 만들고 있음 ###
    my_duty_pool = what_is_my_duty(now_duty, left_cnt, my_idx)
    if my_duty_pool:
        for my_duty in my_duty_pool:
            make_my_duty(now_duty + my_duty[0], left_cnt-1, my_idx)
    return
    

def save_my_duty(my_duty, my_idx):
    # [권장] 첫 번째 근무가 같으면 비슷한 패턴일 것이므로 제외
    if all_made_duties[my_idx] and my_duty[2] == all_made_duties[my_idx][-1][0]:
        return
    # 듀티 기록 저장
    team_duties.append(my_duty[2:])
    all_made_duties[my_idx].append(my_duty[2:])
    # final_duties.append(now_duty[2:])
    update_scheduler(my_duty)
    ### 다음 간호사 ###
    get_final_duty(days_left, my_idx + 1)
    # 듀티 기록 복원
    team_duties.pop(-1)
    update_scheduler(my_duty, 1)


def get_final_duty(left_cnt, nurse_idx=0):    
    ######## 종료 조건 #########
    if nurse_idx == nurse_members:
        print('finished', team_duties)
        print(team_shifts)
        return

    ############# 듀티 만드는 중 ###########
    now_duty = make_my_duty(prev_month_duties[nurse_idx], left_cnt, nurse_idx)
    if now_duty:

        # [권장] 첫 번째 근무가 같으면 비슷한 패턴일 것이므로 제외
        if all_made_duties[nurse_idx] and now_duty[2] == all_made_duties[nurse_idx][-1][0]:
            return
        # 듀티 기록 저장
        print('aaaaaaaaaaaa', team_duties)
        team_duties.append(now_duty[2:])
        all_made_duties[nurse_idx].append(now_duty[2:])
        # final_duties.append(now_duty[2:])
        update_scheduler(now_duty)
        ### 다음 간호사 ###
        get_final_duty(nurse_idx + 1)
        # 듀티 기록 복원
        team_duties.pop(-1)
        update_scheduler(now_duty, 1)

        

year, month = map(int, input('작성할 연도와 월을 입력하세요: ').split())

# 월에 따라 며칠의 duty를 짜야하는지 확인
month_days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

days_left = month_days[month]  # duty를 짤 남은 일수를 해당 월의 일수로 초기화
team_shifts = [0] * days_left  # 한 팀의 일별 간호사 배치 현황, 예를 들어 team_shifts[0]은 1일의 배치 현황
nurse_members = 6
all_made_duties = [[] for _ in range(nurse_members)]

prev_month_duties = list(input('첫 2일의 duty를 입력하세요: ').split())  # 각 간호사의 전달 마지막 2일의 DUTY를 띄어쓰기를 포함하여 입력받음

team_duties = []  # 모든 간호사 duty 저장할 리스트

get_final_duty(days_left)  # 한 간호사의 duty 찾기

# print("Nurse #{}: {}".format(nurse+1, team_duties[nurse][1]))
# print("{} up to nurse #{}".format(team_shifts, nurse+1))
