from django.db import models
from simple_history.models import HistoricalRecords


class Language(models.Model):
    language_id = models.CharField(max_length=2, blank=True, null=True, unique=True)
    description_en = models.CharField(max_length=16, blank=True, null=True, unique=True)
    description_fr = models.CharField(max_length=16, blank=True, null=True, unique=True)
    updated = models.DateTimeField()  # Historical record of previous DB
    history = HistoricalRecords()

    def __str__(self):
        try:
            return f'{self.language_id}: {self.description_en}'
        except TypeError as e:
            return ''


class AcronymType(models.Model):
    acronym_type_id = models.CharField(max_length=16, null=True, blank=True, unique=True)
    description_en = models.CharField(max_length=16, null=True, blank=True)
    description_fr = models.CharField(max_length=16, null=True, blank=True)
    updated = models.DateTimeField()  # Historical record of previous DB
    history = HistoricalRecords()


class Acronym(models.Model):
    acronym_id = models.CharField(max_length=8, null=True, blank=True, unique=True)
    language = models.ForeignKey(Language, related_name="acronyms", on_delete=models.SET_NULL, null=True)
    description_en = models.CharField(max_length=64, blank=True, null=True)
    description_fr = models.CharField(max_length=64, blank=True, null=True)
    acronym_type = models.ForeignKey(AcronymType, related_name="acronyms", on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField()  # Historical record of previous DB
    history = HistoricalRecords()


class Category(models.Model):
    category_id = models.IntegerField(null=True, blank=True, unique=True)
    header_en = models.CharField(max_length=256, blank=True, null=True)
    header_fr = models.CharField(max_length=256, blank=True, null=True)
    note_en = models.TextField(blank=True, null=True)
    note_fr = models.TextField(blank=True, null=True)
    updated = models.DateTimeField()  # Historical record of previous DB
    history = HistoricalRecords()

    def __str__(self):
        try:
            return f'{self.category_id}: {self.header_en}'
        except TypeError as e:
            return ''

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Country(models.Model):
    country_id = models.IntegerField(null=True, blank=True, unique=True)
    description_en = models.CharField(max_length=256, null=True, blank=True)
    description_fr = models.CharField(max_length=256, null=True, blank=True)
    updated = models.DateTimeField()  # Historical record of previous DB
    history = HistoricalRecords()


class ProvinceState(models.Model):
    province_state_id = models.IntegerField(null=True, blank=True, unique=True)
    province_state_code = models.CharField(max_length=8, unique=True, null=True, blank=True)
    description_en = models.CharField(max_length=256, null=True, blank=True)
    description_fr = models.CharField(max_length=256, null=True, blank=True)
    country = models.ForeignKey(Country, related_name="provincestates", on_delete=models.CASCADE)
    updated = models.DateTimeField()  # Historical record of previous DB
    history = HistoricalRecords()


class City(models.Model):
    city_id = models.IntegerField(null=True, blank=True, unique=True)
    description_en = models.CharField(max_length=256, null=True, blank=True)
    description_fr = models.CharField(max_length=256, null=True, blank=True)
    province_state = models.ForeignKey(ProvinceState, on_delete=models.SET_NULL, blank=True, null=True)
    country = models.ForeignKey(Country, related_name="cities", on_delete=models.SET_NULL, null=True, blank=True)
    updated = models.DateTimeField()  # Historical record of previous DB
    history = HistoricalRecords()


class Company(models.Model):
    company_id = models.CharField(max_length=16, unique=True, blank=True, null=True)
    name_en = models.CharField(max_length=256, blank=True, null=True)
    name_fr = models.CharField(max_length=256, blank=True, null=True)
    language = models.ForeignKey(Language, related_name="companies", on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, related_name="companies", on_delete=models.SET_NULL, null=True)
    postal_code = models.CharField(max_length=16, blank=True, null=True)
    updated = models.DateTimeField()  # Historical record of previous DB
    history = HistoricalRecords()

    def __str__(self):
        try:
            return f'{self.company_id}: {self.name_en}'
        except TypeError as e:
            return ''

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Subcategory(models.Model):
    subcategory_id = models.IntegerField(null=True, blank=True, unique=True)
    subcategory_code = models.CharField(max_length=8, null=True, blank=True, unique=True)
    topic_en = models.CharField(max_length=256, null=True, blank=True)
    topic_fr = models.CharField(max_length=256, null=True, blank=True)
    long_topic_en = models.TextField(null=True, blank=True)
    long_topic_fr = models.TextField(null=True, blank=True)
    condition_use_en = models.TextField(null=True, blank=True)
    condition_use_fr = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    updated = models.DateTimeField()  # Historical record of previous DB
    history = HistoricalRecords()

    def __str__(self):
        try:
            return f'{self.subcategory_code}: {self.topic_en}'
        except TypeError as e:
            return ''

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'


class Product(models.Model):
    """
    Corresponds with extremely poorly named 'Final Web Update' table --> might need to combine with original Products
    table, not sure how these datasets overlap though
    """
    product_code = models.CharField(max_length=16, unique=True, blank=True, null=True)
    product_name_en = models.CharField(max_length=256, unique=False, blank=True, null=True)
    product_name_fr = models.CharField(max_length=256, unique=False, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    acceptance_date = models.DateTimeField(blank=True, null=True)
    company = models.ForeignKey(Company, related_name="products", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, related_name="products", on_delete=models.CASCADE, blank=True,
                                    null=True)
    updated = models.DateTimeField(blank=True, null=True)  # Historical record of previous DB
    history = HistoricalRecords()

    @property
    def acceptance_date_pretty(self):
        return f'{self.acceptance_date.strftime("%Y-%m-%d")}'

    def __str__(self):
        try:
            return f'{self.product_code}: {self.product_name_en}'
        except TypeError as e:
            return ''

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
