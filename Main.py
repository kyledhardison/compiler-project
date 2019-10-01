#from pathlib import Path
from Scanner import Scanner
from Parser import Parser
from Definitions import Tokens
from Definitions import Token
import sys


def main():
    #Take first argument from command line is source file name

    file_path = sys.argv[1]
    #file_path = ".\\test.txt"
    #file_path = "test.txt"
    #file_path = "testPgms\correct\\test1.src"

    s = Scanner(file_path)
    p = Parser(s)

    if(len(sys.argv) == 3):
        if(sys.argv[2].find('s') != -1):
            p.Scanner_Debug = True
        if(sys.argv[2].find('p') != -1):
            p.Parser_Debug = True


    p.Parse()


    """
    while (True):
        token = s.Get_Next_Token()
        #if(token.Type == Tokens.UNKNOWN.value):
        print("Token: ", end='')
        print(Tokens(token.Type).name, end = '')
        print(" Line: ", end='')
        print(token.Line_Num, end='')
        print(" Value: ", end='')
        print(token.Value)
        if(token.Type == Tokens.EOF.value):
            break
    """

    
    

    print("")
    if(p.Do_Code_Gen):
        print("Code generation would occur.")
    else:
        print("Code generation would not occurr, errors were found. ")
    


    #test.readFile()
    #print(testscanner.test('2'))



if __name__ == "__main__":
    main()