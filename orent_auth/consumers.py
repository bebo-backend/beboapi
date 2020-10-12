from channels.generic.websocket import WebsocketConsumer
import json
from mainapi.models import Rent,Account,Product_images
from django.core.files.uploadedfile import SimpleUploadedFile
from mainapi.serializers import RentSerializer
import copy


class productHubConsumer(WebsocketConsumer):
	def connect(self):
		self.accept()
		username = self.scope['url_route']['kwargs']['username']

		print("{} is connected".format(username))
		self.send(text_data = json.dumps({
			'connect':'ok'
			}))

		self.account = Account.objects.get(user__username=username)

		self.real_item =  Rent(submit_user=self.account)

		self.item = copy.copy(self.real_item)
		self.item.id = 1



	def disconnect(self,close_code):
		if not (self.item.title and self.item.category and (self.item.price or self.item.from_price) and self.item.email and self.item.address):
			pass

			print('connection disconnect')

	def receive(self,text_data="",bytes_data=None):
		data_json = json.loads(text_data)

		input_val = data_json['data']
		type_val = data_json['type']
		image_val = bytes_data
	

		# image_name  = self.item.title+cur_file
		
		print("receive type of {}".format(type_val))


		if type_val == 'verify_upload':

			data = RentSerializer(self.item).data
			self.send(text_data = json.dumps({'type':"verify_upload",
				'value':data}))




		elif type_val=='category':  self.item.category = input_val 
		elif type_val=='title':  self.item.title = input_val
		elif type_val=='website':  self.item.website = input_val
		elif type_val=='condition':  self.item.condition = input_val
		elif type_val=='negotiable':  self.item.negotiable = input_val
		elif type_val=='from_price':  self.item.from_price = input_val
		elif type_val=='to_price':  self.item.to_price = input_val
		elif type_val=='instock':  self.item.instock = input_val
		elif type_val=='delivery':  self.item.with_delivery = input_val
		elif type_val=='delivery_comp':  self.item.delivery_company = input_val
		elif type_val=='payment_type':  self.item.payment_type = input_val
		elif type_val=='location':  self.item.address = input_val
		elif type_val=='email':  self.item.email = input_val
		elif type_val=='tel':  self.item.phone_no = input_val
		elif type_val=='whatsapp_no':  self.item.whatsapp_no = input_val
		elif type_val=='acquire_type':  self.item.acquire_type = input_val
		elif type_val=='price':  self.item.price = input_val
		elif type_val=='duration':  self.item.duration = input_val
		elif type_val=='dur_count':  self.item.dur_count = input_val
		elif type_val=='description':  self.item.description = input_val
		elif type_val=='issue':  self.item.issue = input_val
		elif type_val=='requirement':  self.item.requirement = input_val
		elif type_val=='exchange_items':  self.item.exchange_item = input_val

		

		


		
		# eval(eval_code)

		# print(repr(self.item))

		if input_val == "" or input_val == " ":

			self.send(text_data = json.dumps({
				'status':0
				}))
		else:
			self.send(text_data = json.dumps({
				'status':1
				}))






