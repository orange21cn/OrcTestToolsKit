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
        if not isinstance(p_value, list):
            return

        self.list = p_value
        self.resolve_list()

    def load_tree(self, p_value):
        """
        读入 tree 数据
        :param p_value:
        :return:
        """
        if not isinstance(p_value, dict):
            return

        self.tree = p_value
        self.resolve_tree()

    def load(self, p_type, p_value):
        """
        读入数据
        :param p_type:
        :param p_value:
        :return:
        """
        if "LIST" == p_type:
            self.load_list(p_value)
        elif "TREE" == p_type:
            self.load_tree(p_value)
        else:
            pass

    def resolve_list(self):
        """
        解析已读入 list 数据
        :return:
        """
        self._clean_duplication()
        self.tree = dict(content='', children=[])

        root_nodes = self._list_get_root()

        for _node in root_nodes:
            self.tree['children'].append(self._list2tree(_node))

    def resolve_tree(self):
        """
        解析已读入 tree 数据
        :return:
        """
        self.list = self._tree2list(self.tree)
        self._clean_duplication()

    def resolve(self, p_type):
        """
        解析已读入的数据
        :param p_type:
        :return:
        """
        if "LIST" == p_type:
            self.resolve_list()
        elif "TREE" == p_type:
            self.resolve_tree()
        else:
            pass

    def get_tree_node(self, p_tree=None):
        """
        获取 TreeNode 类型的树
        :param p_tree:
        :return:
        """
        tree = p_tree or self.tree
        if not tree:
            return TreeNode('')

        node = TreeNode(tree['content'])

        for _item in tree['children']:
            node.append_node(self.get_tree_node(_item))

        return node

    def _list_get_root(self, p_root_id=None):
        """
        获取列表根元素
        :param p_root_id:
        :return:
        """
        root_nodes = []
        ids = [_item['id'] for _item in self.list]

        for _item in self.list:
            if _item['pid'] not in ids:
                root_nodes.append(dict(content=_item, children=[]))

        return root_nodes

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
        node = p_node or self.tree

        if not node['content']:
            node = node['children'][0]

        if p_id == node['content']['id']:
            return node
        else:
            for _child in node['children']:
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
        node = p_node or self.tree

        if not node['content']:
            node = node['children'][0]

        if node['content']['id'] == p_id:
            return [node['content']]
        else:
            result = [node['content']]

            for _item in node['children']:
                temp = self.get_path(p_id, _item)

                if temp is not None:
                    result.extend(temp)
                    return result

            return None
