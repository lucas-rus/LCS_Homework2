import re
from itertools import product

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class PropositionalLogicParser:
    def __init__(self):
        self.operators = {
            '⇔': {'arity': 2, 'precedence': 0},
            '⇒': {'arity': 2, 'precedence': 1},
            '∨': {'arity': 2, 'precedence': 2},
            '∧': {'arity': 2, 'precedence': 3},
            '¬': {'arity': 1, 'precedence': 4}
        }
        self.step = 1
        self.current_node = None

    def is_atomic(self, formula):
        return re.fullmatch(r'[A-Z]\d*', formula.strip()) is not None

    def strip_outer_parentheses(self, formula):
        # Strip one level of outer parentheses if they enclose the entire formula
        formula = formula.strip()
        if not (formula.startswith('(') and formula.endswith(')')):
            return formula, False  # No outer parentheses to strip
        count = 0
        for i in range(len(formula)):
            if formula[i] == '(':
                count += 1
            elif formula[i] == ')':
                count -= 1
            if count == 0 and i < len(formula) - 1:
                # Outer parentheses close before the end; they are necessary
                return formula, False
        # If we reach here, outer parentheses enclose the entire formula
        stripped_formula = formula[1:-1].strip()
        # Check if after stripping, the formula still has outer parentheses that enclose the entire formula
        if stripped_formula.startswith('(') and self.check_outer_parentheses(stripped_formula):
            # Extra outer parentheses detected
            return stripped_formula, True
        else:
            return stripped_formula, False

    def check_outer_parentheses(self, formula):
        # Check if the outer parentheses enclose the entire formula
        if not (formula.startswith('(') and formula.endswith(')')):
            return False
        count = 0
        for i in range(len(formula)):
            if formula[i] == '(':
                count += 1
            elif formula[i] == ')':
                count -= 1
            if count == 0 and i < len(formula) - 1:
                return False  # Outer parentheses close before the end
        return count == 0  # True if parentheses are balanced and enclose the entire formula

    def find_principal_operator(self, formula):
        min_precedence = float('inf')
        principal_op = None
        principal_pos = -1
        paren_count = 0
        i = 0
        while i < len(formula):
            c = formula[i]
            if c == '(':
                paren_count += 1
                i += 1
            elif c == ')':
                paren_count -= 1
                i += 1
            elif c in self.operators and paren_count == 0:
                # Handle multi-character operators like '⇔' and '⇒'
                if formula[i:i+2] in self.operators:
                    op = formula[i:i+2]
                    i += 2
                else:
                    op = c
                    i += 1
                precedence = self.operators[op]['precedence']
                if precedence <= min_precedence:
                    min_precedence = precedence
                    principal_op = op
                    principal_pos = i - len(op)
            else:
                i += 1
        return principal_op, principal_pos

    def parse(self, formula):
        formula = formula.replace(' ', '')
        root = Node('○')
        is_valid = self._parse_iterative(formula, root)
        return is_valid, root

    def _parse_iterative(self, formula, root):
        stack = [(formula, root)]
        while stack:
            current_formula, node = stack.pop()
            # Strip one level of outer parentheses and check for extra outer parentheses
            current_formula, has_extra_parentheses = self.strip_outer_parentheses(current_formula)
            if has_extra_parentheses:
                # Detected unnecessary extra outer parentheses
                node.value = f"Error: Unnecessary extra parentheses in '{current_formula}'"
                self.display_tree(root, f"Invalid due to unnecessary extra parentheses in '{current_formula}'")
                return False  # Formula is invalid
            self.current_node = node
            self.display_tree(root, f"Processing formula '{current_formula}'")
            if self.is_atomic(current_formula):
                node.value = current_formula
                self.display_tree(root, f"Filled with atomic '{current_formula}'")
                continue
            op, pos = self.find_principal_operator(current_formula)
            if op is not None:
                node.value = op
                self.display_tree(root, f"Set operator '{op}'")
                if self.operators[op]['arity'] == 2:
                    left_formula = current_formula[:pos]
                    right_formula = current_formula[pos+len(op):]
                    node.left = Node('○')
                    node.right = Node('○')
                    self.display_tree(root, f"Added left and right children for '{op}'")
                    # Process right first so left is on top of the stack (processed next)
                    stack.append((right_formula, node.right))
                    stack.append((left_formula, node.left))
                elif self.operators[op]['arity'] == 1:
                    operand_formula = current_formula[pos+len(op):]
                    node.left = Node('○')
                    self.display_tree(root, f"Added single child for unary operator '{op}'")
                    stack.append((operand_formula, node.left))
            else:
                node.value = f"Error: Malformed '{current_formula}'"
                self.display_tree(root, f"Malformed formula '{current_formula}'")
                return False  # Formula is invalid
        return True  # Formula is valid

    def display_tree(self, node, description):
        print(f"Step {self.step}: {description}")
        self.print_tree_with_marker(node)
        print("\n" + "-" * 50 + "\n")
        self.step += 1

    def print_tree_with_marker(self, node):
        def traverse(node, indent='', last=True):
            if node is not None:
                marker = ' <-' if node is self.current_node else ''
                print(indent + ('└── ' if last else '├── ') + str(node.value) + marker)
                indent += '    ' if last else '│   '
                children = [child for child in (node.left, node.right) if child]
                for i, child in enumerate(children):
                    traverse(child, indent, i == len(children) - 1)
        traverse(node)

    def check_well_formed(self, node):
        if node is None:
            return True
        if node.value == '○' or 'Error' in node.value:
            return False
        return self.check_well_formed(node.left) and self.check_well_formed(node.right)

    def process_formula(self, formula):
        print(f"\nProcessing formula: {formula}")
        self.step = 1
        is_valid, root = self.parse(formula)
        print("\nFinal tree:")
        self.current_node = None
        self.print_tree_with_marker(root)
        is_well_formed = is_valid and self.check_well_formed(root)
        if is_well_formed:
            print("\nThe formula is well-formed.")
        else:
            print("\nThe formula is not well-formed. There are unfilled nodes or errors.")
        return is_well_formed, root

    def get_variables(self, node):
        # Recursively collect all atomic variables in the formula
        if node is None:
            return set()
        if node.value in self.operators:
            return self.get_variables(node.left) | self.get_variables(node.right)
        elif 'Error' in node.value:
            return set()
        else:
            return {node.value}

    def evaluate_formula_with_steps(self, node, interpretation, steps, step_counter, expression_cache):
        if node is None:
            return True, ''
        if node.value in self.operators:
            op = node.value
            if op == '¬':
                val_left, expr_left = self.evaluate_formula_with_steps(
                    node.left, interpretation, steps, step_counter, expression_cache)
                val = not val_left
                expr = f'¬({expr_left})'
                steps.append(f"Step {step_counter[0]}: {expr} = {val}")
                step_counter[0] += 1
                return val, expr
            else:
                val_left, expr_left = self.evaluate_formula_with_steps(
                    node.left, interpretation, steps, step_counter, expression_cache)
                val_right, expr_right = self.evaluate_formula_with_steps(
                    node.right, interpretation, steps, step_counter, expression_cache)
                if op == '∧':
                    val = val_left and val_right
                    expr = f'({expr_left}) ∧ ({expr_right})'
                elif op == '∨':
                    val = val_left or val_right
                    expr = f'({expr_left}) ∨ ({expr_right})'
                elif op == '⇒':
                    val = (not val_left) or val_right
                    expr = f'({expr_left}) ⇒ ({expr_right})'
                elif op == '⇔':
                    val = val_left == val_right
                    expr = f'({expr_left}) ⇔ ({expr_right})'
                steps.append(f"Step {step_counter[0]}: {expr} = {val}")
                step_counter[0] += 1
                return val, expr
        elif 'Error' in node.value:
            return False, node.value
        else:
            # Atomic proposition
            val = interpretation[node.value]
            expr = f'{node.value}'
            steps.append(f"Step {step_counter[0]}: {expr} = {val}")
            step_counter[0] += 1
            return val, expr

# List of formulas to process
formulas = [
    "((P ⇒ Q) ∧ ((¬Q) ∧ (¬P)))",           # Formula (a)
    "((P ⇒ Q) ⇒ ((Q ⇒ S) ⇒ ((P ∨ Q) ⇒ R)))",  # Formula (b)
    "((¬(P ⇒ Q)) ⇔ ((P ∨ R) ∧ ((¬P) ⇒ Q)))",  # Formula (c)
    "((P ⇔ Q) ⇔ (¬(P ⇒ (¬Q))))"                # Formula (d)
]

parser = PropositionalLogicParser()

# Process each formula
for idx, formula in enumerate(formulas, start=1):
    print("\n" + "=" * 80)
    print(f"Processing formula ({chr(96 + idx)}): {formula}")
    is_well_formed, root = parser.process_formula(formula)
    if is_well_formed:
        # Get all variables in the formula
        variables = sorted(list(parser.get_variables(root)))
        print(f"\nVariables in the formula: {variables}")
        # Generate all possible interpretations
        num_vars = len(variables)
        interpretations = list(product([False, True], repeat=num_vars))
        is_valid = True
        is_satisfiable = False
        all_truth_values = []
        # Evaluate the formula under each interpretation
        for interpretation_values in interpretations:
            interpretation = dict(zip(variables, interpretation_values))
            steps = []
            step_counter = [1]
            expression_cache = {}
            truth_value, _ = parser.evaluate_formula_with_steps(
                root, interpretation, steps, step_counter, expression_cache)
            all_truth_values.append(truth_value)
            print(f"\nInterpretation: {interpretation}")
            print("\nStep-by-step evaluation:")
            for step in steps:
                print(step)
            print(f"\nTruth value of the interpretation: {truth_value}")
            if truth_value:
                is_satisfiable = True
            else:
                is_valid = False
            print("\n" + "-" * 50)
        print("\nEvaluation Result:")
        if is_valid:
            print("The formula is VALID (true under all interpretations).")
        elif is_satisfiable:
            print("The formula is SATISFIABLE but INVALID (true under some interpretations).")
        else:
            print("The formula is UNSATISFIABLE (false under all interpretations).")
    else:
        print(f"\nFormula ({chr(96 + idx)}) is not well-formed due to syntax errors.")
