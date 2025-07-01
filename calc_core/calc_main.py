import ast
import sys


class Calculator(ast.NodeTransformer):
    def __init__(self, parsed_expr):
        """
        :param parsed_expr: parsed by ast-module math expression.
        Will be used to define nodes of math operation such as
        ADD, SUB, MULT and DIV
        """

        # sending attributes to assignment into another function
        self.verify_expression_type(parsed_expr)

        self.result = self.visit(parsed_expr)
        print(self.result)

    def verify_expression_type(self, parsed_expr):
        """
        ast library has term as BinOp (binary operation), UnaryOp and Constant.
        This function will be checking type of ast[.]body that transmitted to class
        and not 'raise NameError()' but accurate inform about what user should to do.
        """
        try:
            if not isinstance(parsed_expr, (ast.BinOp, ast.UnaryOp, ast.Constant)):
                raise AttributeError('Write any binary operation')

        except AttributeError as error:
            self.show_info_about_error(error)

    def visit_BinOp(self, node):
        """
        :param node: a variable that links to the current tree node
        :return: the result of traversing one of the tree nodes
        """
        left_side = self.visit(node.left)
        right_side = self.visit(node.right)
        operator_symbol = self.visit(node.op)

        if isinstance(operator_symbol, ast.Add):
            return left_side + right_side

        if isinstance(operator_symbol, ast.Sub):
            return left_side - right_side

        if isinstance(node.op, ast.Mult):
            return left_side * right_side

        if isinstance(node.op, ast.Div):
            try:
                return left_side / right_side
            except ZeroDivisionError as error:
                self.show_info_about_error(error)

    def visit_UnaryOp(self, node):
        """
        :param node: a variable that links to the current node tree
        :return: return result of traversing nodes tree
        """
        operator = self.visit(node.operand)

        if isinstance(node.op, ast.USub):
            return -operator

        if isinstance(node.op, ast.UAdd):
            return +operator

        return operator

    def visit_Constant(self, node):
        return node.value

    @classmethod
    def show_info_about_error(cls, error):
        """
        :param error: This parameter collect info about errors from validation methods.
        """
        print(f'Error: {error}.\nExpression should include binary operation.\nExample: a + b, a - b, a / b, a * b')
        sys.exit()


try:
    user_input = ast.parse(input().replace(' ', ''), mode='eval').body
    Calculator(user_input)

except SyntaxError as e:
    print(f'Error: {e}\nUncountable expression. {Calculator.show_info_about_error(e)}')
