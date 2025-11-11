import codecs
from analyzer.token import Token, TokenType

class Lexer:
    KEYWORDS = {
        "let": TokenType.LET,
        "fn": TokenType.FN,
        "mut": TokenType.MUT,
    }

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.char = self.source[self.position] if self.position < len(self.source) else None

    def _advance(self):
        if self.char is not None:
            if self.char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            
            self.position += 1
            self.char = self.source[self.position] if self.position < len(self.source) else None

    def _peek(self) -> str | None:
        peek_pos = self.position + 1
        if peek_pos < len(self.source):
            return self.source[peek_pos]
        return None

    def _skip_comment(self):
        # Asume que self.char es '/'
        if self._peek() == '/':
            # Comentario de una línea
            while self.char is not None and self.char != '\n':
                self._advance()
            return True
        elif self._peek() == '*':
            # Comentario multilínea
            self._advance() # Consume '/'
            self._advance() # Consume '*'
            while self.char is not None:
                if self.char == '*' and self._peek() == '/':
                    self._advance() # Consume '*'
                    self._advance() # Consume '/'
                    return True
                self._advance()
            return True # Comentario sin cerrar, pero lo saltamos hasta el final
        return False

    def _scan_number(self) -> Token:
        """Escanea un número, soportando enteros, flotantes y notación científica."""
        start_pos = self.position
        start_col = self.column
        start_line = self.line
        
        # Parte entera
        while self.char is not None and self.char.isdigit():
            self._advance()
        
        is_float = False
        # Parte decimal
        if self.char is not None and self.char == '.':
            if self._peek() is not None and self._peek().isdigit():
                is_float = True
                self._advance()
                while self.char is not None and self.char.isdigit():
                    self._advance()

        # Parte exponencial
        if self.char is not None and self.char in 'eE':
            is_float = True # Un número con exponente siempre es flotante
            self._advance()
            if self.char is not None and self.char in '+-':
                self._advance()
            while self.char is not None and self.char.isdigit():
                self._advance()

        lexeme = self.source[start_pos:self.position]
        
        try:
            literal = float(lexeme) if is_float else int(lexeme)
        except ValueError:
            return Token(TokenType.ERROR, lexeme, start_line, start_col, literal="Número mal formado")
            
        return Token(TokenType.NUMBER, lexeme, start_line, start_col, literal=literal)

    def _scan_identifier(self) -> Token:
        start_pos = self.position
        start_col = self.column
        start_line = self.line
        while self.char is not None and (self.char.isalnum() or self.char == '_'):
            self._advance()
            
        lexeme = self.source[start_pos:self.position]
        token_type = self.KEYWORDS.get(lexeme, TokenType.IDENT)
        return Token(token_type, lexeme, start_line, start_col)

    def _scan_string(self) -> Token:
        start_line = self.line
        start_col = self.column
        start_pos = self.position
        self._advance()  # Consumir la comilla inicial

        literal_builder = []
        while self.char is not None and self.char != '"':
            if self.char == '\\':
                self._advance()
                if self.char is None:
                    return Token(TokenType.ERROR, self.source[start_pos:self.position], start_line, start_col, literal="String sin cerrar")
                
                escape_map = {'n': '\n', 't': '\t', '"': '"', '\\': '\\'}
                if self.char in escape_map:
                    literal_builder.append(escape_map[self.char])
                else:
                    literal_builder.append('\\' + self.char)
            else:
                literal_builder.append(self.char)
            self._advance()

        if self.char is None:
            return Token(TokenType.ERROR, self.source[start_pos:self.position], start_line, start_col, literal="String sin cerrar")

        self._advance()  # Consumir la comilla final
        lexeme = self.source[start_pos:self.position]
        literal = "".join(literal_builder)
        return Token(TokenType.STRING, lexeme, start_line, start_col, literal=literal)

    def next_token(self) -> Token:
        while self.char is not None:
            if self.char.isspace():
                self._advance()
                continue

            if self.char == '/':
                if self._skip_comment():
                    continue

            start_line = self.line
            start_column = self.column

            if self.char.isalpha() or self.char == '_':
                return self._scan_identifier()
            if self.char.isdigit():
                return self._scan_number()
            if self.char == '"':
                return self._scan_string()

            token_map = {
                '=': TokenType.ASSIGN, '+': TokenType.PLUS,
                ';': TokenType.SEMICOLON, '(': TokenType.LPAREN,
                ')': TokenType.RPAREN, '{': TokenType.LBRACE,
                '}': TokenType.RBRACE, '*': TokenType.STAR,
                '/': TokenType.SLASH,
            }
            if self.char in token_map:
                lexeme = self.char
                token_type = token_map[self.char]
                self._advance()
                return Token(token_type, lexeme, start_line, start_column)

            invalid_char = self.char
            self._advance()
            return Token(TokenType.ERROR, invalid_char, start_line, start_column, literal=f"Carácter no reconocido: '{invalid_char}'")

        return Token(TokenType.EOF, "", self.line, self.column)

    def tokenize(self):
        tokens = []
        while True:
            tok = self.next_token()
            tokens.append(tok)
            if tok.type == TokenType.EOF:
                break
        return tokens