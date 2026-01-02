//* Test Cases - Invalid Java Syntax
// * This file contains INVALID examples to show error detection

// ===== CONSTRUCT 1: Simple Data-Type Declaration (ERRORS) =====
// Error: Missing semicolon
int age

// Error: Invalid type
invalidType variable;

// Error: Identifier starts with number
int 123abc;

// Error: Missing identifier
float ;

// ===== CONSTRUCT 2: Array Declaration (ERRORS) =====
// Error: Wrong bracket syntax
int] numbers[;

// Error: Missing brackets
int arr = new int[10];

// Error: Missing size in new
String[] names = new String[];

// ===== CONSTRUCT 3: If-Else Statement (ERRORS) =====

// Error: Missing parentheses
if x > 5 {
    count++;
}

// Error: Missing condition
if () {
    x = 10;
}

// Error: Missing closing brace
if (x > 5) {
    y = 10;


// Error: Missing opening parenthesis
if x > 5) {
    count++;
}

// ===== CONSTRUCT 4: While Loop (ERRORS) =====
// Error: Missing condition
while () {
    count++;
}

// Error: Missing parentheses
while count < 10 {
    count++;
}

// Error: Missing closing parenthesis
while (x > 0 {
    x--;
}

// ===== CONSTRUCT 5: Function Declaration (ERRORS) =====
// Error: Missing return type
public calculateSum(int a, int b) {
    return a + b;
}

// Error: Missing parameter type
public int sum(a, b) {
    return a + b;
}

// Error: Missing closing parenthesis
public int multiply(int a, int b {
    return a * b;
}

// Error: Missing opening brace
public void display()
    count++;
}

// Error: Invalid access modifier
invalid int getValue() {
    return 0;
}
