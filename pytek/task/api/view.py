import task.models as m
import task.serializers as ser
import task.repositories as repo
from rest_framework import viewsets

class ProductViewSet(viewsets.ModelViewSet):
    prRepo = repo.ProductRepository(m.Product)
    queryset =  m.Product.objects.all()
    serializer_class = ser.ProductSerializer
    lookup_field = 'slug'

class CategoryViewSet(viewsets.ModelViewSet):
    catRepo = repo.CategoryRepository(m.Category)
    queryset = catRepo.get_all()
    serializer_class = ser.CategorySerializer
    lookup_field = 'slug'

class SubcategoryViewSet(viewsets.ModelViewSet):
    subcatRepo = repo.SubcategoryRepository(m.Subcategory)
    queryset = subcatRepo.get_all()
    serializer_class = ser.SubcategorySerializer
    lookup_field = 'slug'

class ConnectedProductsViewSet(viewsets.ModelViewSet):
    cpRepo = repo.ConnectedProductsRepository(m.ConnectedProducts)
    queryset = cpRepo.get_all()
    serializer_class = ser.ConnectedProductsSerializer
