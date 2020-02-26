from rest_framework.routers import DefaultRouter, SimpleRouter
from django.conf import settings
from food_reference_listing.users.api.views import UserViewSet
from food_reference_listing.database.api.views import ProductViewSet, CategoryNameViewSet, SubcategoryNameViewSet, \
    CompanyNameViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("products", ProductViewSet, basename='products')
router.register("category_names", CategoryNameViewSet, basename='category_names')
router.register("subcategory_names", SubcategoryNameViewSet, basename='subcategory_names')
router.register("company_names", CompanyNameViewSet, basename='company_names')

app_name = "api"
urlpatterns = router.urls
