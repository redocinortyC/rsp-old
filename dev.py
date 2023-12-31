import numpy as np
import pandas as pd

from scripts.tsne import generate_tsne
from scripts.simulation import plot_simulated_cells
from scripts.rsp import generate_polygon, gene_analysis
from scripts.util import get_genes, get_gene_info, save_plot
from scripts.download import sim_download
from scripts.pager import PAGER

pager = PAGER()

df = pd.read_csv("filtered_data.csv")
selected_genes = df[df["RSP Area"] != 0]["Gene Name"].head(50).tolist()
print(selected_genes)

pager_results = pager.run_pager(
    selected_genes,
    source=[
        "GOA",
        "GOA_EXCL",
        "WikiPathway_2021",
    ],
)
pager_results.to_csv("pager_results.csv", index=False)
pager_results["NAME"].head(20).to_csv("top_20_studies.csv", index=False)

# sim_download(num_genes=100, distribution="even", plots=False, data=True)

# genes = get_genes(dge_file="data/MCA1.txt", target_cluster=1)
# print(genes)

# info = get_gene_info(
#     dge_file="data/MCA1.txt", target_gene="Sparc"
# )
# print(info)

# mitochondrial genes filter
# genes = [gene for gene in genes if gene.startswith("mt-")]

# for gene in genes:
#     _, rsp_fig, rsp_area = gene_analysis(
#         dge_file="data/MCA1.txt",
#         marker_gene=gene,
#         target_cluster=1,
#     )

#     # rsp_fig.show()

#     print(input(f"{gene}: {rsp_area:.2f}; press enter to continue..."))

# tsne_fig, rsp_fig = gene_analysis(
#     dge_file="data/MCA1.txt",
#     marker_gene="Actc1",
#     target_cluster=1,
# )

# for fig in [tsne_fig, rsp_fig]:
#     fig.show()

# save_plot(tsne_fig, "tsne.png")

# coordinates, is_expressing = generate_tsne(
#     dge_file="data/MCA1.txt",
#     marker_gene="Actc1",
#     target_cluster=1,
# )

# coordinates, is_expressing, _ = plot_simulated_cells(
#     num_points=1000,
#     expression_percentage=0.50,
#     distribution="biased",
#     sigma=0.3,
#     display=False,
# )

# fig = generate_polygon(coordinates, is_expressing)
# save_plot(fig, "rsp.png")

# from 0 to 1 in intervals of 0.1
# for i in range(1, 10, 1):
#     expression_percentage = i / 10
#     coordinates, is_expressing, _ = plot_simulated_cells(
#         num_points=1000,
#         expression_percentage=expression_percentage,
#         distribution="biased",
#         seed=12,
#         display=True,
#     )

#     fig = generate_polygon(coordinates, is_expressing)
#     fig.show()

#     print(input(f"{expression_percentage * 100}%; press enter to continue..."))


# # range from 10% to 100% in intervals of 10%
# for i in range(11, 100, 11):
#     expression_percentage = i / 100
#     coordinates, is_expressing, _ = plot_simulated_cells(
#         num_points=1000,
#         expression_percentage=expression_percentage,
#         distribution="biased",
#         sigma=0.3,
#         # seed=42,
#         display=False,
#     )

#     fig = generate_polygon(coordinates, is_expressing)
#     fig.show()

#     print(input("Press enter to continue..."))
