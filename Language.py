import Form
from FormParser  import WFFScanner, WFFParser


class Lexeme( object ):
   # Syntax
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

   def __init__( self, name, symbol, syntax, translation ):
      """Initialize an instance of this class.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Initilize the instance.
      Preconditions: None.
      """
      assert isinstance( name,        str   )
      assert isinstance( symbol,      list  )
      assert isinstance( syntax,      str   )
      assert isinstance( translation, list  )

      if syntax == 'PREFIX OP':
         syntax = Lexeme.PREFIX_OP
      elif syntax == 'POSTFIX OP':
         syntax = Lexeme.POSTFIX_OP
      elif syntax == 'INFIX OP':
         syntax = Lexeme.INFIX_OP
      elif syntax == 'ENTAILS':
         syntax = Lexeme.ENTAILS
      else:
         raise Exception( 'Lexeme definition error:  Unknown syntax specification.' )

      self.name    = name
      self.symbol  = symbol
      self.syntax  = syntax
      self.token   = syntax
      self.trans   = translation


class Language( object ):
   """Implementation of Language."""
   def __init__( self, lexemes, equivalenceOperatorList ):
      assert isinstance( lexemes,                 list )
      assert isinstance( equivalenceOperatorList, list )

      self._lexList   = [ ]

      for lex in lexemes:
         self._lexList.append( Lexeme( *lex ) )

      # Setup Parsing
      self._scanner    = WFFScanner( self._lexList )
      self._parser     = WFFParser( )
      self._equivOpLst = equivalenceOperatorList

   def parseProp( self, aPropStr ):
      """Parse a wff string.
      Category:       Pure Function.
      Returns:        WFF.
      Side Effects:   None.
      Preconditions:  [AssertionError] 'aPropStr' must be a string representation of a WFF.
      """
      assert isinstance( aPropStr,         str        )

      assert isinstance( self._scanner,    WFFScanner )
      assert isinstance( self._parser,     WFFParser  )
      assert isinstance( self._equivOpLst, list       )

      self._scanner.rescan( aString=aPropStr )
      return self._parser.parseProposition( self._scanner )

   def parseSeq( self, aSeqStr ):
      """Parse a sequent string.
      Category:       Pure Function.
      Returns:        Sequent.
      Side Effects:   None.
      Preconditions:  [AssertionError] 'aSeqStr' must be a string representation of a sequent.
      """
      assert isinstance( aSeqStr,          str        )

      assert isinstance( self._scanner,    WFFScanner )
      assert isinstance( self._parser,     WFFParser  )
      assert isinstance( self._equivOpLst, list       )

      self._scanner.rescan( aString=aSeqStr )
      return self._parser.parseSequent( self._scanner )

   def equivalenceOperatorList( self ):
      """Returns the list of equivalence operators.
      Category:       Pure Function.
      Returns:        (list) of equivalence operators.
      Side Effects:   None.
      Preconditions:  None.
      """
      assert isinstance( self._scanner,    WFFScanner )
      assert isinstance( self._parser,     WFFParser  )
      assert isinstance( self._equivOpLst, list       )

      return self._equivOpLst

   def isEquivalenceTheorem( self, aSequent ):
      """Is the sequent represent an equivalence theorem?
      Category:      Predicate.
      Returns:       (bool) True if the sequent is an equivalence theorem.
      Side Effects:  None.
      Preconditions: None.
      """
      if len(aSequent.premiseFormSet()) > 0:
         return False

      if len(aSequent.conclusionFormSet()) != 1:
         return False

      theConclusionForm = aSequent.conclusionFormSet()[0]
      return (theConclusionForm.primary() in self._equivOpLst) and (len(theConclusionForm.subordinates()) == 2)


