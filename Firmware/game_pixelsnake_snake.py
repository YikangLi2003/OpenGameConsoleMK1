from random import choice
from random import randint


class Snake:
    def __init__(self):
        self.body = []
        self.dirc = choice(["u", "d", "l", "r"])
        self._init_body()


    def _init_body(self):
        self.body.append((randint(3, 4), randint(3, 12)))
        for _ in range(2):
            if self.dirc == "u":
                self.body.insert(0, (self.body[0][0], self.body[0][1]+1))
            elif self.dirc == "d":
                self.body.insert(0, (self.body[0][0], self.body[0][1]-1))
            elif self.dirc == "l":
                self.body.insert(0, (self.body[0][0]+1, self.body[0][1]))
            elif self.dirc == "r":
                self.body.insert(0, (self.body[0][0]-1, self.body[0][1]))
    
    
    def move_head(self):
        if self.dirc == "u":
            self.body.append((self.body[-1][0], self.body[-1][1]-1))
        elif self.dirc == "d":
            self.body.append((self.body[-1][0], self.body[-1][1]+1))
        elif self.dirc == "l":
            self.body.append((self.body[-1][0]-1, self.body[-1][1]))
        elif self.dirc == "r":
            self.body.append((self.body[-1][0]+1, self.body[-1][1]))
        return self.body[-1]


    def move_tail(self):
        return self.body.pop(0)
    
    
    def turn(self, dirc):
        if (dirc == "u" and self.dirc != "d") or \
           (dirc == "d" and self.dirc != "u") or \
           (dirc == "l" and self.dirc != "r") or \
           (dirc == "r" and self.dirc != "l"):
            self.dirc = dirc
