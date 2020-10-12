

from rest_framework import status
from rest_framework.views import APIView
# from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView,CreateAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from mainapi.models import Rent,Account, Product_images,Reviews,Search
from .serializers import RentListSerializer,ReviewsSerializer,RentReviewSerializer,RentSearchSerializer
from mainapi.serializers import RentSerializer,AccountSerializer
from django.contrib.auth import authenticate
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from .categoryOptions import getChildren
# from rest_framework.parsers import MultiPartParser,FormParser,FileUploadParser, JSONParser
# from django.core.files.base import ContentFile
# from django.core.files.uploadedfile import SimpleUploadedFile
# import json

# Create your views here.



def get_search(data):
	# save_search = Search(text=data)
	# save_search.save()

	# data = data.split()

	# result = Rent.objects.filter(Q(title__search=data)|Q(category__search=data)|
	# 	Q(address__search=data)| Q(website__search=data)|
	# 	Q(email__search=data)|Q(phone_no__search=data)|
	# 	Q(description__search=data)|Q(requirement__search=data)|
	# 	Q(submit_user__agencyname__search=data)).distinct()


	# result = Rent.objects.annotate(search=SearchVector('title', 'address','category','website','email','phone_no','description','requirement','submit_user__agencyname')).filter(search=data)

	# result = Rent.objects.annotate(search=SearchVector('title')).filter(search=SearchQuery(data))




	vector = SearchVector('title', weight='A') + SearchVector('address',weight='B') + SearchVector('category',weight='B')+SearchVector('website',weight='D') + SearchVector('email',weight='C')+SearchVector('description',weight='D')+SearchVector('acquire_type',weight='B')+SearchVector('submit_user__agencyname',weight='B')
	
	query = SearchQuery(data,search_type="phrase")

	result = Rent.objects.annotate(rank=SearchRank(vector, query)).filter(Q(title__icontains=data)|Q(
		category__icontains=data)|Q(
		address__icontains=data)|Q(email__icontains=data)|Q(website__icontains=data)|Q(
		description__icontains=data)|Q(submit_user__agencyname__icontains=data)|Q(acquire_type__icontains=data)).order_by('rank','-id')

	return result


# def get_suggest_search(data):
# 	try:

# 		get_src = Search.objects.get(text=data)

# 	except ObjectDoesNotExist:
# 		save_search = Search(text=data)
# 		save_search.save()
	

# 	result = Search.objects.filter(text__istartswith=data)



# 	return result



def updateSearch(type,value,rents):

	try:
		if type =='search':
			return get_search(value)
			# print('search_data',rents)

		if type== "acquisition":
			return rents.filter(acquire_type__icontains=value)
		if type=="condition":

			return rents.filter(
				Q(condition__icontains=value)).order_by('-id')
		if type=="category":
			cat = request.query_params.get('category','')

			return rents.filter(
					Q(category__icontains=str(cat).split(" ")[0])).order_by('-id','-views')

		if type=='shop':
			return rents.filter(
				Q(submit_user__agencyname__icontains=value)
				).order_by('submit_user__rate')
		
		if type=='delivery':
			return rents.filter(
				Q(with_delivery__icontains=value)).order_by('-id')

		if type=="duration":
			return rents.filter(Q(acquire_type__icontains='rent'),
				Q(duration__icontains=value)).order_by('-id')

		if type=="location":
			return rents.filter(Q(address__icontains=value)|Q(description__icontains=value)
			).order_by('address','-id')

		if type=="price":
			if value=="any price":
				return rents.order_by('-id')

			elif value=="under 1000":
				return rents.filter(
				Q(price__lt=1000)|Q(to_price__lt=1000)|Q(from_price__lt=1000)).order_by('price','from_price','to_price')



			elif value=="1000 to 10000":

				rents=rents.exclude(
					Q(price__gt=10000)|
				Q(from_price__gt=10000)|
				Q(to_price__gt=10000)
				)

				return rents.filter(
				Q(price__gt=1000)|Q(to_price__gt=1000)|Q(from_price__gt=1000))

			elif value=="10000 to 50000":
				rents=rents.exclude(
					Q(price__gt=50000)|
				Q(from_price__gt=50000)|
				Q(to_price__gt=50000)
				)

				return rents.filter(
				Q(price__gt=10000)|Q(to_price__gt=10000)|Q(from_price__gt=10000))

			elif value=="over 50000":
				return rents.filter(
				Q(price__gt=50000)|Q(to_price__gt=50000)|Q(from_price__gt=50000))


		if type=='configprice':
			if not '-' in value:
				value = "0-100000"
			value=value.split('-')

			rents = rents.exclude(Q(price__gt=value[1])|
				Q(from_price__gt=value[1])|Q(to_price__gt=value[1]))

			return rents.filter(
			Q(price__gt=value[0])|Q(to_price__gt=value[0])|Q(from_price__gt=value[0]))

	except AttributeError:
		return []



class search_data(APIView):

	def get(self,request):

		rents=[]
		# search = request.query_params.get('search','')


		page_number = request.query_params.get('page',1)
		limit = request.query_params.get('limit',15)
		search = request.query_params.get('search','')
		tag = request.query_params.get('tags',False)
		# categoryChildren = getChildren(search.lower())
		print('searc value ',search,' ---tag',tag)

		if search == 'all' and not tag:
			rents=Rent.objects.order_by('-id')
		elif tag:
			categoryChildren = getChildren(search.lower())
			rents = Rent.objects.filter(
							Q(category__in=categoryChildren)).order_by('-id','-views')



		else:
			rents= get_search(search)

		for x in request.query_params.keys():
			value = request.query_params[x]
			type=x

			try:
				if type== "acquisition":
					rents = rents.filter(acquire_type__icontains=value)
				if type=="condition":

					rents = rents.filter(
					Q(condition__icontains=value))

				if type=="category":
					cat = request.query_params.get('category','')
					# print('category ---',cat)

					rents = Rent.objects.filter(
							Q(category__icontains=str(cat).replace('&','and'))).order_by('-id','-views')

				if type=='shop':
					rents= rents.filter(
						Q(submit_user__agencyname__icontains=value)
						).order_by('submit_user__rate')
				
				if type=='delivery':
					rents= rents.filter(
						Q(with_delivery__icontains=value)).order_by('-id')

				if type=="duration":
					rents= rents.filter(Q(acquire_type__icontains='rent'),
						Q(duration__icontains=value)).order_by('-id')

				if type=="location":
					rents= rents.filter(Q(address__icontains=value)|Q(description__icontains=value)
					).order_by('address','-id')

				if type=="price":
					if value=="any price":
						return rents.order_by('-id')

					elif value=="under 1000":
						rents= rents.filter(
						Q(price__lt=1000)|Q(to_price__lt=1000)|Q(from_price__lt=1000)).order_by('price','from_price','to_price')



					elif value=="1000 to 10000":

						rents=rents.exclude(
							Q(price__gt=10000)|
						Q(from_price__gt=10000)|
						Q(to_price__gt=10000)
						)

						rents= rents.filter(
						Q(price__gt=1000)|Q(to_price__gt=1000)|Q(from_price__gt=1000))

					elif value=="10000 to 50000":
						rents=rents.exclude(
							Q(price__gt=50000)|
						Q(from_price__gt=50000)|
						Q(to_price__gt=50000)
						)

						rents=rents.filter(
						Q(price__gt=10000)|Q(to_price__gt=10000)|Q(from_price__gt=10000))

					elif value=="over 50000":
						rents= rents.filter(
						Q(price__gt=50000)|Q(to_price__gt=50000)|Q(from_price__gt=50000))


				if type=='configprice':
					if not '-' in value:
						value = "0-100000"
					value=value.split('-')

					rents = rents.exclude(Q(price__gt=value[1])|
						Q(from_price__gt=value[1])|Q(to_price__gt=value[1]))

					rents= rents.filter(
					Q(price__gt=value[0])|Q(to_price__gt=value[0])|Q(from_price__gt=value[0]))

				if type=='sort':

					if value =='na':
						rents = rents.order_by('-id')
						
					elif value =='pl2h':
						rents = rents.order_by('price','from_price')
					elif value =='ph2l':
						rents = rents.order_by('-price','-from_price')
					elif value =='sr':
						rents = rents.order_by('-submit_user__rate_count')
					elif value =='pl2h':
						rents = rents.order_by('-submit_user__rate')
					elif value =='il':
						rents = rents.order_by('-views')

			except AttributeError:
				return []

			# print(x,'---------',)
			


		paginator = Paginator(rents,limit)
		
		page_obj = paginator.get_page(page_number)

		item_data = RentListSerializer(page_obj,many=True).data

		return Response({'res':item_data,'next':page_obj.has_next()})







class main_search(APIView):

	def get(self,request):
				
		try:
		
			rentsnotloc = Rent.objects.order_by('-id')[0:30]

			rent = RentListSerializer(rentsnotloc,many=True).data
	
			return Response(rent)
			

		except ObjectDoesNotExist:
			
			return Response({"error":'search not found'})


class add_review(APIView):	
	def post(self,request,id,username):
		text_data = request.data.get('text')
				
		try:
			get_user = Account.objects.get(user__username=username)
					
			rents = Rent.objects.get(id=id)

			review = Reviews(text=text_data,account = get_user)
			review.save()

			rents.reviews.add(review)

			print('rents',rents.reviews)
			
			data = RentReviewSerializer(rents).data


			return Response(data)
			

		except ObjectDoesNotExist:
			raise Http404("rent not found")

			return Response({"error":"not found"})
	
class get_reviews(APIView):	
	def get(self,request,id):
		
				
		try:
		
					
			rents = Rent.objects.get(id=id)

			data = RentReviewSerializer(rents).data


			return Response(data)
			

		except ObjectDoesNotExist:


			return Response({"error":"not found"})
	


class get_suggestion(APIView):
	
	def post(self,request):

		search = request.data.get("search")
		category = request.data.get("category","all")
				
		try:

			rents = get_suggest_search(search)

			

			if category != 'all':
				rents = rents.filter(category__icontains=category)

			rent = RentSearchSerializer(rents.order_by('-id').distinct()[0:20],many=True).data

		
			return Response(rent)
			

		except ObjectDoesNotExist:
			raise Http404("category not found")

			return Response({"error":'category not found'})



class search_view(APIView):
	
	def post(self,request):

		
		category = request.data.get("category")
		location =request.data.get('location','lagos')
		# value =request.data.get('value')
		# data_type = request.data.get('type')
		search = request.data.get('search')

				
		try:

			rents = get_search(search).filter(address__icontains=location)

			
			if category != 'all':
				rents = rents.filter(category__icontains=category)

			rent = RentListSerializer(rents.order_by('title','-id').distinct(),many=True).data

			return Response(rent)
			

		except ObjectDoesNotExist:
			raise Http404("category not found")

			return Response({"error":'category not found'})




class tag(APIView):

	def post(self,request):

		# location =request.data.get('location','lagos')
		value =request.data.get('value')
		# data_type = request.data.get('type')
		search = request.data.get('search')
		# category = request.data.get("category","all")

		rents=[]

		if search:
			rents = get_search(value).filter(
					Q(category__icontains=value)).order_by('-id','-views').distinct()
		else:

			if value=="All":
				rents = Rent.objects.order_by('-id','-views').distinct()	
			else:

				rents = Rent.objects.filter(
					Q(category__icontains=value)).order_by('-id','-views').distinct()		


		rent = RentListSerializer(rents,many=True).data

		return Response(rent)


class acquisition(APIView):

	def post(self,request):

		# location =request.data.get('location','lagos')
		value =request.data.get('value')
		# data_type = request.data.get('type')
		search = request.data.get('search')
		# category = request.data.get("category","all")

		rents=[]

		if search:
			rents = get_search(value).filter(
					Q(acquire_type__icontains=value)).order_by('-id','-views').distinct()
		else:
			rents = Rent.objects.filter(acquire_type__icontains=value).order_by('-id').distinct()

		rent = RentListSerializer(rents,many=True).data

		return Response(rent)

class condition(APIView):

	def post(self,request):

		# location =request.data.get('location','lagos')
		value =request.data.get('value')
		# data_type = request.data.get('type')
		search = request.data.get('search')
		# category = request.data.get("category","all")

		rents=[]

		if search:
			rents = get_search(value).filter(
					Q(condition__icontains=value)).order_by('condition','-id').distinct()
		else:
			if value=="both":
				rents = Rent.objects.order_by('condition','-views').distinct()	
			else:

				rents = Rent.objects.filter(
					Q(condition__icontains=value)).order_by('-id').distinct()	

		rent = RentListSerializer(rents,many=True).data

		return Response(rent)


class store(APIView):

	def post(self,request):

		# location =request.data.get('location','lagos')
		value =request.data.get('value')
		# data_type = request.data.get('type')
		search = request.data.get('search')
		# category = request.data.get("category","all")

		rents=[]

		if search:
			rents = get_search(value).filter(
					Q(submit_user__agencyname__icontains=value)
					).order_by('submit_user__rate','-id').distinct()
		else:
			rents = Rent.objects.filter(
					Q(submit_user__agencyname__icontains=value)
					).order_by('submit_user__rate','-id').distinct()


		rent = RentListSerializer(rents,many=True).data

		return Response(rent)



class delivery(APIView):

	def post(self,request):

		# location =request.data.get('location','lagos')
		value =request.data.get('value')
		# data_type = request.data.get('type')
		search = request.data.get('search')
		# category = request.data.get("category","all")

		rents=[]

		if search:
			rents = get_search(value).filter(
					Q(with_delivery__icontains=value)).order_by('-id').distinct()
		else:
			if value=="both":
				rents = Rent.objects.order_by('with_delivery','-views').distinct()	
			else:

				rents = Rent.objects.filter(
					Q(with_delivery__icontains=value)).order_by('-id').distinct()	

		rent = RentListSerializer(rents,many=True).data

		return Response(rent)


class duration(APIView):

	def post(self,request):

		# location =request.data.get('location','lagos')
		value =request.data.get('value')
		# data_type = request.data.get('type')
		search = request.data.get('search')
		# category = request.data.get("category","all")

		rents=[]

		if search:
			rents = get_search(value).filter(Q(acquire_type__icontains='rent'),
					Q(duration__icontains=value)).order_by('-id').distinct()
		else:
			if value=="none":
				rents = Rent.objects.filter(Q(acquire_type__icontains='rent')).order_by('-views').distinct()	
			else:

				rents = Rent.objects.filter(Q(acquire_type__icontains='rent'),
					Q(duration__icontains=value)).order_by('-id').distinct()	

		rent = RentListSerializer(rents,many=True).data

		return Response(rent)

class location(APIView):

	def post(self,request):

		# location =request.data.get('location','lagos')
		value =request.data.get('value')
		# data_type = request.data.get('type')
		search = request.data.get('search')
		# category = request.data.get("category","all")

		rents=[]

		if search:
			rents = get_search(value).filter(Q(address__icontains=value)|Q(description__icontains=value)
				).order_by('address','-id').distinct()
		else:
			rents = Rent.objects.filter(Q(address__icontains=value)|Q(description__icontains=value)
				).order_by('address','-id').distinct()

		rent = RentListSerializer(rents,many=True).data

		return Response(rent)


class configprice(APIView):

	def post(self,request):

		# location =request.data.get('location','lagos')
		value =request.data.get('value',[0,10000])
		# data_type = request.data.get('type')
		search = request.data.get('search')
		# category = request.data.get("category","all")

		rents=[]

		if search:
			rents = get_search(value).exclude(
				Q(price__gt=value[1])|
			Q(from_price__gt=value[1])|
			Q(to_price__gt=value[1])
			)

			rents=rents.filter(
			Q(price__gt=value[0])|Q(to_price__gt=value[0])|Q(from_price__gt=value[0]))

		else:
			rent = Rent.objects.all().exclude(
				Q(price__gt=value[1])|
			Q(from_price__gt=value[1])|
			Q(to_price__gt=value[1])
			)

			rents=rent.filter(
			Q(price__gt=value[0])|Q(to_price__gt=value[0])|Q(from_price__gt=value[0]))


		rent = RentListSerializer(rents.order_by('-price','-from_price'),many=True).data

		return Response(rent)


class price(APIView):

	def post(self,request):

		# location =request.data.get('location','lagos')
		value =request.data.get('value')
		# data_type = request.data.get('type')
		search = request.data.get('search')
		# category = request.data.get("category","all")

		rents=[]

		if search:
			rents = get_search(value)

		else:
			rents = Rent.objects.all()

		if value=="any price":
			rents = rents.order_by('-price','-from_price')

		elif value=="under 1000":
			rents = rents.filter(
			Q(price__lt=1000)|Q(to_price__lt=1000)|Q(from_price__lt=1000)).order_by('price','from_price')



		elif value=="1000 to 10000":

			rents=rents.exclude(
				Q(price__gt=10000)|
			Q(from_price__gt=10000)|
			Q(to_price__gt=10000)
			)

			rents=rents.filter(
			Q(price__gt=1000)|Q(to_price__gt=1000)|Q(from_price__gt=1000)).order_by('price','from_price')

		elif value=="10000 to 50000":
			rents=rents.exclude(
				Q(price__gt=50000)|
			Q(from_price__gt=50000)|
			Q(to_price__gt=50000)
			)

			rents=rents.filter(
			Q(price__gt=10000)|Q(to_price__gt=10000)|Q(from_price__gt=10000)).order_by('price','from_price')

		elif value=="over 50000":
			rents = rents.filter(
			Q(price__gt=50000)|Q(to_price__gt=50000)|Q(from_price__gt=50000)).order_by('price','from_price')





		rent = RentListSerializer(rents,many=True).data

		return Response(rent)


class popular_shop(APIView):
	
	def get(self,request):
		page_number = request.query_params.get('page',1)
		limit = request.query_params.get('limit',25)
				
		try:
			rents = Rent.objects.order_by(
				'-submit_user__user__username','-submit_user__rate_count').distinct('submit_user__user__username')[0:30]
			
		
			paginator = Paginator(rents,limit)
			
			page_obj = paginator.get_page(page_number)

			item_data = RentListSerializer(page_obj,many=True).data

			return Response({'res':item_data,'next':page_obj.has_next()})



			

		except ObjectDoesNotExist:
			# raise Http404("Account not found")

			return Response({"error":'company not found'})

