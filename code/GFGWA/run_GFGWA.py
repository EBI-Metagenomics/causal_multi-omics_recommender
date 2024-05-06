import scipy.cluster.hierarchy as sch
from matplotlib import pyplot as plt
import pandas as pd
from scipy.stats import mannwhitneyu
import math
import numpy as np
from scipy.spatial.distance import jaccard
# from scipy.spatial.distance import pdist
from scipy.spatial.distance import pdist, squareform
import seaborn as sns
from tqdm.auto import tqdm

""" This project received funding from the European Union’s Horizon 2020 research and innovation programme [952914] (FindingPheno).
"""

# First a table that maps SNPS ("marker") to genes ("GeneSymbol")
themap = pd.read_csv("../../data/HoloFish_HostG_SNP_annotation_GENES.txt")

# Next, we have a table that carries the metadata of the samples:
metadata = pd.read_csv("../../data/HoloFish_FishVariables_20221116.csv")

# A table that maps genes to their associated GO terms. Notice that many genes (symbol) are not associated to any GO term
go = pd.read_csv("../../data/salmon_GO_annotations.tsv", sep="\t")
# So we'll drop the genes with no association:
go = go.dropna()

# We want to keep only the SNPs that map to genes for which we have GO terms.
# First we'll isolate the "GO-genes":
go_genes = list(go.SYMBOL.unique())

# And then, from the "themap" table, we keep only the rows where the gene name 
# is found inside the "go_genes" list:
relevant_mutations = themap[themap.GeneSymbol.isin(go_genes)].copy()

# There's 1117765 SNPs/markers left in our table at this point

# The gwasdf is the big table that keeps the dosage data per sample per SNP:
gwasdf = pd.read_csv("../../data/genotype_probabilities_all.dose", sep=" ")

# The gwasdf names the samples as "Ind0","Ind1" etc, but we've been using the "F001" 
# samples IDs from the other tables, so we'll need to rename the smaples:
# Load a mapping of IndX --> FXXX names
sidm = pd.read_csv("../../data/HoloFish_FishVariables_20221116.csv")
sidm = sidm[["Sample.ID","HostG.Ind.ID"]]
sampleD = {b:a for a,b in sidm.dropna().values}
# rename the samples in the raw gwasdf
gwasdf.columns = list(gwasdf.columns[:3]) + [sampleD.get(x) for x in gwasdf.columns[3:]]

# To further process this table, we'll drop the "alleleA/alleleB" columns 
# and set the "marker" column as index.     
# Then we'll only keep the SNPs that we've kept in the "relevant_mutations" table:
gwasi = gwasdf.set_index("marker").drop(["alleleA","alleleB"], axis=1)
gwasi = gwasi.loc[list(set(relevant_mutations.marker.values))]

## The dosage values

# A value of 0 means that there's probability 1 that the sample has 2 wt alleles.
# A value of 1 means there's probability of 1 that the sample has one variant and one wt allele.
# A value of 2 means that there's probability of 1 that the sample has 2 variabt alleles.

# Thus, any value over 0.5 means that the sample has more than 0.5 probability to have at least one variant allele:
# So we'll make a binary version of our table:
gwasib = (gwasi>0.5).astype(bool)
# And we'll filter out the very few cases of SNPs where ALL samples have the variant allele:
mask = gwasib.sum(axis=1)<361
gwasib_f = gwasib[mask]
gwasi_f = gwasi[mask]


