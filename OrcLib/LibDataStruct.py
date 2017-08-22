# coding=utf-8


class TreeNode(object):
    """
    Tree data management
    """
    def __init__(self, p_content, p_parent=None):

        self.content = p_content
        self.parent = p_parent
        self.children = []

    def append_child(self, p_content):
        """
        Append child
        :param p_content:
        :return:
        """
        self.children.append(TreeNode(p_content, self))

    def append_node(self, p_node):
        """
        Append a child node
        :param p_node:
        :return:
        """
        p_node.parent = self
        self.children.append(p_node)

    def get_child(self, row):
        """
        Get the child
        :param row:
        :return:
        """
        return self.children[row]

    def get_index(self, child):
        """
        Get the index of child
        :param child:
        :return:
        """
        for _index, item in enumerate(self.children):
            if item == child:
                return _index

        return -1

    def remove_child(self, row):
        """
        Remove Child of row
        :param row:
        :return:
        """
        value = self.children[row]
        self.children.remove(value)

        return True

    def __len__(self):
        return len(self.children)


class ListTree(object):

    def __init__(self):

        object.__init__(self)

        self.list = list()
        self.tree = dict()

    def load_list(self, p_value):
        """
        读入 list 数据
        :param p_value:
        :return:
        """
        self.load('LIST', p_value)

    def load_tree(self, p_value):
        """
        读入 tree 数据
        :param p_value:
        :return:
        """
        self.load('TREE', p_value)

    def load(self, p_type, p_value):

        if "LIST" == p_type:
            self.list = p_value
            self.resolve_list()

        elif "TREE" == p_type:
            self.tree = p_value
            self.resolve_tree()

        else:
            pass

    def resolve_list(self):
        """
        解析已读入 list 数据
        :param p_value:
        :return:
        """
        self.resolve('LIST')

    def resolve_tree(self):
        """
        解析已读入 tree 数据
        :param p_value:
        :return:
        """
        self.resolve('TREE')

    def resolve(self, p_type):
        """
        解析已读入的数据
        :param p_type:
        :return:
        """
        if "LIST" == p_type:
            self._clean_duplication()
            self.tree = dict()
            self.tree = self._list2tree(self._list_get_root())

        elif "TREE" == p_type:
            self.list = self._tree2list(self.tree)
            self._clean_duplication()

        else:
            pass

    def _list_get_root(self, p_root_id=None):
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

    def _list2tree(self, p_node):
        """
        :param p_node: root_node
        :type p_node: dict
        :return:
        """
        if p_node is None:
            return

        for _item in self.list:
            _parent_id = p_node["content"]["id"]
            _item_pid = _item["pid"]

            if _item_pid == _parent_id:
                _node = dict(content=_item, children=[])
                self._list2tree(_node)
                p_node["children"].append(_node)

        return p_node

    def _tree2list(self, p_tree):
        """
        tree 转化为列表,过程中会有重复
        :param p_tree:
        :type p_tree: dict
        :return:
        :rtype: list
        """
        if not p_tree:
            return list()

        result = [p_tree["content"]]

        for _item in p_tree["children"]:
            result.extend(self._tree2list(_item))

        return result

    def _clean_duplication(self):
        """
        去重
        :return:
        """
        if self.list is None:
            return

        new_list = list()
        for _item in self.list:
            if _item not in new_list:
                new_list.append(_item)

        self.list = new_list

    def get_children_tree(self, p_id, p_node=None):
        """
        获取一个节点的所有子节点
        :param p_node:
        :param p_id:
        :return:
        """
        if p_node is None:
            p_node = self.tree

        if p_id == p_node['content']['id']:
            return p_node
        else:
            for _child in p_node['children']:
                result = self.get_children_tree(p_id, _child)
                if result:
                    return result

        return list()

    def get_children_list(self, p_id):
        """
        获取子节点列表
        :param p_id:
        :return:
        """
        node_child = self.get_children_tree(p_id)
        return self._tree2list(node_child)

    def get_path(self, p_id, p_node=None):
        """
        获取节点的路径
        :param p_node:
        :param p_id:
        :return:
        """
        node_data = p_node if p_node is not None else self.tree

        if node_data['content']['id'] == p_id:
            return [node_data['content']]
        else:
            result = [node_data['content']]

            for _item in node_data['children']:
                temp = self.get_path(p_id, _item)

                if temp is not None:
                    result.extend(temp)
                    return result

            return None

    # def steps(self, p_node=None):
    #     """
    #     形成列表迭代,可能没有用
    #     :param p_node:
    #     :return:
    #     """
    #     if p_node is None:
    #         node = self.tree
    #     else:
    #         node = p_node
    #
    #     for _item in node["children"]:
    #         for _sub in self.steps(_item):
    #             yield _sub
    #
    #     yield node["content"]
