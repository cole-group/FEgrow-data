# Mat: draw
import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import Draw, AllChem
from PIL import Image
import pandas as pd
import networkx as nx

# load the .csv file using pandas
edgelist = pd.read_csv('sars/sarscov2-3toR.csv', names=['node1', 'node2', 'ddG', 'ddGerr'])
# create a graph using pandas
g_no_graphics = nx.from_pandas_edgelist(edgelist, 'node1', 'node2')


# for each node add an RDKit 2D image
g = nx.Graph()
images = []
for i, nodeid in enumerate(g_no_graphics.nodes):
    mol = Chem.MolFromPDBFile(f'sars_mols/l{nodeid}.pdb', removeHs=False)
    mol.RemoveAllConformers()
    AllChem.Compute2DCoords(mol)
    im = Draw.MolToImage(mol)

    g.add_node(nodeid, image=im)
    images.append(im)

g.add_edges_from(g_no_graphics.edges)

# create the figure
fig, ax = plt.subplots(figsize=(10,10))
# turn off the axis 
plt.axis("off")

# get node positions
pos = nx.circular_layout(g, center=(0.5, 0.5), scale=0.45) 
# pos = nx.spectral_layout(g, center=(0.5, 0.5), scale=0.3, weight=None) 
# pos = nx.spring_layout(g, seed=3113794652, center=(0.5, 0.5), scale=0.4)  

nx.draw_networkx_edges(
    g,
    pos=pos,
    ax=ax,
    arrows=True,
    arrowsize=100,
    min_source_margin=0.1,
    min_target_margin=0.1,
)

# Transform from data coordinates (scaled between xlim and ylim) to display coordinates
tr_figure = ax.transData.transform
# Transform from display to figure coordinates
tr_axes = fig.transFigure.inverted().transform

# Select the size of the image (relative to the X axis)
icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.1
icon_center = icon_size / 2.0

# Add the respective image to each node
for i, n in enumerate(g.nodes):
    xf, yf = tr_figure(pos[n])
    xa, ya = tr_axes((xf, yf))

    # get overlapped axes and plot icon
    a = plt.axes([pos[n][0] - icon_center, pos[n][1] - icon_center, icon_size, icon_size])
    # a = plt.axes([xa - icon_center, ya - icon_center, icon_size, icon_size])
    a.imshow(images[i])
    a.axis("off")

    # ax.text(pos[n][0] - icon_center, pos[n][1] - icon_center - 0.05, 'test')
    middle_x =  (a.get_xbound()[0] + a.get_xbound()[1]) / 2
    middle_y =  (a.get_ybound()[0] + a.get_ybound()[1]) * 0.9
    a.text(middle_x, middle_y, f'l{n}', horizontalalignment='center')

plt.tight_layout()
plt.savefig('map.png', dpi=300)