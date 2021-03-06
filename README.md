# EasyDuty Algorithm

## 🤯 Brainstorm 단계

> 1명의 duty를 효과적으로 얻어내는 방법을 구상하는 단계

`algo.py` : 최근 2일의 duty가 주어지면 다음 1주간 duty로 가능한 경우의 수를 출력 (극초반 아이디어)

`algo2.py` : 최근 2일의 duty가 주어지면 다음 한 달간 duty로 가능한 경우의 수를 출력

- 어느 정도 가지치기를 해 경우의 수가 많이 출력되지 않으나 가지치기가 적합하지 않은 부분이 많음

`algo3.py` : 최근 2일의 duty가 주어지면 다음 한 달간 duty로 가능한 경우의 수를 일부 출력 (현재 방향성)

- duty를 하루하루 짜면서, 각 시점에서 조건에 부합하는 정도를 수치화. 부합하는 정도가 높을수록 다음 날의 shift를 정하는 우선순위를 높게 두어 시간을 단축하였음
- 단 우선순위의 1차적 기준은 **현재까지 duty를 짠 날짜 수**이므로 조건에 부합하는 순서대로 경우의 수가 출력되는 것은 아님

### 해결할 문제

- **추가적인 조건과 현실적인 duty 가지치기로 경우의 수 줄이기**
- 듀티 조건을 다시 차근히 확인해 가지치기의 정확성 확보
- duty를 짜는 우선순위를 확실히 하여 알고리즘 수행 시간 단축
- DFS 특성상 가능한 경우의 수의 일부만 출력했을 때 duty가 지나치게 유사해지는 문제 해결

------

## 📓 Update: 10/19

> ```
> algo3.py` -> `algo4.py
> ```

- 듀티를 짜는 함수 `get_final_duty()`와 듀티의 우선 순위를 구하는 함수 `get_priority()`의 큰 틀은 유지
- 전날, 전전날 NIGHT가 오는 경우 가지치기 개선
- 요일에 관계 없이 듀티 전체의 OFF 일수가 해당 월의 휴일 수에 가까울수록 우선순위 높아지도록 수정
  - 요일을 신경쓰지 않고 이를 구현하는게 어려웠는데, **현재 듀티의 OFF 비중과 월 전체의 필요 OFF 비중을 비교하자**는 아주 좋은 아이디어를 적용
- 조건에 부합하는 정도를 계산해 **우선순위가 높은 duty부터 출력**하는데 성공
- 첫 2일 듀티에 따라 출력되는 듀티가 달라짐을 확인, 해당 월의 휴일 수만큼 쉬면서 DAY, EVENING, NIGHT의분배가 적절히 되었음을 확인

### 해결할 문제

- 1일차에 `DAY`가 나오지 않는 문제 발생 (알고리즘 내부 구조상의 문제?)
- 출력되는 듀티가 여전히 유사
  - 단, 이는 조건에 가장 부합한 듀티가 한정적이라는 의미일 수도 있음

## 📓 Update: 10/31

> algo4.py update at branch brainstorm

- `get_final_duty()`함수를 6번 반복 실행해 한 팀에 해당하는 6명의 간호사의 듀티를 짜는 구조 완성

- 전달 마지막 2일의 duty를 입력 받는 부분 (line 99)을 6명 단위로 받도록 수정

  ```
  prev_month_duties = list(input('첫 2일의 duty를 입력하세요: ').split())
  ```

  예: `TE TO OO OO OT OE`

- 한 팀에서 DAY 1명, EVENING 1명, NIGHT 1명이 배치되도록 `team_shifts` 배열 추가

  - `team_shifts` 배열의 길이는 해당 월의 일수와 같음
  - `team_shifts[n]`은 해당 월 `n+1`일의 간호사 배치 현황에 대한 정보를 담고 있음
    - 0: 배치된 간호사가 없음
    - 1: NIGHT만 배치됨 (0b001)
    - 2: EVENING만 배치됨 (0b010)
    - 3: NIGHT, EVENING이 배치됨 (0b011)
    - 4: DAY만 배치됨 (0b100)
    - 5: DAY, NIGHT가 배치됨 (0b101)
    - 6: DAY, EVENING이 배치됨 (0b110)
    - 7: 모두 배치됨 (이후 모든 간호사는 해당 일자에 OFF) (0b111)

### 해결할 문제

- 현재는 각 간호사에 대하여 우선순위가 가장 높은 duty 한 가지를 그 간호사의 duty로 확정짓고 있음

  따라서 4~5번째 간호사에서 duty를 더 이상 찾을 수 없어 에러가 발생하는 경우가 있음

### 출력 예시

[![1031_01](https://github.com/EasyDuty/Algo/raw/master/README.assets/1031_01.png)](https://github.com/EasyDuty/Algo/blob/master/README.assets/1031_01.png)

## 📓 Update: 11/5

각 간호사의 duty를 짤 때, 매 번 우선순위 값을 계산하는 구조에서 (필수 사항 가지치기 + 권장 사항에 따른 DAY, EVENING, NIGHT, OFF 우선순위 변경)의 단순 DFS 구조로 바꿔보았으나 (`algo_team_test2.py`) 여전히 duty를 못 찾는 경우가 많았고, 찾더라도 DFS 구조상 근무가 앞의 간호사에게 몰리는 현상이 발생하였다.

따라서 알고리즘의 방향을 다음과 같은 방향으로 수정하자고 논의하였다.

- 1일부터 한 팀에 DAY, EVENING, NIGHT를 배치할 수 있는 경우의 수를 확인한다.

  (이 때 최대로 가능한 경우의 수는 6 * 5 * 4 = 120가지이며, 각 간호사별로 설 수 없는 DUTY가 있으므로 실제 경우의 수는 더 적게 될 것이다.)

- DAY, EVENING, NIGHT를 배치할 수 있는 경우의 수 별로 우선순위를 산출한다.

  (각 간호사의 지난 duty에 따라 해당 일 duty의 적합성을 판단하여 값을 계산한다. 이 때 사용되는 조건은 필수 조건이 아닌 권장 조건이다 (필수조건은 가지치기가 되기 때문). 다음으로 모든 간호사로부터 산출된 값의 합을 이용해 해당 배치의 우선순위를 판단한다.) 우선순위가 높을수록 (힙을 사용할 경우 산출한 값이 낮을수록) 다음 날 duty를 먼저 탐색하도록 한다.

- 해당 월의 모든 날에 대해 duty가 완성되면 탐색을 종료한다.

- 각 일별 근무 현황을 객체로 만들어 길이 N인 리스트에 저장한다 (N은 해당 월의 일 수)

  - 가령 10월 1일에는 1번 간호사가 DAY, 4번 간호사가 EVENING, 6번 간호사가 NIGHT 근무를 할 경우

    ```
    {D: 1, E: 4, N: 6}
    ```

    위와 같은 딕셔너리 객체가 근무 현황을 담은 리스트의 1번 (혹은 0번) 인덱스에 저장된다.

- (추후 고려사항) duty가 완성된 팀이 있을 때 배치된 간호사의 연차를 고려하여 DAY, EVENING, NIGHT 각각 근무하는 3명의 간호사가 모두 저연차 간호사인 경우를 가지치기한다. (반대로 고연차가 특정 일자의 특정 shift에 몰리는 경우를 가지치기 할 수도 있다.)

## 📓 Update: 11/6

------

> `algo_team_day_first.py`, `algo_team_priority_check.py`, `algo_team_validity_check.py` update at branch brainstorm

- 상술한 방식으로 duty를 짜는 코드 전체적으로 완성!

- 6명의 간호사에 대해서 ``DAY, EVENING, NIGHT, OFF, OFF, OFF`부터`OFF, OFF, OFF, NIGHT, EVENING, DAY`의 총 120가지 배치를 각 일별로 확인

- 유효성 검사 (가지치기) 후 남는 (6명 모두 duty 조건에 위배되지 않는) 배치만 힙에 추가

  > 힙을 사용한 이유는 각 배치에 우선순위를 부여하고, 우선순위가 높은 배치부터 다음 날 탐색을 이어가도록 하기 위함이다. 우선순위는 `algo_team_priority_check.py`모듈의 `check_priority()` 함수로 산출하며, 고려사항은 크게 세 가지이다.
  >
  > 1. 근무 일수가 너무 적은 간호사가 있으면 우선순위 점수가 차감된다. (line 30~32)
  > 2. 두 개 근무가 연속으로 오면 우선순위 점수가 더해지지만, 세 개 근무가 연속으로 오면 우선순위 점수가 차감된다. (line 34~40)
  > 3. 특정 간호사가 DAY, EVENING, NIGHT 중 한 근무에 지나치게 치중되게 근무했는데, 해당 근무를 또 추가하려고 하면 우선순위 점수가 차감된다. 차감은 가장 많이 한 근무와 가장 적게 한 근무의 일수 차가 3 이상일 때부터 이루어지며, 차이가 클 수록 기하급수적으로 차감되는 점수가 커지기 때문에 한 간호사가 한 달 내내 DAY 근무를 한다던가, EVENING 근무를 하는 경우 등을 방지할 수 있다.

- 유효한 배치를 힙에서 하나씩 꺼낸 뒤, 해당 배치를 이용하여 각 간호사의 근무 일정이 담긴 리스트 `(nurses[0] ~ nurses[5])`를 갱신한다. 이후 `make_schedule()` 함수를 재귀적으로 호출해 다음 날의 배치를 정한다.

- 해당 월의 duty가 모두 정해지면 각 간호사의 근무 일정을 출력하고, 50가지의 duty가 정해지면 프로그램이 종료된다.

### 추후 고려 사항

- **각 일별 근무 현황 객체로 만들어 저장하기**
- 현재는 각 날짜의 근무 배치 유효성 검사를 `algo_team_day_first.py`에서 모두 하고 있음. 이를 모듈화 할 수도 있을 것이라 생각함 (현재 이 부분을 모듈로 만들어 놓은 `algo_team_validity_check.py`는 활용되고 있지 않음). 단, 현재 코드 구조상 유효성 검사를 수행하는 모듈은 `algo_team_day_first.py` 자체를 import할 필요가 있어 `circular import`문제가 발생함. 알고리즘 관련 파일을 하나의 패키지로 만들고 `__init__.py`에 적당한 코드를 작성하면 해결할 수 있을 것이라 생각함.
- 3팀의 duty를 짤 때 이 구조를 유지하면 간호사의 GRADE (연차)도 고려할 것
- 2월 duty를 짤 때 윤년 고려
- 더 균형잡힌 duty 출력을 위해 우선순위 알고리즘 (`algo_team_priority_check.py`)의 수치 미세 조정

## 📓 Update: 11/7

------

> team duty ver 2.1 at branch master

- `get_schedule()` 함수 추가: 6명의 간호사의 duty를 2차원 리스트로 반환

- 윤년 고려 추가

- 유효성 검사 모듈화

- 알고리즘 수치 미세 조정

  

> team duty ver 2.2 at branch master

- 사용자 입력 없이 `get_schedule()` 함수 하나 + 전달받은 인자로 간호사의 duty를 반환받을 수 있도록 함

  (`algo_team_validity_check.py`, `algo_team_priority_check.py` 모듈을 `algo_team_day_first.py`로 통합)

- `get_schedule()` 함수의 첫 번째 인자 및 반환값 1차원 리스트로 변경 (각 간호사의 duty를 리스트에서 문자열로 변경)

- 알고리즘 수치 미세 조정

  - 3연속 동일 근무를 가지치기 조건에서 우선순위 저하 조건으로 완화
  - 2연속 동일 근무 우선순위 가중치 상향

- 세 조정



> team duty ver3.0 beta at branch brainstorm

- 18명의 간호사의 duty 및 연차가 주어질 때 **연차까지 고려하여** 듀티를 짜는 함수 `get_schedule()` 구현
- `get_schedule()` 함수에 인자 추가(팀별 연차 `nurses_years`)
  - `nurses_years`는 한 팀의 간호사 6명의 연차 정보를 담은 1차원 리스트임 (예: `[3, 7, 2, 4, 9, 11]`)
  - 알고리즘상 1~3년은 저연차, 4년 이상은 고연차로 분류하며, 특정 일자의 특정 shift (DAY, EVENING, NIGHT)에 근무하는 세 간호사 중 적어도 한 명은 고연차가 배정되도록 함. 적절한 배치를 찾지 못하면 오류 메시지를 반환함
- get_schedule은 한 팀의 duty를 반환하는 함수이므로 총 3회 호출될 필요가 있음
- 연차를 **우선순위 조건이 아닌 유효성 검사 조건으로 두고 있으므로 duty를 찾기 까다로운 면이 있음**

