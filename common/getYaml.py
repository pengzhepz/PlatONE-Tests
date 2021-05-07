import yaml


def get_data(test_data_path):
    case = []  # 存储测试用例名称
    param = []  # 存储请求对象
    expected = []  # 存储预期结果
    with open(test_data_path, 'r', encoding='utf-8') as f:
        dat = yaml.load(f.read(), Loader=yaml.SafeLoader)
        test = dat['test']
        for td in test:
            case.append(td.get('case', ''))
            param.append(td.get('paramters', {}))
            expected.append(td.get('expect', {}))
    parameters = zip(param, expected)
    return case, list(parameters)

# cases, parameters = get_test_data("login.yaml")
# print(parameters)
