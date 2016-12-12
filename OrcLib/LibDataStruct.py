# coding=utf-8


class ListTree:

    def __init__(self):

        self.list = None
        self.tree = None

    def resolve(self, p_type, p_value):

        if "LIST" == p_type:
            self.list = p_value
            self.tree = []
            self.tree = self.__list2tree(self.__list_get_root())

        elif "TREE" == p_type:
            self.list = []
            self.tree = p_value
            self.__tree2list(self.tree)

        else:
            pass

    def __list_get_root(self, p_root_id=None):
        """
        获取列表根元素
        :param p_root_id:
        :return:
        """
        for _item in self.list:
            if _item["pid"] == p_root_id:
                return dict(content=_item, children=[])
        else:
            return None

    def __list2tree(self, p_node):
        """
        :param p_node:
        :type p_node: dict
        :return:
        """
        print "--->", p_node["content"]["pid"], p_node["content"]["id"], p_node["children"]
        for _item in self.list:
            _parent_id = p_node["content"]["id"]
            _item_pid = _item["pid"]

            if _item_pid == _parent_id:
                _node = dict(content=_item, children=[])
                self.__list2tree(_node)
                p_node["children"].append(_node)

        return p_node

    def __tree2list(self, p_tree):
        """
        tree 转化为列表
        :param p_tree:
        :type p_tree: dict
        :return:
        :rtype: list
        """
        self.list.append(p_tree["content"])

        for _item in p_tree["children"]:
            self.__tree2list(_item)

    def steps(self, p_node=None):
        """
        形成列表迭代,可能没有用
        :param p_node:
        :return:
        """
        if p_node is None:
            node = self.tree
        else:
            node = p_node

        for _item in node["children"]:
            for _sub in self.steps(_item):
                yield _sub

        yield node["content"]
