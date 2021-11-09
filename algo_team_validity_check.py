from algo_team_day_first import nurses

def check_validity(combination, days):
    # 각 간호사에 대하여 유효성 검사
    for nurse in range(6):
        # [필수] N - O - D 는 설 수 없음
        if nurses[nurse][days] == 'N' and nurses[nurse][days+1] == 'O' and combination[nurse] == 'T':
            return False

        # [필수] N - D, N - E 는 설 수 없음
        if nurses[nurse][days+1] == 'N' and (combination[nurse] == 'T' or combination[nurse] == 'E'):
            return False
    
        # [필수] E - D 는 설 수 없음
        if nurses[nurse][days+1] == 'E' and (combination[nurse] == 'T'):
            return False

        # [필수] 너무 연속으로 근무하게 됨
        if 'O' not in nurses[nurse][-5:] and (combination[nurse] != 'O'):
            return False

        # [권장] 세 개의 근무가 연속으로 오면 안 좋음
        if nurses[nurse][days] == nurses[nurse][days+1] == combination[nurse]:
            return False

        # [권장] 한 달에 N은 9개 미만
        if nurses[nurse].count('N') == 8 and combination[nurse] == 'N':
            return False

    return True