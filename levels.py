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
                    for col in range(8):
                        self.pips.append([240+20+col*70+35*(row % 2),row*70+100])
                self.tree_lines = []
                self.pot_lines = [(((240+768)/2-100, 672 - 10), ((240+768)/2+100, 672 - 10)),\
                    (((240+768)/2-100, 672 - 10), ((240+768)/2-150, 672 - 60)),\
                    (((240+768)/2+100, 672 - 10), ((240+768)/2+150, 672 - 60))]
            if stage == 2:

                for row in range(4):
                    for col in range(8):
                        self.pips.append((240+20+col*70+35*(row % 2),row*120+100))
                self.tree_lines = []
                self.pot_lines = [(((240+768)/2-100, 672 - 10), ((240+768)/2+100, 672 - 10)),\
                    (((240+768)/2-100, 672 - 10), ((240+768)/2-150, 672 - 60)),\
                    (((240+768)/2+100, 672 - 10), ((240+768)/2+150, 672 - 60))]




        layout = [self.pips,self.tree_lines, self.pot_lines]
        return layout

