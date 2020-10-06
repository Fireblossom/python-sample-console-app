from flask import Flask, request
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

import pdf
import sender

app = Flask(__name__)

executor = ThreadPoolExecutor(2)


@app.route('/webhooks/tk', methods=["POST"])
def receive():
    data = request.values.to_dict()
    sign = request.files['Sign']
    in_memory_file = BytesIO()
    sign.save(in_memory_file)
    in_memory_file.seek(0)
    signimg = Image.open(in_memory_file)
    executor.submit(fill_and_send_tk, data, signimg)
    return 'Hello, World!'


def fill_and_send_tk(data, signimg):
    pdf.fill_tk(data, signimg)
    sender.sender_service(data["Email"] + "/tk_filled.pdf")


@app.route('/webhooks/tksepa', methods=["POST"])
def receive():
    data = request.values.to_dict()
    sign = request.files['Sign']
    in_memory_file = BytesIO()
    sign.save(in_memory_file)
    in_memory_file.seek(0)
    signimg = Image.open(in_memory_file)
    executor.submit(fill_and_send_tk_sepa, data, signimg)
    return 'Hello, World!'


def fill_and_send_tk_sepa(data, signimg):
    pdf.fill_tk_sepa(data, signimg)
    sender.sender_service(data["Email"] + "/tk_filled.pdf")


@app.route('/webhooks/dak', methods=["POST"])
def receive():
    data = request.values.to_dict()
    executor.submit(fill_and_send_dak, data)
    return 'Hello, World!'


def fill_and_send_dak(data):
    pdf.fill_dak(data)
    sender.sender_service(data["Email"] + "/tk_filled.pdf")


@app.route('/webhooks/dak_sepa', methods=["POST"])
def receive():
    data = request.values.to_dict()
    sign = request.files['Sign']
    in_memory_file = BytesIO()
    sign.save(in_memory_file)
    in_memory_file.seek(0)
    signimg = Image.open(in_memory_file)
    executor.submit(fill_and_send_dak_sepa, data, signimg)
    return 'Hello, World!'


def fill_and_send_dak_sepa(data, signimg):
    pdf.fill_dak_sepa(data, signimg)
    sender.sender_service(data["Email"] + "/tk_filled.pdf")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=666)
