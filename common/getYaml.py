import yaml


def get_test_data(data_path):
    """
    读取yaml文件
    :param data_path: yaml文件路径
    :return:
    """
    with open(data_path, 'r', encoding='utf-8') as f:
        data = yaml.load(f.read(), Loader=yaml.SafeLoader)
        test_data = data['test']
    return test_data
