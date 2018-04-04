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
