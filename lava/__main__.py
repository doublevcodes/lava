from lava.core.lexer.lexer import Lexer

for token in Lexer("23y ** 456 + \"53453456\" =\n 234"):
    print(token)
