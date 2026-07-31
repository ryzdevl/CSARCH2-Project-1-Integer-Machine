"""
Machine 1: Integer Machine
===========================
Process: Integer arithmetic and conversion.

1. Decimal <-> Unsigned/Signed Binary conversion (with bounds checking)
2. Multiplication  -> Booth's Algorithm (sequential circuit binary multiplier)
   Division        -> Non-Restoring Division
   Both support decimal or binary input, and print a full step-by-step trace.
"""

def to_unsigned_binary(decimal, bits):
    """
    Convert a decimal integer to an unsigned binary string of the given width.
    Returns (binary_string, error_message). If out of range, binary_string is None.
    """
    if bits < 1:
        return None, f"Error: bit size must be at least 1 (got {bits})."

    min_val = 0
    max_val = (2 ** bits) - 1

    if decimal < min_val or decimal > max_val:
        return None, (f"Error: {decimal} is out of range for UNSIGNED {bits}-bit "
                       f"representation. Valid range is [{min_val}, {max_val}].")

    return format(decimal, f'0{bits}b'), None


def to_signed_binary(decimal, bits):
    """
    Convert a decimal integer to a signed (two's complement) binary string
    of the given width. Returns (binary_string, error_message).
    """
    if bits < 1:
        return None, f"Error: bit size must be at least 1 (got {bits})."

    min_val = -(2 ** (bits - 1))
    max_val = (2 ** (bits - 1)) - 1

    if decimal < min_val or decimal > max_val:
        return None, (f"Error: {decimal} is out of range for SIGNED {bits}-bit "
                       f"representation. Valid range is [{min_val}, {max_val}].")

    if decimal < 0:
        decimal = (1 << bits) + decimal  # encoding for the two's complement

    return format(decimal, f'0{bits}b'), None


def binary_to_decimal(binary_str, signed=False):
    """Convert a binary string to its decimal value (unsigned or two's-complement signed)."""
    bits = len(binary_str)
    value = int(binary_str, 2)
    if signed and value >= (1 << (bits - 1)):
        value -= (1 << bits)
    return value


def convert_decimal(decimal, bits):
    """Convenience wrapper: produce both unsigned and signed binary + errors."""
    unsigned_bin, unsigned_err = to_unsigned_binary(decimal, bits)
    signed_bin, signed_err = to_signed_binary(decimal, bits)
    return {
        "decimal": decimal,
        "bits": bits,
        "unsigned_binary": unsigned_bin,
        "unsigned_error": unsigned_err,
        "signed_binary": signed_bin,
        "signed_error": signed_err,
    }

def _normalize_operand(value, bits, is_binary_input):
    """
    Accepts either a decimal int/str or a binary string, returns the decimal
    (signed, two's-complement-interpreted) integer value, plus an error if
    it doesn't fit in `bits`.
    """
    if is_binary_input:
        value = str(value).strip()
        if len(value) != bits or any(c not in "01" for c in value):
            return None, (f"Error: binary input '{value}' must be exactly {bits} "
                           f"bits long and contain only 0s and 1s.")
        decimal_value = binary_to_decimal(value, signed=True)
        return decimal_value, None
    else:
        decimal_value = int(value)
        min_val = -(2 ** (bits - 1))
        max_val = (2 ** (bits - 1)) - 1
        if decimal_value < min_val or decimal_value > max_val:
            return None, (f"Error: {decimal_value} does not fit in signed {bits}-bit "
                           f"range [{min_val}, {max_val}].")
        return decimal_value, None


def _sign_bit(value, bits):
    return (value >> (bits - 1)) & 1

def booth_multiplier(multiplicand, multiplier, bits, binary_input=False):
    """
    Multiplies `multiplicand` x `multiplier` using Booth's Algorithm.
    Registers A, M, Q are all `bits` wide (two's complement). Q-1 is a single
    guard bit. Returns a dict with the trace (list of step dicts) and result.
    """
    mask = (1 << bits) - 1
    trace = []

    M_dec, err = _normalize_operand(multiplicand, bits, binary_input)
    if err:
        return {"error": err}
    Q_dec, err = _normalize_operand(multiplier, bits, binary_input)
    if err:
        return {"error": err}

    M = M_dec & mask          # multiplicand, n-bit two's complement pattern 
    neg_M = (-M_dec) & mask   # finding the negative m for the multiplier in case of subtraction
    A = 0
    Q = Q_dec & mask
    Q_1 = 0

    trace.append({
        "step": 0, "operation": "Initial",
        "A": format(A, f'0{bits}b'), "Q": format(Q, f'0{bits}b'), "Q-1": Q_1
    })

    for i in range(1, bits + 1):
        q0 = Q & 1
        if q0 == 0 and Q_1 == 1:
            op = "A = A + M"
            A = (A + M) & mask
        elif q0 == 1 and Q_1 == 0:
            op = "A = A - M  (A + (-M))"
            A = (A + neg_M) & mask
        else:
            op = "No arithmetic op (Q0Q-1 = 00 or 11)"

        trace.append({
            "step": f"{i}{chr(0x61)}", "operation": op,
            "A": format(A, f'0{bits}b'), "Q": format(Q, f'0{bits}b'), "Q-1": Q_1
        })

        # The arithmetic shift right function for the sequential circuit multiplication
        sign = _sign_bit(A, bits)
        new_Q_1 = Q & 1
        Q = ((Q >> 1) | ((A & 1) << (bits - 1))) & mask
        A = ((A >> 1) | (sign << (bits - 1))) & mask
        Q_1 = new_Q_1

        trace.append({
            "step": f"{i}{chr(0x62)}", "operation": "Arithmetic Shift Right (A:Q:Q-1)",
            "A": format(A, f'0{bits}b'), "Q": format(Q, f'0{bits}b'), "Q-1": Q_1
        })

    # Final product = (A:Q) as a 2*bits-wide two's complement number
    combined = (A << bits) | Q
    if combined >= (1 << (2 * bits - 1)):
        result_decimal = combined - (1 << (2 * bits))
    else:
        result_decimal = combined

    return {
        "error": None,
        "multiplicand_decimal": M_dec,
        "multiplier_decimal": Q_dec,
        "bits": bits,
        "trace": trace,
        "product_binary": format(combined & ((1 << (2 * bits)) - 1), f'0{2*bits}b'),
        "product_decimal": result_decimal,
    }

def non_restoring_division(dividend, divisor, bits, binary_input=False):
    """
    Divides `dividend` by `divisor` using the Non-Restoring Division algorithm.
    A (remainder accumulator) and Q (quotient) are `bits` wide.
    Returns dict with trace, quotient, remainder.
    NOTE: classic non-restoring division here operates on magnitudes conceptually,
    but we keep it general using the A:Q shift-left register model.
    """
    mask = (1 << bits) - 1

    dividend_dec, err = _normalize_operand(dividend, bits, binary_input)
    if err:
        return {"error": err}
    divisor_dec, err = _normalize_operand(divisor, bits, binary_input)
    if err:
        return {"error": err}

    if divisor_dec == 0:
        return {"error": "Error: division by zero."}

    trace = []

    M = divisor_dec & mask
    neg_M = (-divisor_dec) & mask
    A = 0
    Q = dividend_dec & mask

    trace.append({
        "step": 0, "operation": "Initial",
        "A": format(A, f'0{bits}b'), "Q": format(Q, f'0{bits}b')
    })

    for i in range(1, bits + 1):
        # The arithmetic shift left A:Q by 1 (then, insert 0 into Q's LSB)
        msb_Q = (Q >> (bits - 1)) & 1
        A = ((A << 1) | msb_Q) & mask
        Q = (Q << 1) & mask

        trace.append({
            "step": f"{i}{chr(0x61)}", "operation": "Shift Left (A:Q)",
            "A": format(A, f'0{bits}b'), "Q": format(Q, f'0{bits}b')
        })

        if _sign_bit(A, bits) == 0:
            A = (A + neg_M) & mask
            op = "A = A - M"
        else:
            A = (A + M) & mask
            op = "A = A + M"

        trace.append({
            "step": f"{i}{chr(0x62)}", "operation": op,
            "A": format(A, f'0{bits}b'), "Q": format(Q, f'0{bits}b')
        })

        if _sign_bit(A, bits) == 0:
            Q = Q | 1
            q_op = "Q0 = 1 (A is non-negative)"
        else:
            q_op = "Q0 = 0 (A is negative, no set)"

        trace.append({
            "step": f"{i}{chr(0x63)}", "operation": q_op,
            "A": format(A, f'0{bits}b'), "Q": format(Q, f'0{bits}b')
        })

    # Final step, if a is negative, then we restore it
    if _sign_bit(A, bits) == 1:
        A = (A + M) & mask
        trace.append({
            "step": "final", "operation": "Restore: A = A + M (A was negative)",
            "A": format(A, f'0{bits}b'), "Q": format(Q, f'0{bits}b')
        })

    quotient_signed = binary_to_decimal(format(Q, f'0{bits}b'), signed=True)
    remainder_signed = binary_to_decimal(format(A, f'0{bits}b'), signed=True)

    return {
        "error": None,
        "dividend_decimal": dividend_dec,
        "divisor_decimal": divisor_dec,
        "bits": bits,
        "trace": trace,
        "quotient_binary": format(Q, f'0{bits}b'),
        "quotient_decimal": quotient_signed,
        "remainder_binary": format(A, f'0{bits}b'),
        "remainder_decimal": remainder_signed,
    }


def print_conversion(decimal, bits):
    result = convert_decimal(decimal, bits)
    print(f"\n--- Decimal {decimal} to Binary ({bits}-bit) ---")
    if result["unsigned_error"]:
        print(result["unsigned_error"])
    else:
        print(f"Unsigned: {result['unsigned_binary']}")
    if result["signed_error"]:
        print(result["signed_error"])
    else:
        print(f"Signed  : {result['signed_binary']}")


def print_multiplication_trace(a, b, bits, binary_input=False):
    r = booth_multiplier(a, b, bits, binary_input)
    print(f"\n--- Booth's Algorithm: {a} x {b} ({bits}-bit) ---")
    if r["error"]:
        print(r["error"])
        return
    print(f"{'Step':>6} | {'Operation':<32} | {'A':<{bits}} | {'Q':<{bits}} | Q-1")
    for row in r["trace"]:
        print(f"{str(row['step']):>6} | {row['operation']:<32} | {row['A']:<{bits}} | {row['Q']:<{bits}} | {row['Q-1']}")
    print(f"\nProduct (binary, {2*bits} bits): {r['product_binary']}")
    print(f"Product (decimal): {r['product_decimal']}")


def print_division_trace(a, b, bits, binary_input=False):
    r = non_restoring_division(a, b, bits, binary_input)
    print(f"\n--- Non-Restoring Division: {a} / {b} ({bits}-bit) ---")
    if r["error"]:
        print(r["error"])
        return
    print(f"{'Step':>6} | {'Operation':<32} | {'A':<{bits}} | {'Q':<{bits}}")
    for row in r["trace"]:
        print(f"{str(row['step']):>6} | {row['operation']:<32} | {row['A']:<{bits}} | {row['Q']:<{bits}}")
    print(f"\nQuotient : {r['quotient_binary']}  (decimal: {r['quotient_decimal']})")
    print(f"Remainder: {r['remainder_binary']}  (decimal: {r['remainder_decimal']})")


if __name__ == "__main__":
    # Sample runs 
    print_conversion(25, 8)
    print_conversion(-25, 8)   # no unsigned since negative range
    print_conversion(500, 8)   # out of range, and triggers error checking

    print_multiplication_trace(-6, 5, 6)   # -6 x 5, booth's algo. demonstration = -30
    print_division_trace(11, 3, 8)         # 11/3 Q should be 3 and A should be 2