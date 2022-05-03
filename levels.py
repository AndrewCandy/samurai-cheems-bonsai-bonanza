class LevelSetup():
    def __init__(self) -> None:
        self.pips=[]
        self.tree_lines=[]
        self.pot_lines=[]
        
    def load_level(self,level,stage):
        self.pips=[]
        self.tree_lines=[]
        self.pot_lines=[]
        if level == 1:
            if stage == 1:

                for row in range(6):
                    for col in range(10):
                        self.pips.append([col*70+35*(row % 2),row*70+100])
                self.tree_lines = []
                self.pot_lines = [((200, 600 - 10), (400, 600 - 10)),\
                    ((200.0, 600 - 10), (150.0, 600 - 60)),\
                    ((400.0, 600 - 10), (450.0, 600 - 60))]
            if stage == 2:

                for row in range(4):
                    for col in range(10):
                        self.pips.append((col*70+35*(row % 2),row*120+100))
                self.tree_lines = []
                self.pot_lines = [((200, 600 - 10), (400, 600 - 10)),\
                    ((200.0, 600 - 10), (150.0, 600 - 60)),\
                    ((400.0, 600 - 10), (450.0, 600 - 60))]




        layout = [self.pips,self.tree_lines, self.pot_lines]
        return layout

