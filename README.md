# Mapping Bibliotheca Hertziana

## Introduction

This project was completed during an internship and as a Master's thesis at EPFL and Bibliotheca Hertziana from March 2023 until March 2024 in Rome, Lausanne and Zurich. 

## About the Project

The project introduces an innovative visual method for analysing libraries and archives, with a focus on Bibliotheca Hertziana's library collection. Tracing its origins back over a century, this collection is examined by integrating user loan data with deep mapping techniques to reveal usage patterns and thematic clusters. To achieve this, dimensionality reduction is employed to visualise the catalogue, mapping books based on their loans, and prompt engineering with large language models helps to identify loan clusters with detailed descriptions and titles. This approach not only paves the way for cultural analytics but also lays the groundwork for dynamic classification and developing a recommendation system. This project offers alternative insights into the art historical research conducted at the Bibliotheca Hertziana, capturing the collection's evolution and usage. The method established here provides a flexible framework for visually mapping cultural and academic collections in the digital humanities.


##  :file_folder: Repository Structure

```
.
├── internship                          # Results from internship
│   ├── data                            # Library exports
│   ├── embeddings                      # Preliminary mappings
│   ├── preprocessing                   # Data preprocessing
│   ├── sig_processing                  # Signature system processing
│   └── log.md                          # Internship log
├── thesis                              # Results from thesis 
│   ├── plots                           
│   └──  src
│       ├── data                        # Data inputs and exports
│       ├── exp                         # Exports 
│       ├── 1_analysis.ipynb            # Preliminary data set analysis
│       ├── 2_arrangement.ipynb         # Dimensionality Reduction and Parameterisation
│       ├── 3_evaluation.ipynb          # Evalutaing the mappings
│       ├── 4_separation.ipynb          # Seperating internal user loans
│       ├── 5_atlas.ipynb               # Prompting OpenAI, Cluster Atlas
│       ├── export.css                  # Html to pdf layout
│       └── module.py                   # Common functions
├── cluster_atlas_full.pdf              # Cluster Atlas
├── MappingBibliothecaHertziana.pdf     # Thesis Report
├── README.md                           # This file. 
└── requirements.txt                    # Requirements
```

## Installation and Usage

To set up and use this project, follow these steps:

### Prerequisites

Ensure you have the following installed:
- Python 3.10.11
- pip (Python package installer)

### Clone the Repository

First, clone this repository to your local machine using Git:

```
bash
git clone https://github.com/hanahCasey/BHVIZDATA.git
cd your-repository-name
```

### Install Dependencies

Install the required Python packages using pip:
```
bash
pip install -r requirements.txt
```

## Data

For privacy reasons, the user loan data used in this project is not published. 

## Results

Consult MappingBibliothecaHertziana.pdf to see the result of this thesis. 

## 
