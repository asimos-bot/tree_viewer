import tkinter
import pandas as pd
from data_provider import DataProvider
from navbar import Navbar
from tree import Tree

class Viewer():

    def __init__(self, data_filename, labels_filename):

        # initialize tkinter
        self.tk= Tk()

        # get database in a pandas dataframe
        data = pd.read_csv(data_filename)
        labels = pd.read_csv(labels_filename)

        # create data provider, give the pandas dataframes as argument
        self.provider = DataProvider(x=data, y=labels)

        # create navbar object, give data provider and tkinter object (to add the navbar widget to it) as argument
        self.navbar = Navbar(tk=self.tk, provider=self.provider)

        # create tree object, give data provider and tkinter object (to add the tree widget to it) as argument
        self.tree = Tree(tk=self.tk, provider=self.provider)

        # initialize tkinter main loop
        self.tk.mainloop()

if( __name__ == "__main__" ):

    Viewer("../movingSquares.data", "../movingSquares.labels")
