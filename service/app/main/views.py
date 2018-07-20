#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import main
from flask import jsonify, request
from zokrates_wrapper import ComputeWitnessAndGetProof
import json

@main.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@main.route('/api/execute_auction', methods=['GET', 'POST'])
def execute_auction():
    amount1 = request.args.get('amount1')
    salt1 = request.args.get('salt1')
    amount2 = request.args.get('amount2')
    salt2 = request.args.get('salt2')
    response = handle_auction(amount1, salt1, amount2, salt2)
    if response is None:
        return jsonify(output=u'error while execution')
    return response

def handle_auction(amount1, salt1, amount2, salt2):
    resultString = ComputeWitnessAndGetProof(amount1, salt1, amount2, salt2)
    return jsonify(json.loads(resultString))
