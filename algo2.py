# Nurse_Duty_Algo

def get_final_duty(pre_duty, final_duty, day, day_of_week):
    '''
    전 2일 duty 정보가 주어지면 다음 30일의 duty로 가능한 모든 경우의 수를 저장합니다.
    pre_duty: 전 2일 duty정보 (list)
    final_duty: 찾고자 하는 duty 정보 (str)
    day: 현재 정해진 일수 (int)
    day_of_week: 요일 정보 (int, 0~6)
    '''
    global possible_duty, sols

    if day == 30:
        possible_duty.append(final_duty)
        sols += 1
        return

    if sols > 10000:
        return

    if sols > 0:
        if final_duty.count('N') >= 8:
            return
    elif final_duty.count('N') >= 9:
        return

    most_duty = max(final_duty.count('D'), final_duty.count('E'), final_duty.count('N'))
    least_duty = min(final_duty.count('D'), final_duty.count('E'), final_duty.count('N'))
    if most_duty - least_duty > 1:
        return

    if final_duty.count('O') > 12:
        return

    for duty in ['D', 'E', 'N', 'O']:
        if day_of_week == 5 and final_duty[-day_of_week:].count('O') < 1\
            or day_of_week == 6 and final_duty[-day_of_week:].count('O') < 2:
            continue
        if pre_duty[1] == 'D' and duty == 'D':
            continue
        if pre_duty[1] == 'E' and (duty == 'D' or duty == 'E'):
            continue
        if pre_duty[1] == 'N' and duty != 'O':
            continue
        if pre_duty[0] == 'N' and pre_duty[1] == 'O' and duty == 'D':
            continue

        pre_duty[0] = pre_duty[1]
        pre_duty[1] = duty
            
        get_final_duty(pre_duty, final_duty + duty, day + 1, (day_of_week + 1) % 7)


possible_duty = []

test = list(input('첫 2일의 duty를 입력하세요: '))

sols = 0
get_final_duty(test, '', 0, 0)

for i, duty in enumerate(possible_duty):
    print("#{} {}".format(i+1, duty))
