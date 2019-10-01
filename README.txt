This is the base implementation of the parser and scanner for EECS6083.

Software required:

1) Python 3.7
2) Python copy library (may be included in the standard library)


How to run:

>>>python Main.py [FILENAME] [DEBUG]

-FILENAME is the name of the source file.
-DEBUG is optional. Possible values are p and s, for parser or scanner debug information.




The parser is an LL(1) parser. Both the parser and the scanner have error reporting capabilities, issuing an error or warning message if an unexpected symbol or unrecognized character is found. The parser maintains a boolean flag that tracks whether code generation would occur or not, based on current error status. Both the Parser and Scanner make a reasonable attempt to continue parsing when an error is encountered. 


Work on type checking and the symbol table is mostly done, I just wanted to submit something before the very last week of the semester in case you were busy.

Kyle Hardison