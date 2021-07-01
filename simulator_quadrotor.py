import time
import math
import matplotlib.image as img
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from matplotlib.collections import LineCollection
import matplotlib.animation as animation


class Quadrotor:
    def __init__(self, pos_seq, trace_color='b', name='Quadrotor'):
        # self.x = init_pos[0]
        # self.y = init_pos[1]
        # self.theta = init_pos[2]      # radian
        self.x, self.y = None, None  # 无人机初始位置
        self.last_x, self.last_y = None, None  # 无人机的上一个位置
        self.radius = 0.5  # 四旋翼中心到电机中心长度
        self.trace_color = trace_color  # 运动轨迹的颜色
        self.seq = pos_seq  # 位姿序列

        self.text_name = name
        self.pos_index = 0  # 当前位姿下标

    def modify_pose(self):
        self.pos_index %= len(self.seq)
        curr_pos = self.seq[self.pos_index]
        if self.x != None:
            self.last_x = self.x
            self.last_y = self.y
        self.x = curr_pos[0]
        self.y = curr_pos[1]
        self.theta = curr_pos[2]
        self.pos_index += 1
        time.sleep(0.005)

    def __modify_motor_collection(self):
        drone_patches = []
        motor_x_offset = self.radius*math.cos((self.theta + math.pi/4))
        motor_y_offset = self.radius*math.sin((self.theta + math.pi/4))
        self.center_of_motor = [[self.x+motor_x_offset, self.y+motor_y_offset],
                                [self.x-motor_x_offset, self.y-motor_y_offset],
                                [self.x-motor_y_offset, self.y+motor_x_offset],
                                [self.x+motor_y_offset, self.y-motor_x_offset]]
        for i in range(4):
            drone_circle = mpatches.Circle(
                self.center_of_motor[i], radius=0.4*self.radius)
            drone_patches.append(drone_circle)
        motor_collection = PatchCollection(
            drone_patches, match_original=False, facecolor='w', edgecolors=['r', 'k', 'r', 'k'], linewidth=2, alpha=1)

        return motor_collection

    def __modify_arm_collection(self):
        arm_line_position = [[self.center_of_motor[0],
                              self.center_of_motor[1]],
                             [self.center_of_motor[2],
                              self.center_of_motor[3]]]
        arm_collection = LineCollection(arm_line_position, linewidth=1., color='k',
                                        alpha=1)
        return arm_collection

    def modify_trace(self, ax):
        if self.x != None:
            trace_line_x = [self.last_x, self.x]
            trace_line_y = [self.last_y, self.y]
            line = mlines.Line2D(trace_line_x, trace_line_y,
                                 lw=2, alpha=0.1, color=self.trace_color)
            ax.add_line(line)

    def modify_collection(self, ax):
        ax.add_collection(self.__modify_motor_collection())
        ax.add_collection(self.__modify_arm_collection())

    def modify_robot_label(self, ax):
        ax.text(x=self.x, y=self.y+2*self.radius,
                s=self.text_name, fontsize=7)

# init 函数和 animate函数是框架内置的函数，这里进行覆盖
# init函数会被执行两次


def init():
    pass
    return ax.collections  # 返回值不可修改


def animate(i):
    if i > 10:  # 80
        print(i)
        # print(len(ax.collections))
        ax.collections = []
        ax.texts = []
        for robot in [robot1]:  # 遍历更新各个无人机位姿
            robot.modify_pose()  # 更新无人机的各个变量，包括位姿等
            robot.modify_collection(ax)  # 根据更新后的位姿，绘制无人机
            robot.modify_trace(ax)  # 根据更新后的位姿，绘制轨迹
            robot.modify_robot_label(ax)  # 根据更新后的位姿，显示无人机标签
            ax.set_xlim([-10, 20])  # 设置图像显示范围
            ax.set_ylim([-10, 20])
        if len(ax.lines) > 100:  # 设置保留轨迹长度
            del ax.lines[0:10]
    return ax.collections+ax.lines+ax.texts  # 返回值不可修改


if __name__ == '__main__':

    # 生成位姿序列
    x = [i*0.1 for i in range(-90, 190)]
    y = [i*0.1 for i in range(-90, 190)]
    theta = [0.1*i for i in range(len(x))]
    pos_seq = list(zip(x, y, theta))

    # 实例化无人机
    robot1 = Quadrotor(pos_seq, trace_color='g', name='Quadrotor1')

    fig, ax = plt.subplots()
    ax.set_xlim([-10, 20])  # 设置图像显示范围
    ax.set_ylim([-10, 20])
    ax.axis('equal')  # 显示时保持坐标轴尺度一致
    ax.set_xticks(range(-10, 20))  # 显示刻度
    ax.set_yticks(range(-10, 20))  # 显示刻度
    ax.grid()  # 显示网格
    # ax.axis('off')

    # bgimg = img.imread("./background3.png") # 读取背景图像
    # ax.imshow(bgimg, alpha=0.9,
    #           extent=[0, 150, 0, 100],) # 显示背景图像

    # save_count代表视频存储的frame数,当开启录制gif或mp4时，需要指定，如save_count=1400
    ani = animation.FuncAnimation(
        fig, animate, init_func=init, interval=50, blit=True)
    # 生成gif并存储
    # ani.save('single_pendulum_nodecay.gif', writer='imagemagick')  # , fps=100
    # 生成mp4并存储
    # ani.save('robot_navigation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    plt.show()
