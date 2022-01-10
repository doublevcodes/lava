from enum import auto, Enum
from typing import Any, Final


class TokenType(Enum):
    IDENT = auto()

    # Data types
    INTEGER = auto()
    POINT = auto()
    STRING = auto()

    # Operators
    EQUAL = auto()
    PLUS = auto()
    DASH = auto()
    STAR = auto()
    SLASH = auto()
    DOUBLE_STAR = auto()
    CARET = auto()
    AT_SYMBOL = auto()
    SINGLE_QUOTE = auto()
    AMPERSAND = auto()
    PIPE = auto()

    # Keywords
    PRINT = auto()


class Token:
    """Represents a semantic token within Lava source code as determined by the lexer.

    Attributes:
        type_ (TokenType): The type of the token.
        value (Any): The value of the token.
    """

    def __init__(self, type_: TokenType, value: Any = None):
        print("Here,", type_, flush=True)
        self.type: Final[TokenType] = type_
        self.value: Final[Any] = value

    def __repr__(self) -> str:
        print(self.type, flush=True)
        return f"Token({self.type._name_} with value {self.value})"
