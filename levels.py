"""
levels.py stores the layout of each level is an easy to edit space.
"""
class LevelSetup():
    """
    LevelSetup is a class that specifies where the pips, tree, and pot
    exists in each level layout.
    """
    def __init__(self) -> None:
        """
        Initializes the LevelSetup class.
        """
        self.pips=[]
        self.tree_lines=[]
        self.pot_lines=[]

    def load_level(self,level,stage):
        """
        Loads a level layout for a certain level and stage.

        Args:
            level: An int representing the level number
            stage: An int representing what stage the level is in

        Returns:
            layout: a list contining the locations of every pip,
                tree line start and end point, and pot line start
                and end point.
        """
        self.pips=[]
        self.tree_lines=[]
        self.pot_lines=[]
        center = (240+768)/2
        bottom = 672
        if level == 1:
            if stage == 1:

                for pip in range(4):
                    self.pips.append([center-250+pip*50, pip*40+50])
                    self.pips.append([center+250-pip*50, pip*40+50])

                for pip in range(5):
                    self.pips.append([center+pip*25, pip*15+250])
                    self.pips.append([center-pip*25, pip*15+250])

                for pip in range(3):
                    self.pips.append([center-225+pip*40, pip*50+325])
                    self.pips.append([center+225-pip*40, pip*50+325])

                self.tree_lines = []
                self.pot_lines = [((center-100, bottom - 50),\
                     (center+100, bottom - 50)),\
                    ((center-100, bottom - 50), (center-150, bottom - 160)),\
                    ((center+100, bottom - 50), (center+150, bottom - 160))]

            if stage == 2:
                for row in range(3):
                    for col in range(4):
                        base_x = center-200+col*135 + 67*(row % 2)
                        base_y = row*110+60
                        scale = 10
                        self.pips.append((base_x,base_y-2.5*scale))
                        self.pips.append((base_x+2*scale,base_y-scale))
                        self.pips.append((base_x-2*scale,base_y-scale))
                        self.pips.append((base_x-scale,base_y+scale))
                        self.pips.append((base_x+scale,base_y+scale))


                self.tree_lines = [((center-130, bottom - 320),\
                    (center-180, bottom - 300)),\
                    ((center-130, bottom - 320), (center-50, bottom - 310)),\
                    ((center+130, bottom - 290), (center+50, bottom - 280)),\
                    ((center+130, bottom - 290), (center+170, bottom - 270)),]
                self.pot_lines = [((center-100, bottom - 50),\
                     (center+100, bottom - 50)),\
                    ((center-100, bottom - 50), (center-150, bottom - 160)),\
                    ((center+100, bottom - 50), (center+150, bottom - 160))]

            if stage == 3:
                self.pips.append((center+252,350))
                self.pips.append((center-252,340))
                star_locations = [(0,420),(200,60),(-170,160)]
                for loc in star_locations:
                    scale = 20
                    self.pips.append((center+loc[0],loc[1]-2.5*scale))
                    self.pips.append((center+loc[0]+2*scale,loc[1]-scale))
                    self.pips.append((center+loc[0]-2*scale,loc[1]-scale))
                    self.pips.append((center+loc[0]-scale,loc[1]+scale))
                    self.pips.append((center+loc[0]+scale,loc[1]+scale))
                    scale = -12
                    self.pips.append((center+loc[0],loc[1]-20-2.5*scale))
                    self.pips.append((center+loc[0]+2*scale,loc[1]-20-scale))
                    self.pips.append((center+loc[0]-2*scale,loc[1]-20-scale))
                    self.pips.append((center+loc[0]-scale,loc[1]-20+scale))
                    self.pips.append((center+loc[0]+scale,loc[1]-20+scale))

                self.tree_lines = [((center-110, bottom - 290),\
                    (center-220, bottom - 240)),\
                    ((center-110, bottom - 290), (center-80, bottom - 285)),\
                    ((center+80, bottom - 255), (center+170, bottom - 280)),\
                    ((center+170, bottom - 280), (center+210, bottom - 265)),\
                    ((center-200, bottom - 400), (center-153, bottom - 420)),\
                    ((center-153, bottom - 420), (center-60, bottom - 390)),\
                    ((center+80, bottom - 350), (center+175, bottom - 395)),\
                    ((center+175, bottom - 395), (center+215, bottom - 380)),\

                    ((center-60, bottom - 470), (center+30, bottom - 500)),\
                    ((center+30, bottom - 500), (center+112, bottom - 490)),\
                    ((center+112, bottom - 490), (center+155, bottom - 440)),]
                self.pot_lines = [((center-100, bottom - 50),\
                     (center+100, bottom - 50)),\
                    ((center-100, bottom - 50), (center-150, bottom - 160)),\
                    ((center+100, bottom - 50), (center+150, bottom - 160))]

            if stage == 4:
                #You Win
                for pip in range(3):
                    self.pips.append([center+135-15*pip, 195])
                    self.pips.append([center+15-15*pip, 195])
                    self.pips.append([center+15-15*pip, 105])
                for pip in range(4):
                    self.pips.append([center-120+pip*15, -15*pip+150])
                    self.pips.append([center-120-pip*15, -15*pip+150])
                    self.pips.append([center-120, -15*pip+195])
                for pip in range(5):
                    self.pips.append([center-30+15*pip,395])
                    self.pips.append([center-30+15*pip,320])

                    self.pips.append([center+30, 120+15*pip])
                    self.pips.append([center-30, 120+15*pip])
                for pip in range(6):
                    self.pips.append([center-150+5*pip,-15*pip+395])
                    self.pips.append([center-150-5*pip,-15*pip+395])
                    self.pips.append([center-100+5*pip,-15*pip+395])
                    self.pips.append([center-100-5*pip,-15*pip+395])

                    self.pips.append([center+150, 105+15*pip])
                    self.pips.append([center+90, 105+15*pip])

                    self.pips.append([center,-15*pip+395])

                    self.pips.append([center+150,-15*pip+395])
                    self.pips.append([center+90,-15*pip+395])
                    self.pips.append([center+150-12*pip,-15*pip+395])


                self.pot_lines =[((center-250, bottom - 50),\
                     (center+250, bottom - 50))]
        layout = [self.pips,self.tree_lines, self.pot_lines]
        return layout
