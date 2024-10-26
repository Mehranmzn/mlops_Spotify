
# Mushroom Classification Project

![Mushroom Image](assets/dataset-cover.jpg)  
*Image Source: [Kaggle](https://www.kaggle.com/datasets/uciml/mushroom-classification)*

## Table of Contents

- [Introduction](#introduction)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
- [Modeling](#modeling)
- [Results](#results)
- [Conclusion](#conclusion)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---
## Goal

The objective of this project is to create and implement an MLOps pipeline for developing and deploying a predictive model that assesses the edibility of mushrooms based on their features. For this purpose, we will use:
- Docker
- MLflow
- GitHub Actions
- FastAPI

## Introduction about the data

This project involves the classification of mushrooms into edible or poisonous categories using machine learning techniques. The dataset used for this project is sourced from the [UCI Machine Learning Repository](https://www.kaggle.com/datasets/uciml/mushroom-classification). The goal of the project is to build a model that accurately predicts whether a mushroom is edible or poisonous based on its physical characteristics.

## Dataset

The dataset contains 22 features that describe different characteristics of mushrooms, such as cap shape, color, gill size, and odor. The target variable is a binary classification: whether the mushroom is edible (`e`) or poisonous (`p`).

- **Number of Instances:** 8124
- **Number of Features:** 22 categorical attributes
- **Target Variable:** Edibility (edible/poisonous)

The dataset can be found [here on Kaggle](https://www.kaggle.com/datasets/uciml/mushroom-classification).

## Project Structure

```plaintext
Mushroom-Classification/
│
├── data/
│   ├── mushroom.csv              # Original dataset
│   └── processed_data.csv        # Processed data used for modeling
│
├── notebooks/
│   ├── 01_data_preprocessing.ipynb   # Data preprocessing steps
│   ├── 02_exploratory_analysis.ipynb # Exploratory data analysis
│   └── 03_modeling.ipynb             # Model training and evaluation
│
├── models/
│   ├── random_forest.pkl        # Trained Random Forest model
│   └── decision_tree.pkl        # Trained Decision Tree model
│
├── images/
│   └── mushrooms.jpg            # Example image used in README
│
├── README.md                    # Project overview
└── LICENSE                      # License for the project
```

## Exploratory Data Analysis (EDA)

In the [EDA notebook](notebooks/02_exploratory_analysis.ipynb), various visualizations and statistical methods are employed to understand the relationships between the features and the target variable. Key insights include the importance of odor in determining mushroom edibility and the distribution of other attributes like cap color and gill size.

## Modeling

Several machine learning models were developed and evaluated to classify mushrooms, including:

- **Logistic Regression**
- **Decision Tree**
- **Random Forest**
- **Support Vector Machine**

The [modeling notebook](notebooks/03_modeling.ipynb) contains the details of the model training process, hyperparameter tuning, and evaluation metrics such as accuracy, precision, recall, and F1-score.

## Results

The Random Forest model achieved the highest accuracy of **99.3%**, making it the best-performing model for this task. Feature importance analysis revealed that odor, spore print color, and gill size were the most significant features.

## Conclusion

This project demonstrates the effectiveness of machine learning in classifying mushrooms as edible or poisonous based on their physical characteristics. The models developed in this project can be further optimized or deployed in applications where rapid and accurate mushroom classification is necessary.

## Usage

To run the project locally:

1. Clone the repository:

    ```bash
    git clone https://github.com/YourUsername/Mushroom-Classification.git
    ```

2. Navigate to the project directory and install the required dependencies:

    ```bash
    cd Mushroom-Classification
    pip install -r requirements.txt
    ```

3. Run the Jupyter notebooks to explore the data, visualize results, and train models.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for any suggestions, improvements, or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
