import ast
import numpy as np
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




def get_subject(call_number):
    """
    Returns the subject category given a book's call number.
    
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
    Converts string representations of lists and dictionaries in DataFrame columns to actual lists and dictionaries.
    
    Args:
    df (DataFrame): The DataFrame with string representations of lists and dictionaries.
    
    Returns:
    DataFrame: The modified DataFrame with actual lists and dictionaries.
    """
    df['yearly_frequency'] = df['yearly_frequency'].apply(ast.literal_eval)
    df['yearly_frequency_norm'] = df['yearly_frequency_norm'].apply(ast.literal_eval)
    df['users'] = df['users'].apply(ast.literal_eval)
    df['users_weighed'] = df['users_weighed'].apply(ast.literal_eval)
    return df

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
            plt.text(cluster_x, cluster_y, str(cluster_number), fontsize=8, ha='center')

    plt.text(0.05, 0.95, 'HDBSCAN clustering', transform=plt.gca().transAxes, fontsize=16, ha='left', fontname='Helvetica')
    plt.axis('off')
    plt.show()