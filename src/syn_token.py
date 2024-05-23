class Token:
    def __init__(self, row: int, column: int, lexeme: str, type: str):
        self.row = row
        self.column = column
        self.lexeme = lexeme
        self.type = type

    def __str__(self):
        if self.lexeme != "Null":
            return f"<{self.type}, {self.lexeme}, {self.row}, {self.column}>"
        return f"<{self.type}, {self.row}, {self.column}>"
