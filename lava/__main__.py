from lava.core.lexer.lexer import Lexer

for token in Lexer('y + "53453456" =\n 234'):
    print(token)
