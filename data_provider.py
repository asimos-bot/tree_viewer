import pandas as pd
import numpy as np

# get database in a datastream
# keep track of which timestamp we are in
class DataProvider():

    def check_input(self, kwargs):

        # check if dataframes were given, if they are actual dataframes and if they have the same size
        if all( k in kwargs for k in ['x', 'y'] ):

            return isinstance(kwargs['x'], pd.DataFrame) and isinstance(kwargs['y'], pd.DataFrame) and kwargs['x'].shape[0] == kwargs['y'].shape[0]

        else:
            return False

    def __init__(self, **kwargs):

        # check for invalid input
        if not self.check_input(kwargs):
            raise ValueError('DataProvider expects two dataframes, \'x\' for data and \'y\' for labels')

        # save dataframes in the object
        self.x = kwargs['x']
        self.y = kwargs['y']

        # index of the history we are showing (-1 will show an empty tree)
        self.timestamp = -1

        # index of lastest example that self.timestamp has trained (so we know when to train and when to read from history)
        self.last_train = None

        # list of object to call the 'notify' method, so they know when the timestamp changed
        self.listeners = []

        # list of algorithms to call the 'train' method, so they know when to train from the current object
        self.algorithms = []

        # number of steps to make when a button is pressed
        self.steps=1

    def change_steps(self, new_step_size):

        self.steps = int(new_step_size)

    def next_object(self):

        for i in range(self.steps):

            # check if we aren't already showing the last object
            if( not self.x.shape[0] == self.timestamp ):

                self.timestamp += 1

                # train if we haven't trained anyone else or we currently showing the last object we trained on
                if( self.last_train == None or self.timestamp-1 == self.last_train ):

                    self.train()

                    if( self.last_train == None ): self.last_train = -1
                    self.last_train += 1

                self.notify()

    def previous_object(self):

        if( self.timestamp > 0 ):

            self.timestamp -= self.steps

            if( self.timestamp < 0 ):

                self.timestamp = 0

            self.notify()

    def subscribe_to_listening_list(self, obj):

        if( self.timestamp != -1 ): raise ResourceWarning('Subscribing to DataProvider after calling \'next_object\' or \'previous_object\' may cause unexpected behavior')

        self.listeners.append(obj)

    def notify(self):

        for obj in self.listeners:
            obj.notify()
    
    def subscribe_to_algorithm_list(self, obj):

        if( self.timestamp != -1 ): raise ResourceWarning('Subscribing to DataProvider after calling \'next_object\' or \'previous_object\'')

        self.algorithms.append(obj)

    def train(self):

       for obj in self.algorithms:
            obj.train()

    def get_current_object(self):

        # raise error if haven't trained on any object yet
        if( self.timestamp == -1 ): raise ResourceWarning('Can\'t get object since DataProvider hasn\'t started fetching them')

        return {
                'x': self.x.iloc[[self.timestamp]].to_numpy(),
                'y': self.y.iloc[[self.timestamp]].to_numpy()[0],
                'timestamp': self.timestamp
               }

    def get_timestamp(self):

        return self.timestamp
