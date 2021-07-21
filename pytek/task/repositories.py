from django.db.models import Q

class ProductRepository(object):
	def __init__(self, model):
		self.model = model

	def get_all(self):
		return self.model.objects.all()

	def get_all_active(self):
		return self.model.objects.filter(is_active = True)

	def get_all_active_by_slug(self, slug):
		return self.model.objects.filter(is_active = True, slug = slug).select_related('category')

class PostImageRepository(object):
	def __init__(self, model):
		self.model = model

	def get_all(self):
		return self.model.objects.all()

	def get_by_product_id(self, product_id):
		return self.model.objects.filter(product = product_id)

class PostDocumentRepository(object):
	def __init__(self, model):
		self.model = model

	def get_all(self):
		return self.model.objects.all()

	def get_by_product_id(self, product_id):
		return self.model.objects.filter(product = product_id)
	
	
class ConnectedProductsRepository(object):
	def __init__(self, model):
		self.model = model

	def get_all(self):
		return self.model.objects.all()

	def get_all_active(self):
		return self.model.objects.filter(is_active = True)

	def get_all_active_by_id(self, id):
		return self.model.objects.filter(
			(Q(first_product=id) | Q(second_product=id)) & 
			(Q(are_purchased_together = True) | Q(are_connected = True)) &
			(Q(first_product__is_active = True) & Q(second_product__is_active = True))
		)

class CategoryRepository(object):
	def __init__(self, model):
		self.model = model

	def get_all(self):
		return self.model.objects.all()

class SubcategoryRepository(object):
	def __init__(self, model):
		self.model = model

	def get_all(self):
		return self.model.objects.all()

	def get_main_category_name_by_subcategory(self, cat_id):
		main_category = self.model.objects.filter(id = cat_id).select_related('category').values('category__name')
		if len(main_category) != 0:
			main_category = main_category[0]['category__name']
		else:
			main_category = ""
		return main_category
