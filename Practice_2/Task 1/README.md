# Binary File Reader Assignment 📁

## Task Description 📋

Given a binary file with the following structure: **Domain (20s), port (i)**

Write a Python script supporting the following command line arguments:
- `port <line>`: outputs what service belongs to the port of the line given as parameter
- `domain <line>`: outputs the resolved IP address of the domain of the line given as parameter
- If there is no parameter, outputs the host's name

## File Structure 🏗️

The binary file `data.bin` contains records with this format:
- **Domain**: 20-byte string (null-padded if shorter)
- **Port**: 4-byte signed integer

Each record is exactly 24 bytes total.

## Files Provided 📂

- `solution.py` - Your main implementation file (contains TODO comments)
- `create_test_file.py` - Generates the test data file
- `cheat_sheet.md` - Reference guide with helpful functions and examples
- `README.md` - This file


### Setup
```bash
python3 data_generator.py
```
You should see: `✅ data.bin created successfully.`


## How to Run and Test 🧪

### Step 1: Create the Test File
```bash
python3 create_test_file.py
```
**Expected Output:**
```
✅ data.bin created successfully.
```

### Step 2: Test Your Implementation

**Test Case 1: No arguments (get hostname)**
```bash
python3 solution.py
```
**Expected Output:** Your computer's local hostname (e.g., `My-Laptop`)

**Test Case 2: Get service for port 80**
```bash
python3 solution.py port 1
```
**Expected Output:**
```
http
```

**Test Case 3: Get IP for google.com**
```bash
python3 solution.py domain 1
```
**Expected Output:** An IP address for Google (e.g., `142.250.180.14`)

**Test Case 4: Get service for port 443**
```bash
python3 solution.py port 2
```
**Expected Output:**
```
https
```

**Test Case 5: Unresolvable domain**
```bash
python3 solution.py domain 4
```
**Expected Output:**
```
Error: Domain 'nonexistent12345.xyz' could not be resolved.
```

**Test Case 6: Unknown port service**
```bash
python3 solution.py port 4
```
**Expected Output:**
```
Error: Port 9999 does not correspond to a known service.
```

**Test Case 7: Line number out of bounds**
```bash
python3 solution.py port 100
```
**Expected Output:**
```
Error: Line 100 is out of bounds or file is corrupt.
```

## Sample Test Data 📊

The generated `data.bin` file contains these records:
1. `google.com` : `80`
2. `elte.hu` : `443`
3. `example.com` : `80`
4. `nonexistent12345.xyz` : `9999`

## Debugging Help 🔍

If you're stuck, try adding these debug prints:
```python
print(f"Offset: {offset}")
print(f"Data length: {len(data)}")
print(f"Unpacked: {unpacked_data}")
print(f"Raw domain: {unpacked_data[0]!r}")
```

## Clean Up 🧹

When finished testing:
```bash
rm data.bin
```

## Need Help? 🤔

1. Check the `cheat_sheet.md` for function references
2. Review Python documentation for `struct` and `socket` modules
