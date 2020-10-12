from django.contrib import admin
from .models import Account, Rent,Product_images,Cart,Search

# Register your models here.
class RentAdmin(admin.ModelAdmin):
	list_display = ('title', 'submit_user','views','category')
	list_filter = ['title','category','views']
	search_fields = ['title']




admin.site.register(Account)
admin.site.register(Rent,RentAdmin)

admin.site.register(Product_images)
admin.site.register(Cart)
admin.site.register(Search)