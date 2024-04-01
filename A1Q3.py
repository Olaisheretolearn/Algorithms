# your name
# your student ID

'''Conduct an experimental study to compare the speed of AVL tree, (2,4) tree, 
and red-black tree implementations when subjected to ordered or 
reversed ordered sequences of operations (set, get, delete).'''

from A1Q1 import TreeMap24 as TM24
from avl_tree import AVLTreeMap as AVLTM
from red_black_tree import RedBlackTreeMap as RBTM
import sys
sys.setrecursionlimit(100000) 

# Write your code below

'''
Expected results:

order:
TM24: 0.05624103546142578
AVLTM: 0.08055496215820312
RBTM: 0.09287714958190918
revers order:
TM24: 0.06696105003356934
AVLTM: 0.08003783226013184
RBTM: 0.09322094917297363
'''