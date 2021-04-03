from binary_tree_node import BinaryTreeNode
from test_framework import generic_test
import collections

def is_balanced_binary_tree(tree: BinaryTreeNode) -> bool:
    
    def findHeight(node, h):
        if not node:
            return h
        return max(findHeight(node.left, h+1), findHeight(node.right, h+1))
    
    def isHeightBalanced(node):
        if not node:
            return True
        return abs(findHeight(node.left,0) - findHeight(node.right,0)) <=1 and isHeightBalanced(node.left) and isHeightBalanced(node.right)
    return isHeightBalanced(tree)
    
    
if __name__ == '__main__':
    exit(
        generic_test.generic_test_main('is_tree_balanced.py',
                                       'is_tree_balanced.tsv',
                                       is_balanced_binary_tree))
