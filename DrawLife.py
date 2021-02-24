import time
import uLife
import numpy as np
import seaborn as sns; sns.set_theme()

class World(uLife.World):
    def Draw(self):
        t = []
        for i in range(0,self.xsize):
            r = []
            for j in range(0, self.ysize):
                c = self(i,j)
                if c.Alive():
                    r.append(c.eimmune+c.cimmune)
                else:
                    r.append(0)
            t.append(r)
        print(t)
        a = np.array(t)
        life = sns.heatmap(a, cbar=False)
        life.get_figure().savefig("images/Life%d.png"%self.age)

if __name__ == '__main__':
    w = World(8,8)
    w.ToLife((0,0), (0,1), (1,1), (1,2), (1,3), (0,2))
    c = 0
    while c < 128:
        c += 1
        w.Draw()
        w.Step()
