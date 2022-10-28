from random import choice
from random import randint


class Snake:
    def __init__(self):
        self.body = []
        self.dir = choice(["u", "d", "l", "r"])
        self._init_body()


    def _init_body(self):
        self.body.append((randint(3, 4), randint(3, 12)))
        for _ in range(2):
            if self.dir == "u":
                self.body.insert(0, (self.body[0][0], self.body[0][1]+1))
            elif self.dir == "d":
                self.body.insert(0, (self.body[0][0], self.body[0][1]-1))
            elif self.dir == "l":
                self.body.insert(0, (self.body[0][0]+1, self.body[0][1]))
            elif self.dir == "r":
                self.body.insert(0, (self.body[0][0]-1, self.body[0][1]))
    
    
    def move(self, apple):
        if self.dir == "u":
            self.body.append((self.body[-1][0], self.body[-1][1]-1))
        elif self.dir == "d":
            self.body.append((self.body[-1][0], self.body[-1][1]+1))
        elif self.dir == "l":
            self.body.append((self.body[-1][0]-1, self.body[-1][1]))
        elif self.dir == "r":
            self.body.append((self.body[-1][0]+1, self.body[-1][1]))
        if apple:
            return None
        else:
            return self.body.pop(0)
    
    
    def turn(self, dir):
        self.dir = dir
        