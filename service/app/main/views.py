#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import main
from flask import jsonify, request
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
    resultString = """{"a": ["0x258d64d84f0e304a343275f9d79d0345122ed3a9e49dc5e53fdc71591dedf2e3", "0x18a7042ce16b9333f9ea0dbbc8d2eb86e979bae4c640b745b5711275278d5d2d"], "c_p": ["0x2c9cd79434cafe47ea65f05ebff620fc678e84ef306d2d6e5ca27b4a9fc23385", "0x13f243ec3c971897f25241a9302f370db94e80a80c37b287b7c0639e66278de4"], "c": ["0x8a08a97115f45279109836f763cd5d833b5137b4140cdc701b4c4edda67e0f0", "0x28a1c4ca9a2b8ce9635e7698b47c92e6113dfc92712fed21df96403c556e6ab2"], "b": [["0x23181438ef76423882a8c84b2795518d0368c56766d3eed688feeb9c4f10bfa8", "0x1a8a7bc34cbc33f4bc7a6bbb448122b3e4d116f1ac0404913ad2c0cc7b2fba45"], ["0x2b96d830592205da6d455f50f0b793bedf7e8db77aee5b40c1db9a5457a25f52", "0x29b9fed24d3e4139ef764af33be24cd6055d30df9ae7dc628ccb3fd94a65b232"]], "input": [2, 6], "a_p": ["0x1c23cbaa71fac17d17627110ab102cafb77a8ff982566cae4d3d34467d4985f8", "0x12e3dfbd6ebd5a512c519641bd5a043c39ca4e65d4d7d96edf4857f5333376fa"], "b_p": ["0x1354e1aa089ea5cb7a164bd685149232b24d38e4ab5d7ec3c67875935edc77b", "0x288a3c58003b240bcbe031051efd1b0c0ea60c2193c309951a97c1f1b8057c7f"], "h": ["0xaad30550b1b2d1422ca3e8d9fdb1e75b5eba61c7acbb7affe7807ce65431655", "0xca24425ac5a7a7bcd1374df1e7b71a515e2e903681631ba58c47be6541b8cce"], "k": ["0x3fe64d31f060499932335ed813bcffcef2a6ae5a60e5cdd763290e5629599d2", "0x2eb6af3da42b9732acd990e7ac68fc9bf67651d010a996c6223e7518d6c898ea"]}"""
    return jsonify(json.loads(resultString))
