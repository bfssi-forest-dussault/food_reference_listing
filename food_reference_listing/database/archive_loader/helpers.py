from food_reference_listing.database import models
from pathlib import Path

import csv
from dateutil import parser
from django.utils.timezone import make_aware


def read_csv(f: Path) -> list:
    with open(str(f), 'r') as csv_:
        data = []
        reader = csv.DictReader(csv_)
        for row in reader:
            data.append(row)
    return data


def delete_all_rows_in_all_tables():
    [x.delete() for x in models.Language.objects.all()]
    [x.delete() for x in models.AcronymType.objects.all()]
    [x.delete() for x in models.Acronym.objects.all()]
    [x.delete() for x in models.Category.objects.all()]
    [x.delete() for x in models.Country.objects.all()]
    [x.delete() for x in models.ProvinceState.objects.all()]
    [x.delete() for x in models.City.objects.all()]
    [x.delete() for x in models.Company.objects.all()]
    [x.delete() for x in models.Subcategory.objects.all()]
    [x.delete() for x in models.Product.objects.all()]


def convert_row(header_mapping: dict, row: csv.OrderedDict) -> dict:
    new_row = {}

    for key, val in row.items():
        if key not in header_mapping:
            continue
        if val == "":
            val = None
        if header_mapping[key] == 'updated' or header_mapping[key] == 'acceptance_date':
            val = make_aware(parser.parse(val))  # Update timezone
        new_row[header_mapping[key]] = val
    return new_row


def populate_language_table(data: list):
    print("Populating Language table")
    header_mapping = {
        'LanguageID': 'language_id',
        'DescriptionE': 'description_en',
        'DescriptionF': 'description_fr',
        'LastUpdate': 'updated',
    }

    # Remove junk columns
    for row in data:
        # acronym_row, created = models.Acronym.objects.get_or_create(acronym_id=row_['AcronymID'])
        fields = convert_row(header_mapping=header_mapping, row=row)
        instance = models.Language.objects.create(**fields)
        instance.save()


def populate_acronym_type_table(data: list):
    print("Populating AcronymType table")
    # Map archive columns to corresponding columns in the new database
    header_mapping = {
        'AcronymTypeID': 'acronym_type_id',
        'DescriptionE': 'description_en',
        'DescriptionF': 'description_fr',
        'LastUpdate': 'updated'
    }

    for row in data:
        # acronym_row, created = models.Acronym.objects.get_or_create(acronym_id=row_['AcronymID'])
        fields = convert_row(header_mapping=header_mapping, row=row)
        instance = models.AcronymType.objects.create(**fields)
        instance.save()


def populate_acronym_table(data: list):
    print("Populating Acronym table")
    # Map archive columns to corresponding columns in the new database
    header_mapping = {
        'AcronymID': 'acronym_id',
        'LanguageID': 'language',  # Object
        'DescriptionE': 'description_en',
        'DescriptionF': 'description_fr',
        'AcronymTypeID': 'acronym_type',  # Object
        'LastUpdate': 'updated'
    }

    for row in data:
        fields = convert_row(header_mapping=header_mapping, row=row)
        fields['acronym_type'] = models.AcronymType.objects.get(acronym_type_id=fields['acronym_type'])
        fields['language'] = models.Language.objects.get(language_id=fields['language'])
        instance = models.Acronym.objects.create(**fields)
        instance.save()


def populate_category_table(data: list):
    print("Populating Category table")
    header_mapping = {
        'CategoryID': 'category_id',
        'HeaderE': 'header_en',  # Object
        'HeaderF': 'header_fr',
        'NoteE': 'note_en',
        'NoteF': 'note_fr',  # Object
        'LastUpdate': 'updated'
    }

    for row in data:
        fields = convert_row(header_mapping=header_mapping, row=row)
        instance = models.Category.objects.create(**fields)
        instance.save()


def populate_country_table(data: list):
    print("Populating Country table")
    header_mapping = {
        'CountryID': 'country_id',
        'DescriptionE': 'description_en',  # Object
        'DescriptionF': 'description_fr',
        'LastUpdate': 'updated'
    }
    for row in data:
        fields = convert_row(header_mapping=header_mapping, row=row)
        instance = models.Country.objects.create(**fields)
        instance.save()


def populate_provincestate_table(data: list):
    print("Populating ProvinceState table")
    header_mapping = {
        'ProvinceStateID': 'province_state_id',
        'ProvinceStateCode': 'province_state_code',
        'DescriptionE': 'description_en',
        'DescriptionF': 'description_fr',
        'CountryID': 'country',  # Object
        'LastUpdate': 'updated'
    }
    for row in data:
        fields = convert_row(header_mapping=header_mapping, row=row)
        fields['country'] = models.Country.objects.get(country_id=fields['country'])
        instance = models.ProvinceState.objects.create(**fields)
        instance.save()


def populate_city_table(data: list):
    print("Populating City table")
    header_mapping = {
        'CityID': 'city_id',
        'DescriptionE': 'description_en',
        'DescriptionF': 'description_fr',
        'ProvinceStateID': 'province_state',  # Object
        'CountryID': 'country',  # Object
        'LastUpdate': 'updated'
    }
    for row in data:
        fields = convert_row(header_mapping=header_mapping, row=row)
        fields['country'] = models.Country.objects.get(country_id=fields['country'])

        try:
            fields['province_state'] = models.ProvinceState.objects.get(province_state_id=fields['province_state'])
        except Exception as e:
            fields['province_state'] = None
        instance = models.City.objects.create(**fields)
        instance.save()


def populate_company_table(data: list):
    print("Populating Company table")
    header_mapping = {
        'CompanyID': 'company_id',
        'NameE': 'name_en',
        'NameF': 'name_fr',
        'LanguageID': 'language',  # Object
        'CityID': 'city',  # Object
        'PostalCode': 'postal_code',
        'LastUpdate': 'updated'
    }
    for row in data:
        fields = convert_row(header_mapping=header_mapping, row=row)
        fields['language'] = models.Language.objects.get(language_id=fields['language'])
        fields['city'] = models.City.objects.get(city_id=fields['city'])
        instance = models.Company.objects.create(**fields)
        instance.save()


def populate_subcategory_table(data: list):
    print("Populating Subcategory table")
    header_mapping = {
        'SubCategoryID': 'subcategory_id',
        'sub_category_code': 'subcategory_code',
        'TopicE': 'topic_en',
        'TopicF': 'topic_fr',
        'long_topic_E': 'long_topic_en',
        'long_topic_F': 'long_topic_fr',
        'condition_use_en': 'condition_use_en',
        'condition_use_fr': 'condition_use_fr',
        'CategoryID': 'category',  # Object
        'LastUpdate': 'updated'
    }
    for row in data:
        fields = convert_row(header_mapping=header_mapping, row=row)
        fields['category'] = models.Category.objects.get(category_id=fields['category'])
        try:
            instance = models.Subcategory.objects.create(**fields)
        except Exception as e:
            print(f'Skipping entry due to duplicate key: {fields}')
            continue
        instance.save()


def populate_product_table(data: list):
    print("Populating Product table")
    header_mapping = {
        'ProductID': 'product_code',
        'NameE': 'product_name_en',
        'NameF': 'product_name_fr',
        'LanguageID': 'language',  # Object
        'ApprovalDate': 'acceptance_date',
        'CompanyID': 'company',  # Object
        'SubCategoryID': 'subcategory',  # Object
        'LastUpdate': 'updated'
    }
    for row in data:
        fields = convert_row(header_mapping=header_mapping, row=row)
        fields['language'] = models.Language.objects.get(language_id=fields['language'])
        fields['company'] = models.Company.objects.get(company_id=fields['company'])
        fields['subcategory'] = models.Subcategory.objects.get(subcategory_id=fields['subcategory'])
        instance = models.Product.objects.create(**fields)
        instance.save()
