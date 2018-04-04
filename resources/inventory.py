"""inventory.py

Resource for calls to the Inventory portion of the ebay API.

Author: Brian Perrett
Date: 2018-03-30

"""
import requests

class Inventory():

    def __init__(self, parent, version='v1'):
        """Initialize Inventory object.

        Parameters
        ----------
        parent : Client
        version : str

        """
        self.parent = parent
        self.version = version

    def get_base(self):
        """Get url endpoint base.

        Returns
        -------
        str

        """
        return '{}sell/inventory/{}/'.format(self.parent.get_base(), self.version)

    def get_headers(self):
        return self.parent.get_headers()

    def get_inventory_item(self, sku):
        """Get eBay inventory item.

        Parameters
        ----------
        sku : str

        Returns
        -------
        Response

        """
        url = '{}{}'.format(self.get_base(), sku)
        r = requests.get(url, headers=self.get_headers())
        return r

    def get_inventory_items(self, limit=100, offset=None):
        """Get a page of inventory items

        Parameters
        ----------
        limit : int
            1 to 100
        offset : int
            Page number

        Returns
        -------
        Response

        """
        url = '{}inventory_item'.format(self.get_base())
        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        r = requests.get(url, params=params, headers=self.get_headers())
        return r

    def bulk_update_price_quantity(self, data):
        """Update multiple offerings for a single SKU.
        Yeah, it says bulk but it's not really bulk.  Tough luck.

        https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item/methods/bulkUpdatePriceQuantity

        Parameters
        ----------
        data : list

        Returns
        -------
        Response

        """
        url = '{}bulk_update_price_quantity'.format(self.get_base())
        payload = {'requests': data}
        r = requests.post(url, json=payload, headers=self.get_headers())
        return r

    def delete_inventory_item(self, sku):
        """Delete a SKU.

        Parameters
        ----------
        sku : str

        Returns
        -------
        Response

        """
        url = '{}inventory_item/{}'.format(self.get_base(), sku)
        r = requests.delete(url, headers=self.headers())
        return r
