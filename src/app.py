import os
from flask import Flask, request
from shipstation.api import ShipStation, ShipStationOrder, ShipStationAddress, ShipStationItem, ShipStationWeight

no_weight = ShipStationWeight(units='ounces',value=0)
app = Flask(__name__)
ss = ShipStation(key=os.getenv('SHIPSTATION_API_KEY'), secret=os.getenv('SHIPSTATION_API_SECRET'))
shirts = {
    'S':  ShipStationItem(sku=os.getenv('SHIRT_S_SKU', '605925771853'),quantity=1),
    'M':  ShipStationItem(sku=os.getenv('SHIRT_M_SKU', '605925771860'),quantity=1),
    'L':  ShipStationItem(sku=os.getenv('SHIRT_L_SKU', '605925771877'),quantity=1),
    'XL': ShipStationItem(sku=os.getenv('SHIRT_XL_SKU', '605925771884'),quantity=1)
}


@app.route('/send', methods=['POST'])
def tshirt_cannon():
    body = request.json
    print(body)
    ss_order = ShipStationOrder(order_number=f'tshirt-cannon-{str(body["Entry"]["Number"])}')
    shipping_address = ShipStationAddress(
        name=body['YourName2']['FirstAndLast'],
        street1=body['Address']['Line1'],
        street2=body['Address']['Line2'],
        street3=body['Address']['Line3'],
        city=body['Address']['City'],
        state=body['Address']['State'],
        postal_code=body['Address']['PostalCode'],
        country=body['Address']['Country']
    )
    ss_order.set_billing_address(shipping_address)
    ss_order.set_shipping_address(shipping_address)
    shirts[body['TShirtSize']].set_weight(no_weight)
    ss_order.add_item(shirts[body['TShirtSize']])
    ss.add_order(ss_order)
    ss.submit_orders()
    return 'k bro'
