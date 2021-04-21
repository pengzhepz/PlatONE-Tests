from configparser import ConfigParser

def get_env(title, subtitle):
    """
    :param title: 配置头部
    :param subtitle: 配置内的内容
    :return:
    """
    config = ConfigParser()
    filename = '../conf/host.ini'
    config.read(filename)  # 读取配置文件
    if title not in config.sections():
        print('不存在该配置项目，请检查配置文件config.ini')
    elif subtitle not in config.options(title):
        print(f'该{title}配置项目下不存在{subtitle}元素，请检查配置文件config.ini')
    else:
        setting = config.get(title, subtitle)
    return setting


if __name__ == '__main__':
    print(get_env('test','host'))