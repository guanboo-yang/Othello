# Othello game
### Team members
- Team leader:
    - name: Guan-Bo Yang
    - student_id: b09902064
    - github: [guanboo-yang](https://github.com/guanboo-yang)
- member:
    - name: Guan-Ting Yi
    - student_id: b09902067
    - github: [timyi976](https://github.com/timyi976)
- member:
    - name: Kai-Jyun Yang
    - student_id: b09902059
    - github: [Alex-0718](https://github.com/Alex-0718)
### Report
rate: (RandomAgent) (CornerAgent)
- v1.1: We complete the basic agent with: (rate: 70 ~ 80)
    - geting available actions
    - corner position first
    - side position second
    - X position last.
- v1.2: (rate: 83)
    - v1.2.1: We update the agent with OPENRATE theorem
    - v1.2.4: Add available actions to random agent
- v1.3: We add ALPHA-BETA ALGORITHM to the last ten moves (rate: 88)
- v1.4: Add more side position rules (rate: 92)
    - v1.4.1: Fix a thinking mistake (rate: 98) (rate: 87)
    - v1.4.2: Add more side position rules (rate: 99) (rate: 91)
- v1.5: We fix ab pruning problems
    - v1.5.1: Final
    - v1.5.2: Final 2
    - v1.5.3: Final 3

---

### Prerequsite
```
$ pip install pygame
$ pip install tqdm
```

### Repo structure
```
othello
├── __pycache__
├── agent
│   ├── __pycache__
│   ├── guanboo-yang
│   ├── base_agent.py
│   └── guanboo-yang.py
├── font
│   ├── LICENSE.txt
│   └── OpenSans-Regular.ttf
├── .gitignore
├── arena.py
├── board.py
├── env.py
├── pygamewrapper.py
├── README.md
├── reversi_board.py
├── reversi.py
└── utils.py
```

### Run the project
```
$ git clone https://github.com/guanboo-yang/othello.git
$ cd othello
$ python3 arena.py --agent1 guanboo-yang.HumanAgent --agent2 guanboo-yang.MyAgent --time_limit 600000 --rounds 1
```

---

### Tutorial slides
|
[Github tutorial](https://docs.google.com/presentation/d/1X0YmTyj4BNnG7E8saxtG-jH9XLWm8OiFG3L21HhgRwc/edit#slide=id.gacd295469b_2_15)
|
[Python tutorial](https://docs.google.com/presentation/d/1pyyqS0QBvdS6jl4sLFFINce6fYdUXPpX9f47-3n6AME/edit?usp=sharing)
|
[Markdown tutorial](https://docs.google.com/presentation/d/1BrGTMmXFdGQpRkhMQs3FPhjOsyPv-EwPOy3bguRlIbI/edit?usp=sharing)
|
### Tutorial clips:
|
[Github tutorial](https://www.youtube.com/watch?v=YJNj0JF7p2k&list=PL8RRW7e03_x2FqpgLxWehpbytFKRPy6ba&index=1)
|
[Homework introduction](https://www.youtube.com/watch?v=MG1AsisCY2g&list=PL8RRW7e03_x2FqpgLxWehpbytFKRPy6ba&index=2)
|
[Code introduction](https://www.youtube.com/watch?v=3ySyE1IMbnA&list=PL8RRW7e03_x2FqpgLxWehpbytFKRPy6ba&index=3)
|
[PDB Introduction](https://www.youtube.com/watch?v=3ySyE1IMbnA&list=PL8RRW7e03_x2FqpgLxWehpbytFKRPy6ba&index=4)
|
