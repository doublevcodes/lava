from typing import Any, Iterator, Optional
from unicodedata import normalize as normalise

from lava.core.lexer import Token, TokenType


class Lexer:
    """Lexer for Lava source code.

    The lexer goes through the source code character by character and
    returns a sequence of tokens. Each token is an instance of the
    Token class.

    Attributes:
        source (str): The NFD-normalised source code to lex.
        current_line (int): The lexer's current line.
        current_col (int): The lexer's current column.
    """

    def __init__(self, source: str) -> None:

        # The source code to lex.
        self.source: str = normalise("NFKC", source)

        # The current line in the source code.
        self.current_line: int = 0

        # The current column in the source code.
        self.current_col: int = 0

        # The current index in the source code.
        self.index: int = 0

        self.cache: dict[str, str] = {
            "numeric": "",
            "string": "",
            "ident": ""
        }
        self.should_skip: bool = False

    def __iter__(self) -> Iterator:
        for char in self.source:
            if self.should_skip:
                self.should_skip = False
                self.advance()
                continue

            if char == "\n":
                self.advance(newline=True)
                continue

            elif char.isspace():
                self.advance()
                continue

            elif char == '"':
                if token := self.lex_string(char):
                    yield token
                self.advance()
                continue

            elif char in {"+", "-", "*", "/", "=", "^", "@", "'", "&", "|"}:
                if token := self.lex_arithmetic_op(char):
                    yield token
                self.advance()
                continue

            elif char.isnumeric():
                if token := self.lex_numeric(char):
                    yield token
                self.advance()
                continue

            else:
                if token := self.lex_identifier(char):
                    yield token
                self.advance()
                continue

    def peek(self) -> str:
        try:
            return self.source[self.index + 1]
        except IndexError:
            return ""

    def advance(self, *, newline: Optional[bool] = False) -> None:
        self.index += 1
        self.current_col += 1
        if newline:
            self.current_col = 0
            self.current_line += 1

    def lex_numeric(self, char: str) -> Optional[Token]:
        self.cache["numeric"] += char
        if not self.peek().isnumeric():
            value = self.cache["numeric"]
            self.cache["numeric"] = ""
            return Token(
                TokenType.INTEGER,
                value,
            )

    def lex_arithmetic_op(self, op: str):
        double_char_ops = ("**",)
        op_map: dict[str, TokenType] = {
            "+": TokenType.PLUS,
            "=": TokenType.EQUAL,
            "-": TokenType.DASH,
            "*": TokenType.STAR,
            "**": TokenType.DOUBLE_STAR,
            "/": TokenType.SLASH,
            "^": TokenType.CARET,
            "@": TokenType.AT_SYMBOL,
            "'": TokenType.SINGLE_QUOTE,
            "&": TokenType.AMPERSAND,
            "|": TokenType.PIPE,
        }
        if op in [double_char_op[0] for double_char_op in double_char_ops]:
            if op + self.peek() in double_char_ops:
                op += self.peek()
                self.should_skip = True
        return Token(op_map.get(op), op)

    def lex_string(self, char: str) -> Token:
        self.cache["string"] += char
        if self.peek() == '"':
            value = self.cache["string"]
            value = value.strip('"')
            self.cache["string"] = ""
            return Token(
                TokenType.STRING,
                value,
            )

    def lex_identifier(self, char: str) -> Token:
        self.cache["ident"] += char
        if not self.peek().isalnum():
            value = self.cache["ident"]
            self.cache["ident"] = ""
            return Token(
                TokenType.IDENT,
                value,
            )
