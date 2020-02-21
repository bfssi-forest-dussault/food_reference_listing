from rest_framework import serializers
from food_reference_listing.database.models import Product, Country, Company, Language, Subcategory, City, ProvinceState


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"


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
    updated = serializers.DateTimeField()

    # subcategory_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id",
                  "product_code",
                  "product_name_en",
                  "product_name_fr",
                  "acceptance_date",
                  "updated",
                  "company",
                  "language",
                  # "subcategory_id"
                  ]
