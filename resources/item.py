import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel



class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type = float,
		required=True,
		help = "This field cant be blank:"
		)

	parser.add_argument('store_id',
		type = int,
		required=True,
		help = "Every item needs store_id:"
		)

	@jwt_required()
	def get(self,name):
		item = ItemModel.find_by_name(name)
		
		if item:
			return item.json()
		return {'message': 'Item not found'}, 404


	def post(self,name):
		
		if ItemModel.find_by_name(name):
			return {'message' : "An item with the name '{}' already exists.".format(name)}, 400

		data = Item.parser.parse_args()
		print("post_reso", data)

		# item = ItemModel(name, **data)
		item = ItemModel(name, data['price'], data['store_id'])
		
		try:
			item.save_to_db()
		except:
			return {"message": "An error occured inserting the item."}, 500

		return item.json(), 201	#http status code 201 for created

  
	def delete(self,name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()

		return {'message' : 'Item deleted'}

	def put(self,name):

		data = Item.parser.parse_args()
		print("put res data parser", data)
		
		item = ItemModel.find_by_name(name)
		print("put res item", item)

		
		if item is None:
			item = ItemModel(name,data['price'], data['store_id'])
		else:
			item.price = data['price']
		item.save_to_db()

		return item.json()
		


class ItemList(Resource):
	def get(self):

		return {'item': [item.json() for item in ItemModel.query.all()]}





