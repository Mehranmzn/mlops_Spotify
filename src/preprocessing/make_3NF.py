import pandas as pd

# Load the original CSV file
data = pd.read_csv('data/cleaned/cleaned_data.csv')

# Extract unique records for each dimension and save as separate CSVs

# Date Dimension: Extract unique day_of_week and month
dim_date = data[['day_of_week', 'month']].drop_duplicates()
dim_date['date_id'] = range(1, len(dim_date) + 1)  # Create unique ID
dim_date.to_csv('data/tables/dim_date.csv', index=False)

# Region Dimension: Extract unique region records
dim_region = data[['region']].drop_duplicates()
dim_region['region_id'] = range(1, len(dim_region) + 1)  # Create unique ID
dim_region.to_csv('data/tables/dim_region.csv', index=False)

# Show Dimension: Extract unique show-related records
dim_show = data[['show.publisher', 'explicit', 'is_externally_hosted', 'is_playable', 'language', 'show.explicit', 'show.is_externally_hosted', 'show.media_type']].drop_duplicates()
dim_show['show_id'] = range(1, len(dim_show) + 1)  # Create unique ID
dim_show.to_csv('data/tables/dim_show.csv', index=False)

# Fact Table: Map IDs and save metrics data
# Merge data with dimensions to obtain IDs
fact_show_metrics = data.merge(dim_date, on=['day_of_week', 'month'], how='left') \
                        .merge(dim_region, on='region', how='left') \
                        .merge(dim_show, on=['show.publisher', 'explicit', 'is_externally_hosted', 'is_playable', 'language', 'show.explicit', 'show.is_externally_hosted', 'show.media_type'], how='left')

# Select relevant columns for fact table
fact_show_metrics = fact_show_metrics[['date_id', 'region_id', 'show_id', 'rating', 'log10_duration', 'log10_episodes']]
fact_show_metrics.to_csv('data/tables/fact_show_metrics.csv', index=False)
