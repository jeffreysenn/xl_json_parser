from node import Node

class XlNode(Node):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.col = -1

    def SetName(self, name): self.name = name
    def GetName(self): return self.name
    def SetCol(self, col): self.col = col
    def GetCol(self): return self.col

class RootNode(XlNode):
    def __init__(self):
        super().__init__()
        self.dict = {}

    def Build(self):
        for child in self.GetChildren():
            child.Build(self.dict)

    def GetDict(self): return self.dict

class IdxNode(XlNode):
    def __init__(self):
        super().__init__()
        self.list_node = None

    def SetListNode(self, list_node): self.list_node = list_node
    def GetListNode(self): return self.list_node

    def AddNewItem(self):
        self.GetListNode().AddNewItem()

    def Build(self, dict): pass

class ObjNode(XlNode):
    def __init__(self):
        super().__init__()
        self.dict = None

    def Build(self, dict):
        self.dict = dict

    def WriteVal(self, val):
        self.dict[self.GetName()] = val

class DictNode(XlNode):
    def Build(self, dict):
        dict[self.GetName()] = {}
        new_dict = dict[self.GetName()]
        for child in self.GetChildren():
            child.Build(new_dict)

class ListNode(XlNode):
    def __init__(self):
        super().__init__()
        self.list = None

    def AddNewItem(self):
        item = {}
        for child in self.GetChildren():
            child.Build(item)
        self.list.append(item)

    def Build(self, dict):
        dict[self.GetName()] = []
        self.list = dict[self.GetName()]

def ReplaceNode(old_node, new_node_type):
    new_node = new_node_type()
    new_node.SetName(old_node.GetName())
    new_node.SetParent(old_node.GetParent())
    sibs = old_node.GetSiblings()
    idx = sibs.index(old_node)
    sibs[idx] = new_node
    for child in old_node.GetChildren():
        child.AttachTo(new_node)
    return new_node

def ApplyRule(node):
    new_node = node
    if node.GetName() == '<idx>':
        sibs = node.GetSiblings()
        idx = sibs.index(node)
        next_node = sibs[idx + 1]
        idx_node = ReplaceNode(node, IdxNode)
        list_node = ReplaceNode(next_node, ListNode)
        idx_node.SetListNode(list_node)
        idx_node.SetCol(node.GetCol())
        new_node = list_node
    elif node.HasChildren() and not isinstance(node, RootNode) and not isinstance(node, ListNode):
        new_node = ReplaceNode(node, DictNode)
    elif not node.HasChildren():
        new_node = ReplaceNode(node, ObjNode)
        new_node.SetCol(node.GetCol())
    for child in new_node.GetChildren():
        ApplyRule(child)
    
def PrintNames(node):
    print("<%s> %s" % (type(node).__name__, node.GetName()))
    for child in node.GetChildren():
        PrintNames(child)