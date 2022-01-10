from typing import Any, Iterator, Optional
from unicodedata import normalize as normalise

from lava.core.lexer import Token, TokenType


def is_keyword(keyword: str) -> bool:
    keywords = {
        "print",
    }
    return keyword in keywords


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

        self.value_cache: Any = ""
        self.lexing_string: bool = False
        self.lexing_identifier: bool = False
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

            elif char == "\"" or self.lexing_string:
                if token := self.lex_string(char):
                    yield token
                self.advance()
                continue

            elif char in {"+", "-", "*", "/", "=", "^", "@", "\'", "&", "|"}:
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
                    if keyword := is_keyword(token.value):
                        yield keyword
                        self.advance()
                        continue
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

    def cache(
        self,
        _obj: Optional[str] = None,
        *,
        append: Optional[bool] = False,
        clear: Optional[bool] = False,
    ) -> Optional[str]:
        if clear:
            self.value_cache = ""
            return
        if _obj:
            self.value_cache = self.value_cache + _obj if append else _obj
            return
        return self.value_cache

    def lex_numeric(self, char: str) -> Optional[Token]:
        self.cache(
            char,
            append=True,
        )
        if not self.peek().isnumeric():
            value = self.cache()
            self.cache(clear=True)
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
            "\'": TokenType.SINGLE_QUOTE,
            "&": TokenType.AMPERSAND,
            "|": TokenType.PIPE

        }
        if op in [double_char_op[0] for double_char_op in double_char_ops]:
            if op + self.peek() in double_char_ops:
                op += self.peek()
                self.should_skip = True
        return Token(
            op_map.get(op),
            op
        )

    def lex_string(self, char: str) -> Token:
        self.lexing_string = not self.lexing_string if char == "\"" else self.lexing_string
        self.cache(
            char,
            append=True
        )
        if not self.lexing_string:
            value = self.cache()
            value = value.strip("\"")
            self.cache(clear=True)
            self.lexing_string = False
            return Token(
                TokenType.STRING,
                value,
            )

    def lex_identifier(self, char: str) -> Token:
        self.cache(
            char,
            append=True
        )

