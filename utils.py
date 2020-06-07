def get_response(status, code, message):
    return jsonify({"{}".format(status): "{}".format(code), "message": "{}".format(message)}), code
