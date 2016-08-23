LinLogLayout is a simple program for computing graph layouts
(positions of the nodes of a graph in two- or three-dimensional space)
and graph clusterings for visualization and knowledge discovery.
It reads a graph from a file, computes a layout and a clustering, writes
the layout and the clustering to a file, and displays them in a dialog.
LinLogLayout can be used to identify groups of densely connected nodes
in graphs, like groups of friends or collaborators in social networks,
related documents in hyperlink structures (e.g. web graphs),
cohesive subsystems in software models, etc.
With a change of a parameter in the <code>main</code> method,
it can also compute classical "nice" (i.e. readable) force-directed layouts.

The program is primarily intended as a demo of the use of its core layouter
and clusterer classes MinimizerBarnesHut, MinimizerClassic, and
OptimizerModularity.  While MinimizerBarnesHut is faster, MinimizerClassic
is simpler and not limited to a maximum of three dimensions.


Usage: java LinLogLayout <dim> <inputfile> <outputfile>
Computes a <dim>-dimensional layout and a clustering for the graph
in <inputfile>, writes the layout and the clustering into <outputfile>,
and displays (the first 2 dimensions of) the layout and the clustering.
<dim> must be 2 or 3.

Input file format:
Each line represents an edge and has the format:
<source> <target> <nonnegative real weight>
The weight is optional, the default value is 1.0.

Output file format:
<node> <x-coordinate> <y-coordinate> <z-coordinate (0.0 for 2D)> <cluster>


Example:
java -cp bin LinLogLayout 2 examples/WorldImport1999.el WorldImport1999.lc


LinLogLayout optimizes LinLog and related energy models to compute layouts,
and Newman and Girvan's Modularity to compute clusterings. For more information
about LinLog and Modularity, see

[1] A. Noack: "Energy Models for Graph Clustering",
Journal of Graph Algorithms and Applications, Vol. 11, no. 2, pp. 453-480, 2007.
http://jgaa.info/volume11.html
[2] M. E. J. Newman: "Analysis of weighted networks", Physical Review E 70,
056131, 2004.
[3] A. Noack. "Modularity Clustering is Force-Directed Layout",
Preprint arXiv:0807.4052, 2008. http://arxiv.org/abs/0807.4052

For further documentation of LinLogLayout,
see the wiki at http://code.google.com/p/linloglayout/.


If you find LinLogLayout useful, please recommend it and cite the above papers.
Suggestions, questions, and reports of applications are welcome.
Send them to Andreas Noack, an@informatik.tu-cottbus.de.
