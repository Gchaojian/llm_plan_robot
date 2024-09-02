import errno
import os
import sys
import re
import time
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)

import socket

sys.path.append(os.path.dirname(__file__))
from robot_env import MedicalEnv


class RobotServer():
    """ 机器人服务节点类. """

    def __init__(self, name):
        super().__init__(name)
        self.add_ints_server_ = self.create_service(GPT, "gpt_service", self.gpt_callback)
        self.code = None

    def gpt_callback(self, request, response):
        gpt_message = request.data
        self.code = self.extract_python_code(gpt_message)
        response.res = True
        if self.code is None:
            response.res = False
        return response


def extract_python_code(content):
    """ 
    提供了函数的描述，包括参数和返回值的类型
    content 参数是包含代码的消息字符串
    返回值是提取的 Python 代码字符串，如果没有找到代码块则返回 None
    """
    # 正则表达式用于匹配用 ``` 包裹起来的代码块
    code_block_regex = re.compile(r"```(.*?)```", re.DOTALL)
    # 使用正则表达式查找所有匹配的代码块
    code_blocks = code_block_regex.findall(content)
    if code_blocks:
        # 将所有代码块连接成一个完整的代码字符串
        full_code = "\n".join(code_blocks)
        # 如果代码字符串以 "python" 开头，移除它
        if full_code.startswith("python"):
            full_code = full_code[7:]
        # 如果没有找到代码块，返回 None
        return full_code
    else:
        return None


def execute_python_code(robot, code):
    """ 
    提供了函数的描述，包括参数的类型。
    robot 参数表示在提示中使用的类名。
    code 参数表示要执行的 Python 代码字符串。
    """
    print("\033[32m" + "请稍等,我将要执行配药任务..." + "\033[m")
    print("\033[32m" + "code:" + "\033[m" + code)
    # 使用 exec 函数执行传入的 code 字符串。
    # 使用 try...except 块捕获任何在执行过程中出现的异常。
    # 如果发生异常，使用 logging.warning 记录错误信息。
    try:
        exec(code)
    except Exception as e:
        logging.warning("Found error while running the code: {}".format(e))
    print("\033[32m" + "完成配药!\n" + "\033[m")


def main(args=None):

    logging.info(f"...初始化TCP...")
    HOST = '192.168.3.26'
    #使用 socket.socket() 创建一个新的套接字对象 ss,socket.AF_INET 表示使用 IPv4 地址,socket.SOCK_STREAM 表示使用 TCP 协议
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    ss.bind((HOST, 5001))
    ss.listen(1)
    ss.setblocking(0)  # 设置为非阻塞,在非阻塞模式下，如果没有可用的连接或数据，套接字操作不会等待，而是立即返回
    logging.info(f"Done.")

    logging.info(f"...初始化配药环境...")
    env = MedicalEnv()
    env.initialize_robot()
    logging.info(f"Done.")

    while True:
        try:
            logging.info(f"...等待连接...")
            conn, addr = ss.accept()
            conn.setblocking(0)  # 设置连接为非阻塞
            logging.info(f"Connected by {addr}")
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    logging.info(f"Received: {data.decode()}")
                    code = extract_python_code(data.decode())
                    if code is not None:
                        execute_python_code(env, code)
                except socket.error as e:
                    if e.errno == errno.EWOULDBLOCK:
                        # 非阻塞套接字，没有数据可读时会引发 EWOULDBLOCK 错误
                        pass
                    else:
                        raise
                finally:
                    env.step(env.action)

        except socket.error as e:
            if e.errno == errno.EWOULDBLOCK:
                # 非阻塞套接字，没有连接时会引发 EWOULDBLOCK 错误
                pass
            else:
                raise
        # conn.close()


if __name__ == "__main__":
    main()
