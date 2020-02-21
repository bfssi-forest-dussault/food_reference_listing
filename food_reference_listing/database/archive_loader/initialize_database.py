import sys
import django
from pathlib import Path

# Need to do this in order to access the database models
sys.path.append("/app")
django.setup()

# For some bizarre reason I need to import all functions, rather than have them be defined in this file vOv
from food_reference_listing.database.archive_loader.helpers import *

"""
Script to load the archived data into the new database.

Call it using this command:
docker-compose -f local.yml run --rm django python manage.py shell < food_reference_listing/database/archive_loader/initialize_database.py
"""

# Script starts here
data_dir = Path('/app/food_reference_listing/database/archive_data')
assert data_dir.is_dir()
print(f'Confirmed data is available in {data_dir}')

# Keys correspond 1:1 with database.Model names
table_dict = {
    'Acronym': data_dir / 'Acronyms.csv',
    'AcronymType': data_dir / 'AcronymTypes.csv',
    'Category': data_dir / 'Categories.csv',
    'Country': data_dir / 'Countries.csv',
    'ProvinceState': data_dir / 'ProvinceStates.csv',
    'City': data_dir / 'Cities.csv',
    'Company': data_dir / 'Companies.csv',
    'Subcategory': data_dir / 'SubCategories.csv',
    'Product': data_dir / 'Products_Combined.csv',  # Combination of Products.csv and Final Web Update.csv
    'Language': data_dir / 'Languages.csv',
}

print(f'Confirming expected source data files exist')
# Make sure our data files exist
for model, src in table_dict.items():
    assert src.exists()

print(f'Deleting all entries in existing database')
# Cleanup while we debug
delete_all_rows_in_all_tables()

# Start populating tables
print(f'Recreating database with data files from {data_dir}')
populate_language_table(data=read_csv(table_dict['Language']))
populate_acronym_type_table(data=read_csv(table_dict['AcronymType']))
populate_acronym_table(data=read_csv(table_dict['Acronym']))
populate_category_table(data=read_csv(table_dict['Category']))
populate_country_table(data=read_csv(table_dict['Country']))
populate_provincestate_table(data=read_csv(table_dict['ProvinceState']))
populate_city_table(data=read_csv(table_dict['City']))
populate_company_table(data=read_csv(table_dict['Company']))
populate_subcategory_table(data=read_csv(table_dict['Subcategory']))
populate_product_table(data=read_csv(table_dict['Product']))
