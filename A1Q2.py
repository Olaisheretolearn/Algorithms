# your name
# your student ID

from red_black_tree import RedBlackTreeMap as RBT
from A1Q1 import TreeMap24 as TM2
from queue import Queue

class Convert(RBT,TM2):
    ''' convert RedBlackTree to TreeMap24 or covert TreeMap24 to RedblackTree '''
    def __init__(self):
        if 'y'==input('Convert 24Tree to RedBlackTree pressing y else pressing others: '):
            self._tree=TM2()
            self._arm=RBT()
        else:
            self._tree=RBT()
            self._arm=TM2()
        self._rbt=Queue()
        self._tm=Queue()

    def __getitem__(self,k):
        return self._tree[k]

    def __setitem__(self,k,v):
        self._tree[k]=[v]

    def _convertRBT(self,chain):
        ''' convert 24Tree's node to RedBlackTree;
            return black node
            chain is a _Node of 24Tree;
            consider 3 cases;
                case1: it's a 4-node;
                case2: it's a 3-node;
                case3: It's a 2-node.
        '''
        first=RBT._Node(RBT._Item(chain._key,chain._value))
        second=RBT._Node(RBT._Item(chain._after._key,chain._after._value)) if chain._after is not None else None
        third=RBT._Node(RBT._Item(chain._after._after._key,chain._after._after._value)) if (chain._after is not None and chain._after._after is not None)else None
        # Write your code below 














     
            
    def _combine(self,parent,child,right=True):
        ''' combine parent and right child if right is True,else combine parent and left child ;
            parent and child is _Node of RedBlackTree.
        '''
        if right:
            parent._right=child
        else:
            parent._left=child
        child._parent=parent

    def _circleRBT(self):
        ''' control 24Tree converting to RedBlackTree '''
        if self._tm.empty():
            return
        walk=self._tm.get()
        res = self._convertRBT(walk)
        if walk._before is not None:            # if walk is leaf node return
            self._tm.put(walk._before)          # else put child to self._tm
            while walk is not None:             
                self._tm.put(walk._child)
                walk=walk._after
        black=res
        if black==self._arm._root:return        # Don't conbine the walk when first allocate the method
        info=self._rbt.get()
        if info[1]=='r':
            self._combine(info[0],black)
        else:
            self._combine(info[0],black,False)

    def _convertTM(self,black):
        ''' convert node of RedBlackTree to 24Tree node;
            put position to _tm
        '''
        second=TM2._Node(black._element._key,black._element._value)
        first=TM2._Node(black._left._element._key,black._left._element._value) if (black._left is not None and black._left._red) is True else None
        third=TM2._Node(black._right._element._key,black._right._element._value) if (black._right is not None and black._right._red)is True else None
        second._before=first
        second._after=third
        if self._tm.empty():                    # set root node
            self._arm._root=first if first is not None else second
        head=second
        if first is not None:
            head=first
            first._after=second
            self._tm.put((first,False,head))         # put (first,judge) to _tm, if the judge is Ture meaning _before node
            self._tm.put((first,True,head))
        else:
            self._tm.put((second,False,head))
        if third is not None:
            third._before=second
            self._tm.put((third,False,head))
            self._tm.put((third,True,head))
        else:
            self._tm.put((second,True,head))
        return head

    def _combineTM(self,parent,head,child,right):
        ''' In a 24Tree,conbine child to its parent's child,if parameter right is True '''
        if right:
            parent._child=child
        else:
            if head is not parent:                      # case in 2node or 3node
                parent._before._child=child
            else:                                       # case in 1node
                parent._before=child
        while child is not None:        # repoint to parent
            child._parent=head
            child=child._after

    def _circleTM(self):
        walk=self._rbt.get()
        res = self._convertTM(walk)
        if walk._left is not None :
            if walk._left._red is True:                 # if walk._left is red
                if walk._left._left is not None:            
                    self._rbt.put(walk._left._left)     # this node have to be a black
                    self._rbt.put(walk._left._right)
            else:
                self._rbt.put(walk._left)
        if walk._right is not None:
            if walk._right._red is True:
                if walk._right._left is not None:
                    self._rbt.put(walk._right._left)
                    self._rbt.put(walk._right._right)
            else:
                self._rbt.put(walk._right)
        parent=res
        if parent==self._arm._root:return        # Don't conbine the walk when first allocate the method
        info=self._tm.get()
        self._combineTM(info[0],info[2],parent,info[1])

    def changeTM(self):
        ''' convert RedBlackTree to 24Tree '''
        if len(self._tree)==0:
            raise ValueError('There is no item.')
        self._rbt.put(self._tree._root)
        while not self._rbt.empty():
            self._circleTM()
        self._arm._size=self._tree._size        # set size of arm
    
    def arm(self):
        return self._arm

    def tree(self):
        return self._tree

    def changeRBT(self):
        ''' convert 24Tree to RedBlackTree'''
        if len(self._tree)==0:
            raise ValueError('There is no item.')
        self._tm.put(self._tree._root)
        while not self._tm.empty() :
            self._circleRBT()
        self._arm._size=self._tree._size        # set size of arm

# # test 24 to RBT
# t=Convert()
# for i in range(100):
#    t[i]=str(i)
# t.changeRBT()
# a=[i for i in t.arm().__iter__()]
# for i in range(100):                # text if equal
#     if i not in a:
#         print(i,'*')

# # test RBT to 24
# t = Convert()
# for i in range(100):
#    t[i]=str(i)
# t.changeTM()
# a=[i for i in t.arm().__iter__()]
# print(a)
