#!/usr/bin/env python

import sys, os
import ROOT
import pylhe
from itertools import combinations
from collections import Counter


def savehist(hist, histname):
    """At the end of the function, there are no more references to `file`.
    The `TFile` object gets deleted, which in turn saves and closes
    the ROOT file."""
    myFile.WriteObject(hist, histname)


try:
    input = raw_input
except:
    pass

if len(sys.argv) < 2:
    print("Usage: python histogram.py input_LHE_file")
    sys.exit(1)

# p p > t t~, (t > w+ b, (w+ > j j)), (t~ > w- b~, (w- > j j))
myFile = ROOT.TFile.Open("MultiJet_histograms.root", "RECREATE")

h = {}
bins = [20, 50]
combs = ["all", "2b", "wdecay", "bwithmixedq", "mixed", "unmixed"]
# Book histograms
# TH1F::TH1F(const char* name, const char* title, int nbinsx, double xlow, double xup) =>
for binconfig in bins:
    for comb in combs:
        h[f"hist3JetM_{comb}_{binconfig}"] = ROOT.TH1F(f"3Jet_mass_{comb}_{binconfig}bins", "3Jet Mass; 3Jet Mass", binconfig, 0.0, 1000.0)

#lhe_file = sys.argv[1]
lhe_file = 'unweighted_events.lhe.gz'
events = pylhe.read_lhe_with_attributes(lhe_file)
num_events = pylhe.read_num_events(lhe_file)
print(f"Number of events:", num_events)

arr = pylhe.to_awkward(events)

#i = 0
#print(f"Particle IDs:", arr[0].particles.id)
#print(f"Particle Status:", arr[i].particles.status)
#print(f"Particle Mother1:", arr[i].particles.mother1)
#print(f"Particle Mother2:", arr[i].particles.mother2)
#print(f"Particle Color1:", arr[i].particles.color1)
#print(f"Particle Color2:", arr[i].particles.color2)
#print(f"Particle Mass:", arr[i].particles.m)
#print(f"Particle Lifetime:", arr[i].particles.lifetime)
#print(f"Particle Spin:", arr[i].particles.spin)
#print(arr.type.show())

for i in range(0, 1000):
    if (i % 100) == 0:
        print(i)
    event_list = []

    for part in arr[i].particles:
        if part.status == 1:
            particle_list = []
            particle_list.append(part.vector)
            particle_list.append(part.id)
            particle_list.append(part.mother1)
            particle_list.append(part.m)
            particle_list.append(part.spin)
            event_list.append(particle_list)

    comb = combinations(event_list, 3)

    for j in list(comb):
        four_vec = j[0][0] + j[1][0] + j[2][0]
        for binconfig in bins:
            h[f"hist3JetM_all_{binconfig}"].Fill(four_vec.m)

        pdgid_list = []
        par_pdgid_list = []
        for k in range(0,3):
            pdgid_list.append(j[k][1])
            par_pdgid_list.append(arr[i].particles[int(j[k][2]) - 1].id)

        counter = Counter(par_pdgid_list)

        if (-5 in pdgid_list) and (5 in pdgid_list):
            for binconfig in bins:
                h[f"hist3JetM_2b_{binconfig}"].Fill(four_vec.m)

        if all(abs(x) == 24 for x in par_pdgid_list):
            for binconfig in bins:
                h[f"hist3JetM_wdecay_{binconfig}"].Fill(four_vec.m)

        if (24 in par_pdgid_list) and (-24 in par_pdgid_list) and (any(abs(x) == 5 for x in pdgid_list)):
            for binconfig in bins:
                h[f"hist3JetM_bwithmixedq_{binconfig}"].Fill(four_vec.m)

        if counter[-24] == 2 and (5 in pdgid_list):
            for binconfig in bins:
                h[f"hist3JetM_mixed_{binconfig}"].Fill(four_vec.m)

        elif counter[24] == 2 and (-5 in pdgid_list):
            for binconfig in bins:
                h[f"hist3JetM_mixed_{binconfig}"].Fill(four_vec.m)

        elif counter[-24] == 2 and (-5 in pdgid_list):
            for binconfig in bins:
                h[f"hist3JetM_unmixed_{binconfig}"].Fill(four_vec.m)

        elif counter[24] == 2 and (5 in pdgid_list):
            for binconfig in bins:
                h[f"hist3JetM_unmixed_{binconfig}"].Fill(four_vec.m)
        else:
            continue

c0 = ROOT.TCanvas()
c0.SetLogy()

for key,value in h.items():
    c0.Update()
    value.Draw("E")
    c0.Print(f"pics/{key}.png")
    c0.Clear()
    savehist(value, key)

