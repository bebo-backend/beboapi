from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token
from mainapi.models import Account, Rent,Product_images,Reviews,Search
from django.contrib.auth.models import User
from mainapi.serializers import AccountSerializer, Product_imagesSerializer





class RentListSerializer(ModelSerializer):
	submit_user = AccountSerializer(many=False)
	images = Product_imagesSerializer(many=True)

	class Meta:
		model = Rent
		fields=['title','from_price','id','submit_user',
		'to_price','price','acquire_type','images','created','category','instock','address','likes']


class RentReviewSerializer(ModelSerializer):
	submit_user = AccountSerializer(many=False)
	images = Product_imagesSerializer(many=True)

	class Meta:
		model = Rent
		fields=['title','from_price','id','submit_user',
		'to_price','price','acquire_type','images','created','category']



class ReviewsSerializer(ModelSerializer):
	account = AccountSerializer(many=False)

	class Meta:
		model = Reviews
		fields='__all__'

class RentReviewSerializer(ModelSerializer):
	# submit_user = AccountSerializer(many=False)
	# images = Product_imagesSerializer(many=True)
	reviews = ReviewsSerializer(many=True)

	class Meta:
		model = Rent
		fields=['reviews']


class RentSearchSerializer(ModelSerializer):
	# submit_user = AccountSerializer(many=False)
	# images = Product_imagesSerializer(many=True)
	# reviews = ReviewsSerializer(many=True)

	class Meta:
		model = Search
		fields='__all__'