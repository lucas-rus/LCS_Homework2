from binarytree import Node
import re

class PropositionalLogicParser:
    def __init__(self): #defining our object
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
        # strip one level of outer parentheses if they enclose the entire formula
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
                # outer parentheses close before the end; they are necessary
                return formula, False
        # if we reach here, outer parentheses enclose the entire formula
        stripped_formula = formula[1:-1].strip()
        # check if after stripping, the formula still has outer parentheses that enclose the entire formula
        if stripped_formula.startswith('(') and self.check_outer_parentheses(stripped_formula):
            # extra outer parentheses detected
            return stripped_formula, True
        else:
            return stripped_formula, False

    def check_outer_parentheses(self, formula):
        # check if the outer parentheses enclose the entire formula
        if not (formula.startswith('(') and formula.endswith(')')):
            return False
        count = 0
        for i in range(len(formula)):
            if formula[i] == '(':
                count += 1
            elif formula[i] == ')':
                count -= 1
            if count == 0 and i < len(formula) - 1:
                return False  # outer parentheses close before the end
        return count == 0  # true if parentheses are balanced and enclose the entire formula

    def find_principal_operator(self, formula):
        min_precedence = float('inf')
        principal_op = None
        principal_pos = -1
        paren_count = 0
        for i, c in enumerate(formula):
            if c == '(':
                paren_count += 1
            elif c == ')':
                paren_count -= 1
            elif c in self.operators and paren_count == 0:
                precedence = self.operators[c]['precedence']
                if precedence <= min_precedence:
                    min_precedence = precedence
                    principal_op = c
                    principal_pos = i
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
            # strip one level of outer parentheses and check for extra outer parentheses
            current_formula, has_extra_parentheses = self.strip_outer_parentheses(current_formula)
            if has_extra_parentheses:
                # detected unnecessary extra outer parentheses
                node.value = f"Error: Unnecessary extra parentheses in '{current_formula}'"
                self.display_tree(root, f"Invalid due to unnecessary extra parentheses in '{current_formula}'")
                return False  # formula is invalid
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
                    right_formula = current_formula[pos+1:]
                    node.left = Node('○')
                    node.right = Node('○')
                    self.display_tree(root, f"Added left and right children for '{op}'")
                    # process right first so left is on top of the stack (processed next)
                    stack.append((right_formula, node.right))
                    stack.append((left_formula, node.left))
                elif self.operators[op]['arity'] == 1:
                    operand_formula = current_formula[pos+1:]
                    node.left = Node('○')
                    self.display_tree(root, f"Added single child for unary operator '{op}'")
                    stack.append((operand_formula, node.left))
            else:
                node.value = f"Error: Malformed '{current_formula}'"
                self.display_tree(root, f"Malformed formula '{current_formula}'")
                return False  # formula is invalid
        return True  # formula is valid

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

# list of formulas to process
formulas = [
    "(((P ⇒ Q) ∨ S) ⇔ T)",         #(a)
    "((P ⇒ (Q ∧ (S ⇒ T))))",       #(b)
    "(¬(B(¬Q)) ∧ R)",              #(c)
    "((P ⇒ Q) ∧ ((¬Q) ∧ P))",      #(d)
    "((P ⇒ Q) ⇒ (Q ⇒ P))",         #(e)
    "((¬(P ∨ Q)) ∧ (¬Q))"          #(f)
]

parser = PropositionalLogicParser()
well_formed_formulas = []

# Process each formula and determine if it's well-formed
for idx, formula in enumerate(formulas, start=1):
    print("\n" + "=" * 80)
    print(f"Processing formula ({chr(96 + idx)}): {formula}")
    is_well_formed, root = parser.process_formula(formula)
    if is_well_formed:
        well_formed_formulas.append((formula, root))
    else:
        print(f"\nFormula ({chr(96 + idx)}) is not well-formed due to improper use of parentheses or other syntax errors.")

# if there are well-formed formulas, evaluate the first one under different interpretations
if well_formed_formulas:
    first_formula, root = well_formed_formulas[0]
    print("\n" + "=" * 80)
    print(f"\nEvaluating the first well-formed formula: {first_formula}")

    # define interpretations as dictionaries mapping variables to truth values
    interpretations = [
        {'P': True, 'Q': True, 'S': False, 'T': True},
        {'P': False, 'Q': True, 'S': True, 'T': False},
        {'P': True, 'Q': False, 'S': True, 'T': True}
    ]

    # function to evaluate the formula under a given interpretation with numbered steps
    def evaluate_with_steps(node, interp, steps, step_counter):
        if node is None:
            return True
        if node.value in parser.operators:
            op = node.value
            if op == '¬':
                val_left = evaluate_with_steps(node.left, interp, steps, step_counter)
                val = not val_left
                steps.append(f"Step {step_counter[0]}: ¬{val_left} = {val}")
                step_counter[0] += 1
                return val
            else:
                val_left = evaluate_with_steps(node.left, interp, steps, step_counter)
                val_right = evaluate_with_steps(node.right, interp, steps, step_counter)
                if op == '∧':
                    val = val_left and val_right
                    steps.append(f"Step {step_counter[0]}: {val_left} ∧ {val_right} = {val}")
                elif op == '∨':
                    val = val_left or val_right
                    steps.append(f"Step {step_counter[0]}: {val_left} ∨ {val_right} = {val}")
                elif op == '⇒':
                    val = (not val_left) or val_right
                    steps.append(f"Step {step_counter[0]}: {val_left} ⇒ {val_right} = {val}")
                elif op == '⇔':
                    val = val_left == val_right
                    steps.append(f"Step {step_counter[0]}: {val_left} ⇔ {val_right} = {val}")
                step_counter[0] += 1
                return val
        elif 'Error' in node.value:
            return False
        else:
            # atomic proposition
            val = interp.get(node.value, False)
            steps.append(f"Step {step_counter[0]}: {node.value} = {val}")
            step_counter[0] += 1
            return val

    # evaluate the formula under each interpretation
    for i, interp in enumerate(interpretations, start=1):
        print(f"\nInterpretation {i}: {interp}")
        steps = []
        step_counter = [1]  # we are using a list to pass by reference
        truth_value = evaluate_with_steps(root, interp, steps, step_counter)
        print("\nStep-by-step evaluation:")
        for step in steps:
            print(step)
        print(f"\nTruth value of the formula: {truth_value}")

