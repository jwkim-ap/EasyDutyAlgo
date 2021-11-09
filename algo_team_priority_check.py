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
            # 세 개 근무 연속으로 오면 좋지 않음
            if nurses[nurse_idx][-2] == nurses[nurse_idx][-1]:
                points -= 100
            # 두 개 근무 연속으로 오면 좋음
            else:
                points += 10

        # DAY, EVENING, NIGHT중 어느 하나에 너무 치중되게 근무한 경우 점수 감소
        min_shifts = min(day_shifts, evening_shifts, night_shifts)  # DAY, EVENING, NIGHT 중 근무 수가 가장 적은 shift의 근무일수
        
        if day_shifts - min_shifts > 2 and combination[nurse_idx] == 'T':
                points -= 5 * (day_shifts - min_shifts) ** 2
        elif evening_shifts - min_shifts > 2 and combination[nurse_idx] == 'E':
                points -= 5 * (evening_shifts - min_shifts) ** 2
        elif night_shifts - min_shifts > 2 and combination[nurse_idx] == 'N':
                points -= 5 * (night_shifts - min_shifts) ** 2

    return points
