# coding=utf-8
from PySide.QtGui import QMessageBox


class OrcMessage(object):
    def __init__(self):
        object.__init__(self)

    @staticmethod
    def question(p_parent, p_message):
        """
        确认框,可确定或取消
        :param p_parent:
        :param p_message:
        :return:
        """
        button = QMessageBox.question(
            p_parent, "Question", p_message, QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)

        return button == QMessageBox.Ok

    @staticmethod
    def info(p_parent, p_message):
        """
        提示框
        :param p_parent:
        :param p_message:
        :return:
        """
        QMessageBox.information(p_parent, "Information", p_message)
