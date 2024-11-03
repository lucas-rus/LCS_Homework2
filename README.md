# Propositional Logic Analysis Tools

A collection of Python tools for analyzing propositional logic formulas. This repository contains two complementary tools for parsing, validating, and evaluating propositional logic formulas with different feature sets.

## Tools Overview

### 1. Basic Propositional Formula Checker (prop_formula_checker_ex2.py)
- Basic formula parsing and validation
- Tree visualization
- Simple truth value evaluation
- Supports multiple interpretations
- Requires binarytree package

### 2. Advanced Propositional Formula Checker (prop_formula_checker_ex3.py)
- Enhanced formula parsing and validation
- Comprehensive truth table generation
- Satisfiability checking
- Validity testing
- No external dependencies
- Built-in tree visualization

## Prerequisites

### Common Requirements
- Python 3.6 or higher
- pip (Python package installer)

### Tool-Specific Requirements
- For prop_formula_checker_ex2.py:
  ```bash
  pip install binarytree
  ```
- For prop_formula_checker_ex3.py:
  - No additional packages required
  - Uses only Python standard libraries (re, itertools)

## Installation

1. **Install Python:**
   
   **Windows:**
   ```bash
   # Download from python.org
   # Run installer (check "Add Python to PATH")
   python --version  # Verify installation
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

2. **Install Required Package (for Ex2 only):**
   ```bash
   pip install binarytree
   ```

3. **Download the Scripts:**
   - Save as `prop_formula_checker_ex2.py`
   - Save as `prop_formula_checker_ex3.py`

## Supported Logical Operators

Both tools support the same operators:
- `⇔` : Equivalence (bi-implication)
- `⇒` : Implication
- `∨` : Disjunction (OR)
- `∧` : Conjunction (AND)
- `¬` : Negation (NOT)

## Usage

### Basic Tool (Ex2)
```python
from prop_formula_checker_ex2 import PropositionalLogicParser

parser = PropositionalLogicParser()
formula = "(P ∧ Q)"
is_well_formed, root = parser.process_formula(formula)
```

### Advanced Tool (Ex3)
```python
from prop_formula_checker_ex3 import PropositionalLogicParser

parser = PropositionalLogicParser()
formula = "((P ⇒ Q) ∧ ((¬Q) ∧ P))"
is_well_formed, root = parser.process_formula(formula)
```

### Feature Comparison

| Feature                    | Ex2 (Basic) | Ex3 (Advanced) |
|---------------------------|-------------|----------------|
| Formula Parsing           | ✓           | ✓              |
| Tree Visualization        | ✓           | ✓              |
| Truth Value Evaluation    | ✓           | ✓              |
| Truth Table Generation    | ✗           | ✓              |
| Satisfiability Check      | ✗           | ✓              |
| Validity Testing          | ✗           | ✓              |
| External Dependencies     | Yes         | No             |
| Step-by-Step Evaluation   | ✓           | ✓              |

## Formula Writing Guidelines

### Valid Formula Structure (Both Tools)
```python
# Simple formulas
"(P ∧ Q)"                    # Conjunction
"(¬P)"                       # Negation
"((P ⇒ Q) ∨ R)"             # Multiple operators

# Complex formulas
"((P ⇒ Q) ∧ ((¬Q) ∧ P))"    # Nested operations
"(((P ⇒ Q) ∨ S) ⇔ T)"      # Multiple levels
```

### Invalid Formulas
```python
"P ∧ Q"                     # Missing parentheses
"(P)"                       # Single proposition
"¬P"                        # Negation without parentheses
"((P ∧ Q)"                 # Unbalanced parentheses
```

## Input Methods for Operators

1. **Copy-Paste Method:**
   - Copy operators from this README
   
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

## Output Examples

### Basic Tool (Ex2)
```
Processing formula: (P ∧ Q)
└── ∧
    ├── P
    └── Q

Truth value under interpretation {'P': True, 'Q': False}: False
```

### Advanced Tool (Ex3)
```
Processing formula: ((P ⇒ Q) ∧ ((¬Q) ∧ P))
Variables: ['P', 'Q']
Interpretation: {'P': True, 'Q': False}
Step 1: P = True
Step 2: Q = False
Step 3: (P) ⇒ (Q) = False
...
Evaluation Result:
The formula is SATISFIABLE but INVALID
```

## Adding Custom Formulas

### For Basic Tool (Ex2)
```python
formulas = [
    "(((P ⇒ Q) ∨ S) ⇔ T)",
    "((P ⇒ (Q ∧ (S ⇒ T))))",
    # Add your formulas here
]
```

### For Advanced Tool (Ex3)
```python
formulas = [
    "((P ⇒ Q) ∧ ((¬Q) ∧ (¬P)))",
    "((P ⇒ Q) ⇒ ((Q ⇒ S) ⇒ ((P ∨ Q) ⇒ R)))",
    # Add your formulas here
]
```

## Troubleshooting

1. **Installation Issues:**
   ```bash
   # For Ex2:
   python -m pip install --upgrade pip
   python -m pip install binarytree
   ```

2. **Unicode Issues (Windows):**
   - Use Windows Terminal
   - Set console font to Unicode-compatible font
   - Copy operators from README

3. **Common Errors:**
   - "Error: Unnecessary extra parentheses" - Remove redundant parentheses
   - "Error: Malformed formula" - Check syntax
   - "Not well-formed" - Verify formula structure

## When to Use Which Tool

### Use Basic Tool (Ex2) when:
- You need simple formula validation
- Basic truth value evaluation is sufficient
- You prefer a simpler output format
- Tree visualization is your primary need

### Use Advanced Tool (Ex3) when:
- You need comprehensive truth table analysis
- You want to check formula satisfiability
- You need to determine formula validity
- You prefer no external dependencies
- You need detailed step-by-step evaluation

## Contributing

Feel free to submit issues and enhancement requests!

