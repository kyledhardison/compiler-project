from Definitions import Token

class ErrorHandler:
    def Warning(self, token, message):
        print("WARNING: line " + str(token.Line_Num) + ": " + message)

    def Warning_Tokenless(self, message):
        print("WARNING: " + message)

    def Error(self, token, message):
        print("ERROR: line " + str(token.Line_Num) + ": " + message)

    def Error_Expected(self, token, expected):
        print("ERROR: line " + str(token.Line_Num) + ": '" + expected + "' expected")