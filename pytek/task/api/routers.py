import task.api.view as apiv
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api-v1/products', apiv.ProductViewSet)
router.register(r'api-v1/categorys', apiv.CategoryViewSet)
router.register(r'api-v1/subcategorys', apiv.SubcategoryViewSet)
router.register(r'api-v1/connected-products', apiv.ConnectedProductsViewSet)