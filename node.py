import tkinter
from skmultiflow.trees.nodes import SplitNode
from skmultiflow.rules.base_rule import Rule
from operator import itemgetter
import copy

# class to save a Rule and the nodes childs
class Node():

    def __init__(self, real_node):

        self.children=dict()
        self.rule = self._get_rule(real_node)
        self.label = None
        self.frame = None
        self.child_frame = None

        # build subtree
        self._build_subtree(real_node)

    def _get_rule(self, node):

        rule = Rule()

        if isinstance(node, SplitNode):
            for i, child in node._children.items():
                predicate = node.get_predicate(i)
                r = copy.deepcopy(rule)
                r.predicate_set.append(predicate)
                return r
        else:
            rule.observed_class_distribution = node.get_observed_class_distribution().copy()
            rule.class_idx = max(node.get_observed_class_distribution().items(), key=itemgetter(1))[0]
            return rule
        
    def _build_subtree(self, node):

        if( isinstance(node, SplitNode) ):

            left = node.get_child(0)
            if( left ):
                self.children['left'] = Node(left)

            right = node.get_child(1)

            if( right ):
                self.children['right'] = Node(right)

    def build_widget(self, master, direction=tkinter.TOP):

        if( self.frame != None ): self._destroy()

        # create frame
        self.frame = tkinter.Frame(master, borderwidth=1, highlightcolor='red')
        self.frame.pack( side = direction)

        # create label text
        self.label = tkinter.Label(self.frame, text=str(self.rule))
        self.label.pack( side = tkinter.TOP )

        # build widget for each subtree
        for key, child in self.children.items():

            child.build_widget(self.frame, tkinter.LEFT if key == 'left' else tkinter.RIGHT)

    def _destroy(self):

        self.label.destroy()
        self.label=None

        self.frame.destroy()
        self.frame=None

    def destroy(self):

        # destroy leaves first
        if( self._is_leaf() ):
            self._destroy()
        else:
            for key, value in self.children:
                if( value != None ): value.destroy()
            self._destroy()

    def _is_leaf(self):

        return self.children.get('left', False) and self.children.get('right', False)
