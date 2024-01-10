#!/usr/bin/env python

import ROOT
import itertools
import pylhe
import awkward as ak
import uproot
import vector as vec
from statistics import mean
import numpy
from itertools import combinations

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
i = 0
arr = pylhe.to_awkward(events)
#print(arr)
print(arr[i].particles.id)
print(arr[i].particles.status)
print(arr[i].particles.mother1)
print(arr[i].particles.mother2)
print(arr[i].particles.color1)
print(arr[i].particles.color2)
print(arr[i].particles.m)
print(arr[i].particles.lifetime)
print(arr[i].particles.spin)
print(" ")
print(arr.type.show())

#returns pt!!!!
#print(arr[i].particles.vector.mass)


for i in range(0, 1):
    event_list = []
    for part in arr[i].particles:
        if part.status == 1:
            particle_list = []
            particle_list.append(part.vector)
            particle_list.append(part.id)
            particle_list.append(part.mother1)
            #print(part.vector)
            #print(part.id)
            #print(part.mother1)
            #print(part.mother2)
            event_list.append(particle_list)
    #print(particle_list)
    print(" ")
    print(event_list)
    comb = combinations(event_list, 3)
    print(" ")
    for j in list(comb):
        four_vec = j[0][0] + j[1][0] + j[2][0]
        print(four_vec.m)
    #print(list(comb))
    #print(len(comb))
    #print(event_list[6])
    #print(event_list[6][0])
    new_vec = event_list[0][0] + event_list[1][0] + event_list[2][0]
    #print(new_vec.m)

    #print(particle_list[0][1])
    #sum = numpy.sum(particle_list[0][0], particle_list[1][0])
    #print(sum)


    #print(mass_list)
    #print(mean(mass_list))

#vector.register_awkward()
#vec = vector.awk(arr)
#print(vec)

#myFile = ROOT.TFile.Open("myroot.root", "RECREATE")
#with uproot.open("myroot.root") as tfile:
#    tfile["tree1"] = {"branch": arr}
#    tfile["tree1"].show()

#for i in range(0, num_events):
#    print(arr[i].eventinfo.nparticles)

