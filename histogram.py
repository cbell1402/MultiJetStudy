#!/usr/bin/env python

import ROOT
import itertools
import pylhe
import awkward as ak
import uproot

lhe_file = "current_unweighted_events.lhe"
events = pylhe.read_lhe_with_attributes(lhe_file)
print(f"Number of events: {pylhe.read_num_events(lhe_file)}")

# Get event 1
event = next(itertools.islice(events, 1, 2))

# A DOT language graph of the event can be inspected as follows
#print(event.graph.source)

# The graph is nicely displayed as SVG in Jupyter notebooks
#print(event)

# To save a DOT graph render the graph to a supported image format
# (refer to the Graphviz documentation for more)
event.graph.render(filename="test", format="png", cleanup=True)
event.graph.render(filename="test", format="pdf", cleanup=True)

arr = pylhe.to_awkward(events)
#print(arr)

myFile = ROOT.TFile.Open("myroot.root", "RECREATE")
with uproot.open("myroot.root") as tfile:
    tfile["tree1"] = {"branch": arr}
    tfile["tree1"].show()
