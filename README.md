# Tetris2 (NumPy + Pygame)

현재의 tetris.py에서는, PC의  sound 채널이 2라는 가정하게 프로그래밍 되어 있다. 
내 PC에서는 sound 채널이 2로 설정되어 있기 때문에, 정상적으로 소리가 나온다.
그러나 탬 PC에서는 6개 채널로 설정되어 있기 때문에, 이 프로그램을 실행하면 에러가 발생한다.

그래서 탬 PC에서는, tetris.py 파일을 수정해서  해당 PC의 sound 채널수에 맞게 동작하도록 설정이 되어 있다.
따라서 추후에 tetris.py 파일을, 탬PC의 tetris.py에 맞게 수정해야 한다.




YSH: 이 프로젝트는 최초에, Tetris 폴더를 통째로 copy해서 만든 프로젝트이다.  
그런다음, 게임을 시작시켰을때의 실행속도를, Tetris게임보다 훨씬 느리게 설정했다.
이 Tetris2 게임은....탬이 플래이 할 수 있도록, 처음 실행 속도를 확 느리게 설정한 것이다.

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
