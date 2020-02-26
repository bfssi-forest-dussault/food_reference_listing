from rest_framework import serializers
from food_reference_listing.database.models import Product, Country, Company, Language, Subcategory, City, \
    ProvinceState, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SubcategorySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    category = CategorySerializer()

    class Meta:
        model = Subcategory
        fields = [
            'id',
            'subcategory_code',
            'topic_en',
            'topic_fr',
            'long_topic_en',
            'long_topic_fr',
            'condition_use_en',
            'condition_use_fr',
            'category'
        ]


class SubcategoryNameSerializer(serializers.ModelSerializer):
    """ Retrieve only the topic_en and topic_fr values for the select2 dropdown menu on webpage """
    id = serializers.ReadOnlyField()
    # category = serializers.CharField(
    #     source='category.header_en',
    #     read_only=True,
    # )
    category = CategorySerializer()

    class Meta:
        model = Subcategory
        fields = [
            'id',
            'topic_en',
            'topic_fr',
            'category'
        ]


class CategoryNameSerializer(serializers.ModelSerializer):
    """ Retrieve only the header_en and header_fr values for the select2 dropdown menu on webpage """
    id = serializers.ReadOnlyField()
    text = serializers.CharField(source='header_en')

    class Meta:
        model = Category
        fields = [
            'id',
            'text',
            # 'header_fr'
        ]


class CompanyNameSerializer(serializers.ModelSerializer):
    """ Retrieve only the header_en and header_fr values for the select2 dropdown menu on webpage """
    id = serializers.ReadOnlyField()
    text = serializers.CharField(source='name_en')

    class Meta:
        model = Company
        fields = [
            'id',
            'text',
            # 'header_fr'
        ]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['language_id']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class ProvinceStateSerializer():
    class Meta:
        model = ProvinceState
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    country_id = CountrySerializer()
    province_state_id = ProvinceStateSerializer()

    class Meta:
        model = City
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    # city_id = CitySerializer()
    # language_id = LanguageSerializer()

    class Meta:
        model = Company
        fields = [
            'company_id',
            'name_en',
            'name_fr',
        ]


class ProductSerializer(serializers.ModelSerializer):
    """ TODO: Return correct language product name depending on current browser language """

    id = serializers.ReadOnlyField()

    company = CompanySerializer()

    language = serializers.CharField(
        source='language.language_id',
        read_only=True,
    )
    acceptance_date = serializers.DateTimeField()
    acceptance_date_pretty = serializers.ReadOnlyField()
    updated = serializers.DateTimeField()
    subcategory = SubcategorySerializer()

    # subcategory = serializers.CharField(
    #     source='subcategory.topic_en',
    #     read_only=True,
    # )

    class Meta:
        model = Product
        fields = ["id",
                  "product_code",
                  "product_name_en",
                  "product_name_fr",
                  "acceptance_date",
                  "acceptance_date_pretty",
                  "updated",
                  "company",
                  "language",
                  "subcategory"
                  ]
