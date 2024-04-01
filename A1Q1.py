# your name
# your student ID

class TreeMap24:
    BLANK=object()                  # in down_split method, substitute other node
    class Position:
        ''' position class'''
        def __init__(self,node,container):
            self._node=node
            self._container=container

        def element(self):
            ''' return value of position '''
            return self._node._value

        def key(self):
            return self._node._key

        def __eq__(self,other):
            return type(self)==type(other) and self._node is other._node
    #
    class _Node:
        ''' creat the link node,'''
        #                         _parent    
        #                            |  
        #                 _before - node - _after
        #                            |
        #                         _child

        def __init__(self,k,v,before=None,after=None,parent=None,child=None):
            self._key=k
            self._value=v
            self._before=before
            self._after=after
            self._parent=parent
            self._child=child
        #--------------------------convennient the node------------------------        
        def __eq__(self,k):
            ''' return true, if k==self._key'''
            if type(k) ==int:
                return self._key==k
            elif isinstance(k,type(self)):
                return self._key==k._key
            
        def __nq__(self,k):
            return not self==k

        def __lt__(self,k):
            ''' return true if k < self._key'''
            if type(k) ==int:
                return self._key<k
            elif isinstance(k,type(self)):
                return self._key<k._key
        
        def __gt__(self,k):
            return not self<k and self!=k

        def __le__(self,k):
            return self<k or self == k

        def __ge__(self, k):
            return self>k or self ==k
    #--------------------------------
    def __init__(self):
        ''' root return the first node'''
        self._root=None
        self._size=0

    def _validate(self,p):
        ''' Return associated node, if position is valid.'''
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:      # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self,node):
        ''' return position of node '''
        return self.Position(node,self) if node != None else None
    
    def _add_after(self,p,temp,head_node=None):
        ''' add a node after p,p is Position class;
            reconect node's after,before parent,without child.
        '''
        node=self._validate(p)
        # temp's before is node,after is node's after
        #,parent is node's parent
        temp._before=node
        temp._after=node._after
        temp._parent=node._parent
        node._after = temp
        if temp._after is not None:
            temp._after._before=temp
        if head_node is not None:
            while temp is not None:  # repoint child's parent，_add_beofre method can't repoint
                subnode = temp._child
                while subnode is not None:
                    subnode._parent = head_node
                    subnode = subnode._after
                temp = temp._after
        return self._make_position(temp)

    def _add_before(self,p,temp,head_node=None):
        ''' this method can only be used for p which before node is none;
            add a node before p,p is Position and head node;
            temp is a _Node;
            head_node is _Node class;
            reconnect node's child,parent'before and after.
        '''
        node=self._validate(p)
        # temp's before is node._before,after is node,
        #parent is node._parent
        if temp._before is not None and temp._child is None:  # in case 2.1 of down_split method
            temp._child=node._before
        else:
            temp._before=node._before
        temp._after=node
        temp._parent=node._parent
        node._before=temp
        parent=self.parent(p)
        if parent is None:
            self._root=temp
        else:
            parent=self._validate(parent)
            if parent._before is node:
                parent._before = temp
            if parent._child is node:
                parent._child = temp
        tempnode=temp
        if head_node is not None:
            while tempnode is not None:  # repoint child's parent，
                subnode = tempnode._child
                while subnode is not None:
                    subnode._parent = head_node
                    subnode = subnode._after
                tempnode = tempnode._after
        return self._make_position(temp)   # now temp is the head
    
    def _add(self,p,k,v,head):
        ''' add a node in a proper posiiton '''
        node=self._validate(p)
        temp=self._Node(k,v)
        self._size+=1
        if node < k:
            self._add_after(p,temp)
            self._up_split(head)
        else:
            self._up_split(self._add_before(p,temp,temp))

    def _search(self,k,head=None,node=None):
        ''' return the proper Position and head if chain's child is None;
            find begin of root if node is None
            head and node are _Node class
        '''
        if node is None:
            node=self._root
            head=node
        #print(node,k,self._root)
        if node>k:                  # recursion to node's before
            if node._before is None:# break the cursion if there is none child
                return self._make_position(node),self._make_position(head)
            return self._search(k,node._before,node._before)
        if node==k:                 # break the cursion
            return self._make_position(node),self._make_position(head)
        if node<k:                  # recursion to node's after
            if node._after is not None:     # if there is item after node
                if k<node._after:           # node<k<node._after
                    if node._child is None: # node is the last node
                        return self._make_position(node),self._make_position(head)
                    return self._search(k,node._child,node._child)
                else:                       # noke._after <k
                    return self._search(k,head,node._after)
            else:
                if node._child is None:     # if node is last Position
                    return self._make_position(node),self._make_position(head)
                return self._search(k,node._child,node._child)

    def _up_split(self,head):
        ''' head is a Position class'''        
        if self.is_filled(head):
            node=self._validate(head)
            mid=node._after._after  # split in to three parts, (node,mid,p2)
            p2=mid._after           # p2 is the mid's child            
            parent=node._parent
            # combine the tree parts
            node._after._after=None
            p2._before=mid._child
            mid._child=p2
            p2._parent = parent      # if parent is None , p2._parent is mid
            temp=p2._before
            while temp is not None:# p2 became a head node ,repoint child and child._after
                temp._parent=p2
                temp=temp._after
            temp=p2._child
            while temp is not None:
                temp._parent = p2
                temp=temp._after
            # find the proper position for mid
            if parent is not None:  # if node isn't root
                parent=self._validate(self.parent(self._make_position(node)))# get the parent node
                if parent>mid:
                    if parent._before is node:# if mid add to the head ,the node and p2 's parent should be mid
                        self._add_before(self._make_position(parent),mid,mid)
                        node._parent=mid
                        node._after._parent=mid
                        return self._up_split(self._make_position(mid))
                    mid._before=parent._before
                    if mid._before is not None:
                        mid._before._after=mid
                    mid._after=parent
                    parent._before=mid
                    mid._parent=parent._parent                                                
                if parent<mid:
                    self._add_after(self._make_position(parent),mid)
                return self._up_split(self._make_position(node._parent))# Prevent overflow from passing upwards
            else: # if node is root
                # make mid is the root
                self._root=mid
                mid._before=node
                mid._after=None
                mid._parent=None
                # the node and p2 's parent should be mid
                node._parent=mid
                node._after._parent=mid
                p2._parent=mid

    def _pop(self,p,head):
        # warrring pop need to be devided in to situations
        ''' cut all links related p;
            p is the Position;
            p._before will be p._after._before and the p._child need to be None
        '''
        node=self._validate(p)
        after=node._after
        if after is not None:     
            before=node._before
            self._pointer_repoint(self._make_position(node._after),p,head)
            after._before=before    # repoint node's after node, node._after._before node
        else:
            self._pointer_repoint(None,p,head)

        return self._make_position(node)

    def _replace(self,p,position,head):
        ''' substitue position for p and return position '''
        node=self._validate(p)
        p_node=self._validate(position)
        if p_node._parent is not node:
            node._parent=p_node._parent
        node._child=p_node._child
        node._before=p_node._before
        node._after=p_node._after
        self._pointer_repoint(p,position,head)
        return position

    def _pointer_repoint(self,p,position,head):
        ''' the pointer to position repoints p ；
            when p is root and p.after is not empty,let p.after be root
        '''
        if p is not None:                   # in case p is None,when _pop() method
            node=self._validate(p)
        else:
            node = None
        p_node=self._validate(position)
        if p_node is self._root:                # if position is root node
            self._root=node
        if position == head:                   # repoint node's child and parent
            parent=self._validate(self.parent(position)) if p_node._parent is not None else None
            # all of child repoint to node
            temp = p_node._before       # before fraction
            while temp is not None:
                temp._parent = node
                temp = temp._after
            temp_node = p_node      # child fraction
            while temp_node is not None:
                temp = temp_node._child
                while temp is not None:
                    temp._parent = node
                    temp = temp._after
                temp_node = temp_node._after
            if parent is not None:          # repoint parent's child
                if parent._before is p_node:
                    parent._before=node
                else:
                    parent._child=node
        else:                              # if node is not head
            p_node._before._after=node
        if p_node._after is not None:     # repoint node's after node, node._after._before node
            p_node._after._before =node
        p_node._parent=None
        p_node._after=None
        p_node._before=None
        p_node._child=None

    def _brother(self,p,r=True):
        ''' return p's brother node;
            if r is Flase,denote the method working for recursion；
        '''
        node=self._validate(p)
        parent=self._validate(self.parent(p))
        parent_h=node._parent
        if parent._before is node:      # get brother
            brother=parent._child
            brother_head=brother
        else:
            brother1=parent._before if parent is parent_h else parent._before._child
            brother_head =brother1
            while brother1._after is not None:
                brother1=brother1._after
            if r:
                brother2=parent._after._child if parent._after is not None else None
                if not self.is_singular(self._make_position(brother2)) and self.is_singular(self._make_position(brother_head)):# let len less node be brother
                    brother = brother2
                    brother_head=brother2
                else:
                    brother=brother1
            else:
                brother=brother1
        return self._make_position(brother),self._make_position(brother_head)

    def _down_split(self,position,r=True):
        ''' cut chain of position ;
            case 1 :
                    position's brother is not singular
            case 2 :
                    position's brother is singular
                    case 2.1 :
                        position's parent is singular  (this way need recursion)
                    case 2.2 :
                        position's parnet is not singual
        '''
        node = self._validate(position)
        parent=self._validate(self.parent(position))
        parent_h=node._parent           # parent_h is parent's head
        brother,brother_head=self._brother(position,r)
        brother=self._validate(brother)
        if not self.is_singular(brother_head) and r:        # case 1
            brother_parent=self.parent(brother_head)
            temp1=self._pop(self._make_position(brother),brother_head)
                # replace temp1 with parent
            if node>brother:        # there are different parents when different size relationship of brother and node
                temp2=self._replace(temp1,self._make_position(parent),self._make_position(parent_h))
            else:
                temp2 = self._replace(temp1, brother_parent, self._make_position(parent_h))
               # replace temp2 with position
            temp3=self._replace(temp2,position,position)
            return temp3
        else:                                       # if brother is singular,case 2
            if self.is_singular(self._make_position(parent_h)):              # case 2.1
                blank_node=self._Node(parent._key,TreeMap24.BLANK)
                blank=self._make_position(blank_node)
                temp1=self._replace(blank,self._make_position(parent),self._make_position(parent))   # replace parent Position
                self._replace(temp1,position,position)            # replace position with parent
                if brother>parent:
                    blank_node._before = None
                    self._add_before(self._make_position(brother),parent,parent)
                    brother_head = self._make_position(parent)
                    if blank_node<blank_node._parent:# Deal with the before and child value issues of blank nodes
                        blank_node._before,blank_node._child=blank_node._child,blank_node._before
                else:
                    blank_node._child=None
                    self._add_after(self._make_position(brother),parent,self._validate(brother_head))
                    if blank_node>blank_node._parent:# Deal with the before and child value issues of blank nodes
                        blank_node._before, blank_node._child = blank_node._child, blank_node._before
                if blank_node._parent is None:                  # if blank is root
                    blank_node._before=blank_node._child if blank_node._child is not None else blank_node._before   # incase pop the node
                    blank_node._child=None
                    self._pop(blank,blank)
                    self._root=self._validate(brother_head) if self._validate(brother_head)<parent else parent
                    return self.root()
                # in case node is filled
                if self.is_filled(brother_head):
                    blank_node._before, blank_node._child = blank_node._child, blank_node._before
                    self._up_split(brother_head)
                    if parent<brother and blank_node._before is None:      # let new node be the _before of blank_node
                        blank_node._before=blank_node._child
                    blank_head=blank if blank_node<brother else self._make_position(blank_node._before)
                    self._pop(blank,blank_head)
                    return
                return self._down_split(blank,False)
            else:                                # if parent is not sigular ,case 2.2
                TEMP=self._make_position(self._Node(TreeMap24.BLANK,TreeMap24.BLANK))    # TEMP  uesed to repalce parent node
                self._replace(TEMP,self._make_position(parent),self._make_position(parent_h))  # parent Position
                res=self._replace(self._make_position(parent),position,position)               # position Position
                if brother > parent:        # add the older parent to brother
                    self._add_before(self._make_position(brother),parent,parent)
                    brother_head=self._make_position(parent)

                else:
                    self._add_after(self._make_position(brother),parent,self._validate(brother_head))
                if parent_h is parent:              # delete temp
                    if parent<brother:              # let new node be the left node of TEMP
                        TEMP._node._before=TEMP._node._child  # for _pop mtehod
                    TEMP._node._child=None          # let parent._before be parent._after._before for the pop method
                    parent_h=TEMP
                else:
                    parent_h=self._make_position(parent_h)
                self._pop(TEMP,parent_h)
                self._up_split(brother_head)
                return self._make_position(res)

    def _subnode(self,p,head):
        ''' find the subnode which should lt p of p  '''
        node = self._validate(p)
        if p == head:
            temp=node._before
        else:
            temp=node._before._child
        head=temp
        if temp is not None:
            while temp._after is not None or temp._child is not None:
                while temp._after is not None:
                    temp = temp._after
                if temp._child is not None:
                    temp=temp._child
                    head=temp
            return self._make_position(temp),self._make_position(head)
        else:
            return None,None

    def _before(self,p,head):
        ''' p is position ,head is p's head and a position;
            return position and head,position less than p 
        '''
        node=self._validate(p)   # find a proper subtree to search
        if node._before is None:   # node is leaf node
            if node._parent is None:                         # if p is the root node
                return None,None
            head=node._parent
            temp=self._validate(self.parent(p))
            while temp._before is node: # looking up to the top, find the before the node
                node=temp
                head=temp._parent
                temp=self._validate(self.parent(self._make_position(temp)))
                if temp is None:                            # if p is the leftmost node
                    return None,None
            if temp._before is not node:
                return self._make_position(temp),self._make_position(head)
        else:
            temp=node._before         # temp is the target node
            if p == head :         # if p is not head node
                return self._search(node._key, temp, temp)
            elif temp._child is not None:
                temp=temp._child
                return self._search(node._key, temp, temp)
            else:
                return self._make_position(temp),head


    def _next(self,p,head):
        ''' p is position ,head is p's head and head is position
             return position and head,position great than p
        '''
        node=self._validate(p)
        if node._child is not None:
            return self._search(node._key,node._child,node._child)
        if node._after is not None:
            return self._make_position(node._after),head
        temp=self._validate(self.parent(head))     # parent's child or before node is head
        head=self._make_position(node._parent)                          # get the parent 's head
        while temp<=node:                       # lookup the parent's node
            if temp._after is not None:         # if the parent has after node to return it, else travel to the top of the tree
                return self._make_position(temp._after),head
            head,temp=self._make_position(temp._parent),self._validate(self.parent(head))
        return self._make_position(temp), head

    def _generate(self,p,head):
        ''' recuisively yield _Node;
            n,head are class _Node;
            if return whole tree,p and head should convey both self._root.
        '''
        if p is None:
            return
        if p is head:
            for i in self._generate(p._before,p._before):
                yield  i
        yield self._make_position(p)
        for i in self._generate(p._child,p._child):
            yield i
        for i in self._generate(p._after,head):
            yield i

    def _get_head(self,n):
        ''' n is a Position, returning a node that is a Position '''
        n=self._validate(n)
        if n._child is not None:
            return self._make_position(n._child._parent)
        else:
            while n._before is not None:
                n=n._before
            return self._make_position(n)
            
    def __len__(self):
        return self._size
    
    def __setitem__(self,k,v):
        if len(self)==0:
            self._root=self._Node(k,v)
            self._size+=1
            return
        node,head=self._search(k)   # get the position and head
        if node.key()==k:
            node._node._value=v
        else:
            self._add(node,k,v,head)

    def __delitem__(self,k):
        position,head=self._search(k)           # delete node
        self._size-=1
        if position.key() !=k:
            raise KeyError('key warring')
        subs,subs_head=self._subnode(position,head)
        if subs is not None:                # dispose the position
            if self.is_singular(subs_head):
                self._down_split(subs)
                if self._validate(position)._parent is not None:    # in case head is changed,research position
                    t,head=self._search(position.element(),self._validate(position)._parent,self._validate(position)._parent)
                else :
                    t,head=position, self.root()
            else:
                self._pop(subs,subs_head)
            return self._replace(subs, position, head)
        else:
            if self.root()==position:       # if tree only has root node
                self._pop(position,position)
                self._size=0
                return
            else:
                if self.is_singular(head):  # if position is a leaf node , a head
                    return self._down_split(position)
                else:
                    return self._pop(position,head)
    
    def __getitem__(self, k):
        ''' return value of Position which key ==k,
            raise KeyError if k not find
         '''
        p,head=self._search(k)
        if p.key()==k:
            return p.element()
        else:
            raise KeyError('invalid key')

    def __contains__(self, k):
        p,head=self._search(k)
        if p.key()==k:
            return True
        else:
            return False

    def __iter__(self):
        for i in self._generate(self._root,self._root):
            yield i.element()

    def get(self, k, d):
        ''' if k is found return k.element else return d'''
        p,head=self._search(k)
        return p.element() if p.key()==k else d

    def is_filled(self,head):
        ''' return True, If the head is connected to two nodes'''
        head=self._validate(head)
        n=1
        while head._after is not None:
            head=head._after
            n+=1
        return n==4         # 4 is the  maxinum

    def is_singular(self,head):
        if head is None:
            return True        
        node=self._validate(head)
        return node._after is None

    def root(self):
        return self._make_position(self._root)

    def parent(self,p):
        ''' find p's parent position;
            p have to be  a head node.
        '''
        node=self._validate(p)
        parent=node._parent
        if parent is None:
            return None
        while not ( parent._before is node or parent._child is node):   # may
            parent=parent._after            
        return self._make_position(parent)

    def items(self):
        return [(i.key(),i.element()) for i in self._generate(self._root,self._root)]
    
    def pop(self,k,d=None):
        if d is None:
            raise KeyError('d have be not None')
        try:
            self.__delitem__(k)
        except KeyError:
            return d

    def popitem(self):
        import random
        seed=random.randint(0,len(self))                            
        for i in self._generate(self._root,self._root):
            if seed == 0:
                break           
            seed-=1
        self.__delitem__(i.key())
        return (i.key(),i.element())
    
    def setdefault(self,k,d):
        if len(self)==0:
            self._root=self._Node(k,d)
            self._size+=1
            return
        node,head=self._search(k)   # get the position and head
        if node.key()==k:
            return node.element()
        else:
            self._add(node,k,d,head)

    def find_min(self):
        ''' return first node of _generate'''
        temp=next(self._generate(self._root,self._root))
        return temp.key(),temp.element()
    
    def find_max(self):
        ''' find the last and rightmost node'''
        temp=self._root
        while temp._after is not None:
            temp=temp._after
        while temp._child is not None:
            temp=temp._child
            while temp._after is not None:
                temp=temp._after
        return temp._key,temp._value
        
    def find_lt(self,k):
        p,h=self._search(k)
        if p.key()==k:
            p,h=self._before(p,h)
        return p.key(),p.element()
    
    def find_le(self,k):
        p,h=self._search(k)
        return p.key(),p.element()
    
    def find_gt(self,k):
        p,h=self._search(k)
        p,h=self._next(p,h)
        return p.key(),p.element()
            
    def find_ge(self,k):
        p,h=self._search(k)
        if p.key()!=k:
            p,h=self._next(p,h)
        return p.key(),p.element()

    def find_range(self,start,stop=None):
        ''' start and stop is key '''
        if stop==None:
            stop=start
            start=self.first().key()    # define the initial number of start
        if stop < start or stop>len(self):
            raise IndexError('parameter is invalid')
        nex,h=self._search(start)    # find the first node
        while 1:            # get the next node in cycles
            yield nex.element()
            if nex.key()< stop-1:
                nex,h=self._next(nex,h)
            else:
                break

    def reversed(self):
        ''' return k all of the tree that reversed iter '''
        walk=self.last()
        head=self._get_head(walk)
        yield walk.element()
        for i in range(len(self)-1):
            walk,head=self._before(walk,head)
            yield walk.element()

    def first(self):
        ''' Return the first Position in the tree (or None if empty).'''
        # Write your code below
        raise NotImplementedError('Write you code to replace this raise')


    
    def last(self):
        ''' Return the last Position in the tree (or None if empty).'''
        # Write your code below
        raise NotImplementedError('Write you code to replace this raise')

        
    def before(self,p):
        ''' Return the Position just before p in the natural order.
        Return None if p is the first position.'''
        # Write your code below
        raise NotImplementedError('Write you code to replace this raise')



        
    def after(self,p):
        '''Return the Position just after p in the natural order.
        Return None if p is the last position.'''
        # Write your code below
        raise NotImplementedError('Write you code to replace this raise')



    def find_position(self,k):
        ''' if k in the tree return a Position that belong k, else raise Error'''
                ''' if k in the tree return a Position that belong k, else raise Error'''
        p,h=self._search(k)
        if p.key()==k:
            return p
        else:
            raise KeyError('invalid key')

