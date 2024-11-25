# Python code to convert infix to prefix expression
 
 
# Function to check if the character is an operator
def isOperator(c):
    return (not c.isalpha()) and (not c.isdigit())
 
 
 
# Function to get the priority of operators
def getPriority(c):
    if c == '-' or c == '+':
        return 1
    elif c == '*' or c == '/':
        return 2
    elif c == '^':
        return 3
    return 0
 
 
   
# Function to convert the infix expression to postfix
def infixToPostfix(infix):
    infix = '(' + infix + ')'
    l = len(infix)
    char_stack = []
    output = ""
 
    for i in range(l):
         
        # Check if the character is alphabet or digit
        if infix[i].isalpha() or infix[i].isdigit():
            output += infix[i]
             
        # If the character is '(' push it in the stack
        elif infix[i] == '(':
            char_stack.append(infix[i])
         
        # If the character is ')' pop from the stack
        elif infix[i] == ')':
            while char_stack[-1] != '(':
                output += char_stack.pop()
            char_stack.pop()
         
        # Found an operator
        else:
            if isOperator(char_stack[-1]):
                if infix[i] == '^':
                    while getPriority(infix[i]) <= getPriority(char_stack[-1]):
                        output += char_stack.pop()
                else:
                    while getPriority(infix[i]) < getPriority(char_stack[-1]):
                        output += char_stack.pop()
                char_stack.append(infix[i])
 
    while len(char_stack) != 0:
        output += char_stack.pop()
    return output
 
 
 
# Function to convert infix expression to prefix
def infixToPrefix(infix):
    l = len(infix)
 
    infix = list(infix[::-1])

 
    for i in range(l):
        # print(i, ' -- ' , list(infix[i]),' -- ', infix)
        if infix[i] == '(':
            infix[i] = ')'
        elif infix[i] == ')':
            infix[i] = '('
 
    infix = ''.join(infix)
    prefix = infixToPostfix(infix)
    prefix = prefix[::-1]
 
    return prefix

    # infixs = infix.split(' ')

    # for i, infix in enumerate(infixs):
    #     if infixs[i] == '(':
    #         infixs[i] = ')'
    #     elif infixs[i] == ')':
    #         infixs[i] = '('


    # infix = ''.join(infix)
    # prefix = infixToPostfix(infix)
    # prefix = prefix[::-1]
    # return prefix
 
# Driver code
if __name__ == '__main__':
    # s = "x+y*z/w+u"

    s = '( "name" | "category_id_name" | "sub_category_id_name" | "type_id_name" ) & "krassky_product" & "active"'
    s = '( n | d | c | s | t ) & ( k | a )'
     
    # Function call
    print(infixToPrefix(s))



    # '&', '&', '|', '|', '|',
