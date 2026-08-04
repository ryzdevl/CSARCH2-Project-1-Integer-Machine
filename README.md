# CSARCH2 S40 GROUP 1 ANALYSIS WRITE UP: INTEGER MACHINE
This README documents the technical discussions, features, and test cases of our project. Our web-based calculator performs binary arithmetic operations including signed/unsigned conversions, sequential binary multiplication, and non-restoring division. 

## Course: CSARCH2 (Computer Architecture)
## Instructor: Ronald Pascual
## De La Salle University - College of Computer Studies
## Date: 04 / 08 / 2026

---

## 1. Introduction

### 1.1 Project Overview
The Binary Arithmetic Calculator is a web-based application designed to demonstrate fundamental binary arithmetic operations. It provides users with an interactive platform to visualize three core concepts from computer architecture:

1. **Binary Representation** - Signed and unsigned integer conversion
2. **Binary Multiplication** - Sequential circuit binary multiplier
3. **Binary Division** - Non-restoring division algorithm

### 1.2 Objectives
- To create a visual learning tool for binary arithmetic
- To implement sequential multiplication as described in NLec 17
- To implement non-restoring division as covered in course material
- To provide real-time, step-by-step feedback for educational purposes

### 1.3 Scope
The project focuses on 4-bit and 8-bit binary operations, with support for both positive and negative integers using 2's complement representation.

---

## 2. System Design

### 2.1 Architecture Overview
(insert photos)

### 2.2 Technology Stack

| Component | Technology | Justification |
|-----------|------------|---------------|
| Structure | HTML5 | Semantic markup for accessibility |
| Styling | Tailwind CSS | Utility-first, rapid development |
| Logic | Vanilla JavaScript | No dependencies, fast execution |
| Version Control | Git | Track changes and collaboration |

### 2.3 User Interface Design

The interface follows a **tabbed layout** with three main sections:

1. **Converter Tab** - Input decimal → Output binary (signed/unsigned)
2. **Multiplication Tab** - Input M and Q → Show iterative process
3. **Division Tab** - Input dividend and divisor → Show iterative process

Each section displays:
- Input fields with validation
- Step-by-step output with register states
- Final result in both binary and decimal

---

## 3. Algorithms Implemented

### 3.1 Binary Conversion (Signed & Unsigned)

#### 3.1.1 Unsigned Conversion
**Process:**
1. Take decimal input
2. Convert to binary using repeated division by 2
3. Pad to specified bit-width


#### 3.1.2 Signed Conversion (2's Complement)
**Process:**
1. If number is positive:
   - Convert to binary normally
   - Pad with leading zeros
2. If number is negative:
   - Convert absolute value to binary
   - Invert all bits (1's complement)
   - Add 1 (2's complement)


---

### 3.2 Sequential Binary Multiplication

#### 3.2.1 Algorithm Overview
This implements the **sequential circuit binary multiplier** as described in NLec 17.

**Register Setup:**
| Register | Purpose |
|----------|---------|
| A | Accumulator (initially 0) |
| Q | Multiplier |
| Q₋₁ | Extra bit (initially 0) |
| M | Multiplicand |

### 3.3 Non-Restoring Division

#### 3.3.1 Algorithm Overview

**Register Setup:**
| Register | Purpose |
|----------|---------|
| A | Accumulator (initially 0) |
| Q | Dividend (starts here, becomes quotient) |
| M | Divisor |

**Algorithm:**

## Unlisted YouTube Link
