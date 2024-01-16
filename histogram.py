#!/usr/bin/env python

import ROOT
import pylhe
from itertools import combinations


def savehist(hist, histname):
    """At the end of the function, there are no more references to `file`.
    The `TFile` object gets deleted, which in turn saves and closes
    the ROOT file."""
    myFile.WriteObject(hist, histname)


# p p > t t~, (t > w+ b, (w+ > j j)), (t~ > w- b~, (w- > j j))
myFile = ROOT.TFile.Open("MultiJet_histograms.root", "RECREATE")

bins = 50
# Book histograms
# TH1F::TH1F(const char* name, const char* title, int nbinsx, double xlow, double xup) =>
hist3JetM = ROOT.TH1F("3Jet_mass", "3Jet Mass; 3Jet Mass", bins, 0.0, 1000.0)
hist3JetM_2b = ROOT.TH1F("3Jet_mass", "Two b 3Jet Mass; 3Jet Mass", bins, 0.0, 1000.0)
hist3JetM_wdecay = ROOT.TH1F("3Jet_mass", "W Decay 3Jet Mass; 3Jet Mass", bins, 0.0, 1000.0)
hist3JetM_mixed = ROOT.TH1F("3Jet_mass", "Mixed 3Jet Mass; 3Jet Mass", bins, 0.0, 1000.0)
hist3JetM_mixed_correct = ROOT.TH1F("3Jet_mass", "UnMixed 3Jet Mass; 3Jet Mass", bins, 0.0, 1000.0)

lhe_file = "current_unweighted_events.lhe"
events = pylhe.read_lhe_with_attributes(lhe_file)
num_events = pylhe.read_num_events(lhe_file)
print(f"Number of events:", num_events)

i = 0
arr = pylhe.to_awkward(events)
print(f"Particle IDs:", arr[i].particles.id)
print(f"Particle Status:", arr[i].particles.status)
print(f"Particle Mother1:", arr[i].particles.mother1)
print(f"Particle Mother2:", arr[i].particles.mother2)
print(f"Particle Color1:", arr[i].particles.color1)
print(f"Particle Color2:", arr[i].particles.color2)
print(f"Particle Mass:", arr[i].particles.m)
print(f"Particle Lifetime:", arr[i].particles.lifetime)
print(f"Particle Spin:", arr[i].particles.spin)
print(" ")
print(arr.type.show())

for i in range(0, 1):
    if (i % 100) == 0:
        print(i)
    event_list = []
    #print("Vector Data, Particle ID, Mother Place, Mass, Spin")
    for part in arr[i].particles:
        if part.status == 1:
            particle_list = []
            particle_list.append(part.vector)
            particle_list.append(part.id)
            particle_list.append(part.mother1)
            #particle_list.append(part.mother2)
            particle_list.append(part.m)
            particle_list.append(part.spin)
            event_list.append(particle_list)

    comb = combinations(event_list, 3)

    for j in list(comb):
        four_vec = j[0][0] + j[1][0] + j[2][0]
        hist3JetM.Fill(four_vec.m)

        print(f"PDGID:", arr[i].particles[int(j[1][2]) - 1].id)

        if (abs(j[0][1]) == 5 and abs(j[1][1]) == 5) or (abs(j[0][1]) == 5 and abs(j[2][1]) == 5) or (abs(j[1][1]) == 5 and abs(j[2][1]) == 5):
            #four_vec = j[0][0] + j[1][0] + j[2][0]
            hist3JetM_2b.Fill(four_vec.m)

        if (j[0][2] in {4, 6}) and (j[1][2] in {4, 6}) and (j[2][2] in {4, 6}):
            #four_vec = j[0][0] + j[1][0] + j[2][0]
            hist3JetM_wdecay.Fill(four_vec.m)

        if (j[0][1] == 5 and (j[1][2] == 4 and j[2][2] == 4)) or (j[1][1] == 5 and (j[0][2] == 4 and j[2][2] == 4)) or (j[2][1] == 5 and (j[0][2] == 4 and j[1][2] == 4)):
            #four_vec = j[0][0] + j[1][0] + j[2][0]
            hist3JetM_mixed.Fill(four_vec.m)
            print("b with W- products")
            print(f"Inv Mass:", four_vec.m)
            #print(" ")
            #print(j)
            #print("First If")
        elif (j[0][1] == -5 and (j[1][2] == 6 and j[2][2] == 6)) or (j[1][1] == -5 and (j[0][2] == 6 and j[2][2] == 6)) or (j[2][1] == -5 and (j[0][2] == 6 and j[1][2] == 6)):
            #four_vec = j[0][0] + j[1][0] + j[2][0]
            hist3JetM_mixed.Fill(four_vec.m)
            print("b~ with W+ products")
            print(f"Inv Mass:", four_vec.m)
            #print(" ")
            #print(j)
            #print("Second If")
        elif (j[0][1] == -5 and (j[1][2] == 4 and j[2][2] == 4)) or (j[1][1] == -5 and (j[0][2] == 4 and j[2][2] == 4)) or (j[2][1] == -5 and (j[0][2] == 4 and j[1][2] == 4)):
            #four_vec = j[0][0] + j[1][0] + j[2][0]
            hist3JetM_mixed_correct.Fill(four_vec.m)
            print("b~ with W- products")
            print(f"Inv Mass:", four_vec.m)
        elif (j[0][1] == 5 and (j[1][2] == 6 and j[2][2] == 6)) or (j[1][1] == 5 and (j[0][2] == 6 and j[2][2] == 6)) or (j[2][1] == 5 and (j[0][2] == 6 and j[1][2] == 6)):
            #four_vec = j[0][0] + j[1][0] + j[2][0]
            hist3JetM_mixed_correct.Fill(four_vec.m)
            print("b with W+ products")
            print(f"Inv Mass:", four_vec.m)
        else:
            continue

c0 = ROOT.TCanvas()
c0.SetLogy()
c0.Update()
hist3JetM.Draw("E")
c0.Print("3JetMass.png")
c0.Clear()
c0.Update()
hist3JetM_2b.Draw("E")
c0.Print("3JetMass_2b.png")
c0.Clear()
c0.Update()
hist3JetM_wdecay.Draw("E")
c0.Print("3JetMass_wdecay.png")
c0.Clear()
c0.Update()
hist3JetM_mixed.Draw("E")
c0.Print("3JetMass_mixed.png")
c0.Clear()
c0.Update()
hist3JetM_mixed_correct.Draw("E")
c0.Print("3JetMass_mixed_correct.png")
c0.Clear()

savehist(hist3JetM, "3JetMass")
savehist(hist3JetM_2b, "3JetMass_2b")
savehist(hist3JetM_wdecay, "3JetMass_wdecay")
savehist(hist3JetM_mixed, "3JetMass_mixed")

