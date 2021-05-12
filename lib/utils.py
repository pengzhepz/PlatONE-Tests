


def assert_code(result, code):
    '''
    assert the ErrorCode
    :param result:
    :param code:
    :return:
    '''
    if isinstance(result, int):
        assert result == code, "code error，expect：{}，actually:{}".format(code, result)
    else:
        assert result.get('code') == code or result.get('Code') == code, "code error，expect：{}，actually:{}".format(code, result)
