from rest_framework.routers import DefaultRouter, SimpleRouter
from django.conf import settings
from food_reference_listing.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls
