from django.contrib import admin
import task.models as tm

# Register your models here.
admin.site.register(tm.Category)
admin.site.register(tm.Subcategory)
admin.site.register(tm.ConnectedProducts)
 
class PostImageAdmin(admin.StackedInline):
    model = tm.PostImage

class PostDocumentAdmin(admin.StackedInline):
    model = tm.PostDocument
 
@admin.register(tm.Product)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin, PostDocumentAdmin]
 
    class Meta:
       model = tm.Product
 
@admin.register(tm.PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass

@admin.register(tm.PostDocument)
class PostDocumentAdmin(admin.ModelAdmin):
    pass
