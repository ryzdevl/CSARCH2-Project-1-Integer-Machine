from flask import Flask, render_template, request, jsonify
from integer_machine import (
    convert_decimal,
    booth_multiplier,
    non_restoring_division,
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/convert", methods=["POST"])
def api_convert():
    data = request.get_json(force=True)
    try:
        decimal = int(data.get("decimal"))
        bits = int(data.get("bits"))
    except (TypeError, ValueError):
        return jsonify({"error": "Decimal and bit size must be valid integers."}), 400

    if bits < 1:
        return jsonify({"error": "Bit size must be at least 1."}), 400

    result = convert_decimal(decimal, bits)
    return jsonify(result)


@app.route("/api/multiply", methods=["POST"])
def api_multiply():
    data = request.get_json(force=True)
    binary_input = bool(data.get("binary_input", False))
    bits = data.get("bits")
    try:
        bits = int(bits)
    except (TypeError, ValueError):
        return jsonify({"error": "Bit size must be a valid integer."}), 400
    if bits < 1:
        return jsonify({"error": "Bit size must be at least 1."}), 400

    multiplicand = data.get("multiplicand")
    multiplier = data.get("multiplier")
    if not binary_input:
        try:
            multiplicand = int(multiplicand)
            multiplier = int(multiplier)
        except (TypeError, ValueError):
            return jsonify({"error": "Operands must be valid decimal integers."}), 400

    result = booth_multiplier(multiplicand, multiplier, bits, binary_input)
    if result.get("error"):
        return jsonify({"error": result["error"]}), 400
    return jsonify(result)


@app.route("/api/divide", methods=["POST"])
def api_divide():
    data = request.get_json(force=True)
    binary_input = bool(data.get("binary_input", False))
    bits = data.get("bits")
    try:
        bits = int(bits)
    except (TypeError, ValueError):
        return jsonify({"error": "Bit size must be a valid integer."}), 400
    if bits < 1:
        return jsonify({"error": "Bit size must be at least 1."}), 400

    dividend = data.get("dividend")
    divisor = data.get("divisor")
    if not binary_input:
        try:
            dividend = int(dividend)
            divisor = int(divisor)
        except (TypeError, ValueError):
            return jsonify({"error": "Operands must be valid decimal integers."}), 400

    result = non_restoring_division(dividend, divisor, bits, binary_input)
    if result.get("error"):
        return jsonify({"error": result["error"]}), 400
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)