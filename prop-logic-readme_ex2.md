# Propositional Formula Checker

A Python tool for parsing, validating, and evaluating propositional logic formulas. This tool creates visual tree representations of logical formulas and evaluates their truth values under different interpretations.

## Features

- Parses propositional logic formulas
- Creates visual tree representations
- Validates formula well-formedness
- Evaluates formulas under different interpretations
- Provides step-by-step evaluation process
- Handles complex nested expressions

## Prerequisites

### All Operating Systems
- Python 3.6 or higher
- pip (Python package installer)

### Required Package
- binarytree

## Installation

1. **Install Python:**
   
   **Windows:**
   - Download Python from [python.org](https://www.python.org/downloads/)
   - Run installer (make sure to check "Add Python to PATH")
   - Verify installation:
   ```bash
   python --version
   ```

   **macOS:**
   ```bash
   brew install python
   ```

   **Linux:**
   ```bash
   sudo apt-get update
   sudo apt-get install python3
   ```

2. **Install Required Package:**
   
   All operating systems:
   ```bash
   pip install binarytree
   ```

3. **Download the Script:**
   - Save the code as `prop_formula_checker_ex2.py`

## Supported Logical Operators

- `⇔` : Equivalence (bi-implication)
- `⇒` : Implication
- `∨` : Disjunction (OR)
- `∧` : Conjunction (AND)
- `¬` : Negation (NOT)

## Usage

1. **Basic Usage:**
   ```python
   from prop_formula_checker_ex2 import PropositionalLogicParser
   
   parser = PropositionalLogicParser()
   formula = "(P ∧ Q)"
   is_well_formed, root = parser.process_formula(formula)
   ```

2. **Running Multiple Formulas:**
   ```python
   formulas = [
       "(P ∧ Q)",
       "((P ⇒ Q) ∨ R)",
       "(¬(P ∧ Q))"
   ]

   for formula in formulas:
       parser.process_formula(formula)
   ```

## Formula Writing Guidelines

1. **Valid Formula Structure:**
   - Binary operations must be in parentheses: `(P ∧ Q)`
   - Atomic propositions are capital letters: `P`, `Q`, `R`
   - Complex formulas need proper nesting: `((P ⇒ Q) ∨ R)`

2. **Examples:**
   ```python
   Valid:
   "(P ∧ Q)"                    # Simple conjunction
   "((P ⇒ Q) ∨ R)"             # Nested operations
   "(¬(P ∧ Q))"                # Negation
   "(((P ⇒ Q) ∨ S) ⇔ T)"      # Complex nested formula

   Invalid:
   "P ∧ Q"                     # Missing parentheses
   "(P)"                       # Single proposition
   "¬P"                        # Negation without parentheses
   "((P ∧ Q)"                 # Unbalanced parentheses
   ```

## Input Methods for Logical Operators

1. **Copy-Paste Method:**
   - Copy operators from this README: `⇔`, `⇒`, `∨`, `∧`, `¬`

2. **Variable Definition:**
   ```python
   operators = {
       'equiv': '⇔',
       'implies': '⇒',
       'or': '∨',
       'and': '∧',
       'not': '¬'
   }
   formula = f"({operators['not']}P {operators['and']} Q)"
   ```

## Output Understanding

The tool provides three types of output:

1. **Tree Visualization:**
   ```
   Step 1: Processing formula '(P ∧ Q)'
   └── ∧
       ├── P
       └── Q
   ```

2. **Well-formedness Check:**
   ```
   The formula is well-formed.
   ```

3. **Truth Value Evaluation:**
   ```
   Step 1: P = True
   Step 2: Q = False
   Step 3: True ∧ False = False
   
   Truth value of the formula: False
   ```

## Error Messages

Common error messages and their meanings:
- "Error: Unnecessary extra parentheses" - Remove extra outer parentheses
- "Error: Malformed formula" - Check syntax and operator placement
- "The formula is not well-formed" - Review formula structure

## Customization

### Adding New Formulas
Modify the `formulas` list in the script:
```python
formulas = [
    "(P ∧ Q)",
    # Add your formulas here
]
```

### Adding New Interpretations
Modify the `interpretations` list:
```python
interpretations = [
    {'P': True, 'Q': False},
    # Add your interpretations here
]
```

## Troubleshooting

1. **Installation Issues:**
   ```bash
   # Upgrade pip
   python -m pip install --upgrade pip
   
   # Install binarytree with alternate method
   python -m pip install binarytree
   ```

2. **Unicode Issues (Windows):**
   - Use Windows Terminal instead of CMD
   - Set console font to a Unicode-compatible font

## Examples

```python
# Complete example with interpretation
parser = PropositionalLogicParser()
formula = "(((P ⇒ Q) ∨ S) ⇔ T)"
is_well_formed, root = parser.process_formula(formula)

# Evaluate with interpretation
interpretation = {'P': True, 'Q': True, 'S': False, 'T': True}
steps = []
step_counter = [1]
truth_value = evaluate_with_steps(root, interpretation, steps, step_counter)
```

## Contributing

Feel free to submit issues and enhancement requests!
