# Nurse_Duty_Algo

def seven_days(pre_duty, week_duty, day):
    '''
    전 2일 duty 정보가 주어지면 다음 7일의 duty로 가능한 모든 경우의 수를 저장합니다.
    pre_duty: 전 2일 duty정보 (list)
    week_duty: 찾고자 하는 7일 duty 정보 (str)
    day: 현재 정해진 일수 (int)
    '''
    global possible_week

    if day == 7:
        if max(week_duty.count('D'), week_duty.count('E'), week_duty.count('N')) >= 3:
            return
        else:
            possible_week.append(week_duty)
            return
    else:

        for duty in ['D', 'E', 'N', 'O']:
            # 5일 근무시 off
            if ((week_duty.count('O') < 1 and day == 5)\
                or (week_duty.count('O') < 2 and day == 6))\
                and duty != 'O':
                continue  

            if pre_duty[1] == 'N' and (duty == 'D' or duty == 'E'):
                continue
            if pre_duty[1] == 'E' and duty == 'D':
                continue
            if pre_duty[0] == 'N' and pre_duty[1] == 'O' and duty == 'D':
                continue

            temp = pre_duty
            pre_duty[0] = pre_duty[1]
            pre_duty[1] = duty
            week_duty += duty

            seven_days(pre_duty, week_duty, day + 1)
            
            week_duty = week_duty[:-1]
            pre_duty = temp

possible_week = []

test = list(input('첫 2일의 duty를 입력하세요: '))

seven_days(test, '', 0)

for i, duty in enumerate(possible_week):
    print("#{} {}".format(i, duty))
