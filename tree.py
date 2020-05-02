import tkinter
import skmultiflow

if( skmultiflow.__version__ == '0.4.1' ):
    from skmultiflow.trees import HATT as TreeClass
else:
    from skmultiflow.trees import ExtremelyFastDecisionTreeClassifier as TreeClass

from data_provider import DataProvider
from node import Node

# posses the ExtremelyFastDecisionTreeClassifier object from multiflow that will do the actual learning
class Tree():

    def check_input(self, kwargs):

        if all( k in kwargs for k in ['tk', 'provider'] ):

            return isinstance(kwargs['tk'], tkinter.Tk) and isinstance(kwargs['provider'], DataProvider)

    def __init__(self, **kwargs):

        if not self.check_input(kwargs):
            raise ValueError('Tree expects two arguments: \'tk\', a Tkinter object, and \'provider\' a DataProvider object')

        # save arguments
        self.tk = kwargs['tk']
        self.provider = kwargs['provider']

        # subscribe to algorithm and listeners lists
        self.provider.subscribe_to_listening_list(self)
        self.provider.subscribe_to_algorithm_list(self)

        # list to save all tree states (store root nodes)
        self.history = []
        self.current_timestamp = -1

        # get the actual ExtremlyFastDecisionTreeClassifier here
        self.tree = TreeClass()

        # master frame
        self.frame = tkinter.Frame(self.tk, highlightthickness=5, highlightbackground='black', bd=0)
        self.frame.pack( side = tkinter.TOP, fill = tkinter.BOTH )

    def _save_tree_state(self):

        self.history.append(Node(self.tree._tree_root))

    def notify(self):

        # destroy previous widgets
        if( self.current_timestamp != -1 ): self.history[self.current_timestamp].destroy()

        # update 'self.current_timestamp' and build widgets for the new timestamp
        self.current_timestamp = self.provider.get_timestamp()
        self.history[self.current_timestamp].build_widget(self.frame)

    def train(self):
        
        # just save the new tree state to 'self.history', 'notify' will take care of the widget

        # train tree using current object
        obj = self.provider.get_current_object()
        self.tree.partial_fit(obj['x'], obj['y'])

        # save new tree
        self._save_tree_state()
