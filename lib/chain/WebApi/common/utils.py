import yaml

def get_test_data(data_path):
    with open(data_path,'r',encoding='utf-8') as f:
        data = yaml.load(f.read(),Loader=yaml.SafeLoader)
        test_data = data['test']
    return test_data


if __name__ == '__main__':
    print(get_test_data('../data/createNode.yaml'))