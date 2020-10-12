from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.fields import Field

# Create your models here.

class Account(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	agencyname = models.TextField(null=True)
	website = models.TextField(null=True)
	created = models.DateTimeField(auto_now_add=True)
	phone_no= models.CharField(max_length=20, null=True)
	image = models.ImageField(upload_to="profile_images",null=True)
	rate = models.IntegerField(default=0, null=True)
	rate_count = models.IntegerField(default=0, null=True)



	def __str__(self):
		return self.user.username


class Product_images(models.Model):
	images = models.ImageField(upload_to="product_images")
	def ___str__(self):
		return images

class Reviews(models.Model):
	text = models.TextField(null=True)
	created = models.DateTimeField(auto_now_add=True)
	account = models.ForeignKey(Account, on_delete=models.CASCADE)

	def ___str__(self):
		return account.user.username

	class Meta:
		ordering = ["-created"]



class Rent(models.Model):
	submit_user = models.ForeignKey(Account, on_delete=models.CASCADE)
	title = models.CharField(max_length=120,null=True)
	
	# store_name = models.CharField(max_length=120,null=True)
	website = models.CharField(max_length=100,null=True)
	condition = models.CharField(max_length=10,default="new")
	negotiable = models.CharField(max_length=10,null=True)
	from_price = models.IntegerField(default=0, null=True)
	to_price = models.IntegerField(default=0,null=True)
	instock = models.CharField(max_length=20,null=True,default=1)
	with_delivery = models.CharField(max_length=10,null=True)
	delivery_company = models.CharField(max_length=50,null=True)
	payment_type = models.CharField(max_length=50,null=True)
	exchange_item= models.TextField(null=True,blank=True)
	
	category = models.CharField(max_length=100,null=True)
	address = models.TextField(null=True)
	price = models.IntegerField(default=0,null=True)
	acquire_type = models.CharField(max_length=10, default="sale")
	duration = models.CharField(max_length=15, null=True,blank=True)
	dur_count= models.IntegerField(default=0, null=True)
	views = models.IntegerField(default=1, null=True)
	likes = models.IntegerField(default=1, null=True)
	images = models.ManyToManyField(Product_images)
	reviews = models.ManyToManyField(Reviews,blank=True)
	email = models.EmailField(null=True)
	phone_no= models.CharField(max_length=20, null=True)
	whatsapp_no= models.CharField(max_length=20, null=True)
	description = models.TextField(null=True,blank=True)
	requirement = models.TextField(null=True,blank=True)
	issue = models.TextField(null=True,blank=True)
	created = models.DateTimeField(auto_now_add=True)


	# def get_last_image(self):
	# 	return self.images.objects.order_by('-id')[0]




	def ___str__(self):
		return self.title



class Cart(models.Model):
	submit_user = models.ForeignKey(Account, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	rents = models.ManyToManyField(Rent,blank=True)
	

	def ___str__(self):
		return submit_user.user.username

	class Meta:
		ordering = ["-created"]



class Search(models.Model):
	text = models.CharField(max_length=80,null=True)
	

	def ___str__(self):
		return '{}'.format(self.text)

	# class Meta:
	# 	ordering = ["-text"]



# class Search_Lookup(models.Lookup):
# 	lookup_name = 'search'

# 	def as_sql(self, compiler, connection):
# 		lhs, lhs_params = self.process_lhs(compiler, connection)
# 		rhs, rhs_params = self.process_rhs(compiler, connection)

# 		params = lhs_params + rhs_params

# 		return 'MATCH (%s) AGAINST (%s IN BOOLEAN MODE)' % (lhs, rhs), params


# Field.register_lookup(Search_Lookup)


