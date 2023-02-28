# 1
print("Hello world")

# 2
ADD = "add"
SUB = "sub"
MULT = "mult"
DIV = "div"


def math_operations(num1, num2, op):
    if op == ADD:
        return num1 + num2
    elif op == SUB:
        return num1 - num2
    elif op == MULT:
        return num1 * num2
    elif op == DIV:
        return num1 / num2
    else:
        print("invalid operation")
        return 0
