import random

# --- Configuration ---
# The dimensions of our data matrix, as per the exercise.
K = 3  # Number of data rows
L = 4  # Number of data columns

# --- Helper Functions (DO NOT MODIFY) ---


def create_random_matrix(k, l):
    """Creates a k x l matrix of random 0s and 1s."""
    return [[random.randint(0, 1) for _ in range(l)] for _ in range(k)]


def print_matrix(matrix, label=""):
    """Prints a matrix with a label in a readable format."""
    print(f"--- {label} ---")
    if not matrix:
        print("[]")
        return
    for row in matrix:
        print(" ".join(map(str, row)))
    print("-" * (len(label) + 4))


def matrix_to_stream(matrix):
    """Converts a matrix into a single list of bits (sent row by row)."""
    stream = []
    for row in matrix:
        stream.extend(row)
    return stream


def stream_to_matrix(stream, rows, cols):
    """Converts a stream of bits back into a matrix."""
    return [stream[i * cols : (i + 1) * cols] for i in range(rows)]


def simulate_single_bit_error(data_stream):
    """Flips a single random bit in a data stream."""
    corrupted_stream = list(data_stream)
    error_pos = random.randint(0, len(corrupted_stream) - 1)
    corrupted_stream[error_pos] = 1 - corrupted_stream[error_pos]
    print(f"\n>>> Simulating a single bit error at position {error_pos}...")
    return corrupted_stream


def simulate_burst_error(data_stream, length):
    """Flips a consecutive sequence of bits in a data stream."""
    corrupted_stream = list(data_stream)
    if len(corrupted_stream) <= length:
        # Flip all bits if burst is longer than stream
        return [1 - bit for bit in corrupted_stream]
    start_pos = random.randint(0, len(corrupted_stream) - length - 1)
    print(
        f"\n>>> Simulating a burst error of length {length} starting at position {start_pos}..."
    )
    for i in range(length):
        pos = start_pos + i
        corrupted_stream[pos] = 1 - corrupted_stream[pos]
    return corrupted_stream


# --- PART 1: Column Parity Generation ---


def calculate_column_parity(matrix, k, l):
    """
    Calculates the odd parity bit for each column.
    Returns a list containing the parity bits for each column.
    """
    parity_row = []
    # TODO 1: Implement the column parity logic.
    # --- SOLUTION ---
    # Iterate through each column index.
    for j in range(l):
        # Sum all the bits in the current column.
        column_sum = 0
        for i in range(k):
            column_sum += matrix[i][j]

        # For ODD parity:
        # If the sum of 1s is even, we need a '1' to make the total odd.
        # If the sum of 1s is odd, we need a '0' to keep the total odd.
        if column_sum % 2 == 0:  # Even sum
            parity_row.append(1)
        else:  # Odd sum
            parity_row.append(0)
    # ----------------------
    return parity_row


# --- PART 2: Column Parity Error Detection ---


def check_column_parity(received_matrix, k, l):
    """
    Checks the column parity of a received matrix (k+1 rows).
    The last row is the received parity row.
    Returns True if an error is detected, False otherwise.
    """
    error_detected = False
    errors_in_columns = []
    # TODO 2: Implement the column parity check.
    # --- SOLUTION ---
    # The last row of the received matrix is the parity row sent by the sender.
    received_parity_row = received_matrix[k]
    # The rest of the matrix is the original data.
    data_matrix = received_matrix[:k]

    # We recalculate the parity bits from the data we received.
    calculated_parity_row = calculate_column_parity(data_matrix, k, l)

    # Compare our calculation with what we received.
    for j in range(l):
        if calculated_parity_row[j] != received_parity_row[j]:
            print(f"   Error detected in column {j}!")
            errors_in_columns.append(j)
            error_detected = True
    # ----------------------
    return error_detected, errors_in_columns


# --- PART 3: 2D Parity Generation ---


def calculate_2d_parity(matrix, k, l):
    """
    Extends the matrix with both row parity and column parity.
    Returns a new, larger matrix of size (k+1) x (l+1).
    """
    extended_matrix = [row[:] for row in matrix]  # Make a copy

    # TODO 3: Calculate and add ROW parity bits.
    # --- SOLUTION ---
    # First, iterate through each data row to add its parity bit.
    for i in range(k):
        row_sum = sum(extended_matrix[i])
        # Same odd parity logic as before.
        if row_sum % 2 == 0:
            extended_matrix[i].append(1)
        else:
            extended_matrix[i].append(0)
    # ----------------------

    # Now that all rows are extended, the matrix is k x (l+1).
    # We calculate the final column parity row based on this new shape.
    column_parity_row = calculate_column_parity(extended_matrix, k, l + 1)
    extended_matrix.append(column_parity_row)

    return extended_matrix


# --- PART 4: 2D Parity Error Detection and Correction ---


def check_and_correct_2d_parity(matrix, k, l):
    """
    Checks a (k+1)x(l+1) matrix for a single bit error and corrects it.
    Returns the corrected matrix.
    """
    corrected_matrix = [row[:] for row in matrix]
    error_row_idx = -1
    error_col_idx = -1

    # TODO 4: Implement the 2D parity check and correction.
    # --- SOLUTION ---
    # Part A: Find the column with the error.
    # Iterate through all columns (including the new parity column).
    for j in range(l + 1):
        # Sum bits in the column from data rows only.
        col_sum = sum(corrected_matrix[i][j] for i in range(k))
        calculated_parity = 1 if col_sum % 2 == 0 else 0
        # Compare with the received parity bit in the last row.
        if calculated_parity != corrected_matrix[k][j]:
            error_col_idx = j
            break  # Assume only one error, so we can stop.

    # Part B: Find the row with the error.
    # Iterate through all rows (including the new parity row).
    for i in range(k + 1):
        # Sum bits in the row from data columns only.
        row_sum = sum(corrected_matrix[i][j] for j in range(l))
        calculated_parity = 1 if row_sum % 2 == 0 else 0
        # Compare with the received parity bit in the last column.
        if calculated_parity != corrected_matrix[i][l]:
            error_row_idx = i
            break  # Assume only one error, so we can stop.

    # Part C: Correct the error if exactly one row and one column are faulty.
    if error_row_idx != -1 and error_col_idx != -1:
        print(
            f"\n   Single bit error located at (row {error_row_idx}, col {error_col_idx})!"
        )
        # The bit to flip is at the intersection of the bad row and bad column.
        bit_to_flip = corrected_matrix[error_row_idx][error_col_idx]
        # A simple way to flip a bit (0->1, 1->0) is 1 - bit.
        corrected_matrix[error_row_idx][error_col_idx] = 1 - bit_to_flip
        print(f"   Flipping bit from {bit_to_flip} to {1 - bit_to_flip}.")
    elif error_row_idx != -1 or error_col_idx != -1:
        print("\n   Multiple or uncorrectable errors detected.")
    else:
        print("\n   No errors detected.")
    # ----------------------
    return corrected_matrix


# --- Main Demonstration (DO NOT MODIFY) ---
# ... (The rest of the file is identical to the exercise file) ...
if __name__ == "__main__":
    print("====== PART 1 & 2: COLUMN PARITY DEMONSTRATION ======")
    original_data = create_random_matrix(K, L)
    print_matrix(original_data, f"Original {K}x{L} Data Matrix")

    # Generate and add parity row
    parity_row = calculate_column_parity(original_data, K, L)
    matrix_with_parity = original_data + [parity_row]
    print_matrix(matrix_with_parity, "Matrix with Column Parity Row Added")

    # Simulate sending the data
    sent_stream = matrix_to_stream(matrix_with_parity)

    # Test Case 1: Single Bit Error
    corrupted_stream_1 = simulate_single_bit_error(sent_stream)
    received_matrix_1 = stream_to_matrix(corrupted_stream_1, K + 1, L)
    print_matrix(received_matrix_1, "Received Matrix (with single bit error)")
    error_detected_1, error_cols_1 = check_column_parity(received_matrix_1, K, L)
    if not error_detected_1:
        print("   ERROR: Your check function failed to detect the error!")
    else:
        print(
            f"\n   CONCLUSION: Column parity successfully detected the single bit error in column {error_cols_1[0]}."
        )
        print(
            f"   This demonstrates that column parity is ALWAYS effective at detecting single bit errors,"
        )
        print(f"   since any single bit flip will change exactly one column's parity.")

    # Test Case 2: Burst Error
    burst_length = 3  # A burst of 3 consecutive errors
    corrupted_stream_2 = simulate_burst_error(sent_stream, burst_length)
    received_matrix_2 = stream_to_matrix(corrupted_stream_2, K + 1, L)
    print_matrix(
        received_matrix_2,
        f"Received Matrix (with burst error of length {burst_length})",
    )
    print("   Checking for errors...")
    error_detected_2, error_cols_2 = check_column_parity(received_matrix_2, K, L)

    if error_detected_2:
        print(
            f"\n   CONCLUSION: Column parity detected errors in {len(error_cols_2)} column(s): {error_cols_2}."
        )
        print(
            f"   A burst error of length {burst_length} affected multiple columns, and column parity"
        )
        print(
            f"   successfully detected the corruption. However, we cannot pinpoint the exact error locations"
        )
        print(f"   or correct them - we only know which columns are affected.")
    else:
        print(
            f"\n   CONCLUSION: Column parity FAILED to detect the burst error of length {burst_length}!"
        )
        print(
            f"   This occurred because the burst happened to flip an even number of bits in each column,"
        )
        print(
            f"   leaving all column parities unchanged. This is a known weakness of simple parity schemes."
        )
        print(
            f"   Maximum guaranteed detection: burst length < L (column count), but even-bit flips per column can slip through."
        )

    print("\n\n====== PART 3 & 4: 2D PARITY DEMONSTRATION ======")
    original_data_2d = create_random_matrix(K, L)
    print_matrix(original_data_2d, f"Original {K}x{L} Data Matrix for 2D")

    matrix_2d_parity = calculate_2d_parity(original_data_2d, K, L)
    print_matrix(matrix_2d_parity, f"Matrix with 2D Parity Added (now {(K+1)}x{(L+1)})")

    # Simulate sending and a single bit error
    sent_stream_2d = matrix_to_stream(matrix_2d_parity)
    corrupted_stream_2d = simulate_single_bit_error(sent_stream_2d)
    received_matrix_2d = stream_to_matrix(corrupted_stream_2d, K + 1, L + 1)
    print_matrix(received_matrix_2d, "Received 2D Matrix (with single bit error)")

    # Attempt to correct
    corrected_matrix = check_and_correct_2d_parity(received_matrix_2d, K, L)
    print_matrix(corrected_matrix, "Matrix After Correction Attempt")

    # Final check
    if corrected_matrix == matrix_2d_parity:
        print("\n   SUCCESS: The matrix was restored to its original state!")
        print(
            "\n   CONCLUSION: 2D parity enables ERROR CORRECTION for single bit errors."
        )
        print(
            "   By checking both row and column parities, we identified the exact intersection"
        )
        print(
            "   where the error occurred. The faulty bit is at the intersection of the bad row"
        )
        print("   and bad column, allowing us to flip it back to the correct value.")
        print(
            "\n   KEY INSIGHT: 2D parity provides two dimensions of checking, creating a coordinate"
        )
        print(
            "   system that pinpoints single bit errors precisely. This is a significant advantage"
        )
        print(
            "   over simple column parity, which can only detect errors, not locate or fix them."
        )
    else:
        print("\n   FAILURE: The matrix was not corrected properly.")
        print("\n   CONCLUSION: The 2D parity scheme failed to correct the error.")
        print(
            "   This suggests either multiple errors occurred, or errors in the parity bits themselves."
        )
        print(
            "   2D parity can only reliably correct SINGLE bit errors. Multiple errors create"
        )
        print("   ambiguous parity violations that prevent accurate correction.")

    print("\n\n====== THEORETICAL QUESTIONS ======")
    print(
        """
    Based on the exercise and the output of your working code, answer these questions:

    1. How does simple column parity behave with single bit errors?
       Answer: Column parity ALWAYS detects single bit errors because any single bit flip
       changes exactly one column's parity, which will be detected during verification.

    2. How does simple column parity behave with burst-like errors?
       - Consider a burst error of length 3. Can it be detected?
         Answer: Usually YES, but not guaranteed. If the burst flips an even number of bits
         in each affected column, it may go undetected.
       - Consider a burst error of length 4 (equal to L). What happens? Why?
         Answer: High probability of detection, but still not guaranteed. If the burst
         happens to flip bits such that each column has an even number of flips, the
         column parities remain valid and the error is missed.

    3. What is the maximal length of a burst error (in our k=3, l=4 example)
       for which column parity can GUARANTEE detection?
       Answer: Length L-1 = 3. Any burst of length L-1 or less MUST affect at least one
       column with an odd number of bit flips, ensuring detection. A burst of length L or
       more could potentially flip all bits in a column twice (or an even number of times),
       leaving its parity unchanged.

    4. How does the 2D parity technique allow you to FIX a single bit error?
       Answer: 2D parity creates a coordinate system. Row parity checks identify which ROW
       has an error, and column parity checks identify which COLUMN has an error. The
       intersection of the faulty row and faulty column pinpoints the exact location of
       the corrupted bit, allowing us to flip it back to the correct value.

    5. Can 2D parity fix multiple faulty bits or burst-like errors? Why or why not?
       Answer: NO. Multiple errors create ambiguous or inconsistent parity violations.
       For example, two errors in the same row but different columns would show two column
       errors but only one row error, making it impossible to determine which specific bits
       are wrong. The "intersection" method only works when exactly one row and one column
       show parity violations, which only occurs with a single bit error.
    """
    )
