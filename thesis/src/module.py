import ast
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns


SUBJECT_DICT = {'A': 'Manuals', 'B': 'Italian Art', 'C': 'Italian Artists', 'D': 'Rome','E':'Italian Topography', 'F': 'Travel Literature', 
               'G': 'Sources', 'H': 'Iconography', 'J': 'Ornament','Kat': 'Catalogues','K': 'Commemorative and Collected Writings','L': 'Congress Publications', 'M': 'Art in General',
                'N': 'Architecture', 'O':'Sculpture','Per': 'Periodicals', 'P': 'Painting', 'Q': 'Manuscript Illumination', 'R': 'Graphic Arts', 
               'S': 'Applied Arts', 'T': 'Collecting Art, Museum Studies', 'U': 'Registers of Artistic Monuments', 'V': 'Cultural Institutions', 
               'W': 'Non-Italian Artists','X': 'European Topography', 'Y': 'World Topography', 'Z': 'Related Disciplines'}

CUSTOM_COLOURS = [
    "#EA522B", "#EFD4D1", "#2A4978", "#8BDBE1", "#ECA19D", "#B48E36", "#EB84D6", "#B8BFCE", "#FAC73B", "#91C5E4",
    "#6E8EAC", "#D2E7E0","#DAA47F", "#ECD096", "#6C9686", "#9ACC8C", "#9D4B37", "#A3B49D", "#BDC920", "#DBE3E5", "#6A8B8D",
    "#EFB3D1", "#F6A1B4", "#5499C7", "#1C2833", "#F0B27A", "#2E7F7F", "#CB4335", "#4A235A"
]

CUSTOM_CMAP = ListedColormap(CUSTOM_COLOURS)

#########################################
# DataFrame Processing Functions
#########################################

def get_subject(call_number):
    """
    Retrieves the subject category for a given book call number.
    
    Args:
        call_number (str): The call number of the book.
    
    Returns:
        str: The subject category corresponding to the call number.
    """
    for key, category in SUBJECT_DICT.items():
        if call_number.startswith(key):
            return category
    return 'Unknown'

def eval_as(df):
    """
    Converts string representations in DataFrame columns to their respective 
    literal structures (lists or dictionaries).
    
    Args:
        df (DataFrame): DataFrame with string representations to convert.
    
    Returns:
        DataFrame: DataFrame with converted structures.
    """
    df['yearly_frequency'] = df['yearly_frequency'].apply(ast.literal_eval)
    df['yearly_frequency_norm'] = df['yearly_frequency_norm'].apply(ast.literal_eval)
    df['users'] = df['users'].apply(ast.literal_eval)
    df['users_weighed'] = df['users_weighed'].apply(ast.literal_eval)
    return df

def sum_loan_times(freq_dicts):
    """
    Aggregates loan times for each year.
    
    Args:
        freq_dicts (list of dict): List of dictionaries with year as key and loan times as values.
    
    Returns:
        dict: Dictionary with years as keys and aggregated loan times as values.
    """
    summed_times = {}

    for year in range(2013, 2024):
        summed_times[year] = 0

    for freq_dict in freq_dicts:
        for year, time in freq_dict.items():
            summed_times.setdefault(year, 0)
            summed_times[year] += time
    return summed_times


#########################################
# PLotting Functions
#########################################

def plot_embedding(embedding, title):
    """
    Plots an embedding in a 2D space.
    
    Args:
    embedding (array-like): The embedding to be plotted, typically an Nx2 array.
    title (str): The title of the plot.
    """
    plt.figure(figsize=(20, 15), dpi=300)
    plt.scatter(embedding[:, 0], embedding[:, 1], s=8, c='black')
    plt.text(0.05, 0.95, title, transform=plt.gca().transAxes, fontsize=16, ha='left', fontname='Helvetica')
    plt.axis('off')
    plt.show()

def plot_clustering(df, hdb):
    """
    Plots the result of HDBSCAN clustering.
    
    Args:
    df (DataFrame): The DataFrame containing the data points and their coordinates.
    hdb (HDBSCAN): The HDBSCAN clustering result object.
    """
    color_palette = sns.color_palette('deep', 500)
    cluster_colors = [color_palette[x] if x >= 0 else (0.5, 0.5, 0.5) for x in hdb.labels_]
    cluster_member_colors = [sns.desaturate(x, p) for x, p in zip(cluster_colors, hdb.probabilities_)]

    plt.figure(figsize=(20, 15), dpi=300)
    plt.scatter(df['x'], df['y'], s=2, c=cluster_member_colors)

    for cluster_number in np.unique(hdb.labels_):
        if cluster_number != -1:
            cluster_indices = np.where(hdb.labels_ == cluster_number)[0]
            cluster_x = df.iloc[cluster_indices]['x'].mean()
            cluster_y = df.iloc[cluster_indices]['y'].mean()
            plt.text(cluster_x, cluster_y, str(cluster_number), fontsize=16, ha='center')

    # plt.text(0.05, 0.95, 'HDBSCAN clustering', transform=plt.gca().transAxes, fontsize=16, ha='left', fontname='Helvetica')
    plt.axis('off')
    plt.show()


def small_multiple_subject(df):
    """
    Plots a grid of scatter plots for each subject, showing their embeddings.
    
    Args:
        df (DataFrame): DataFrame containing subject, x, and y columns for plotting.
    """
    unique_subjects = df['Subject'].unique()
    n_subjects = len(unique_subjects)

    num_cols = 4
    num_rows = (n_subjects - 1) // num_cols + 1

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 40), dpi=300)

    for i, subject in enumerate(unique_subjects):
        row, col = i // num_cols, i % num_cols
        ax = axes[row, col]
        ax.set_title(f'{subject}')

        subject_data = df[df.Subject == subject]
        x_values = subject_data['x'].to_list()
        y_values = subject_data['y'].to_list()
        color = CUSTOM_CMAP(i / (n_subjects - 1))
        ax.scatter(x_values, y_values, s=2, c=color)
        ax.axis("off")

    # Hide empty subplots
    for i in range(len(unique_subjects), num_rows * num_cols):
        row, col = i // num_cols, i % num_cols
        fig.delaxes(axes[row, col])

    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.show()


def subject_heatmap(df):
    """
    Creates a heatmap showing the percentage of each subject in each cluster.
    
    Args:
        df (DataFrame): DataFrame containing cluster, Subject, and frequency information.
    """
    subject_cluster_matrix = pd.crosstab(df['cluster'], df['Subject'], values=df['frequency'], aggfunc='sum').fillna(0)
    ordered_subjects = [SUBJECT_DICT[key] for key in sorted(SUBJECT_DICT.keys())]
    subject_cluster_matrix = subject_cluster_matrix[ordered_subjects]
    cluster_totals = subject_cluster_matrix.sum(axis=1)
    subject_cluster_percentage = subject_cluster_matrix.div(cluster_totals, axis=0)

    plt.figure(figsize=(12, 8), dpi=300)
    sns.heatmap(subject_cluster_percentage, xticklabels=True, vmax=1.0)
    plt.title("Subject Percentage in Clusters")
    plt.xlabel("Subject")
    plt.ylabel("Cluster")
    plt.xticks(rotation=45, ha='right')
    plt.show()


def temporality_heatmap(df):
    """
    Creates a heatmap to visualize loan times for each cluster over the years.
    
    Args:
        df (DataFrame): DataFrame containing cluster and yearly_frequency information.
    """
    cluster_frequencies = df.groupby('cluster')['yearly_frequency'].aggregate(sum_loan_times)
    cluster_yearly_time_df = pd.DataFrame(cluster_frequencies.tolist()).fillna(0)
    sorted_columns = sorted(cluster_yearly_time_df.columns)
    cluster_yearly_time_df = cluster_yearly_time_df[sorted_columns]
    cluster_total_loan_times = cluster_yearly_time_df.sum(axis=1)
    cluster_yearly_percentage = cluster_yearly_time_df.div(cluster_total_loan_times, axis=0)

    plt.figure(figsize=(12, 8), dpi=300)
    sns.heatmap(cluster_yearly_percentage, vmax=1.0)
    plt.title("Normalized Loan Time by Cluster and Year")
    plt.xlabel("Year")
    plt.ylabel("Cluster")
    plt.show()


def language_heatmap(df):
    """
    Creates a heatmap showing the percentage of different languages per cluster.
    
    Args:
        df (DataFrame): DataFrame containing cluster, language, and frequency information.
    """
    lang_cluster_matrix = pd.crosstab(df['cluster'], df['lang'], values=df['frequency'], aggfunc='sum').fillna(0)
    cluster_totals = lang_cluster_matrix.sum(axis=1)
    lang_cluster_percentage = lang_cluster_matrix.div(cluster_totals, axis=0)

    plt.figure(figsize=(12, 8), dpi=300)
    sns.heatmap(lang_cluster_percentage, xticklabels=True, vmax=1.0)
    plt.title("Percentage of languages per cluster")
    plt.xlabel("Language")
    plt.ylabel("Cluster")
    plt.xticks(rotation=45, ha='right')
    plt.show()

def plot_loan_density(df):
    """
    Plots loan density across different years using scatter and KDE plots.
    
    Args:
        df (DataFrame): DataFrame containing x and y coordinates and the yearly frequency of loans
    """
    
    unique_years = np.arange(2013, 2024)

    num_cols = 2
    num_rows = (len(unique_years) - 1) // num_cols + 1 # subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 6 * num_rows), dpi=300)

    for i, year in enumerate(unique_years):
        row, col = i // num_cols, i % num_cols
        ax = axes[row, col]
        ax.set_title(f'{year}', fontdict={'fontsize':16})

        year_data = df[df['yearly_frequency_norm'].apply(lambda norm: norm.get(year, 0) > 0)]
        x_values = year_data['x'].to_list()
        y_values = year_data['y'].to_list()
        frequencies = [row['yearly_frequency_norm'].get(year, 0) for _, row in year_data.iterrows()]

        sc = ax.scatter(x_values, y_values, s=5 ,alpha = 0.5)
        sns.kdeplot(x=x_values, y=y_values, weights=frequencies, ax=ax, cmap="Reds", fill=True, alpha=0.7)
        ax.axis("off")

    # Hide empty subplots
    for i in range(len(unique_years), num_rows * num_cols):
        row, col = i // num_cols, i % num_cols
        fig.delaxes(axes[row, col])

    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.show()