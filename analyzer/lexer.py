from analyzer.token import Token


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        # ...inicialización interna...

    def next_token(self) -> Token:
        # TODO: Implementar escaneo real
        return Token(type="EOF", lexeme="", line=self.line, column=self.column)

    def tokenize(self):
        tokens = []
        while True:
            tok = self.next_token()
            tokens.append(tok)
            if tok.type == "EOF":
                break
        return tokens
