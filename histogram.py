#!/usr/bin/env python

import ROOT
import pylhe
from itertools import combinations


def savehist(hist, histname):
    """At the end of the function, there are no more references to `file`.
    The `TFile` object gets deleted, which in turn saves and closes
    the ROOT file."""
    myFile.WriteObject(hist, histname)


myFile = ROOT.TFile.Open("MultiJet_histograms.root", "RECREATE")

# Book histograms
# TH1F::TH1F(const char* name, const char* title, int nbinsx, double xlow, double xup) =>
hist3JetM = ROOT.TH1F("3Jet_mass", "3Jet Mass; 3Jet Mass", 100, 0.0, 1000.0)

lhe_file = "current_unweighted_events.lhe"
events = pylhe.read_lhe_with_attributes(lhe_file)
num_events = pylhe.read_num_events(lhe_file)
print(f"Number of events:", num_events)

i = 0
arr = pylhe.to_awkward(events)
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

for i in range(0, num_events):
    if (i % 10) == 0:
        print(i)
    event_list = []
    for part in arr[i].particles:
        if part.status == 1:
            particle_list = []
            particle_list.append(part.vector)
            particle_list.append(part.id)
            particle_list.append(part.mother1)
            event_list.append(particle_list)

    comb = combinations(event_list, 3)

    for j in list(comb):
        four_vec = j[0][0] + j[1][0] + j[2][0]
        hist3JetM.Fill(four_vec.m)


c0 = ROOT.TCanvas()
c0.SetLogy()
c0.Update()
hist3JetM.Draw()
c0.Print("3JetMass.png")
c0.Clear()

savehist(hist3JetM, "3JetMass")
