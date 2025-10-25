# Tetris (NumPy + Pygame)

간단한 테트리스 게임입니다.

키 바인딩:
- 위쪽 화살표: 블록을 반시계 방향으로 회전
- 왼쪽 화살표: 왼쪽으로 한 칸 이동
- 오른쪽 화살표: 오른쪽으로 한 칸 이동
- 스페이스바: 하드 드롭 (즉시 아래로 이동)
- 아래 화살표: 누르고 있는 동안 블록이 2배 빠르게 떨어짐 (soft drop)
 - 레벨 업: 매 10개의 블록이 고정될 때마다 떨어지는 속도가 10% 빨라집니다.

요구사항:
- Python 3.8+
- numpy
- pygame

설치:

```powershell
python -m pip install -r requirements.txt
```

실행:

```powershell
python tetris.py
```

참고: 윈도우에서 pygame 설치에 문제가 있으면 `python -m pip install pygame --pre` 같은 옵션을 시도해보세요.
