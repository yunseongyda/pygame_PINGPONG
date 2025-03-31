# pygame_PINGPONG
파이게임 수행평가 핑퐁게임

## 참고
- 필요에 따라 파일을 나뉘어도 됨 (예: client.py와 server.py)
- import os \n os.chdir(os.path.dirname(os.path.abspath(__file__))) <- 이거 꼭 필요함

## 기획

### 개요
- AI 기능 필요
- 서버 : 멀티플레이
- 1:1과 2:2가 있음
- PvP를 선택하면 1:1 듀얼, 2:2 팀전을 할 수 있음 (팀전에서 플레이어는 각 팀에 배치되고, AI가 팀원으로 들어가서 2:2 진행)
- PvE를 선택하면 1:1 듀얼, 2:2 팀전을 할 수 있음 (1:1 듀얼에서는 플레이어와 AI가 플레이함, 2:2 팀전은 플레이어가 같은 팀에 있고 상대팀에 AI가 2개 배치됨)
- 시작하기 전에 몇점 내기 할 건지와, 듀스 여부를 정함 
- 공의 속도가 플레이어의 속도보다 느려야 함(공을 계속 따라가게 되면 게임이 너무 쉬워짐)
- - 따라서 AI는 공을 치기 전에 가운데에 있다가 공의 방향에 맞춰서 미리 움직여야 함
- 공이 상대 진영 뒤로 넘어가면 점수를 얻음

### 메인화면
- PvP와 PvE 선택
- PvP를 선택하면 1:1 듀얼과 2:2 팀전을 선택할 수 있음
- PvE를 선택해도 1:1 듀얼과 2:2 팀전을 선택할 수 있음
- 게임 플레이 도중 ESC 누르면 메인 화면으로 돌아옴

### 멀티플레이
- PvP를 선택하면 다른 플레이어가 서버에 접속할 때 까지 기다림
- 화면에 서버에 접속한 IP 목록이 뜸
- 서버에 접속하면 플레이 화면에 IP가 나오면서 "2명 접속중"(영어로) 라고 뜸
- 모두 준비가 완료되면 시작됨
- 플레이어들은 한 게임에서 같이 플레이할 수 있어야 함

### 맵
- 왼쪽 진영과 오른쪽 진영으로 나뉨
- 가운데에 진영을 나누는 선이 그어져 있음 

### 기술 개요
- 기술은 한번에 한개씩만 발동
- 기술을 시전하려면 철권, 스트리트파이터 처럼 커맨드 입력이 필요함
- 커맨드 입력은 화살표 키와 스페이스바를 사용
- 화살표로 입력하고 마지막에 스페이스바를 눌러야 발동됨
- 동시입력X, 무조건 순차적으로 눌러야 발동됨 
- 공을 튕기기 0.5초 이내에 커맨드를 입력해야 발동됨

### 기술 목록
- 스파이크 (조금 빠른 공)
- - 커맨드 : SPACEBAR
- 멈추는 공 (날아가다가 랜덤으로 공이 잠깐 멈춤)
- - 커맨드 : 위 -> 아래 -> 아래 -> 위 -> SPACEBAR  
- 불꽃슛 (빠른 공)
- - 커맨드 : 왼쪽 -> 오른쪽 -> 왼쪽 -> 오른쪽 -> SPACEBAR
- 변화구 (상대 진영(중앙선을 넘음)으로 갔을 때 공의 방향이 -30 ~ +30 사이의 값으로 랜덤하게 바뀜)
- - 커맨드 : 왼쪽 -> 아래 -> 오른쪽 -> SPACEBAR
- 공 분신술 (시전시 공이 2개 추가되고(총3개) 분신인 공들은 상대 진영으로 넘어가기 전까지 깜박거리다가 상대진영으로 넘어가게 되면 깜박임이 멈춤 -> 상대가 진짜 공을 맞춰야 함, 가짜공은 튕겨지지 않음)
- - 커맨드 : 왼쪽 -> 아래 -> 위 -> 아래 -> 오른쪽 -> SPACEBAR

### 아이템 개요
- 플레이하다 보면 10초에 한번 아이템 박스가 각 진영에 1개씩 랜덤한 위치로 나옴
- 아이템 박스를 먼저 공으로 맞추는 사람이 아이템을 받음
- 아이템은 최대 2개까지 소지할 수 있음
- 아이템은 플레이어가 원할 때 사용할 수 있음

### 아이템 목록
- 공이 커짐 (사용하면 공이 튕겨지기 전까지 크기가 점점 커져서 맞추기 쉽게 됨) 
