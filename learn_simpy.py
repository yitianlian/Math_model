
import simpy
# def car(env):
#    while True:
#       print('Start parking at %d' % env.now)
#       parking_duration = 5
#       yield env.timeout(parking_duration)
#
#       print('Start driving at %d' % env.now)
#       trip_duration = 2
#       yield env.timeout(trip_duration)
#
# env = simpy.Environment()
# env.process(car(env))
# env.run(until=15)

from random import seed, randint
seed(23)

import simpy

class EV:
    def __init__(self, env):
        self.env = env
        self.drive_proc = env.process(self.drive(env))
        self.bat_ctrl_proc = env.process(self.bat_ctrl(env))
        self.bat_ctrl_reactivate = env.event()
        self.bat_ctrl_sleep = env.event()


    def drive(self, env):
        """驾驶进程"""
        while True:
            # 驾驶 20-40 分钟
            print("开始驾驶 时间: ", env.now)
            yield env.timeout(randint(20, 40))
            print("停止驾驶 时间: ", env.now)

            # 停车 1-6 小时
            print("开始停车 时间: ", env.now)
            self.bat_ctrl_reactivate.succeed()  # 激活充电事件
            self.bat_ctrl_reactivate = env.event()  # 变成未激活状态
            yield env.timeout(randint(60, 360)) & self.bat_ctrl_sleep # 停车时间和充电程序同时都满足
            print("结束停车 时间:", env.now)

    def bat_ctrl(self, env):  # 循环执行的，知道结束
        """电池充电进程"""
        while True:
            print("充电程序休眠 时间:", env.now)
            yield self.bat_ctrl_reactivate  # 休眠直到充电事件被激活
            print("充电程序激活 时间:", env.now)
            yield env.timeout(randint(30, 90))
            print("充电程序结束 时间:", env.now)
            self.bat_ctrl_sleep.succeed()
            self.bat_ctrl_sleep = env.event()

def main():
    env = simpy.Environment()
    ev = EV(env)
    env.run(until=300)


if __name__ == '__main__':
    main()

    """
    银行排队服务例子

    情景:
      一个柜台对客户进行服务, 服务耗时, 客户等候过长会离开柜台
    """
    import random

    RANDOM_SEED = 42
    NEW_CUSTOMERS = 5  # 客户数
    INTERVAL_CUSTOMERS = 10.0  # 客户到达的间距时间
    MIN_PATIENCE = 1  # 客户等待时间, 最小
    MAX_PATIENCE = 3  # 客户等待时间, 最大


    def source(env, number, interval, counter):
       """进程用于生成客户"""
       for i in range(number):
          c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
          env.process(c)
          t = random.expovariate(1.0 / interval)  # 指数分布的浮点数，也就是指数分布的到达间隔时间
          yield env.timeout(t)


    def customer(env, name, counter, time_in_bank):
       """一个客户表达为一个协程, 客户到达, 被服务, 然后离开"""

       arrive = env.now
       print('%7.4f %s: Here I am' % (arrive, name))

       with counter.request() as req:
          patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
          # 等待柜员服务或者超出忍耐时间离开队伍
          results = yield req | env.timeout(patience)
          wait = env.now - arrive

       if req in results:
          # 到达柜台
          print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))
          tib = random.expovariate(1.0 / time_in_bank)
          yield env.timeout(tib)
          print('%7.4f %s: Finished' % (env.now, name))
       else:
          # 没有服务到位
          print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))


    # Setup and start the simulation
    print('Bank renege')
    random.seed(RANDOM_SEED)
    env = simpy.Environment()

    # Start processes and run
    counter = simpy.Resource(env, capacity=1)
    env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
    env.run()