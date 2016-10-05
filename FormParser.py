"""This module implements all that's needed for parsing logic forms (wffs, sequents, etc.)"""

# Parsing Tools
from Scanner import *

# Product Classes
import copy
from Form import *


class Token( object ):
   """Implements a WFF Token class."""
   # Constants (Identical to those in Lexeme)
   EOF            =    0
   UNKNOWN        =    1

   PREFIX_OP      =  100
   POSTFIX_OP     =  101
   INFIX_OP       =  102
   OPEN           =  103
   CLOSE          =  104

   SYMBOL         =  200
   OBJECT         =  201
   VARIABLE       =  202
   FUNCTION       =  203
   PREDICATE      =  204

   COMMA          =  500
   ENTAILS        =  501

   PUNCT          =  600

   # Standard Methods
   def __init__( self, aToken, aValue = None ):
      """Initialize a new instance of the class.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Initializes an instance.
      Preconditions: [AssertionError] aToken must be an int.
                     [AssertionError] If specified, aLexeme must be a string.
      """
      assert isinstance( aToken, int )
      assert isinstance( aValue, str ) or ( aValue is None )

      self.tok   = aToken
      self.lex   = aValue

   def __str__( self ):
      """Implement the str() operation.
      Category:       Pure Function.
      Returns:        (str) A string representation of this instance.
      Side Effects:   None.
      Preconditions:  None.
      """
      assert isinstance( self.tok, int )
      assert isinstance( self.lex, str ) or ( self.lex is None )

      return                       \
         '[' +                     \
         {
         self.EOF:         'EOF:',
         self.UNKNOWN:     'UNK:',
         self.PREFIX_OP:   'PRE:',
         self.POSTFIX_OP:  'PST:',
         self.INFIX_OP:    'INF:',
         self.OPEN:        'OPN:',
         self.CLOSE:       'CLS:',
         self.SYMBOL:      'SYM:',
         self.OBJECT:      'OBJ:',
         self.VARIABLE:    'VAR:',
         self.FUNCTION:    'FNC:',
         self.PREDICATE:   'PRD:',
         self.COMMA:       'CMA:',
         self.ENTAILS:     'ENT:',
         self.PUNCT:       'PUN:'
         } [ self.tok ]             \
         + self.lex                 \
         + ']'

   def __repr__( self ):
      """Implement the repr() operation.
      Category:       Pure Function.
      Returns:        (str) A string representation of this instance.
      Side Effects:   None.
      Preconditions:  None.
      """
      assert isinstance( self.tok, int )
      assert isinstance( self.lex, str ) or ( self.lex is None )

      return self.__str__( )


class WFFScanner( Scanner ):
   """Scanner for the traditional logic notation wffs."""
   # Constants
   WHITE_SPACE     = """ \t\n"""
   PUNCT           = """,;."""
   QUOTE           = """\"\'\`"""
   GROUPER         = """(){}[]"""
   SIGN            = """+-"""
   DIGIT           = """0123456789"""
   ALPHA_CAP       = """ABCDEFGHIJKLMNOPQRSTUVWXYZ"""
   ALPHA_SMALL     = """abcdefghijklmnopqrstuvwxyz"""
   ALPHA           = (ALPHA_CAP + ALPHA_SMALL)
   OBJECT          = """abcdefghijklmnopqrst"""
   VARIABLE        = """uvwxyz"""
   SPECIAL         = """@#$%^&*_=\|~:<>/?!"""
   SYMBOL          = (SPECIAL + SIGN)

   # Standard Methods
   def __init__( self, aLexList ):
      """Initialize a new instance of the class.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Initializes an instance.
      Preconditions: [AssertionError] aDict must be a dictionary.
      """
      assert isinstance( aLexList, list )

      Scanner.__init__( self )
      self._lexList  = aLexList

      self._lexDict = { }
      for lexIdx,lexDef in enumerate(self._lexList):

         self._lexDict[ lexDef.symbol[0] ] = lexIdx

   # Specialization of Scanner
   def _scanNextToken( self ):
      """Consume the next token (i.e. scan past it).
      Category:      Mutator.
      Returns:       Token.
      Side Effects:  Scans the next token from the source string.
      Preconditions: The scanner must hold a Scanner buffer which wraps
                        a string.
      """
      assert isinstance( self._lexList,     list          )
      assert isinstance( self._lexDict,     dict          )
      assert isinstance( self._tok,         int           ) or ( self._tok is None )
      assert isinstance( self._buffer,      ScannerBuffer )
      assert isinstance( self._tokPos,      int           )
      assert isinstance( self._tokLineNum,  int           )
      assert isinstance( self._tokColNum,   int           )
      assert isinstance( self._tokLineText, str           )

      self._buffer.consumePast( self.WHITE_SPACE )         # skip whitespace
      theNextChar = self._buffer.peek()
      if theNextChar == None:
         self._buffer.setMark( )
         return Token.EOF
      elif theNextChar in ',':                            #    comma
         self._buffer.setMark( )
         self._buffer.consume( )
         return Token.COMMA
      elif theNextChar in self.PUNCT:                     #    punctuation
         self._buffer.setMark( )
         self._buffer.consume( )
         return Token.PUNCT
      elif theNextChar in '([{':                          #    open
         self._buffer.setMark( )
         self._buffer.consume( )
         return Token.OPEN
      elif theNextChar in ')]}':                          #    close
         self._buffer.setMark( )
         self._buffer.consume( )
         return self._lookupSymbolLex( Token.CLOSE, self.peekLex() )
      elif theNextChar in (self.ALPHA_CAP + self.DIGIT):  #    Name Symbol
         self._buffer.setMark( )
         self._buffer.consumePast(self.ALPHA_CAP + self.DIGIT)
         self._buffer.consumeIf( ':' )
         return self._lookupSymbolLex( Token.SYMBOL, self.peekLex() )
      elif theNextChar in '-~':                           #    Negation or Op Symbol
         self._buffer.setMark( )
         self._buffer.consume( )
         if self._buffer.peek( ) in '-~':
            return self._lookupSymbolLex( Token.SYMBOL, self.peekLex() )
         else:
            self._buffer.consumePast( self.SYMBOL + self.SIGN )
            return self._lookupSymbolLex( Token.SYMBOL, self.peekLex() )
      elif theNextChar in self.SYMBOL:                    #    Op Symbol
         self._buffer.setMark( )
         self._buffer.consumePast( self.SYMBOL + self.SIGN )
         return self._lookupSymbolLex( Token.SYMBOL, self.peekLex() )
      elif theNextChar in self.OBJECT:                    #    Object Symbol
         self._buffer.setMark( )
         self._buffer.consume( )
         return self._lookupSymbolLex( Token.OBJECT, self.peekLex() )
      elif theNextChar in self.VARIABLE:                  #    Variable Symbol
         self._buffer.setMark( )
         self._buffer.consume( )
         return self._lookupSymbolLex( Token.VARIABLE, self.peekLex() )
      else:                                               #    Unknown
         self._buffer.consume( )
         return Token.UNKNOWN

   # Extension
   def _lookupSymbolLex( self, aTok, aLex ):
      """Makes a Token.  If aLex is supplied and aTok is not None,
      aToken is looked up in the dictionary.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Saves the next token.
      Preconditions: [AssertionError] aTok must be an int.
                     [AssertionError] If supplied, aLex must be a string.
      """
      assert isinstance( aTok,              int           )
      assert isinstance( aLex,              str           ) or ( aLex is None )

      assert isinstance( self._lexDict,     dict          )
      assert isinstance( self._tok,         int           ) or ( self._tok is None )
      assert isinstance( self._buffer,      ScannerBuffer )
      assert isinstance( self._tokPos,      int           )
      assert isinstance( self._tokLineNum,  int           )
      assert isinstance( self._tokColNum,   int           )
      assert isinstance( self._tokLineText, str           )

      theTok = aTok
      theLex = aLex
      if theLex is not None:
         if (theTok != Token.EOF) and (theLex in self._lexDict):
            theTok = self._lexList[ self._lexDict[ theLex ] ].token

      return theTok

   def expect( self, aTok, aMsg ):
      """If the next token in the input stream is 'aTok', consume it.  Otherwise,
      raise a ParseError exception withat 'aMsg'.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Consume the next token in the input stream.
      Preconditions: [AssertionError] 'aTok' must be an int.
                     [AssertionError] 'aMsg' must be a str.
      """
      assert isinstance( aTok,             int           )
      assert isinstance( aMsg,             str           )

      assert isinstance( self._lexDict,    dict          )
      assert isinstance( self._tok,         int           ) or ( self._tok is None )
      assert isinstance( self._buffer,      ScannerBuffer )
      assert isinstance( self._tokPos,      int           )
      assert isinstance( self._tokLineNum,  int           )
      assert isinstance( self._tokColNum,   int           )
      assert isinstance( self._tokLineText, str           )

      nextTok = self.peek( )
      if nextTok != aTok:
         raise ParseError( self.genErr( aMsg ) )
      self.consume( )


class WFFParser( object ):
   """This class implements a parser for WFFs."""
   # Shared
   def __init__( self ):
      """Initialize a new instance of Parser.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Initialize an instance.
      Preconditions: None.
      """
      self._scanner = None

   def parseProposition( self, scanner, parseFull = True ):
      """Parse a proposition from the string wrapped by scanner.
      Category:      Mutator.
      Returns:       (WFF) A wff.
      Side Effects:  Advances the scanner pointer.
      Preconditions: [ParseError] If parseFull is True, the proposition in
                        the wrapped string must be followed immediately by
                        end of the string.  If Fase, the parser only tries to
                        parse the beginning of the wrapped string.
      """
      assert isinstance( scanner,       Scanner )
      assert isinstance( parseFull,     bool    )

      assert isinstance( self._scanner, Scanner ) or ( self._scanner is None )

      self._scanner = scanner
      expr = self._parseExpr( )

      if parseFull:
         self._scanner.expect( Token.EOF, "EOF expected." )

      return expr

   def parseSequent( self, scanner, parseFull = True ):
      """Parse a sequent from the string wrapped by the scanner.
      Category:      Mutator.
      Returns:       (Sequent) A sequent.
      Side Effects:  Advances teh scanner pointer.
      Preconditions: [ParseError] If parseFull is True, the sequent in
                        the wrapped string must be followed immediately by
                        end of the string.  If Fase, the parser only tries to
                        parse the beginning of the wrapped string.
      """
      assert isinstance( scanner,       Scanner )
      assert isinstance( parseFull,     bool    )

      assert isinstance( self._scanner, Scanner ) or ( self._scanner is None )

      self._scanner = scanner
      expr = self._parseSequent( )

      if parseFull:
         self._scanner.expect( Token.EOF, "EOF expected." )

      return expr

   def _parseExpr( self ):
      """Parse an expression.
      Category:      Mutator.
      Returns:       (WFF) The parsed expression.
      Side Effects:  Advances the scanner pointer.
      Preconditions: [ParseError] The scanner must wrap a valid string
                        representation of an expression.
      """
      assert isinstance( self._scanner, Scanner )

      term1 = self._parseTerm( )

      tok = self._scanner.peek()
      if tok == Token.INFIX_OP:
         binOp = self._scanner.peekLex( )
         self._scanner.consume( )
         term2 = self._parseTerm( )
         return StructuredWFF( binOp, term1, term2 )
      else:
         return term1

   def _parseTerm( self ):
      """Parse a term.
      Category:      Mutator.
      Returns:       (WFF) The parsed term.
      Side Effects:  Advances the scanner pointer.
      Preconditions: [ParseError] The scanner must wrap a valid string
                        representation of a term.
      """
      assert isinstance( self._scanner, Scanner )

      nextToken = self._scanner.peek( )
      if nextToken == Token.PREFIX_OP:
         operation = self._scanner.peekLex( )
         self._scanner.consume( )
         operand = self._parseTerm( )
         result = StructuredWFF( operation, operand )
      elif nextToken == Token.OPEN:
         self._scanner.consume( )
         result = self._parseExpr( )
         self._scanner.expect( Token.CLOSE, "')', ']' or '}' expected." )
      elif nextToken == Token.SYMBOL:
         symbol = self._scanner.peekLex( )
         self._scanner.consume( )
         result = AtomicWFF( symbol )
      else:
         raise ParseError( self._scanner.genErr( "Term expected." ) )

      return result

   def _parseSequent( self, isNested = False ):
      """recursive implementation for parse().
      Category:      Mutator.
      Returns:       (Sequent) The parsed Sequent object.
      Side Effects:  None.
      Preconditions: [AssertionError] aScanner must be a Scanner.
                     [ParseError] The string held in the scanner must
                        syntactically be a valid sequent.
      """
      # create an empty sequent
      assert isinstance( isNested, bool )

      assert isinstance( self._scanner, Scanner )

      if isNested:
         self._scanner.expect( Token.OPEN, "'(' expected." )

      # parse the premises
      premises = FormSet( )
      if self._scanner.peek( ) != Token.ENTAILS:
         premises.append( self._parsePremise( ) )
         while self._scanner.peek( ) == Token.COMMA:
            self._scanner.consume( )
            premises.append( self._parsePremise( ) )

      # Parse the turnstile '|-'
      self._scanner.expect( Token.ENTAILS, "'|-' expected." )

      # Parse the conclusions
      conclusions = FormSet( )
      conclusions.append( self.parseProposition( self._scanner, False ) )

      while self._scanner.peek( ) == Token.COMMA:
         self._scanner.consume( )
         conclusions.append( self.parseProposition( self._scanner, False ) )

      seq = Sequent( premises, conclusions )

      if isNested:
         self._scanner.expect( Token.CLOSE, "')' expected." )

      return seq

   def _parsePremise( self ):
      """Parse a single premise.
      Category:      Mutator.
      Returns:       (WFF or Sequent) wff or sequent.
      Side Effects:  Advances the scanner position past the parsed item.
      Preconditions: A scanner must have been selected which wraps a string.
                     [ParseError] The scanner string does not contain a valid
                        wff or sequent.
      Implementation Notes:
         Determining if a premise is a wff or sequent is ambiguous for LL(1)
         parsing.  For this reason, we start parsing a proposition by saving
         the current scanner position.  Then attempt to parse a proposition.
         If the premise is in fact not a proposition an exception will be
         raised.  If so, we restore the saved scanner position and try to
         parse a sequent.
      """
      assert isinstance( self._scanner, Scanner )

      pos = self._scanner.scanPos( )

      try:
         return self.parseProposition( self._scanner, False )
      except:
         self._scanner.rescan( pos )
         return self._parseSequent( True )
