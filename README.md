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


### GPT history
아주 재미있는 아이디어네요! Ping Pong 게임에 다양한 기술을 추가하는 것이라니, 정말 흥미롭습니다. 여러분의 기존 기술에 몇 가지를 더 추가해서 게임을 더욱 다채롭게 만들어보겠습니다.

추가 기술 목록
폭풍 공 (빠르게 여러 번 튕기면서 지나감)

커맨드: 위 -> 오른쪽 -> 왼쪽 -> 위 -> SPACEBAR

효과: 공이 여러 번 튕기면서 빠르게 상대방 쪽으로 가며, 각 튕길 때마다 방향이 조금씩 바뀌어 예측하기 어렵습니다.

어둠의 공 (어두운 상태에서 상대방 시야를 좁히는 기술)

커맨드: 아래 -> 왼쪽 -> 오른쪽 -> 위 -> SPACEBAR

효과: 일정 시간 동안 화면이 어두워져 상대방의 시야가 좁아지고, 공이 보이지 않게 됩니다. 그 사이 공은 일반 공처럼 튕기지만 상대는 공을 정확히 맞추기가 힘듭니다.

빙글빙글 공 (회전하는 공으로 상대를 헷갈리게 함)

커맨드: 오른쪽 -> 위 -> 왼쪽 -> 아래 -> SPACEBAR

효과: 공에 회전력을 부여하여, 공이 튕길 때 그 방향이 예측하기 힘들어집니다. 상대방은 공이 어떻게 튕길지 예측하기 어렵습니다.

플라즈마 공 (멀리 날아가는 강력한 공)

커맨드: 아래 -> 아래 -> 오른쪽 -> 왼쪽 -> SPACEBAR

효과: 공의 속도와 비행 거리가 엄청나게 증가합니다. 튕겨나갈 때 강력한 힘을 발휘하여 상대방이 받아내기 힘들 수 있습니다.

투명 공 (일정 시간 동안 공이 투명해져 보이지 않음)

커맨드: 왼쪽 -> 오른쪽 -> 위 -> 위 -> SPACEBAR

효과: 공이 상대방에게 보이지 않게 되어, 상대가 공의 위치를 추적하기 힘듭니다. 잠깐 동안만 투명해지고 다시 보이게 됩니다.

복제 공 (상대에게 두 개의 공을 보내며 혼란을 줌)

커맨드: 오른쪽 -> 왼쪽 -> 아래 -> 위 -> 위 -> SPACEBAR

효과: 공이 복제되어 두 개의 공이 동시에 상대방에게 날아갑니다. 상대는 두 개의 공을 모두 처리해야 합니다.

기술 설명
폭풍 공: 상대가 공을 받아낼 때, 튕기면서 난이도가 높아지는 기술입니다. 공이 이동할 때마다 방향이 조금씩 변해서 상대방의 반응 속도를 테스트할 수 있습니다.

어둠의 공: 시각적인 효과를 추가하여 상대방의 반응 시간을 늦추는 기술입니다. 공이 어떻게 튕길지 예측할 수 없고, 어두운 화면에서 공을 맞추는 것이 어려워집니다.

빙글빙글 공: 공에 회전력을 추가하여 튕길 때마다 예측을 어렵게 만드는 기술로, 공의 경로를 읽기 힘들게 만듭니다.

플라즈마 공: 속도와 비행 거리를 대폭 증가시켜, 상대방이 거의 받아낼 수 없게 만듭니다. 빠르게 넘어오는 강력한 공을 처리하는 것은 매우 어려운 도전이 될 것입니다.

투명 공: 일정 시간 동안 공이 보이지 않게 만들어 상대의 반응을 방해하는 기술입니다. 상대는 공이 어디에 있는지 몰라서 방어하기 힘들어집니다.

복제 공: 두 개의 공을 동시에 보내 상대방에게 두 가지 타격을 동시에 주는 기술입니다. 하나의 공에 집중하게 만든 후, 또 다른 공이 날아오는 방식으로 혼란을 줄 수 있습니다.

이렇게 몇 가지 기술을 추가하면 게임이 훨씬 더 재미있고 전략적인 요소가 가미될 것 같습니다! 어떤 기술이 가장 마음에 드시나요?
