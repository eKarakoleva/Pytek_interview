from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
import task.models as m
import task.serializers as ser
import task.repositories as repo
from task.helper import get_filename, get_files_from_db
from django.http import Http404
#from rest_framework.decorators import api_view
#@api_view(['GET', 'PUT', 'DELETE'])

class ProductList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products.html'

    def get(self, request):
        productRepo = repo.ProductRepository(m.Product)
        queryset = productRepo.get_all_active()
        serializer = ser.ProductSerializer(queryset, many = True)
        return Response({'products': serializer.data}, status=status.HTTP_200_OK)

class ProductDetails(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product-details.html'
    def get(self, request, slug):
        serializerProduct = []
        productRepo = repo.ProductRepository(m.Product)
        queryset = productRepo.get_all_active_by_slug(slug)
        if queryset:
            serializerProduct = ser.ProductSerializer(queryset[0])
            serializerProduct = serializerProduct.data
            if float(queryset[0].quantity) > 0.0:
                available = True
            else:
                 available = False

            prductImages = get_files_from_db(repo.PostImageRepository, m.PostImage, ser.PostImageSerializer, queryset[0].id)
            prductDocuments = get_files_from_db(repo.PostDocumentRepository, m.PostDocument, ser.PostDocumentSerializer, queryset[0].id)
            
            if len(prductDocuments) != 0:
                for pr in prductDocuments:
                    pr['filename'] = get_filename(pr['doc'])

            serializerConProduct = []
            main_category = ""
            if available:
                if len(serializerProduct['category']) != 0:
                    subCatRepo = repo.SubcategoryRepository(m.Subcategory)
                    main_category = subCatRepo.get_main_category_name_by_subcategory(serializerProduct['category']['id'])

                cpRepo = repo.ConnectedProductsRepository(m.ConnectedProducts)
                activeConnections = cpRepo.get_all_active_by_id(queryset[0].id)
                if activeConnections:
                    serializerConProduct = ser.ConnectedProductsSerializer(activeConnections, many = True)
                    serializerConProduct = serializerConProduct.data
                    
            return Response({'product': serializerProduct, 'available': available, 'imags': prductImages, 'docs': prductDocuments, 'conprod': serializerConProduct, 'main_cat': main_category}, status=status.HTTP_200_OK)
        else:
            raise Http404
            #return Response({'products': queryset}, status=status.HTTP_404_NOT_FOUND)
