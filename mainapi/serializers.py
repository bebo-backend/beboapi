from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token
from .models import Account, Rent,Product_images,Reviews,Cart
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist





class UserSerializer(ModelSerializer):

	class Meta:
		model=User
		fields=("username","password","email",)
		extra_kwargs = {"password":{"write_only":True}}

	def create(self, validated_data):
		user =User(
			email=validated_data["email"], 
			username=validated_data['username'])

		user.set_password(validated_data['password'])
		user.save()
		Token.objects.create(user=user)


		
		return user



# vote
class AccountSerializer(ModelSerializer):
	user = UserSerializer()
	class Meta:
		model=Account
		fields="__all__"

	def create(self, validated_data):

		

		user =User(
				email=validated_data["user"]["email"], 
				username=validated_data["user"]['username'])

		user.set_password(validated_data["user"]['password'])
		user.save()
		Token.objects.create(user=user)
		account = Account(user = user,
			
		phone_no=validated_data['phone_no'],
		agencyname = validated_data['agencyname'],
		website=validated_data['website']
			
				)
		account.save()

		saveCart= Cart(submit_user = account)
		saveCart.save()
		
		return account



# choice

class Product_imagesSerializer(ModelSerializer):
	class Meta:
		model = Product_images
		fields="__all__"




class RentMayLikeSerializer(ModelSerializer):
	# submit_user = AccountSerializer(many=False)
	images = Product_imagesSerializer(many=True)

	class Meta:
		model = Rent
		fields=['title','from_price','id',
		'to_price','price','images']

		

class RentListSerializer(ModelSerializer):
	submit_user = AccountSerializer(many=False)
	images = Product_imagesSerializer(many=True)

	class Meta:
		model = Rent
		fields=['title','from_price','id','submit_user',
		'to_price','price','acquire_type','images','created','address','category','views']


class RentCatSerializer(ModelSerializer):
	# submit_user = AccountSerializer(many=False)
	images = Product_imagesSerializer(many=True)

	class Meta:
		model = Rent
		fields=['images','category']

class ReviewsSerializer(ModelSerializer):
	account = AccountSerializer(many=False)

	class Meta:
		model = Reviews
		fields='__all__'



class RentSerializer(ModelSerializer):
	submit_user = AccountSerializer(many=False)
	images = Product_imagesSerializer(many=True)
	reviews = ReviewsSerializer(many=True)



	class Meta:
		model = Rent
		fields="__all__"


class RentStoreSerializer(ModelSerializer):
	submit_user = AccountSerializer(many=False)
	images = Product_imagesSerializer(many=True)

	class Meta:
		model = Rent
		fields=['images','submit_user']


class CartSerializer(ModelSerializer):
	submit_user = AccountSerializer(many=False)
	rents = RentSerializer(many=True)

	class Meta:
		model = Cart
		fields='__all__'

