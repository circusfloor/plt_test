import matplotlib.pyplot as plt

from randomwalk import RandomWalk

while True:
    # 创建一个RandomWalk实例，并将其包含的点都绘制出来
    rw = RandomWalk()
    rw.fill_walk()
    plt.scatter(rw.x_values, rw.y_values, s=15)
    plt.show()

    keep_running = input('make anther walk?(y/n):')
    if keep_running == 'n':
        break
