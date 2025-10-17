# crc_demonstration.py
# This script demonstrates the CRC (Cyclic Redundancy Check) algorithm.
# It serves as a runnable explanation for students to understand how CRC is
# calculated and why certain errors can go undetected.

# --- EXERCISE V DEFINITIONS ---

# Generator Polynomial: G(x) = x^4 + x^3 + x + 1
# This translates to the binary key by taking the coefficients of each power of x.
# 1*x^4 + 1*x^3 + 0*x^2 + 1*x^1 + 1*x^0  =>  11011
GENERATOR_KEY = "11011"
CRC_DEGREE = 4  # The degree is the highest power in G(x), which is 4.

# The original message to be sent.
MESSAGE = "1100101011101100"

# The corrupted message that the receiver gets.
RECEIVED_MESSAGE = "11001010110110100100"


def xor_division(dividend, divisor, verbose=True):
    """
    Performs binary polynomial division using XOR.
    Returns the remainder of the division.
    """
    # The divisor must be longer than the part of the dividend we're working on.
    divisor_len = len(divisor)
    dividend = list(dividend)  # Convert to list for mutable operations

    if verbose:
        print(f"  Performing XOR division...")
        print(f"  Dividend: {''.join(dividend)}")
        print(f"  Divisor:  {divisor}")

    # Loop through the dividend, processing one bit at a time.
    for i in range(len(dividend) - divisor_len + 1):
        if dividend[i] == "1":
            # If the current leading bit is 1, we perform XOR with the divisor.
            if verbose and i < 3:  # Show first few steps
                print(f"  Step {i+1}: XORing at position {i}")
            for j in range(divisor_len):
                # XOR operation: 1^1=0, 0^0=0, 1^0=1, 0^1=1
                dividend[i + j] = "0" if dividend[i + j] == divisor[j] else "1"

    # The remainder is the last 'CRC_DEGREE' bits of the result.
    remainder = "".join(dividend[-(CRC_DEGREE):])
    if verbose:
        print(f"  Final remainder: {remainder}")
    return remainder


def find_error_pattern(original, corrupted):
    """
    Finds the error polynomial E(x) by XORing the original and corrupted messages.
    The result shows where the bit flips occurred.
    """
    # Pad the shorter string with leading zeros to match lengths
    max_len = max(len(original), len(corrupted))
    original = original.zfill(max_len)
    corrupted = corrupted.zfill(max_len)

    error_bits = []
    error_positions = []
    for i in range(max_len):
        # XORing the bits shows where they differ (i.e., where an error occurred)
        if original[i] != corrupted[i]:
            error_bits.append("1")
            error_positions.append(i)
        else:
            error_bits.append("0")

    return "".join(error_bits), error_positions


def visualize_comparison(str1, str2, label1="Original", label2="Corrupted"):
    """
    Visually compares two binary strings, highlighting differences.
    """
    max_len = max(len(str1), len(str2))
    str1 = str1.zfill(max_len)
    str2 = str2.zfill(max_len)

    print(f"   {label1:12}: {str1}")
    print(f"   {label2:12}: {str2}")

    # Create a difference indicator line
    diff_line = ""
    for i in range(max_len):
        if str1[i] != str2[i]:
            diff_line += "^"
        else:
            diff_line += " "
    print(f"   {'Differences':12}: {diff_line}")


if __name__ == "__main__":
    print("=" * 70)
    print("CRC (CYCLIC REDUNDANCY CHECK) DEMONSTRATION")
    print("=" * 70)

    print("\n📋 SETUP:")
    print(f"   Original Message (M):  {MESSAGE}")
    print(f"   Message Length:        {len(MESSAGE)} bits")
    print(f"   Generator G(x):        x^4 + x^3 + x + 1")
    print(f"   Generator Key (G):     {GENERATOR_KEY}")
    print(f"   CRC Degree:            {CRC_DEGREE} bits")

    print("\n💡 KEY CONCEPT:")
    print("   CRC works by treating binary numbers as polynomials and performing")
    print("   division using XOR instead of subtraction. The remainder becomes")
    print("   our error-checking code.")

    # --- PART 1: SENDER - Compute the CRC value ---
    print("\n" + "=" * 70)
    print("STEP 1: SENDER CALCULATES CRC")
    print("=" * 70)

    # Step 1: Append 'n' zero bits to the message, where n is the CRC degree.
    padded_message = MESSAGE + "0" * CRC_DEGREE
    print(f"\n1️⃣  Pad the message with {CRC_DEGREE} zeros:")
    print(f"   Original:  {MESSAGE}")
    print(f"   Padded:    {padded_message}")
    print(f"   └─ We add {CRC_DEGREE} zeros to make room for the CRC checksum")

    # Step 2: Perform XOR division to find the remainder.
    print(f"\n2️⃣  Divide padded message by generator key using XOR:")
    crc_remainder = xor_division(padded_message, GENERATOR_KEY, verbose=True)

    print(f"\n   ✓ CRC checksum calculated: {crc_remainder}")

    # Step 3: Append the CRC to the original message to create the codeword.
    transmitted_codeword = MESSAGE + crc_remainder
    print(f"\n3️⃣  Create the final codeword (Message + CRC):")
    print(f"   Message:   {MESSAGE}")
    print(f"   CRC:       {' ' * len(MESSAGE)}{crc_remainder}")
    print(f"   Codeword:  {transmitted_codeword}")
    print(f"\n   📤 SENDER transmits: {transmitted_codeword}")

    print("\n   💡 INSIGHT: The codeword is mathematically designed so that when")
    print("      divided by the generator, it produces a remainder of zero.")
    print("      Any transmission error will (usually) break this property!")

    # --- PART 2: RECEIVER - Check the corrupted message ---
    print("\n" + "=" * 70)
    print("STEP 2: RECEIVER CHECKS FOR ERRORS")
    print("=" * 70)

    print(f"\n📥 RECEIVER gets: {RECEIVED_MESSAGE}")
    print(f"\n   Let's compare what was sent vs. what was received:")
    visualize_comparison(
        transmitted_codeword, RECEIVED_MESSAGE, "Transmitted", "Received"
    )

    # Count the errors
    error_pattern_temp, error_pos = find_error_pattern(
        transmitted_codeword, RECEIVED_MESSAGE
    )
    num_errors = len(error_pos)
    print(f"\n   ⚠️  {num_errors} bit(s) were flipped at position(s): {error_pos}")

    # Step 1: The receiver divides the ENTIRE received message by the generator key.
    print(f"\n1️⃣  Receiver divides the received message by generator key:")
    check_remainder = xor_division(RECEIVED_MESSAGE, GENERATOR_KEY, verbose=True)

    print(f"\n   Result: Remainder = {check_remainder}")

    # Step 2: Check if the remainder is zero.
    print(f"\n2️⃣  Check the remainder:")
    if int(check_remainder, 2) == 0:
        print(f"   Remainder = 0000 (zero)")
        print(f"   🟢 RECEIVER CONCLUSION: NO ERROR DETECTED")
        print(f"   └─ The message appears valid (divisible by generator)")

        print(f"\n   ⚠️  BUT WAIT! We know {num_errors} error(s) actually occurred!")
        print(f"   └─ This is a FALSE NEGATIVE - the CRC missed the errors!")
    else:
        print(f"   Remainder = {check_remainder} (non-zero)")
        print(f"   🔴 RECEIVER CONCLUSION: ERROR DETECTED")
        print(f"   └─ The message is corrupted (not divisible by generator)")

    # --- PART 3: CONCLUSION AND EXPLANATION ---
    print("\n" + "=" * 70)
    print("STEP 3: UNDERSTANDING WHY CRC FAILED")
    print("=" * 70)

    print("\n❓ QUESTION: Why didn't CRC detect these errors?")
    print("\n💡 ANSWER: CRC fails when the error pattern itself is divisible")
    print("   by the generator polynomial. Let's prove this mathematically!")

    # The error pattern E(x) is the result of XORing the transmitted message with the received one.
    error_pattern, error_positions = find_error_pattern(
        transmitted_codeword, RECEIVED_MESSAGE
    )

    print(f"\n1️⃣  Calculate the Error Pattern (E):")
    print(f"   The error pattern shows WHICH bits were flipped:")
    visualize_comparison(
        transmitted_codeword, RECEIVED_MESSAGE, "Transmitted", "Received"
    )
    print(f"   Error Pattern: {error_pattern}")
    print(f"   └─ Each '1' indicates a bit that was flipped")
    print(f"   └─ Total of {error_pattern.count('1')} bit(s) flipped")

    print(f"\n2️⃣  Test if Error Pattern is divisible by Generator:")
    print(f"   Dividing E by G to check if remainder is zero...")
    error_check_remainder = xor_division(error_pattern, GENERATOR_KEY, verbose=True)

    print(f"\n3️⃣  MATHEMATICAL PROOF:")
    print(f"   • Transmitted codeword T = {transmitted_codeword}")
    print(f"   • Received message T'    = {RECEIVED_MESSAGE}")
    print(f"   • Error pattern E        = {error_pattern}")
    print(f"   • E ÷ G remainder        = {error_check_remainder}")

    if int(error_check_remainder, 2) == 0:
        print(f"\n   ✓ Remainder is ZERO! This proves E is a multiple of G.")
        print(f"\n   🎯 KEY INSIGHT: When we receive T', the CRC check computes:")
        print(f"      T' ÷ G = (T + E) ÷ G = (T ÷ G) + (E ÷ G)")
        print(f"             = 0 + 0 = 0")
        print(f"\n   Since both T and E are divisible by G, their XOR (T') is also")
        print(f"   divisible by G. The CRC algorithm cannot distinguish T' from T!")

        print(f"\n   🔍 WHY THIS HAPPENED:")
        print(
            f"   • The specific pattern of {num_errors} bit flip(s) at position(s) {error_positions}"
        )
        print(f"     created an error polynomial that happens to be a multiple of")
        print(f"     our generator polynomial G(x) = x^4 + x^3 + x + 1")
        print(f"   • This is like accidentally adding a multiple of 7 to a number:")
        print(f"     you won't notice when checking divisibility by 7!")

        print(f"\n   📊 PROBABILITY:")
        print(
            f"   • For a degree-{CRC_DEGREE} CRC, there are 2^{CRC_DEGREE} = {2**CRC_DEGREE} possible remainders"
        )
        print(f"   • Only 1 of these ({2**CRC_DEGREE}) gives remainder 0")
        print(
            f"   • So roughly 1 in {2**CRC_DEGREE} random error patterns will go undetected"
        )
        print(f"   • This particular error pattern was one of the 'unlucky' ones!")

    else:
        print(f"\n   ✗ Remainder is NON-ZERO. The error should have been detectable.")
        print(f"   └─ There may be an error in the calculation.")

    # Final summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("\n✅ WHAT CRC DOES WELL:")
    print("   • Detects ALL single-bit errors")
    print("   • Detects ALL double-bit errors (for most generators)")
    print("   • Detects ALL odd number of bit errors (for generators with x+1 factor)")
    print("   • Detects most burst errors up to the CRC degree length")

    print("\n❌ CRC LIMITATION:")
    print("   • Cannot detect errors when the error pattern E(x) is a multiple")
    print("     of the generator polynomial G(x)")
    print(
        f"   • Probability of undetected error ≈ 1/{2**CRC_DEGREE} = {1/(2**CRC_DEGREE)*100:.1f}%"
    )

    print("\n🎓 STUDENT TAKEAWAY:")
    print("   CRC is a powerful error detection technique, but it's not perfect!")
    print("   The choice of generator polynomial determines which error patterns")
    print("   can slip through undetected. Good generators minimize this risk,")
    print("   but cannot eliminate it entirely.")
    print("\n" + "=" * 70)
