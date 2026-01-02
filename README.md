# Java Syntax Validator using PLY

A Context Free Grammar (CFG) based syntax validator for Java programming constructs using PLY (Python Lex-Yacc).

## Supported Constructs

1. **Simple Data-Type Declaration** - `int age;` or `float salary = 3.14;`
2. **Array Declaration** - `int[] numbers;` or `int[] arr = new int[10];`
3. **Selection Statement (If-Else)** - `if (x > 5) { } else { }`
4. **Looping Construct (While)** - `while (count < 10) { }`
5. **Function Declaration** - `int sum(int a, int b) { }`
6. **Increment/Decrement Statements** - `count++;` or `x--;`

Note: Access modifiers (public, private, etc.) are not currently supported in function declarations.

## Installation

```bash
pip install -r requirements.txt
```

Or install PLY directly:

```bash
pip install ply
```

## Usage

### Validate a Java file:

```bash
python java_syntax_validator.py test_cases/valid_syntax.java
```

### Test with invalid syntax:

```bash
python java_syntax_validator.py test_cases/invalid_syntax.java
```

### Run individual components (via the single entrypoint):

The project now exposes lexer, parser and CLI from a single script. You can
import the module or run the script directly.

**Run the lexer/parser from Python:**

```py
import java_syntax_validator as j
# tokens are in j.tokens, lexer object is j.lexer, parse function is j.parse_code
```

**Run the CLI:**

```powershell
python java_syntax_validator.py test_cases/valid_syntax.java
```

## Output Examples

### Valid Syntax:

```
Validating test_cases/valid_syntax.java...

----- Starting Syntax Check -----
Yes, Valid simple data-type declaration: int age;
Yes, Valid array declaration: int[] numbers;
Yes, Valid if-else statement
Yes, Valid while loop
----- Parsing Complete -----
Syntax errors found:
- unexpected token -> pi
- unexpected token -> ++
Validation complete.
```

### Invalid Syntax:

```
Validating test_cases/invalid_syntax.java...

----- Starting Syntax Check -----
Error: unexpected token -> invalidType
Error: unexpected token -> new
----- Parsing Complete -----
Syntax errors found:
- unexpected token -> invalidType
- unexpected token -> ]
Validation complete.
```

## BNF Grammar

The validator implements the following CFG rules:

### Simple Data-Type Declaration:

```
<declaration> ::= <type> <identifier> ;
                | <type> <identifier> = <expression> ;
<type> ::= int | float | char | boolean | String
```

### Array Declaration:

```
<array_declaration> ::= <type> [] <identifier> ;
                       | <type> <identifier> [] ;
                       | <type> [] <identifier> = new <type> [ <number> ] ;
```

### If-Else Statement:

```
<if_statement> ::= if ( <condition> ) <block>
                 | if ( <condition> ) <block> else <block>
```

### While Loop:

```
<while_statement> ::= while ( <condition> ) <block>
```

### Function Declaration:

```
<function_declaration> ::= <type> <identifier> ( <parameter_list> ) <block>
```

### Increment/Decrement Statements:

```
<increment_statement> ::= <identifier> ++ ;
<decrement_statement> ::= <identifier> -- ;
```

## Project Structure

```
JavaSyntaxValidator/
├── java_syntax_validator.py    # Combined lexer, parser and CLI (single entrypoint)
├── test_cases/
│   ├── valid_syntax.java       # Valid Java examples
│   └── invalid_syntax.java     # Invalid Java examples
├── outputs/
│   ├── valid_output.txt        # Success messages
│   └── invalid_output.txt      # Error messages
├── grammar_bnf.txt             # BNF notation documentation
├── README.md                   # Usage instructions
└── requirements.txt            # PLY dependency
```

## Author

Assignment: ORANGE LEVEL PROBLEM - AFLL Course  
PLY Tool Implementation for Java Syntax Validation

## Course Information

**Course:** UE24CS243A - Automata Formal Languages and Logic  
**Semester:** III  
**Assignment Type:** Experiential Learning - Orange Level Problem  
**Marks:** 3M (Coding) + 3M (Viva) = 6M Total

## Features

- Lexical analysis with token definitions
- Syntax parsing using Context Free Grammar
- Error detection and reporting
- Support for core Java constructs
- Test cases for validation

## Requirements

- Python 3.6+
- PLY (Python Lex-Yacc) 3.11

