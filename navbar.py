import tkinter
from data_provider import DataProvider

# builds navbar widget
# controls DataProvider timestamp
# shows database object that will be evaluated and the ones that already got evaluated (the one in the center is the next to be evaluated)
# small steps -> see how example traverse the tree
# big steps -> see how example impact the tree after traversing it
class Navbar():

    def check_input(self, kwargs):

        if all( k in kwargs for k in ['tk', 'provider'] ):

            return isinstance(kwargs['tk'], tkinter.Tk) and isinstance(kwargs['provider'], DataProvider)

    def __init__(self, **kwargs):

        if not self.check_input(kwargs):
            raise ValueError('Navbar expects two arguments: \'tk\', a Tkinter object, and \'provider\' a DataProvider object')

        # save arguments
        self.tk = kwargs['tk']
        self.provider = kwargs['provider']

        # subscribe to notification list (navbar's 'notify' method is called when timestamp change in 'DatsProvider')
        self.provider.subscribe_to_listening_list(self)

        # where we save the label from the widget
        self.object_label=None
        
        # where we save the scale that determine the step size
        self.scale=None

        # where we save the buttons from the widget
        self.buttons = []

        # where we save the description label
        self.description_label=None

        # build widget and give it to tk
        self.build_widget()

    def _build_object_label(self, master, timestamp, x, y):

        self.object_label = tkinter.Label(master, text="x={}\ny={}\n{}".format(x, y, timestamp))
        self.object_label.pack( side = tkinter.TOP )

    def _build_scale(self, master):

        self.scale = tkinter.Scale(master, orient='horizontal', from_=1, to=1000, command=self.provider.change_steps)
        self.scale.pack( side = tkinter.BOTTOM, fill = tkinter.X )

    def _build_buttons(self, master):

        frame = tkinter.Frame(master)
        frame.pack( side = tkinter.BOTTOM )

        button_previous = tkinter.Button(frame, text='<-', command=self.provider.previous_object)
        button_previous.pack( side = tkinter.LEFT )

        button_next = tkinter.Button(frame, text='->', command=self.provider.next_object)
        button_next.pack( side = tkinter.RIGHT )

        self.buttons.append(button_previous)
        self.buttons.append(button_next)

    def _build_label_description(self, master):

        frame = tkinter.Frame(master)
        frame.pack( side = tkinter.BOTTOM )

        self.description_label = tkinter.Label(frame, text="If condition is True, proceed to the right branch. If False, proceed to the left.\nChange scale value to increase/decrease step size.")
        self.description_label.pack( side = tkinter.BOTTOM )

    def build_widget(self):

        # get frame in the top
        frame = tkinter.Frame(self.tk)
        frame.pack( side = tkinter.TOP, fill = tkinter.X )

        # build label in the center of the frame
        self._build_object_label(frame, None, None, None)

        # build scale that determine the size of the steps
        self._build_scale(frame)

        # build buttons just below the label
        self._build_buttons(frame)

        # build tree description label
        self._build_label_description(frame)

    def notify(self):
        
        obj = self.provider.get_current_object()

        self.object_label['text'] = "x={}\ny={}\n{}".format(obj['x'], obj['y'], obj['timestamp'])
