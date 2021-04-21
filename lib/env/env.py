"""
TODO:
    在s2实现node, host的抽象，支持更细化的环境操作
"""


class Env:
    # 注意部署相关的环境变量

    def running(self):
        pass

    def deploy(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass

    def clean(self):
        pass
