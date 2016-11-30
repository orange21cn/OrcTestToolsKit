# coding=utf-8


def connect_list(p_lists, p_detail, p_flag):
    """
    连接两个数组
    :param self:
    :param p_lists: list 1
    :type p_lists: list
    :param p_detail: list 2
    :type p_detail: list
    :param p_flag: 标志字段
    :type p_flag: str
    :return:
    :rtype: list
    """
    result = []

    if 0 == len(p_detail):
        return result

    for _item in p_lists:

        _item.pop("create_time")

        for _det in p_detail:

            if _det["id"] == _item[p_flag]:

                temp = _det.copy()
                temp.pop("id")

                _item.update(temp)

                break

        result.append(_item)

    return result
