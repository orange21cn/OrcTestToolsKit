# coding=utf-8
import platform


class OrcSystem(object):

    def __init__(self):

        object.__init__(self)

    @staticmethod
    def get_platform():
        return platform.architecture()

    @classmethod
    def get_path(cls, p_path):
        """
        根据系统转换路径格式
        :param p_path:
        :return:
        """
        if isinstance(p_path, str):
            res_path = p_path
        else:
            res_path = '/'.join(p_path)

        if 'Windows' == cls.get_platform():
            res_path = res_path.replace('/', '\\\\')
            res_path = res_path.replace('\\', '\\\\')

        return res_path
