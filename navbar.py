from tkinter import Tk
from data_provider import DataProvider

# builds navbar widget
# controls DataProvider timestamp
# shows database object that will be evaluated and the ones that already got evaluated (the one in the center is the next to be evaluated)
# small steps -> see how example traverse the tree
# big steps -> see how example impact the tree after traversing it
class Navbar():

    def check_input(self, kwargs):

        if all( k in kwargs for k in ['tk', 'provider'] ):

        return isinstance(kwargs['tk'], Tk) and isinstance(kwargs['provider'], DataProvider)

    def __init__(self, **kwargs):

        if not self.check_input(kwargs):
            raise ValueError('Navbar expects two arguments: \'tk\', a Tkinter object, and \'provider\' a DataProvider object')

        # save arguments
        self.tk = kwargs['tk']
        self.provider = kwargs['provider']

        # build widget and give it to tk
        self.build_widget(self.tk)

    def build_widget(self);
