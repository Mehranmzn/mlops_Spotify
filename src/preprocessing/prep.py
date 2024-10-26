import numpy as np  # Import NumPy for handling numerical operations
import pandas as pd  # Import Pandas for data manipulation and analysis
import warnings  # Import Warnings to suppress unnecessary warnings
from feature_engine.encoding import RareLabelEncoder

# Suppress warning messages
warnings.filterwarnings("ignore")


def read_():
    # Load the dataset
    df = pd.read_csv("data/raw/top_podcasts.csv")

    # Remove duplicates and report the number found
    initial_count = df.shape[0]
    df = df.drop_duplicates()
    duplicate_count = initial_count - df.shape[0]
    print(f"{duplicate_count} duplicates were found and removed from the dataset.")

    # Display dataset shape and column names for initial inspection
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

    # Calculate a 'rating' score based on the inverse log10 of rank
    max_rank = df['rank'].max()
    df['rating'] = df['rank'].apply(lambda x: np.log10(max_rank / x))

    # Function to log10-transform and bin numeric columns with rounding to nearest 0.5
    def log10_transform_bin(value):
        try:
            transformed = np.log10(value)
            return str(round(round(transformed * 2) / 2, 1))
        except (ValueError, TypeError):  # Handles missing or invalid values
            return 'None'

    # Apply transformation and binning to 'duration_ms' and 'show.total_episodes' columns
    df['log10_duration'] = df['duration_ms'].apply(log10_transform_bin)
    df['log10_episodes'] = df['show.total_episodes'].apply(log10_transform_bin)

    # Extract day of the week and month from the 'date' column
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()

    # Select relevant columns for analysis
    selected_columns = [
        'rating', 'day_of_week', 'month', 'region', 'show.publisher', 
        'log10_duration', 'log10_episodes', 'explicit', 'is_externally_hosted',
        'is_playable', 'language', 'show.explicit', 'show.is_externally_hosted',
        'show.media_type'
    ]
    df = df[selected_columns]

    # Display the final DataFrame's structure for verification
    print("Final dataset structure:")
    print(df.info())

    # Return the cleaned DataFrame
    return df  # <-- Added return statement here


def encoding_main_label(df):
    """
    Encodes non-numeric categorical columns in the DataFrame by replacing rare labels
    with a common placeholder ('Other'), except for the main target label.

    Parameters:
    df (pd.DataFrame): Input DataFrame to encode.

    Returns:
    pd.DataFrame: DataFrame with encoded categorical features.
    """

    # Define the main label column to exclude from encoding
    main_label = 'rating'

    # Initialize RareLabelEncoder for categorical encoding with specified tolerance
    encoder = RareLabelEncoder(n_categories=1, max_n_categories=100, tol=1 / df.shape[0])

    # Encode each column, excluding the main label column
    for col in df.columns:
        if col != main_label:
            print(f"Encoding rare labels in column: {col}")
            df[col] = df[col].fillna('None').astype(str)  # Fill missing and convert to string
            df[col] = encoder.fit_transform(df[[col]])

    return df


def main():
    df = read_()  # Now df will not be None
    print(df.head())  # This will now work as df is returned from read_()
    df = encoding_main_label(df)
    df.to_csv("data/cleaned/cleaned_data.csv", index=False)  # Added index=False to avoid index in the output CSV


if __name__ == '__main__':
    main()
