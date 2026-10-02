# Greek Language Compiler

A compiler implementation written in **Python** for a small programming language using Greek keywords.

The project implements the main stages of compiler front-end processing, including lexical analysis, syntax analysis, symbol table management, and intermediate code generation.

## Features

- Lexical analysis
- Recursive descent parsing
- Symbol table with nested scopes
- Functions and procedures
- Pass-by-value and pass-by-reference parameters
- Arithmetic and boolean expressions
- Conditional statements and loops
- Intermediate code generation using quadruples
- Temporary variable generation
- Backpatching for control flow
- Error detection with source line reporting

## Supported Constructs

The language supports constructs such as:

- Variable declarations
- Assignments
- `if / else`
- `while`
- `repeat-until`
- `for`
- Input and output
- Functions
- Procedures
- Function/procedure calls

The language uses Greek keywords, including:

```text
πρόγραμμα
δήλωση
εάν
τότε
αλλιώς
όσο
επανάλαβε
για
διάβασε
γράψε
συνάρτηση
διαδικασία
```

## Project Structure

```text
.
├── compiler.py
├── test.greek
├── test.int
├── symbtest.symb
└── README.md
```

- `compiler.py` — compiler implementation
- `test.greek` — input source program
- `test.int` — generated intermediate code
- `symbtest.symb` — generated symbol table

## Usage

### Requirements

- Python 3

No external libraries are required.

### Run

Place the source program in:

```text
test.greek
```

Then execute:

```bash
python compiler.py
```

If the source program is valid, the compiler performs syntax analysis and generates the intermediate representation and symbol table.

## Intermediate Code

Intermediate code is represented using quadruples of the form:

```text
label operation operand1 operand2 result
```

Example:

```text
1 begin_block test _ _
2 := 5 _ x
3 + x 1 T_1
4 := T_1 _ x
5 halt _ _ _
```

## Compiler Pipeline

```text
Source Code
    ↓
Lexical Analysis
    ↓
Syntax Analysis
    ↓
Symbol Table
    ↓
Intermediate Code
```

## Technologies

- Python
- Recursive Descent Parsing
- Symbol Tables
- Quadruples
- Backpatching
- Compiler Design

## About

This project was developed for educational purposes as part of a compiler implementation assignment.# Greek Language Compiler

A compiler implementation written in **Python** for a small programming language using Greek keywords.

The project implements the main stages of compiler front-end processing, including lexical analysis, syntax analysis, symbol table management, and intermediate code generation.

## Features

- Lexical analysis
- Recursive descent parsing
- Symbol table with nested scopes
- Functions and procedures
- Pass-by-value and pass-by-reference parameters
- Arithmetic and boolean expressions
- Conditional statements and loops
- Intermediate code generation using quadruples
- Temporary variable generation
- Backpatching for control flow
- Error detection with source line reporting

## Supported Constructs

The language supports constructs such as:

- Variable declarations
- Assignments
- `if / else`
- `while`
- `repeat-until`
- `for`
- Input and output
- Functions
- Procedures
- Function/procedure calls

The language uses Greek keywords, including:

```text
πρόγραμμα
δήλωση
εάν
τότε
αλλιώς
όσο
επανάλαβε
για
διάβασε
γράψε
συνάρτηση
διαδικασία
```

## Project Structure

```text
.
├── compiler.py
├── test.greek
├── test.int
├── symbtest.symb
└── README.md
```

- `compiler.py` — compiler implementation
- `test.greek` — input source program
- `test.int` — generated intermediate code
- `symbtest.symb` — generated symbol table

## Usage

### Requirements

- Python 3

No external libraries are required.

### Run

Place the source program in:

```text
test.greek
```

Then execute:

```bash
python compiler.py
```

If the source program is valid, the compiler performs syntax analysis and generates the intermediate representation and symbol table.

## Intermediate Code

Intermediate code is represented using quadruples of the form:

```text
label operation operand1 operand2 result
```

Example:

```text
1 begin_block test _ _
2 := 5 _ x
3 + x 1 T_1
4 := T_1 _ x
5 halt _ _ _
```

## Compiler Pipeline

```text
Source Code
    ↓
Lexical Analysis
    ↓
Syntax Analysis
    ↓
Symbol Table
    ↓
Intermediate Code
```

## Technologies

- Python
- Recursive Descent Parsing
- Symbol Tables
- Quadruples
- Backpatching
- Compiler Design

## About

This project was developed for educational purposes as part of a compiler implementation assignment.
