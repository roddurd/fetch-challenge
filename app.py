from flask import Flask, jsonify, request
from math import ceil
import uuid

app = Flask(__name__)

processed_receipts = {}

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt_data = request.get_json()

    # calculate points earned

    # One point for every alphanumeric character in the retailer name
    retailer = receipt_data['retailer']
    points = sum(c.isalnum() for c in retailer)

    # 50 points if the total is a round dollar amount with no cents.
    total = receipt_data['total']
    if float(total) == round(float(total)):
        points += 50

    # 25 points if the total is a multiple of 0.25.
    if float(total) % 0.25 == 0:
        points += 25

    # 5 points for every two items on the receipt.
    points += 5 * (len(receipt_data['items']) // 2)

    # If the trimmed length of the item description is a multiple of 3, 
    # multiply the price by 0.2 and round up to the nearest integer.
    # The result is the number of points earned.
    for item in receipt_data['items']:
        if len(item['shortDescription'].strip()) % 3 == 0:
            points += ceil(float(item['price']) * 0.2)

    # 6 points if the day in the purchase date is odd.
    if int(receipt_data['purchaseDate'].split('-')[2]) % 2 == 1:
        points += 6

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    hour = int(receipt_data['purchaseTime'].split(':')[0])
    # Since I'm not sure about endpoints, I'm including 2:00pm but excluding
    # 4:00pm, as a stated time of 14:00 could technically be 'after' 14:00:00.0,
    # but 16:00 is not before 16:00:00.0.
    if 14 <= hour < 16:
        points += 10

    receipt_id = str(uuid.uuid4())

    # store receipt details and points in memory
    processed_receipts[receipt_id] = {'receipt_data': receipt_data, 'points': points}

    return jsonify({'id': receipt_id})

@app.route('/receipts/<string:id>/points', methods=['GET'])
def get_points(id):
    if id in processed_receipts:
        points = processed_receipts[id]['points']
        return jsonify({'points': points})
    else:
        return 'Invalid receipt ID', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
