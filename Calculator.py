import tkinter as tk
import math

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

def tokenise(expression):
    """Convert a string into a list of tokens."""
    tokens = []
    i = 0
    n = len(expression)
    while i < n:
        ch = expression[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit() or ch == '.':
            start = i
            while i < n and (expression[i].isdigit() or expression[i] == '.'):
                i += 1
            num_str = expression[start:i]
            tokens.append(Token('NUM', float(num_str)))
            continue
        if ch in '+-*/^()':
            if ch in '+-*/^':
                tokens.append(Token('OP', ch))
            elif ch == '(':
                tokens.append(Token('LPAREN'))
            else:
                tokens.append(Token('RPAREN'))
            i += 1
            continue
        raise SyntaxError(f"Invalid character: {ch}")
    tokens.append(Token('EOF'))
    return tokens

# --------------------------------------------- Parser ------------------------------------------- #
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos]

    def eat(self, expected_type, expected_value=None):
        """Consume the current token if it matches, else raise error."""
        tok = self.current_token()
        if tok.type != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {tok.type}")
        if expected_value is not None and tok.value != expected_value:
            raise SyntaxError(f"Expected '{expected_value}', got '{tok.value}'")
        self.pos += 1
        return tok

    def parse(self):
        """Parse the whole expression and return the result."""
        result = self.parse_expression()
        if self.current_token().type != 'EOF':
            raise SyntaxError("Unexpected characters after expression")
        return result

    def parse_expression(self):
        left = self.parse_term()
        while self.current_token().type == 'OP' and self.current_token().value in ('+', '-'):
            op = self.eat('OP').value
            right = self.parse_term()
            if op == '+':
                left = left + right
            else:
                left = left - right
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token().type == 'OP' and self.current_token().value in ('*', '/'):
            op = self.eat('OP').value
            right = self.parse_factor()
            if op == '*':
                left = left * right
            else:
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                left = left / right
        return left

    def parse_factor(self):
        base = self.parse_primary()
        if self.current_token().type == 'OP' and self.current_token().value == '^':
            self.eat('OP', '^')
            exponent = self.parse_factor()
            return base ** exponent
        return base

    def parse_primary(self):
        tok = self.current_token()
        if tok.type == 'NUM':
            self.eat('NUM')
            return tok.value
        if tok.type == 'LPAREN':
            self.eat('LPAREN')
            expr_val = self.parse_expression()
            self.eat('RPAREN')
            return expr_val
        if tok.type == 'OP' and tok.value == '-':
            self.eat('OP', '-')
            inner = self.parse_primary()
            return -inner
        raise SyntaxError(f"Unexpected token: {tok.type} {tok.value if tok.value else ''}")


def evaluate(expression):
    """Evaluate a mathematical expression string and return the result."""
    tokens = tokenise(expression)
    parser = Parser(tokens)
    return parser.parse()


def calculate():
    """Get expression from text widget, parse and evaluate, show result."""
    expression = text.get("1.0", tk.END).strip()
    if not expression:
        return
    try:
        result = evaluate(expression)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        text.delete("1.0", tk.END)
        text.insert(tk.END, str(result))
    except (SyntaxError, ZeroDivisionError, ValueError) as e:
        text.delete("1.0", tk.END)
        text.insert(tk.END, f"Error: {e}")
    except Exception as e:
        text.delete("1.0", tk.END)
        text.insert(tk.END, "Error")

# --------------------------------------- GUI Setup ------------------------------------ #
FONT = ("Arial", 15, "bold")

window = tk.Tk()
window.config(padx=50, pady=50)
window.title("Calculator")

text = tk.Text(height=1, width=10, font=("Arial", 40, "bold"))
text.grid(row=0, column=0, columnspan=3)

buttons = [
    ('1', 1, 0), ('2', 1, 1), ('3', 1, 2),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
    ('0', 6, 2), ('.', 6, 1)
]
for btn_text, row, col in buttons:
    tk.Button(text=btn_text, width=3, height=1, font=FONT,
              command=lambda t=btn_text: text.insert(tk.END, t)).grid(row=row, column=col)

tk.Button(text="➕", width=3, height=1, font=FONT,
          command=lambda: text.insert(tk.END, "+")).grid(row=4, column=0)
tk.Button(text="➖", width=3, height=1, font=FONT,
          command=lambda: text.insert(tk.END, "-")).grid(row=4, column=1)
tk.Button(text="✖", width=3, height=1, font=FONT,
          command=lambda: text.insert(tk.END, "*")).grid(row=5, column=1)
tk.Button(text="➗", width=3, height=1, font=FONT,
          command=lambda: text.insert(tk.END, "/")).grid(row=5, column=0)
tk.Button(text="^", width=3, height=1, font=FONT,
          command=lambda: text.insert(tk.END, "^")).grid(row=4, column=2)
tk.Button(text="=", width=3, height=1, font=FONT,
          command=calculate).grid(row=5, column=2)
tk.Button(text="C", width=3, height=1, font=FONT,
          command=lambda: text.delete("1.0", tk.END)).grid(row=6, column=0)

window.mainloop()