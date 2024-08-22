import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ndtest
from matplotlib.gridspec import GridSpec

# Define the path variable
path = os.path.dirname(os.path.realpath(__file__)) + '\\Total Probabilities\\'
output_filename = "ks_results_ex3.csv"

# Load and preprocess the data
def load_data(path):
    df_plot = pd.read_csv(path + "final_combined_data.csv", usecols=["Star Name", "Experiment", "Overlap Star",
                                                                "[Fe/H]", "Mg/Si", "Disk Location"])
    df_plot = df_plot.set_index('Star Name')
    
    return df_plot

def preprocess_data(df):
    # Filter the DataFrame for the overlap stars and the desired experiment
    overlap_df = df[(df['Overlap Star'] == 'Yes') & (df['Experiment'] == 3)]
    # Filter the DataFrame for the non-overlap stars and the desired experiment
    non_overlap_df = df[(df['Overlap Star'] == 'No') & (df['Experiment'] == 3)]
    return overlap_df, non_overlap_df

# Define bins
def define_bins():
    xbinl, xbinr, binwidth = -1.0, 1.0, 0.1
    bins_x = np.arange(xbinl, xbinr + binwidth, binwidth)

    ybinl, ybinr, binwidth_y = 0.4, 2.0, 0.1
    bins_y = np.arange(ybinl, ybinr + binwidth_y, binwidth_y)

    return bins_x, bins_y, xbinl, xbinr, binwidth, ybinl, ybinr, binwidth_y

# Normalize histograms
def normalize_histogram(data, bins):
    histPredFe = np.histogram(data, bins=bins)
    max_count = float(max(histPredFe[0]))
    normPredFe = [float(num)/max_count for num in histPredFe[0]]
    return normPredFe

# Plotting function
def plot_data(overlap_df, non_overlap_df, bins_x, bins_y, xbinl, xbinr, binwidth, ybinl, ybinr, binwidth_y):
    fig = plt.figure(figsize=(8, 8))  # Set figure size to 800x800 pixels
    gs = GridSpec(4, 4, width_ratios=[1, 1, 1, 0.5], height_ratios=[0.5, 1, 1, 0.5])

    # Scatterplot
    ax_scatter = plt.subplot(gs[1:3, 0:3])
    ax_scatter.scatter(non_overlap_df['[Fe/H]'], non_overlap_df['Mg/Si'], edgecolor='#D81B60',
                       s=30, linewidths=0.8, marker='o', facecolor='none', label='Non-Overlap Stars')
    ax_scatter.scatter(overlap_df['[Fe/H]'], overlap_df['Mg/Si'], edgecolor='#1E88E5',
                       s=30, linewidths=0.8, marker='o', facecolor='none', label='Overlap Stars')
    ax_scatter.set_xlabel('[Fe/H]', fontsize=15)
    ax_scatter.set_ylabel('Mg/Si', fontsize=15)
    #ax_scatter.set_title('Scatterplot of Mg/Si vs. [Fe/H]')
    ax_scatter.set_xlim(xbinl, xbinr)
    ax_scatter.set_ylim(ybinl, ybinr)
    ax_scatter.set_xticks(np.arange(xbinl, xbinr + 0.2, 0.2))  # Scatterplot x-ticks in increments of 0.2
    ax_scatter.set_yticks(np.arange(ybinl, ybinr + 0.2, 0.2))  # Scatterplot y-ticks in increments of 0.2
    ax_scatter.grid(False)
    ax_scatter.legend(loc='upper right')  # Add legend to the scatterplot

    # Histogram for [Fe/H] (Top)
    ax_hist_x = plt.subplot(gs[0, 0:3], sharex=ax_scatter)
    non_overlap_hist_x = normalize_histogram(non_overlap_df['[Fe/H]'], bins_x)
    overlap_hist_x = normalize_histogram(overlap_df['[Fe/H]'], bins_x)
    ax_hist_x.bar(bins_x[:-1], non_overlap_hist_x, width=0.1, edgecolor='#D81B60', facecolor='None',
                  hatch='////', label='Non-Overlap Stars')
    ax_hist_x.bar(bins_x[:-1], overlap_hist_x, width=0.1, edgecolor='#1E88E5', facecolor='None',
                  hatch='\\\\', label='Overlap Stars')
    ax_hist_x.set_ylabel('Relative Dist.')  # Title for y-axis
    ax_hist_x.set_xticks(np.arange(xbinl, xbinr + 0.2, 0.2))  # Histogram x-ticks in increments of 0.2
    ax_hist_x.set_yticks(np.arange(0, 1.1, 0.5))  # Histogram y-ticks in increments of 0.2
    ax_hist_x.axis('on')  # Show x-axis labels and ticks

    # Histogram for Mg/Si (Right)
    ax_hist_y = plt.subplot(gs[1:3, 3], sharey=ax_scatter)
    non_overlap_hist_y = normalize_histogram(non_overlap_df['Mg/Si'], bins_y)
    overlap_hist_y = normalize_histogram(overlap_df['Mg/Si'], bins_y)
    ax_hist_y.barh(bins_y[:-1], non_overlap_hist_y, height=0.1, edgecolor='#D81B60', facecolor='None',
                   hatch='////', label='Non-Overlap Stars')
    ax_hist_y.barh(bins_y[:-1], overlap_hist_y, height=0.1, edgecolor='#1E88E5', facecolor='None',
                   hatch='\\\\', label='Overlap Stars')
    ax_hist_y.set_xlabel('Relative Dist.')  # Title for x-axis
    ax_hist_y.set_yticks(np.arange(ybinl, ybinr + 0.2, 0.2))  # Histogram y-ticks in increments of 0.2
    ax_hist_y.set_xticks(np.arange(0, 1.1, 0.5))  # Histogram x-ticks in increments of 0.2
    ax_hist_y.axis('on')  # Show y-axis labels and ticks

    # Adjust layout
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df_plot = load_data(path)
    overlap_df_plot, non_overlap_df_plot = preprocess_data(df_plot)
    bins_x, bins_y, xbinl, xbinr, binwidth, ybinl, ybinr, binwidth_y = define_bins()
    plot_data(overlap_df_plot, non_overlap_df_plot, bins_x, bins_y, xbinl, xbinr, binwidth, ybinl, ybinr, binwidth_y)
