---
title: "POVME: The POcket Volume MEasurer"
permalink: /povme/
toc: true

summary: ""
---

Written by Jeff Wagner

Jeff’s note: I am the current lead developer of POVME. I also have two other essentially full-time projects. You can expect far less stability and user-friendliness from this software than you could from things like VMD. Please don’t hesitate to complain - The problems that give you the hardest time are the ones I’ll focus on fixing first!

gcq#395: "It was something to at least have a choice of nightmares" (Joseph Conrad)
grompp -h

## Why is POVME important?

Molecular Dynamics simulations are getting really popular in our field of science. However, what usually happens is that scientists run simulations (at great computational cost), and then see a big protein wiggling around, and have no idea what to do with it. There are a growing number of tools that try to quantitatively answer the question of "what in the world just happened in this simulation", but they often do abstract analyses with no clear actionable output. In other words, conclusions like “The RMSD went up” do not tell us why people get cancer or what to do about it.

Everyone does simulations different ways and for different specific reasons, but I’d argue that the most directly valuable question that people can try to answer is "how does this simulation help me make a drug?" The normal way for people to use a protein structure to make a drug is by using "docking" software, which tells them how likely a given small molecule is to fit into a binding site. However, even moderately effective docking is computationally expensive. Sometimes, a scientist will do a simulation and end up with hundreds of thousands of snapshots (each a single protein structure), and it is impractical to dock to all of them. POVME3 is primarily intended to solve this problem of making molecular dynamics simulations more useful to drug designers.

## How does POVME enable better drug design?

In the above situation, POVME can perform two useful tasks:

1. Pocket shape-based clustering: POVME will analyze the whole simulation from the perspective of the binding pocket, and find unique families of conformations that were visited. This way, a scientist can dock to just a few, unique snapshots of the protein binding pocket (the cluster representatives), under the assumption that the drugs revealed by docking to these few conformations are the same as the drugs that you'd discover by docking to every single frame.

2. PCA and simulation summary: POVME can generate a 3D model overlaid on the binding pocket, showing what kinds of subpockets, motions and/or conformational changes were observed in the simulation. Actual drug designers will find this output far more useful than the clustering, since drug design is present(2016)ly more of an art than a science, and this information is more readily visualized. 

## What is POVME3.0?

The best way to learn about POVME3.0 is to first learn about POVME2.0. Read through Jacob’s original (beautiful) documentation here to understand what POVME’s all about. The core of POVME remains the same, but I’ve made it leaner, meaner, and greener (among other colors). Confused? Let’s learn by doing.

## Today’s projects

We’ll be a bit busy, so let’s get moving. Today, we’ll
Set up POVME and its VMD plugin
Run POVME on the binding pocket in our toy system the old-fashioned way
Do more complex post-analysis on these POVME results
Analyze the same binding pocket using a ligand-based pocket-definition algorithm, and look into chemical colors
Run an advanced POVME analysis workflow on multiple trajectories of the same protein bound to different ligands

**1. Set up POVME and its VMD plugin

The POVME VMD plugin is best for processing small cases (< 1000 frames), but I still use it in larger cases to define the binding pocket region.  Installing VMD plugins is a pain in the neck, but thankfully I’ve prepared the important file for you.

In your home directory, create or open the file “.vmdrc” and enter the following:

```
set auto_path "$auto_path $::env(POVME_PATH)/POVME/vmdplugin"
menu main on
vmd_install_extension povme2 povme2_tk_cb "Analysis/POVME2"
set ::povme2::povme2_directory "$::env(POVME_PATH)/POVME/POVME3.py"
```
Now open VMD and go to Extensions -> Analysis -> POVME2. **Ensure that this opens.

**2. Run POVME on the binding pocket the old-fashioned way

We’re going to look at a drug-binding pocket on Heat Shock Protein 90 (HSP90). You can find this file at /home/sa19/2VCI_demo_clean.pdb

Make a new directory in your /scratch for the analysis, and copy this trajectory into there

Load the trajectory into VMD. Be sure to open VMD in your /scratch directory.

Usually, you’d have to align the trajectory, however I’ve already done it for you this time.

Open the Povme2 plugin by going to Extensions -> Analysis -> POVME2

Under “Select molecule”, choose the protein.

Change “selection” from “all” to “protein”. If we don’t do this, POVME will think that the space which the ligand occupies isn’t part of the pocket. 

Now, you’ll want to draw an inclusion shape that encompasses the binding pocket. Under “Inclusion Shapes”, go to “Add new shape...”. Say “yes” to switching to GLSL mode. You will play around with the different options, but you will ultimately decide to use a sphere (cylinders and cubes are broken right now). You can use the mouse to snap the shape center to an atom - One click snaps it to an atom center, another releases it. I usually snap it to an atom center near where I want it, and then use the arrows by the number box values to move it around. VMD is a bit rough around the edges when it comes to input boxes like this. If I modify a number by hand, I sometimes have to increase and decrease the value by 1 before VMD recognizes it and updates the shape on the screen. 

Here is a short digression on seed regions: Seed regions are a smaller, “core” part of the binding pocket, whereas the inclusion region is a kind of “maximum size”, or limit for how large our pocket can be defined. Why did we do this? One problem that arose often in doing POVME analysis of binding pockets was that some conformational changes would “split’ the binding pockets into two smaller pockets. If we’re focusing on putting a drug in one of the smaller pockets, then it’s a waste of time to analyze the other while the protein conformation is splitting them. But when the two pockets are joined, we are interested in their combined shape. How do we manage this?

We solve this problem using “seed” regions. These are regions that we are definitely interested in, and we are only interested in the rest of the pocket if it’s connected to a seed region. When POVME runs on a frame, it starts by defining the pocket as the seed region only, then discards any points which are overlapping with a protein atom. It then iteratively grows the seed region out in all directions, one grid point at a time, until it runs into a protein atom or the edge of the inclusion region. When the pocket stops growing, it moves onto the next frame. This way, we define only useful contiguous regions each frame, rather than adding noise from disconnected pockets and little bubbles between imperfectly-packed amino acids in the protein.

Add a “Contiguous Pocked Seed” sphere as well (in the third box) with the same center as the original, but only half the radius.

Because the plugin is still under development, we need to do one more technical fix. Go to Settings -> Files… and change the python executable box from “python” to “/home/<your keck2 username>/POVME/arun python”. 

Also, for the sake of speed, go to Settings -> Output… and change the number of processors to however many you can spare (max 8).

Now hit “Run POVME”.  This should take a few minutes. 

When it finishes (there will be a bunch of error messages in the terminal which I should fix), you can load the volume trajectory file into VMD (in the VMD Main window, go to New Molecule, and load volume_trajectory.pdb), which is a separate object showing the pocket shape through the simulation. 

VMD is going to have trouble understanding what’s going on with the binding pocket, which is a bunch of dummy atoms that pop around on a grid. In the VMD Main window, go to Graphics -> Representations and change volume_trajectory’s drawing style to “VDW”. 

For complicated reasons, loading the volume trajectory will un-center your camera. To fix that, go to the VMD Main window and double-click the “T” column next to the protein to make that the “Top” molecule, then go to the 3D window and hit “=” to re-center the visualization on the “Top” molecule. 


Now hit play and watch the binding site change with each frame!

Here is a short digression on the meaning of “average” in the context of a pocket: We have seen what binding pocket look like in each frame. What does it look like on average? In the volume_trajectory file, each frame shows a single snapshot of the pocket. Each point is either a 1 (part of the pocket) or a 0 (not part of the pocket - Maybe it was blocked by the protein or outside the inclusion region). Since the grid that these 0’s and 1’s are on is always in the same location in space, we can take the average value of each grid point over all of the frames, to see what fraction of the time a certain region is part of the binding pocket. So maybe a certain grid point was part of the pocket in 10 frames, and not part of the pocket in 90 frames. Then it would have an average value of 10%, or 0.1.

We will visualize this “average pocket” by loading ./frameInfo/volumetric_density.dx as a new molecule. 

A Data Explorer (DX) file doesn’t contain atoms - It instead describes the density of some phenomenon in a 3D region. In this case, our phenomenon is “volumes that are part of the binding pocket”. We visualize dx files by giving VMD a cutoff (eg. “I want to see everything that’s part of the binding pocket at least 50% of the time”), and then VMD draws an “isosurface” around all of the points that satisfy our condition.

To draw an isosurface, go to Graphics -> Representations, and under Selected Molecule go to “volumetric_density.dx”. Ensure that “Drawing Method” for this molecule is set to “Isosurface”, and change the “Draw” option to “Wireframe”. In the VMD Main window, turn off the volume_trajectory.pdb depiction by double-clicking the “D” next to it. Now you should see a white wireframe drawn around the regions of space that are part of your pocket at least 50% of the time, corresponding to an isovalue of 0.5.

Before you try it, try to predict the following: If you change the isovalue to 0.2, will the isosurface (pocket shape) expand or contract? 


Why?



Try it. Were you right?



Once you’re comfortable with the concept of averages and isosurfaces, let’s tinker around with seed regions. We’ll do that by removing the seed region (so that the entire inclusion region becomes the seed) and re-running the analysis


In the VMD Main window, double click the “T” column next to our original protein trajectory (not the pocket trajectory - Just the protein!) to make it “top”
 
Delete the seed region in the POVME2 window. 

To avoid overwriting our original files, go to Settings -> Output… and change “Output Filename Prefix” to “./noSeed_”, then hit OK

In the POVME2 window, press “Run POVME2”
 
When this is complete, load up noSeed_volume_trajectory.pdb and compare the two volume trajectories (maybe draw one of them in VDW with a sphere scale of 0.4 and the transparent material, and the other in VDW with a sphere scale of 0.3 and the Coloring Method ColorID with a value of “10 cyan”)

How do these two pocket trajectories differ?




The pocket-growing algorithm requires a certain number of “neighbors” before the pocket can grow out to a new point (default 3 neighbors). This prevents it from going way down into little crevices, and so the pocket only fills in places where a ligand atom might reasonably fit. When we don’t use a seed region, we don’t use these growing rules. 

Take a screenshot of a place where the pockets differ and put it in your notes. Be sure to label which representation is which mode.



Based on the user’s discretion and the nature of the pocket, we can forego using a seed region altogether. In essence, when we don’t define a seed region, the entire inclusion region becomes the seed. This means that we’ll occasionally capture little packing defects in the protein and little random crevices as part of the pocket. But in some cases, there can be proteins with segmented, tight pockets or other factors that make abandoning the seed region worthwhile.

In this case, I’d say that the pocket is open enough to justify using the seed regions.

3. Do more complex post-analysis on these results

There’s no GUI for this part, so hold on to your hats and work slowly and carefully. 

```Exit VMD. ```

When POVME ran in VMD, it was actually spewing files all over the place. Most of them were stored in a mean little folder called “frameInfo”, which is packed to the gills with all sorts of information about each frame. The post-analysis tools will be interested in these.

Run `ls frameInfo` and appreciate how much junk is in there.

We often perform clustering with a similarity matrix. How do we determine how “similar” two pockets are? In the case of POVME post-analysis, we choose to use the “Tanimoto similarity metric”. Since our pocket points are defined on a regular grid, any two frames from the same analysis will have some points in common. The “Tanimoto Similarity” between two frames is defined as the number of points they have in common (their “intersection”) divided by the number of points in either of them (their “union”). Therefore, every pair of frames can have a maximum similarity of 1 (they are identical) and a minimum similarity of 0 (they have no regions in common).

To calculate this similarity matrix, we use a script called “binding_site_overlap.py”, which is in the POVME directory. You’ll find it in “/home/<your keck2 username>/POVME/clustering/binding_site_overlap.py”. The package structure in POVME is in the middle of a shakeup, so just like above, we’ll need to precede our POVME python scripts with “/home/<your keck2 username>/POVME/arun”

Print the help message: Run 

```/home/<your keck2 username>/POVME/arun python /home/<your keck2 username>/POVME/clustering/binding_site_overlap.py -h```

On a better day, we’d just run `python binding_site_overlap.py -h`, but:
We have to do the whole arun thing because POVME is downloaded, but not installed, so all of its dependencies aren’t in the normal system locations. The “arun” script fixes this for the current command.
We put the whole path on binding_site_overlap.py because it is not in our current directory, and it’s not in a normal system location, so we have to tell linux exactly where it is.
Now, let’s put together our actual run command:
I need to put “-f” and then all of the pocket shape filenames. These are in frameInfo, and they look like 
```
frameInfo/frame_1.npy, 
frameInfo/frame_2.npy 
… 
“frameInfo/frame_100.npy
```
So I don’t have to write out 100 filenames, I’m going to use “wildcards” to describe all of the frame files. 
However, there are some other files that will prevent me from just saying `frameInfo/frame_*.npy` (this would, for example, also pick up “frameInfo/frame_2_aromatic.npy”, which I do not want.)
A different wildcard is `?` - This can only match one character, as opposed to `*` which can match multiple. So a simple pattern that would only grab the files I want is 
“frameInfo/frame_?.npy” and “frameInfo/frame_??.npy” and “frameInfo/frame_???.npy” 
Except that, here, I don’t have to put the “and” - the commandline interpreter will just expand these in place into all of the filenames that match those patterns.
We don’t want to run with color in this tutorial, so we’re not going to use the -c flag.
We don’t need csv files, so I’m not going to use the --csv option
So my final run command is 
```
/home/<your keck2 username>/POVME/arun python /home/<your keck2 username>/POVME/clustering/binding_site_overlap.py -f frameInfo/frame_?.npy frameInfo/frame_??.npy frameInfo/frame_???.npy
```
Run that

Now run `ls -lrth`. You should see three new files in the directory.
binding_site_overlap.py spat out two overlap matrices - Tanimoto (which we will use) and Tversky (which we will not use). Since these matrices are literally just squares of numbers, it also produces a file called indexMapToFrames.csv, which keeps track of which rows correspond to which frame filenames, so we can go recover our frame numbers later on.
Now, let’s cluster our trajectories. Run: 

`/home/<your keck2 username>/POVME/arun python /home/<your keck2 username>/POVME/clustering/cluster.py -h`

The command is big and ugly, again because POVME isn’t properly installed, so we have to be specific about where our files are.

The help message reads:
```
usage: cluster.py [-h] [-m M] [-t [T]] [-T [T]] [-i [I]] [--kmeans] [-n [N]]
                  [-N [N]] [-o [O]] [-a]

Cluster POVME pocket volumes.

optional arguments:
  -h, --help  show this help message and exit
  -m M        The pocket overlap matrix (generated by binding_site_overlap.py)
  -t [T]      A mapping between .npy file prefixes and their original pdb
              file/trajectory, separated by a colon. Can be used repeatedly.
              Ex: -t 1BYQ:./trajectories/1BYQ.pdb -t
              1UYF:./trajectories/1UYF.pdb
  -T [T]      A file containing a series of -t arguments
  -i [I]      The index file mapping the pocket overlap matrix to frame
              numbers. Required to return cluster representatives.
  --kmeans    Use kmeans clustering instead of hierarchical.
  -n [N]      Manually set number of clusters. Otherwise the Kelley penalty
              will calculate the optimal number.
  -N [N]      Set min, min:max, or min:max:skip values for number of clusters
              that the Kelley penalty can consider.
  -o [O]      Specify an output prefix.
  -a          Output all frames into cluster subdirectories (not just cluster
              reps).
   ```

As with most programs, we don’t want to use anywhere near all of the possible arguments. We’ll just do a minimal clustering run here, with the command