from rest_framework.viewsets import ModelViewSet
from food_reference_listing.database.models import Product

from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('language', 'company').all().order_by('-id')
