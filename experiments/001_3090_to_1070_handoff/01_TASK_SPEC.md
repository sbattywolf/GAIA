# Task Specification: Simple Python Function Implementation

## TASK_ID
TASK-001-SIMPLE-FUNCTION

## OBJECTIVE
Implement a simple Python function that calculates the factorial of a given integer using recursion.

## INPUT
A single positive integer n (where 0 <= n <= 10)

## EXPECTED_OUTPUT
A Python function named `factorial` that:
- Takes one parameter `n` (integer)
- Returns the factorial of n (n!)
- Handles edge cases properly (0! = 1)
- Raises ValueError for negative inputs

## CONSTRAINTS
- Must be implemented using recursion
- Cannot use built-in math functions or libraries
- Function must be self-contained in a single file
- No external dependencies beyond standard Python library
- Code must be less than 200 lines

## TEST_REQUIREMENTS
- Include unit tests using pytest
- Tests must cover:
  - Normal cases (n=1, n=5)
  - Edge cases (n=0, n=10)
  - Error cases (negative input)

## SUCCESS_CRITERIA
- Function correctly calculates factorials for all valid inputs
- All unit tests pass
- Code is properly formatted and documented
- No runtime errors or exceptions

## FORBIDDEN_ACTIONS
- Do not modify any existing files outside this task scope
- Do not access external services or network
- Do not import additional modules beyond standard library
- Do not change architecture or system configuration
- Do not commit changes to Git
- Do not use iterative approaches (must be recursive)