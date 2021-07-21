from django.contrib.postgres import fields
from rest_framework import serializers
import task.models as tm


class SubcategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = tm.Subcategory
		fields ='__all__'

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = tm.Category
		fields ='__all__'

class PostImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = tm.PostImage
		fields ='__all__'

class PostDocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = tm.PostDocument
		fields ='__all__'

class ProductSerializer(serializers.ModelSerializer):

	category = CategorySerializer()
	class Meta:
		model = tm.Product
		fields = '__all__'

class ConnectedProductsSerializer(serializers.ModelSerializer):
	first_product = ProductSerializer()
	second_product = ProductSerializer()
	class Meta:
		model = tm.ConnectedProducts
		#fields ='__all__'
		fields = ('are_connected', 'are_purchased_together', 'first_product', 'second_product')
