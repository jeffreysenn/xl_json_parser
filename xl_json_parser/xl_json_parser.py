from openpyxl import Workbook
from openpyxl import load_workbook
import json
from enum import Enum

from node import SearchTree
from xl_node import*

def IsRowEmpty(row):
    for cell in row:
        if cell.value != None:
            return False
    return True

def FindEmptyRowIdx(rows):
    for i, row in enumerate(rows):
        if IsRowEmpty(row):
            return i
    return -1

def SplitSpecDataRows(rows):
    ept_row_idx = FindEmptyRowIdx(rows)
    spec_rows = rows[:ept_row_idx]
    data_rows = rows[ept_row_idx + 1:]
    return spec_rows, data_rows

def BuildNodes(row):
    nodes = []
    for i, cell in enumerate(row):
        if cell.value:
            node = XlNode()
            node.SetName(cell.value)
            node.SetCol(i)
            nodes.append(node)
    return nodes

def BuildLayeredNodes(rows):
    node_lists = []
    for row in rows:
        nodes = BuildNodes(row)
        node_lists.append(nodes)
    return node_lists

def BuildTree(rows):
    layered_nodes = BuildLayeredNodes(rows)
    root = RootNode()
    for i, nodes in enumerate(layered_nodes):
        for j, node in enumerate(nodes):
            parent_node = root
            if i != 0:
                for node_abv in layered_nodes[i - 1]:
                    if node.GetCol() >= node_abv.GetCol():
                        parent_node = node_abv
            node.AttachTo(parent_node)
    ApplyRule(root)
    # PrintNames(root)
    return root

def WriteData(rows, tree):
    tree.Build()
    for row in rows:
        for i, cell in enumerate(row):
            if cell.value:
                node = SearchTree(tree, lambda node: node.GetCol() == i)[0]
                if isinstance(node, IdxNode):
                    node.AddNewItem()
                elif isinstance(node, ObjNode):
                    node.WriteVal(cell.value)

def main():
    # path = input("Enter the xl file path: ")
    path = ("xl/test.xlsx")
    dict = {}
    wb = load_workbook(path, read_only = True)
    for ws in wb:
        print("parsing %s" % ws.title)
        rows = tuple(ws.rows)
        spec_rows, data_rows = SplitSpecDataRows(rows)
        tree = BuildTree(spec_rows)
        WriteData(data_rows, tree)
        print(tree.GetDict())



main()