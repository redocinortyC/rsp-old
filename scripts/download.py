"""
This module provides functionalities to download and analyze gene data.
It includes options to download plots and CSV data derived from the gene analysis.
"""

import os
import numpy as np
import pandas as pd

from scripts.rsp import generate_polygon, gene_analysis
from scripts.simulation import plot_simulated_cells
from scripts.util import get_genes, get_gene_info, save_plot


def download(plots=True, data=True):
    """
    Download and analyze gene data. Optionally save plots and CSV data to disk.

    Parameters:
    plots (bool): If True, download and save plots to the 'plots' directory. Default is True.
    data (bool): If True, save gene data to a CSV file. Default is True.
    """

    if plots:
        os.makedirs("plots", exist_ok=True)

    def collect_rows(rows, new_row):
        """
        Append a new row to a list of rows.

        Parameters:
        rows (list): The list of existing rows.
        new_row (dict): The new row to be added to the list.

        Returns:
        list: The updated list of rows.
        """

        rows.append(new_row)
        return rows

    # List to store rows
    rows = []

    genes = get_genes(dge_file="data/MCA1.txt", target_cluster=1)

    for gene in genes:
        print(f"Reading {gene}...")
        # Get the gene information
        info = get_gene_info(dge_file="data/MCA1.txt", target_gene=gene)

        # Get the RSP Area from the gene_analysis function
        tsne_fig, rsp_fig, rsp_area = gene_analysis(
            dge_file="data/MCA1.txt",
            marker_gene=gene,
            target_cluster=1,
        )

        # Collect data row by row
        new_row = {
            "Gene Name": info[0],
            "Coverage (%)": info[1],
            "Mean Expression": info[2],
            "Total Expression": info[3],
            "RSP Area": rsp_area,
        }
        rows = collect_rows(rows, new_row)

        if plots:
            for fig in [tsne_fig, rsp_fig]:
                os.makedirs(f"plots/{gene}", exist_ok=True)
                save_plot(fig, f"plots/{gene}/{fig.layout.title.text}.png")

    if data:
        # Convert the list of rows into a DataFrame
        master_df = pd.DataFrame(rows)

        # Save the master DataFrame to a CSV file
        master_df.to_csv("master_file.csv", index=False)


def sim_download(num_genes=1000, distribution="even", plots=True, data=True):
    """
    Simulate and analyze gene data. Optionally save plots to disk.

    Parameters:
    num_genes (int): Number of fake genes to simulate.
    plots (bool): If True, save plots to the 'plots' directory. Default is True.
    """

    if plots:
        os.makedirs("plots", exist_ok=True)

    rows = []

    # Get a list of increasing coverage values based on how many fake genes to generate
    coverage_values = np.linspace(0.01, 1, num_genes)
    coverage_values = coverage_values[::-1]

    for i in range(num_genes):
        gene = f"Gene_{i+1}"
        print(f"Simulating {gene}...")

        # Simulate cells and get the expressing cells
        coordinates, is_expressing, tsne_fig = plot_simulated_cells(
            num_points=1000,
            expression_percentage=coverage_values[i],
            distribution=distribution,
            seed=69,
        )

        # Calculate the RSP area (for simplicity, let's assume it's the sum of coordinates for expressing cells)
        rsp_fig, rsp_area = generate_polygon(coordinates, is_expressing)

        # Collect data row by row
        rows.append(
            {
                "Gene Name": gene,
                "Coverage (%)": coverage_values[i] * 100,
                "RSP Area": rsp_area,
            }
        )

        if plots:
            os.makedirs(f"plots/simulation/{gene}", exist_ok=True)
            tsne_fig.write_image(
                f"plots/simulation/{gene}/{tsne_fig.layout.title.text}.png"
            )
            rsp_fig.write_image(
                f"plots/simulation/{gene}/{rsp_fig.layout.title.text}.png"
            )

    if data:
        # Convert the list of rows into a DataFrame
        master_df = pd.DataFrame(rows)

        # Save the master DataFrame to a CSV file
        master_df.to_csv("master_file.csv", index=False)
