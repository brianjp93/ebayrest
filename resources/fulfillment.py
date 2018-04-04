"""fulfillment.py

Resource for calls to the Inventory portion of the ebay API.

Author: Brian Perrett
Date: 2018-03-30

"""
import requests

class Fulfillment():

	def __init__(self, parent, version='v1'):
		"""Initialize Fulfillment object.

		Parameters
		----------
		parent : Client
		version : str

		"""
		self.parent = parent
		self.version = version

	def get_headers(self):
		"""Get headers for requests.
		"""
		return self.parent.get_headers()

	def get_base(self):
		"""Get base URL for the fulfillment endpoint.
		"""
		return '{}sell/fulfillment/{}/'.format(self.parent.get_base(), self.version)

	def get_order(self, order_id):
		"""Get specific order by order id.

		Parameters
		----------
		order_id : str
			The unique identifier of the order. This value was returned
			by the getOrders call in the orders.orderId field
			for example, 170009092860-9849164007!140000000544476

		Returns
		-------
		Response

		"""
		url = '{}order/{}'.format(self.get_base(), order_id)
		r = requests.get(url, headers=self.get_headers())
		return r

	def get_orders(self, offset=None, limit=200, order_ids=[],
				   creation_date_start=None, creation_date_end=None,
				   last_modified_date_start=None, last_modified_date_end=None,
				   order_fulfillment_status=[]):
		"""Get a page of orders.

		Parameters
		----------
		offset : int
			index offset - not page offset
		limit : int
			1 - 1000
		order_ids : list[str]
			A list of order ids to fetch.  All other parameters will be ignored
			if order_ids is provided.
		creation_date_start : str
			ISO Datetime
		creation_date_end : str
			ISO Datetime
		last_modified_date_start : str
			ISO Datetime
		last_modified_date_end : str
			ISO datetime
		order_fulfillment_status : list[str]
			{NOT_STARTED, IN_PROGRESS, FULFILLED}

		Returns
		-------
		Response

		"""
		url = '{}order'.format(self.get_base())
		params = {'limit': limit}
		if offset is not None:
			params['offset'] = offset
		if order_ids:
			params['orderIds'] = ','.join(order_ids)
		# order filters
		order_filter = []
		if creation_date_start:
			creation = '{}..'.format(creation_date_start)
			if creation_date_end:
				creation += creation_date_end
			order_filter.append('creationdate:[{}]'.format(creation))
		if last_modified_date_start:
			modified = '{}..'.format(last_modified_date_start)
			if last_modified_date_end:
				modified += last_modified_date_end
			order_filter.append('lastmodifieddate:[{}]'.format(modified))
		if order_fulfillment_status:
			order_filter.append('orderfulfillmentstatus:{{{}}}'.format('|'.join(order_fulfillment_status)))
		# add filter to params if there are any filters.
		if order_filter:
			params['filter'] = ','.join(order_filter)
		r = requests.get(url, headers=self.get_headers(), params=params)
		return r

	def get_shipping_fulfillments(self, order_id):
		"""Get shipping fulfillments for an order.

		Parameters
		----------
		order_id : str

		Returns
		-------
		Response

		"""
		url = '{}order/{}/shipping_fulfillment'.format(self.get_base(), order_id)
		r = requests.get(url, headers=self.get_headers())
		return r