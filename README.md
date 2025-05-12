# Formal Languages & Compilers Fianl Project

## Group Members

* \[Cristian Cárdenas]
* \[Isabella Marquez]

## Environment

* **Operating System**: Ubuntu 22.04 / Windows 10 (compatible with both)
* **Programming Language**: Python 3.11+
* **Editor/Tools Used**: VSCode, Python CLI

## Requirements

* Python 3.11 or higher installed
* A file named `input.txt` containing the grammar definition in the following format:

```
<number of nonterminals>
<NonTerminal> -> <alternative1> | <alternative2> | ...
...
```

Example:

```
5
S -> T E'
E' -> + T E' | e
T -> F T'
T' -> * F T' | e
F -> ( S ) | id
```

## Usage

Run the program from a terminal using Python:

```bash
python main.py
```

### Behavior:

1. The program reads a grammar from `input.txt`.

2. It computes and prints the FIRST and FOLLOW sets.

3. Then, it evaluates the type of grammar:

   * If it is both **LL(1)** and **SLR(1)**:

     ```
     Select a parser (T: for LL(1), B: for SLR(1), Q: quit):
     ```

     Then the user can input strings ending in `$`. A `yes` or `no` will be printed indicating acceptance.
   * If only **LL(1)**:

     ```
     Grammar is LL(1).
     ```

     Then parse strings until an empty line.
   * If only **SLR(1)**:

     ```
     Grammar is SLR(1).
     ```

     Then parse strings until an empty line.
   * If neither:

     ```
     Grammar is neither LL(1) nor SLR(1).
     ```

4. Each parsed string must be printed as `yes` or `no` in a single line.

## Notes

* The empty string is represented by `e`.
* The end-of-input symbol is `$`.
* No terminal in the input grammar can be `e` or `$`.

---

*This project is part of the Formal Languages and Compilers course.*
