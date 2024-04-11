from django.contrib import admin
from django.urls import path
from sales.views import sales_statistics, SaleViewSet, ProductViewSet
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'vendas', SaleViewSet)
router.register(r'produtos', ProductViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="sales",
      default_version='v1',
      description="sales api",
   ),
   public=True,
   permission_classes=(AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('sales-stats/', sales_statistics),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += router.urls
