class Node:
    def __init__(self):
        self.parent = None
        self.children = []

    def GetParent(self): return self.parent
    def SetParent(self, parent): self.parent = parent
    def ResetParent(self): self.parent = None

    def AddChild(self, child): self.children.append(child)
    def RemoveChild(self, child): self.children.remove(child)
    def SetChildren(self, children): self.children = children
    def HasChildren(self): return len(self.children) != 0
    def GetChildren(self): return self.children
    def GetSiblings(self): return self.GetParent().GetChildren()

    def AttachTo(self, parent):
        parent.AddChild(self)
        self.SetParent(parent)

    def Detach(self):
        self.parent.RemoveChild(self)
        self.ResetParent()

def SearchTree(node, pred):
    matched_nodes = []
    if pred(node):
        matched_nodes.append(node)
    for child in node.GetChildren():
        matched_nodes += SearchTree(child, pred)
    return matched_nodes
