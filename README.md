# CSARCH2 S40 GROUP 1 ANALYSIS WRITE UP: INTEGER MACHINE
This README documents the technical discussions, features, and test cases of our project. Our web-based calculator performs binary arithmetic operations including signed/unsigned conversions, sequential binary multiplication, and non-restoring division. 

**Course:** CSARCH2 (Computer Architecture)

**Instructor:** Ronald Pascual

**Date:** 04 / 08 / 2026

---

## 1. Introduction

### 1.1 Project Overview
Our assigned case project is a web-based application designed to demonstrate fundamental binary arithmetic operations. It provides users with an interactive platform to visualize three core concepts from computer architecture:

1. **Binary Representation** - Signed and unsigned integer conversion
2. **Binary Multiplication** - Sequential circuit binary multiplier
3. **Binary Division** - Non-restoring division algorithm

### 1.2 Objectives
- To create a visual learning tool for binary arithmetic
- To implement binary conversion, sequential multiplication, and non-restoring division as described in the course material.
- To provide real-time, step-by-step feedback for educational purposes.

### 1.3 Scope
The project focuses on a max of 64-bit binary operations, with support for both positive and negative integers using 2's complement representation.

---

## 2. System Design

### 2.1 Architecture Overview
<img width="1893" height="788" alt="architecture-overview" src="https://github.com/user-attachments/assets/16fca7d9-a06e-45fc-8fc4-8dbd0b0949ac" />

### 2.2 Technology Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| Structure | HTML5 | Semantic markup for accessibility |
| Styling | Tailwind CSS | Utility-first, rapid development |
| Logic | Vanilla JavaScript | No dependencies, fast execution |
| Version Control | Git | Track changes and collaboration |

### 2.3 User Interface Design

The interface follows a **tabbed layout** with three main sections:

1. **Convert Tab** - Input decimal, data size → Output binary (signed/unsigned)
2. **Multiply Tab** - Input multiplicand, multiplier, data size → Show iterative process → Output product
3. **Divide Tab** - Input dividend, divisor, data size → Show iterative process → Output quotient and remainder

Each section displays:
- Input fields with validation
- Step-by-step output with register states
- Final result in both binary and decimal

---

## 3. Algorithms Implemented

### 3.1 Binary Conversion (Signed & Unsigned)

#### 3.1.1 Unsigned Conversion
**Process:**
1. Take decimal input and data size
2. Check if bit size is at least 1
3. Validate if the decimal number is within range
4. If the decimal is out of range then return an error message, otherwise proceed with the next step  
5. Convert to binary using Python's format(decimal, f'0{bits}b')
6. Return binary string padded to the specified bit width

#### 3.1.2 Signed Conversion (2's Complement)
**Process:**
1. Take decimal input and data size
2. Check if bit size is at least 1
3. Validate if the decimal number is within range
4. If number is positive:
   - Convert to binary normally
   - Return binary string
5. If number is negative:
   - Convert absolute value to binary
   - Add 2 ^ data size to the number
   - Return binary string

### 3.2 Sequential Binary Multiplication

#### 3.2.1 Algorithm Overview
**Register Setup:**
| Register | Purpose |
|----------|---------|
| A | Accumulator (initially 0) |
| Q | Multiplier |
| Q<sub>-1</sub> | Extra bit (initially 0) |
| M | Multiplicand |

**Process:**
1. Normalize inputs 
   - If input is decimal: Convert to integer, validate within signed range
   - If input is binary: Convert to decimal using signed interpretation, validate length
   - Return error if validation fails
2. Initialize registers
   - Set A = 0
   - Set M = multiplicand (in two's complement)
   - Set neg_M = two's complement of M (for subtraction)
   - Set Q = multiplier (in two's complement)
   - Set Q<sub>-1</sub> = 0
4. Save current values of A, Q, and Q<sub>-1</sub> as initial step
5. Repeat for each bit
   - Check Q and Q<sub>-1</sub> (the two rightmost bits)
      - Look at Q's least significant bit (Q₀) and the guard bit (Q<sub>-1</sub>)
      - If Q Q<sub>-1</sub> = 01: Add multiplicand to A (A = A + M)
      - If Q Q<sub>-1</sub> = 10: Subtract multiplicand from A (A = A - M)
      - If Q Q<sub>-1</sub> = 00 or 11: No arithmetic operation
   - Save A, Q, Q<sub>-1</sub> after arithmetic operation
   - Arithmetic Shift Right (ASR)
      - Save the current LSB of Q as the new Q<sub>-1</sub>
      - Shift Q right by 1, bringing in the LSB of A into Q's MSB
      - Shift A right by 1, preserving the sign bit (MSB)
      - Mask to keep only 'bits' number of bits
   - Save A, Q, Q<sub>-1</sub> after shift operation
7. Return binary and decimal representation of the product

### 3.3 Non-Restoring Division

#### 3.3.1 Algorithm Overview
**Register Setup:**
| Register | Purpose |
|----------|---------|
| A | Accumulator (initially 0) |
| Q | Dividend (starts here, becomes quotient) |
| M | Divisor |

**Process:**
1. Normalize input
   - If input is decimal: Convert to integer, validate within signed range
   - If input is binary: Convert to decimal using signed interpretation, validate length
   - Check for division by zero
   - Return error if validation fails
2. Initialize registers
   - Set A = 0
   - Set M = divisor (in two's complement)
   - Set neg_M = two's complement of M (for subtraction)
   - Set Q = dividend (in two's complement)
3. Save current values of A and Q as "Initial" step
4. Repeat for each bit
   - Shift left A:Q
      - Save the MSB of Q (will move into A's LSB)
      - Shift A left by 1
      - Shift Q left by 1
      - Insert saved MSB of Q into A's LSB
      - Insert 0 into Q's LSB
   - Save A and Q after shift operation
   - Add or Subtract based on A's sign
      - If A is positive (MSB = 0): A = A - M
      - If A is negative (MSB = 1): A = A + M 
   - Save A and Q after addition/subtraction operation
   - Set quotient bit
      - If A is positive (MSB = 0): Set Q = 1
      - If A is negative (MSB = 1): Set Q = 0 (leave as is)
   - Save A and Q after setting quotient bit
5. Return binary and decimal representation of the quotient and remainder

---

## 4. Unlisted YouTube Link

[(CSARCH2 S40 GROUP 1 DEMO VIDEO)](https://youtu.be/iF_VCFmzHhM?si=UvYSixOR2f5y4Hx_)

Note: Given the time constraint we only chose to demo selected inputs. Other test cases can be found inside the screenshots-updated folder.

---

## 5. Declaration of AI Usage
AI Tools including Claude and ChatGPT were utilized to research ideas and insights on the theme and layout for the website; these include the color scheme, font styles, and divider dimensions. They were also utilized to check for correct grammar output and tone in the reports and documentation.
