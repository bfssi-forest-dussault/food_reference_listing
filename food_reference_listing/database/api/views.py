from rest_framework.viewsets import ModelViewSet
from food_reference_listing.database.models import Product, Category, Subcategory, Company
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import ProductSerializer, CategoryNameSerializer, SubcategoryNameSerializer, CompanyNameSerializer


class Select2PaginationClass(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related('language', 'company', 'subcategory').all().order_by('-id')

        category = self.request.query_params.get('category', None)
        subcategory = self.request.query_params.get('subcategory', None)
        company = self.request.query_params.get('company', None)

        if category is not None and category is not '':
            queryset = queryset.filter(subcategory__category_id__header_en__iexact=category)

        if subcategory is not None and subcategory is not '':
            queryset = queryset.filter(subcategory__topic_en__iexact=subcategory)

        if company is not None and company is not '':
            queryset = queryset.filter(company__name_en__iexact=company)

        return queryset


class CompanyNameViewSet(ModelViewSet):
    pagination_class = Select2PaginationClass
    serializer_class = CompanyNameSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search', None)
        if search is not None:
            return Company.objects.filter(name_en__icontains=search)
        else:
            return Company.objects.all()


class CategoryNameViewSet(ModelViewSet):
    pagination_class = Select2PaginationClass
    serializer_class = CategoryNameSerializer

    def get_queryset(self):
        search = self.request.query_params.get('search', None)
        if search is not None:
            return Category.objects.filter(header_en__icontains=search)
        else:
            return Category.objects.all()


class SubcategoryNameViewSet(ModelViewSet):
    pagination_class = Select2PaginationClass
    serializer_class = SubcategoryNameSerializer

    def get_queryset(self):
        queryset = Subcategory.objects.all()

        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)

        if category is not None and category is not '':
            queryset = queryset.filter(category__header_en__iexact=category)
        if search is not None:
            queryset = queryset.filter(topic_en__icontains=search)

        return queryset
