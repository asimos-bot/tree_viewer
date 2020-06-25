# Tree Viewer

Little project to show the layout of the ExtremelyFastDecisionTree (or HATT)
in the [scikit-multiflow](https://scikit-multiflow.github.io/) library.

# Motivation

The idea is to better visualize how the tree grows overtime and with
what rules.

# Installation

Just install the dependencies at `requirements.txt` with `pip`:

```
pip install -r requirements.txt
```

# How To Use?

To use it, just pass your dataset as a `.data` and `.labels` files to
the `Viewer` class.

In `viewer.py`, you can see an example:

```
Viewer("../movingSquares.data", "../movingSquares.labels")
```
