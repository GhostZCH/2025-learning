import pygame
import sys

# 定义物理对象
class PhysicsObject:
    def __init__(self, x, y, width, height, mass, vx=0, vy=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.mass = mass
        self.vx = vx  # 水平速度
        self.vy = vy  # 垂直速度
        self.ax = 0  # 水平加速度
        self.ay = 0  # 垂直加速度

    def apply_force(self, fx, fy):
        """应用力，更新加速度"""
        self.ax += fx / self.mass
        self.ay += fy / self.mass

    def update(self, dt):
        """更新物体的位置和速度"""
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.ax = 0  # 重置加速度
        self.ay = 0

    def draw(self, screen):
        """绘制物体"""
        pygame.draw.rect(screen, (255, 0, 0), (int(self.x), int(self.y), self.width, self.height))


# 碰撞检测
def check_collision(obj1, obj2):
    """检测两个物体是否碰撞"""
    return (obj1.x < obj2.x + obj2.width and
            obj1.x + obj1.width > obj2.x and
            obj1.y < obj2.y + obj2.height and
            obj1.y + obj1.height > obj2.y)


# 碰撞响应
def resolve_collision(obj1, obj2):
    """简单的碰撞响应：反转速度"""
    if check_collision(obj1, obj2):
        obj1.vx *= -1
        obj1.vy *= -1
        obj2.vx *= -1
        obj2.vy *= -1


# 主程序
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("2D Physics Engine")
    clock = pygame.time.Clock()

    # 创建两个物理对象，并设置水平初速度
    obj1 = PhysicsObject(100, 100, 50, 50, 1, vx=100)  # 水平初速度为 100
    obj2 = PhysicsObject(200, 200, 50, 50, 1, vx=-100)  # 水平初速度为 -100

    # 设置重力
    gravity = 9.8

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 应用重力
        obj1.apply_force(0, gravity * obj1.mass)
        obj2.apply_force(0, gravity * obj2.mass)

        # 更新物体状态
        dt = 0.01  # 时间步长
        obj1.update(dt)
        obj2.update(dt)

        # 碰撞检测与响应
        resolve_collision(obj1, obj2)

        # 边界检测（防止物体飞出屏幕）
        if obj1.y + obj1.height > 600:
            obj1.y = 600 - obj1.height
            obj1.vy *= -1
        if obj2.y + obj2.height > 600:
            obj2.y = 600 - obj2.height
            obj2.vy *= -1

        # 水平边界检测
        if obj1.x < 0 or obj1.x + obj1.width > 800:
            obj1.vx *= -1
        if obj2.x < 0 or obj2.x + obj2.width > 800:
            obj2.vx *= -1

        # 绘制物体
        screen.fill((0, 0, 0))  # 清屏
        obj1.draw(screen)
        obj2.draw(screen)

        pygame.display.flip()  # 更新屏幕
        clock.tick(120)  # 限制帧率为60 FPS


if __name__ == "__main__":
    main()physics_model.py
