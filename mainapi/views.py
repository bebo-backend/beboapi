from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView,CreateAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Rent,Account, Product_images,Cart
from .serializers import AccountSerializer, RentSerializer, UserSerializer, Product_imagesSerializer,RentListSerializer,RentMayLikeSerializer,RentCatSerializer,RentStoreSerializer,CartSerializer
from django.contrib.auth import authenticate
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import MultiPartParser,FormParser,FileUploadParser, JSONParser
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
import json
from django.db.models import Count,Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage


# Create your views here.



class rents_list(ListCreateAPIView):
	queryset = Rent.objects.all()
	serializer_class = RentSerializer

class accounts_detail(RetrieveDestroyAPIView):
	queryset = Account.objects.all()
	serializer_class = AccountSerializer


class accounts_signup(CreateAPIView):
	authentication_classes=()
	permission_classes=()
	serializer_class = AccountSerializer

class login(APIView):
	permission_classes = ()

	def post(self,request):
		username = request.data.get('username')
		password = request.data.get('password')
		print('cred ',username,'+',password)

		user = authenticate(username=username, password=password)

		if user:
			getAcc = Account.objects.get(user__username=username)
			data = AccountSerializer(getAcc).data


			return Response({"token":user.auth_token.key,
				"username":username,"image":data['image']})

		else:
			print('error: username or passwrd not correct')
		
			return Response({"error":"Username or Password incorrect"})



class upload_property(APIView):
	parser_classes=(MultiPartParser,FormParser)
	
	def post(self,request):
		# print('xchunks',x.chunksg)

		username = request.data.get('username')
		

		# store_name = request.data.get('store_name').title()
		website = request.data.get('website')
		condition = request.data.get('condition','').title()
		negotiable = request.data.get('negotiable','').title()
		from_price = request.data.get('from_price',False)
		to_price = request.data.get('to_price',False)
		instock = request.data.get('instock','').title()
		delivery = request.data.get('delivery','').title()
		delivery_comp = request.data.get('delivery_comp','').title()
		payment_type = request.data.get('payment_type','').title()
		issue = request.data.get('issue','')
		acquire_type = request.data.get('acquire_type','')
		category = request.data.get('category','').title()
		description = request.data.get('description','')
		email = request.data.get('email')
		location = request.data.get('location','').title()
		price = request.data.get('price',0)
		requirement = request.data.get('requirement','')
		exchange_items = request.data.get('exchange_items','')
		title = request.data.get('title','').title()
		tel = request.data.get('tel')
		images = request.data.getlist('images')
		duration = request.data.get('duration',False)
		dur_count = request.data.get('dur_count',False)
		whatsapp_no = request.data.get('whatsapp_no')




		if username: 
			user = Account.objects.get(user__username=username)
			self.item  = Rent(submit_user=user)

		if category:  self.item.category = category.replace('&','and') 
		if title:  self.item.title = title
		if website:  self.item.website = website
		if condition:  self.item.condition = condition
		if negotiable:  self.item.negotiable = negotiable
		if from_price:  self.item.from_price = from_price
		if to_price:  self.item.to_price = to_price
		if instock:  self.item.instock = instock
		if delivery:  self.item.with_delivery = delivery
		if delivery_comp:  self.item.delivery_company = delivery_comp
		if payment_type:  self.item.payment_type = payment_type
		if location:  self.item.address = location
		if email:  self.item.email = email
		if tel:  self.item.phone_no = tel
		if whatsapp_no:  self.item.whatsapp_no = whatsapp_no
		if acquire_type:  self.item.acquire_type = acquire_type
		if price:  self.item.price = price
		if duration:  self.item.duration = duration
		if dur_count:  self.item.dur_count = dur_count
		if description:  self.item.description = description
		if issue:  self.item.issue = issue
		if requirement:  self.item.requirement = requirement
		if exchange_items:  self.item.exchange_item = exchange_items



		self.item.save()


		
		for x in images:
			print('xlist ',x)
			print('xchunks',x.chunks)
			img = SimpleUploadedFile(''+x.name, x.read())
			pro_image = Product_images(images=img)
			pro_image.save()

			self.item.images.add(pro_image)


		return Response({"data":"Upload successful"})


class get_profile(APIView):
	
	def get(self,request,username):
				
		try:
			getuser = Account.objects.get(user__username=username)
			print('user',getuser)

			data = AccountSerializer(getuser).data


			return Response(data)
			

		except ObjectDoesNotExist:
			# raise Http404("Account not found")

			return Response({"error":'account not found'})
			

class get_property(APIView):
	
	def get(self,request,username):

		page_number = request.query_params.get('page',1)
		limit = request.query_params.get('limit',25)
			
				
		try:
			# getuser = Account.objects.get(user__username=username)
			# print('user',getuser)
			
			rents = Rent.objects.filter(submit_user__user__username=username).order_by('-id')

	
			paginator = Paginator(rents,limit)
			
			page_obj = paginator.get_page(page_number)

			item_data = RentListSerializer(page_obj,many=True).data

			return Response({'res':item_data,'next':page_obj.has_next()})
			

		except ObjectDoesNotExist:
			# raise Http404("Account not found")

			return Response({"error":'account not found'})


class get_view_property(APIView):
	
	def get(self,request,id):
				
		try:
			
			rents = Rent.objects.get(id=id)
			print('rents',rents)
			
			data = RentSerializer(rents).data


			return Response(data)
			

		except ObjectDoesNotExist:
			# raise Http404("Account not found")

			return Response({"error":"Item not found"})




class get_all_items(APIView):
	
	def get(self,request):
				
		try:
			
			rents = Rent.objects.order_by('-id')
			# print('rents',rents)
			
			data = RentSerializer(rents,many=True).data


			return Response(data)
			

		except ObjectDoesNotExist:
			# raise Http404("Account not found")

			return Response({"error":"No Items found"})

			

class add_view(APIView):
	
	def get(self,request,id):
				
		try:
		
			
			rents = Rent.objects.get(id=id)
			rents.views+=1
			rents.save()

			print('rents',rents)
			
			data = RentSerializer(rents).data


			return Response({'view':rents.views})
			

		except ObjectDoesNotExist:

			# raise Http404("rent not found")

			return Response({"error":"not found"})

			

class add_like(APIView):
	
	def get(self,request,id):
				
		try:
		
			
			rents = Rent.objects.get(id=id)
			rents.likes+=1
			rents.save()

			print('rents',rents)
			
			data = RentSerializer(rents).data


			return Response({'like':rents.likes})
			

		except ObjectDoesNotExist:
			# raise Http404("rent not found")

			return Response({"error":"not found"})


class add_rate(APIView):
	
	def get(self,request,id,value,username):
				
		try:
		
			
			rents = Rent.objects.get(id=id)

			get_account = Account.objects.get(user=rents.submit_user.user)

			if get_account.rate_count:

					get_account.rate_count += 1
			else:
				get_account.rate_count = 1


			if rents.submit_user.rate < int(value):

				# rents.submit_user.rate=int(value)
				
				get_account.rate = int(value)
				

			get_account.save()
				# rents.save()

			# print('rents',rents)
			
			data = RentSerializer(rents).data


			return Response({'rate':rents.submit_user.rate_count})
			

		except ObjectDoesNotExist:
			# raise Http404("rent not found")

			return Response({"error":"not found"})
	

class you_may_like(APIView):
	
	def get(self,request,store,id):
				
		try:
			
			rents = Rent.objects.filter(submit_user__agencyname__icontains=store).order_by('-views')[0:30]
			
			data = RentMayLikeSerializer(rents,many=True).data


			return Response(data)
			

		except ObjectDoesNotExist:
			raise Http404("rent not found")

			return Response({"error":"not found"})

			

class update_profile(APIView):
	parser_classes=(MultiPartParser,FormParser)
	
	def post(self,request):
		
		try:
			username = request.data.get('username')
			
			user = Account.objects.get(user__username=username)

			images = request.data.get('image',False)
			email = request.data.get('email',"")
			
			tel = request.data.get('tel',"")
			website = request.data.get('website',"")
			
			agencyname = request.data.get('agency_name',"")
			
			if email:
				getuser = User.objects.get(username=username)

				getuser.email = email
				getuser.save()

			if tel:
				user.phone_no = tel

			if website:
				user.website = website

			if agencyname:
				user.agencyname = agencyname

			if images:
				img = SimpleUploadedFile(''+images.name, images.read())
				user.image = img


			user.save()


			

			

			return Response({"done":"success"})

		except ObjectDoesNotExist:

			return Response({'error':"Account not found"})



class update_item(APIView):

	
	def post(self,request):
		# print('xchunks',x.chunksg)
		try:
			item_id = request.data.get('item id')
			# user = Account.objects.get(user__username=username)

			instock = request.data.get('instock')
			email = request.data.get('email')
			
			tel = request.data.get('tel')
			
			title = request.data.get('title')

			getitem = Rent.objects.get(id=item_id)
			
			if email:
			
				getitem.email = email
				
			if tel:
				getitem.phone_no = tel

			if title:
				getitem.title = title

			if instock:
				getitem.instock = instock
				

			getitem.save()

			rents = Rent.objects.filter(submit_user=getitem.submit_user).order_by('-id')
			print('rents',rents)
			
			data = RentListSerializer(rents,many=True).data

			return Response(data)

		except ObjectDoesNotExist:

			return Response({'error':"Account not found"})




class get_top_company(APIView):
	
	def get(self,request):
				
		try:
			rents = Rent.objects.order_by(
				'-submit_user__user__username','-submit_user__rate_count').distinct('submit_user__user__username')[0:16]
			
		
			rent = RentSerializer(rents,many=True).data


			return Response(rent)
			

		except ObjectDoesNotExist:
			# raise Http404("Account not found")

			return Response({"error":'company not found'})



class get_category(APIView):
	
	def get(self,request):
				
		try:

			# distinct=Rent.objects.values('category').annotate(
			# 	category_count=Count('category')).filter(category_count__gte=1)

						
			rents = Rent.objects.order_by('category','-views').distinct('category')[0:10]

			rent = RentCatSerializer(rents,many=True).data

			# cat = CatSerializer(rents,many=True).data

		
			# print('distinct---- ',distinct)

			# data = filter(lambda x: x.category not in setcat,rent)
			return Response(rent)
			

		except ObjectDoesNotExist:
			raise Http404("category not found")

			return Response({"error":'category not found'})




class get_cart(APIView):
	
	def get(self,request,username):

		data = []
				
		
		try:

			getcart = Cart.objects.get(submit_user__user__username=username)			

			data = getcart.rents.all()
		
			# print('user',getuser)

			# data = CartSerializer(getcart,many=True).data
			data = RentSerializer(data,many=True).data

		except ObjectDoesNotExist:
			data=[]


		return Response(data)
		

		# except ObjectDoesNotExist:
		# 	# raise Http404("Account not found")

		# 	return Response({"error":'not found'})

class get_cart_len(APIView):
	
	def get(self,request,username):

		data = []
				
		
		try:

			getcart = Cart.objects.get(submit_user__user__username=username)			

			data = getcart.rents.all()
		
			# print('user',getuser)

			# data = CartSerializer(getcart,many=True).data
			data = RentCatSerializer(data,many=True).data

		except ObjectDoesNotExist:
			data=[]


		return Response({'len':len(data)})


class add_to_cart(APIView):
	
	def get(self,request,id,username):
				
	
		rents = Rent.objects.get(id=id)
		user = Account.objects.get(user__username=username)

		try:
			getCart = Cart.objects.get(submit_user=user)
			getCart.rents.add(rents)

			data = CartSerializer(getCart).data


			return Response(data)




		except ObjectDoesNotExist:
			saveCart= Cart(submit_user = user)
			saveCart.save()

			saveCart.rents.add(rents)
			

			# print('rents',rents)
			
			data = CartSerializer(saveCart).data


			return Response(data)
			






class remove_from_cart(APIView):
	
	def get(self,request,cart_user,item_id):
				
		try:
		
			
			rents = Rent.objects.get(id=item_id)			

			getCart = Cart.objects.get(submit_user__user__username = cart_user)

			getCart.rents.remove(rents)

			data = []

			if getCart:
				data = getCart.rents.all()
			else:
				data =[]

		
			data = RentSerializer(data,many=True).data


			return Response(data)
			

		except ObjectDoesNotExist:
			raise Http404("rent not found")

			return Response({"error":"not found"})



class remove_Item(APIView):
	
	def get(self,request,item_id):
				
		try:
		
			
			rents = Rent.objects.get(id=item_id)	
			rents.delete()		

			



			return Response({"done":"success"})
			

		except ObjectDoesNotExist:
			
			return Response({"error":"not found"})



class cart_recommend(APIView):

	
	def post(self,request):
		# print('xchunks',x.chunksg)
		try:
			category = request.data.get('category',[])
			# address =  request.data.get('address','lagos')
			exclude = request.data.get('excludeData',[])
		
			rents = Rent.objects.filter(category__in=category).exclude(id__in=exclude).order_by('-id')
			# print('cart_recommend',category)
			
			data = RentListSerializer(rents,many=True).data

			return Response(data)

		except ObjectDoesNotExist:

			return Response({'error':"Account not found"})


