dvc add models/model.pkl

dvc push

git add data/cleaned/cleaned_data.csv.dvc models/catboost_model.pkl.dvc .gitignore
git commit -m "Track dataset and model with DVC"
