#!/usr/bin/env python

import ROOT
import itertools
import pylhe
import awkward as ak
import uproot
import vector as vec

lhe_file = "current_unweighted_events.lhe"
events = pylhe.read_lhe_with_attributes(lhe_file)
num_events = pylhe.read_num_events(lhe_file)
print(f"Number of events:", num_events)
type(num_events)

# Get event 1
#event = next(itertools.islice(events, 1, 2))

# A DOT language graph of the event can be inspected as follows
#print(event.graph.source)

# The graph is nicely displayed as SVG in Jupyter notebooks
#print(event)

# To save a DOT graph render the graph to a supported image format
# (refer to the Graphviz documentation for more)
#event.graph.render(filename="test", format="png", cleanup=True)
#event.graph.render(filename="test", format="pdf", cleanup=True)

arr = pylhe.to_awkward(events)
#print(arr)
print(arr[1].particles.id)
print(arr[1].particles.status)
print(arr[1].particles.mother1)
print(arr[1].particles.mother2)
print(arr[1].particles.color1)
print(arr[1].particles.color2)
print(arr[1].particles.m)
print(arr[1].particles.lifetime)
print(arr[1].particles.spin)
print(" ")
print(arr.type.show())

#returns pt!!!!
print(arr[1].particles.vector.pt)

#vector.register_awkward()
#vec = vector.awk(arr)
#print(vec)

#myFile = ROOT.TFile.Open("myroot.root", "RECREATE")
#with uproot.open("myroot.root") as tfile:
#    tfile["tree1"] = {"branch": arr}
#    tfile["tree1"].show()

#for i in range(0, num_events):
#    print(arr[i].eventinfo.nparticles)

