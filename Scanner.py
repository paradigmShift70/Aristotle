class ScannerBuffer( object ):
   """A buffer specifically designed for use by a lexical analizer."""
   # Standard Methods
   def __init__( self ):
      """Initialize the scanner buffer.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Initializes the instance.
      Preconditions: None.
      """
      self._source  = ''
      self._point   = 0
      self._mark    = 0
      self._lineNum = 0
      self._linePos = 0

      self.rescan( )

   # Extension
   def rescan( self, aPos = 0, aString=None ):
      """Reset the scanner to begin scanning from the beginning.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Initialzes the instance.
      Preconditions: [AssertionError] if aPos is supplied, it must be an int.
      """
      assert isinstance( aPos,          int )
      assert isinstance( aString,       str ) or ( aString is None )

      assert isinstance( self._source,  str )
      assert isinstance( self._point,   int )
      assert isinstance( self._mark,    int )
      assert isinstance( self._lineNum, int )
      assert isinstance( self._linePos, int )

      if aString is not None:
         self._source = aString

      self._point    = aPos       # Current scan pos
      self._mark     = 0          # Index of current lexeme in aScource
      self._lineNum  = 0          # The current line in aSource
      self._linePos  = 0          # Index of current line in aSource

   def more( self ):
      """Returns true if there are any more characters to be scanned.
      Category:      Predicate.
      Returns:       Nothing.
      Side Effects:  None.
      Preconditions: [AssertionError] The instance must wrap a string.
      """
      assert isinstance( self._source,  str )
      assert isinstance( self._point,   int )
      assert isinstance( self._mark,    int )
      assert isinstance( self._lineNum, int )
      assert isinstance( self._linePos, int )

      return self._point < len( self._source )

   def peek( self ):
      """Return the next character.
      Category:      Pure Function.
      Returns;       (string) The current character pointed to by the scan pos.
      Side Effects:  None.
      Preconditions: [AssertionError] The instance must wrap a string.
      """
      assert isinstance( self._source,  str )
      assert isinstance( self._point,   int )
      assert isinstance( self._mark,    int )
      assert isinstance( self._lineNum, int )
      assert isinstance( self._linePos, int )

      if not self.more( ):
         return None
      return self._source[ self._point ]

   def consume( self ):
      """Scan past the next character.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Advance the scanner pos.
      Preconditions: [AssertionError] The instance must wrap a string.
      """
      assert isinstance( self._source,  str )
      assert isinstance( self._point,   int )
      assert isinstance( self._mark,    int )
      assert isinstance( self._lineNum, int )
      assert isinstance( self._linePos, int )

      if not self.more( ):
         return None
      if self._source[ self._point ] == '\n':
         self._lineNum += 1
         self._linePos = self._point + 1
      self._point += 1

   def consumeIf( self, aCharSet ):
      """Consume the next character if it\'s in aCharSet.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Advances the scan pos.
      Preconditions: [AssertionError] The instance must wrap a string.
      """
      assert isinstance( aCharSet,      str )

      assert isinstance( self._source,  str )
      assert isinstance( self._point,   int )
      assert isinstance( self._mark,    int )
      assert isinstance( self._lineNum, int )
      assert isinstance( self._linePos, int )

      if self.more() and (self.peek() in aCharSet):
         self.consume( )

   def consumePast( self, aCharSet ):
      """Scan up to the first character not in aCharSet.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Advances the scan pos.
      Preconditions: [AssertionError] The instance must wrap a string.
      """
      assert isinstance( self._source,  str )
      assert isinstance( self._point,   int )
      assert isinstance( self._mark,    int )
      assert isinstance( self._lineNum, int )
      assert isinstance( self._linePos, int )

      while self.more() and (self.peek( ) in aCharSet):
          self.consume( )

   def consumeUpTo( self, aCharSet ):
      """Scan up to the first character in aCharSet.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Advances the scan pos.
      Preconditions: [TypeError] The instance must wrap a string.
      """
      assert isinstance( aCharSet,      str )

      assert isinstance( self._source,  str )
      assert isinstance( self._point,   int )
      assert isinstance( self._mark,    int )
      assert isinstance( self._lineNum, int )
      assert isinstance( self._linePos, int )

      while self.more and (self.peek( ) not in aCharSet):
         self.consume( )

   def setMark( self ):
      """Mark the current scan pos as the beginning of a token.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Marks the current scan position.
      Preconditions: [AssertionError] The instance must wrap a string.
      """
      assert isinstance( self._source,  str )
      assert isinstance( self._point,   int )
      assert isinstance( self._mark,    int )
      assert isinstance( self._lineNum, int )
      assert isinstance( self._linePos, int )

      self._mark = self._point

   def getLex( self, aPos = None ):
      """Returns a substring starting from either the mark position or aPos
      up to the current scan pos.
      Category:      Pure Function.
      Returns:       (string) A substring of the wrapped string.
      Side Effects:  None.
      Preconditions: [TypeError] The instance must wrap a string.
                     [AssertionError] If supplied, aPos it must be a
                        positive integer, less than the current scan pos.
      """
      assert isinstance( aPos,          int ) or ( aPos is None )

      assert isinstance( self._source,  str )
      assert isinstance( self._point,   int )
      assert isinstance( self._mark,    int )
      assert isinstance( self._lineNum, int )
      assert isinstance( self._linePos, int )

      if aPos is None:
         return self._source[ self._mark : self._point ]
      else:
         assert isinstance( aPos, int ) and (aPos >= 0) and (aPos < self._point)
         return self._source[ aPos, self._point ]

   def scanPos( self, aPos = None ):
      """Get/Set the current scan pos.
      Cateogry:      Mutator.
      Returns:       (int) The scan pos before this call was made.
      Side Effects:  None.
      Preconditions: [AssertionError] The instance must wrap a string.
                     [AssertionError] If supplied, aPos must be a positive
                        integer, less than the length of the wrapped string.
      """
      assert isinstance( aPos,          int ) or ( aPos is None )

      assert isinstance( self._source,  str )
      assert isinstance( self._point,   int )
      assert isinstance( self._mark,    int )
      assert isinstance( self._lineNum, int )
      assert isinstance( self._linePos, int )

      theOldPos = self._point
      if aPos is not None:
         assert isinstance( aPos, int ) and ( aPos >= 0 ) and ( aPos < len(self._source) )
         self._point = aPos
      return self._point

   def scanLineNum( self ):
      """Return the current line number within the scan string
      (first line is 0).
      Category:      Pure Function.
      Returns:       (int) The current scan line number.
      Side Effects:  None.
      Preconditions: [AssertionError] The instance must wrap a string.
      """
      assert isinstance( self._source,  str )
      assert isinstance( self._point,   int )
      assert isinstance( self._mark,    int )
      assert isinstance( self._lineNum, int )
      assert isinstance( self._linePos, int )

      return self._lineNum

   def scanColNum( self ):
      """Return the current scan column
      (first column is 0).
      Category:      Pure Function.
      Returns:       (int) The current scan column.
      Side Effects:  None.
      Preconditions: [AssertionError] The instance must wrap a string.
      """
      assert isinstance( self._source,  str )
      assert isinstance( self._point,   int )
      assert isinstance( self._mark,    int )
      assert isinstance( self._lineNum, int )
      assert isinstance( self._linePos, int )

      return self._point - self._linePos

   def scanLineTxt( self ):
      """Return the text of the current scan line.
      Category:      Pure Function.
      Returns:       (string) The current scan text line.
      Side Effects:  None.
      Preconditions: [AssertionError] The instance must wrap a string.
      """
      assert isinstance( self._source,  str )
      assert isinstance( self._point,   int )
      assert isinstance( self._mark,    int )
      assert isinstance( self._lineNum, int )
      assert isinstance( self._linePos, int )

      fromIdx = self._linePos
      toIdx   = self._source.find( '\n', fromIdx )
      if toIdx == -1:
         toIdx = len( self._source )
      return self._source[ fromIdx : toIdx ]


class Scanner( object ):
   """Scanner interface."""
   # Standard Methods
   def __init__( self ):
      """Initialize a Scanner instance.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Initilize the instance.
      Preconditions: None.
      """
      self._tok         = -1                 # The next token
      self._buffer      = ScannerBuffer( )

      self._tokPos      = 0                  # The scanPos of self.tok
      self._tokLineNum  = 0                  # The lineNum of self.tok
      self._tokColNum   = 0                  # The column of self.tok
      self._tokLineText = ''                 # The text for line: lineNum

   # Extension
   def peek( self ):
      """Peek at the next token, but do not consume it.
      Category:      Pure Function.
      Returns:       (Token) The next token in the scan stream.
      Side Effects:  None.
      Preconditions: [AssertionError] The underlying buffer must wrap a string.
      """
      assert isinstance( self._tok,         int           )
      assert isinstance( self._buffer,      ScannerBuffer )
      assert isinstance( self._tokPos,      int           )
      assert isinstance( self._tokLineNum,  int           )
      assert isinstance( self._tokColNum,   int           )
      assert isinstance( self._tokLineText, str           )

      return self._tok

   def peekLex( self ):
      return self._buffer.getLex()

   def consume( self ):
      """Consume the next token from the input stream.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Remove the next token from the input stream.  Scan the
                     input stream for the new next token.
      Preconditions: None.
      """
      assert isinstance( self._tok,         int           )
      assert isinstance( self._buffer,      ScannerBuffer )
      assert isinstance( self._tokPos,      int           )
      assert isinstance( self._tokLineNum,  int           )
      assert isinstance( self._tokColNum,   int           )
      assert isinstance( self._tokLineText, str           )

      self._tokPos       = self._buffer.scanPos( )
      self._tokLineNum   = self._buffer.scanLineNum( )
      self._tokColNum    = self._buffer.scanColNum( )
      self._tokLineText  = self._buffer.scanLineTxt( )
      self._consume( )

   def rescan( self, aPos = 0, aString=None ):
      """Move the scan pos to aPos.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Sets the scan pos to aPos.
      Preconditions: [AssertionError] aPos must be an integer.
      """
      assert isinstance( aPos,              int           )
      assert isinstance( aString,           str           ) or ( aString is None )

      assert isinstance( self._tok,         int           )
      assert isinstance( self._buffer,      ScannerBuffer )
      assert isinstance( self._tokPos,      int           )
      assert isinstance( self._tokLineNum,  int           )
      assert isinstance( self._tokColNum,   int           )
      assert isinstance( self._tokLineText, str           )

      self._buffer.rescan( aPos, aString )
      self.consume( )

   def scanPos( self ):
      """Returns the current scan position within the source string.
      Category:      Pure Function.
      Returns:       (int) The current scan pos.
      Side Effects:  None.
      Preconditions: [AssertionError] The underlying buffer must wrap a string.
      """
      assert isinstance( self._tok,         int           )
      assert isinstance( self._buffer,      ScannerBuffer )
      assert isinstance( self._tokPos,      int           )
      assert isinstance( self._tokLineNum,  int           )
      assert isinstance( self._tokColNum,   int           )
      assert isinstance( self._tokLineText, str           )

      return self._tokPos

   def scanLineNum( self ):
      """Returns the current scan line number within the source string
      (first line is 0).
      Category:      Pure Function.
      Returns:       (int) The current scan line number.
      Side Effects:  None.
      Preconditions: [AssertionError] The underlying buffer must wrap a string.
      """
      assert isinstance( self._tok,         int           )
      assert isinstance( self._buffer,      ScannerBuffer )
      assert isinstance( self._tokPos,      int           )
      assert isinstance( self._tokLineNum,  int           )
      assert isinstance( self._tokColNum,   int           )
      assert isinstance( self._tokLineText, str           )

      return self._tokLineNum

   def scanColNum( self ):
      """Returns the current scan column within the source string
      (first column is 0).
      Category:      Pure Function.
      Returns:       (int) The current scan column number.
      Side Effects:  None.
      Preconditions: [AssertionError] The underlying buffer must wrap a string.
      """
      assert isinstance( self._tok,         int           )
      assert isinstance( self._buffer,      ScannerBuffer )
      assert isinstance( self._tokPos,      int           )
      assert isinstance( self._tokLineNum,  int           )
      assert isinstance( self._tokColNum,   int           )
      assert isinstance( self._tokLineText, str           )

      return self._tokColNum

   def scanLineText( self ):
      """Returns the text line of the source string currently being scanned.
      Category:      Pure Function.
      Returns:       (int) The text of the current scan line.
      Side Effects:  None.
      Preconditions: [AssertionError] The underlying buffer must wrap a string.
      """
      assert isinstance( self._tok,         int           )
      assert isinstance( self._buffer,      ScannerBuffer )
      assert isinstance( self._tokPos,      int           )
      assert isinstance( self._tokLineNum,  int           )
      assert isinstance( self._tokColNum,   int           )
      assert isinstance( self._tokLineText, str           )

      return self._tokLineText

   # Extension:  Error generation
   def genErr( self, errorText ):
      """Generate an error string.
      Category:      Pure Function.
      Returns:       (str) A detailed textual representation of the error.
      Side Effects:  None.
      Preconditions: [AssertionError] The underlying buffer must wrap a string.
      """
      assert isinstance( errorText,         str           )

      assert isinstance( self._tok,         int           )
      assert isinstance( self._buffer,      ScannerBuffer )
      assert isinstance( self._tokPos,      int           )
      assert isinstance( self._tokLineNum,  int           )
      assert isinstance( self._tokColNum,   int           )
      assert isinstance( self._tokLineText, str           )

      lineNum = self.scanLineNum( )      # raises:  AssertionError
      colNum  = self.scanColNum( )       # raises:  AssertionError
      return 'Error (%i,%i): %s\n%s\n%s^' % (
                 lineNum + 1, colNum + 1, errorText,
                 self.scanLineText( ),   # raises:  AssertionError
                 ' ' * colNum )

   def _consume( self ):
      """Consume the next token (i.e. scan past it).
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Scans the next token from the source string and
                        assigns it to self.tok.
      Preconditions: The scanner must hold a Scanner buffer which wraps
                        a string.
      """
      assert isinstance( self._tok,         int           )
      assert isinstance( self._buffer,      ScannerBuffer )
      assert isinstance( self._tokPos,      int           )
      assert isinstance( self._tokLineNum,  int           )
      assert isinstance( self._tokColNum,   int           )
      assert isinstance( self._tokLineText, str           )

      self._tok = self._scanNextToken( )

   # Contract
   def _scanNextToken( self ):
      """Consume the next token (i.e. scan past it).
      Category:      Mutator.
      Returns:       Token.
      Side Effects:  Scans the next token from the source string.
      Preconditions: The scanner must hold a Scanner buffer which wraps
                        a string.
      """
      assert isinstance( self._tok,         int           )
      assert isinstance( self._buffer,      ScannerBuffer )
      assert isinstance( self._tokPos,      int           )
      assert isinstance( self._tokLineNum,  int           )
      assert isinstance( self._tokColNum,   int           )
      assert isinstance( self._tokLineText, str           )

      raise NotImplementedError( )



class ParseError( Exception ):
   """Exception class for reporting errors in parsing."""
   pass
