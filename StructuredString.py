"""Utility methods for built-in classes."""
import copy


class InvalidRegionException( Exception ):
   pass


# TODO: Restructure StructuredString as follows:
#
# Additional Enhancement
#    - Add subordinate list to the the StructuredStringRegion object.  It would
#      contain a list of references to the StructuredStringRegion objects that
#      represent each of the subordinates.

class StructuredStringRegion( object ):
   def __init__( self, completeString, domIndecies, regIndecies, clientData=None ):
      assert isinstance( completeString, str  )
      assert isinstance( domIndecies,    list )
      assert isinstance( regIndecies,    list )

      # The parameters are reasonable
      self._completeString   = completeString
      self._dominantIndecies = domIndecies
      self._regionIndecies   = regIndecies
      self._clientData       = clientData

   def dominantIndecies( self ):
      return self._dominantIndecies

   def dominantSubstring( self ):
      begin, end = self._dominantIndecies
      return self._completeString[ begin : end ]

   def regionIndecies( self ):
      return self._regionIndecies

   def regionSubstring( self ):
      begin, end = self._regionIndecies
      return self._completeString[ begin : end ]

   def getClientData( self ):
      return self._clientData

   def setClientData( self, value ):
      self._clientData = value

   def validate( self, theCompleteString ):
      # reasonability checks on the region
      if (self._primaryString is None) or (len(self._primaryString) == 0):
         raise InvalidRegionException()

      maxIndex = len(theCompleteString) + 1

      if len(self._dominantIndecies) != 2:
         raise InvalidRegionException()
      if not ( 0 <= self._dominantIndecies[0] <= maxIndex ):
         raise InvalidRegionException()
      if not ( 0 <= self._dominantIndecies[1] <= maxIndex ):
         raise InvalidRegionException()
      if self._dominantIndecies[0] > self._dominantIndecies[1]:
         raise InvalidRegionException()

      if len(self._regionIndecies) != 2:
         raise InvalidRegionException()
      if not ( 0 <= self._regionIndecies[0] <= maxIndex ):
         raise InvalidRegionException()
      if not ( 0 <= self._regionIndecies[1] <= maxIndex ):
         raise InvalidRegionException()
      if self._regionIndecies[0] > self._regionIndecies[1]:
         raise InvalidRegionException()


class StructuredString( object ):
   '''Immutable.
   A string object which has structure such as any string which conforms
   to a grammar and connective relationship among its elements such that they
   can be organized into a syntax tree.  A StructuredString instance provides
   means of working with structured string objects.

   It's implemented as a string and corresponding list of the same length.
   Each index position in the string has a corresponding set of data at the
   same index position in the list.

   Each entry in the list
   It contains
   a list of dominant substrings and their subordinates.

   Internal dict object has the following organization:
   #   #index           Dominant           Region            Client Data
   #   <index>  :  [  [ dFirst, dLast ], [ sFirst, sLast ], <client>    ]

   index is a character index in the string.  In practice for a given entry
   index should be within the interval expressed by Dominant.  There should be
   one entry for each position within the Dominant.

   Dominant is the index of the first and last characters of the dominant.

   Region is the index of the first and last characters of the complete
   substring (dominanant and all subordinates) reigned over by the dominant.

   Name is some unique name chosen for the dominant.

   Client Data is some additional data to associate with the dominant.  This
   is most likely some sort of reference back to the node in the syntax tree.
   '''
   def __init__( self, aMappedString, aNamedRegionMap, aRegionDefList ):
      """Initialize a new instance of this class.
      Category:      Mutator
      Returns:       Nothing.
      Side Effects:  None.
      Preconditions: None.
      """
      assert isinstance( aMappedString,     str  )
      assert isinstance( aNamedRegionMap,   dict )
      assert isinstance( aRegionDefList,    list )

      self._completeString     = aMappedString
      self._namedRegions       = aNamedRegionMap
      self._regionDefList      = aRegionDefList

   def __str__( self ):
      """Implementation of function str( )."""
      assert isinstance( self._completeString, str  )
      assert isinstance( self._namedRegions,   dict )
      assert isinstance( self._regionDefList,  list )

      return self._completeString

   def __repr__( self ):
      """Implementation of function repr( )."""
      assert isinstance( self._completeString, str  )
      assert isinstance( self._namedRegions,   dict )
      assert isinstance( self._regionDefList,  list )

      return self._completeString

   def __len__( self ):
      """Implement the len() function."""
      assert isinstance( self._completeString, str  )
      assert isinstance( self._namedRegions,   dict )
      assert isinstance( self._regionDefList,  list )

      return len(self._completeString)

   def regionInfo( self, index ):
      assert isinstance( index,               int  )

      assert isinstance( self._completeString, str  )
      assert isinstance( self._namedRegions,   dict )
      assert isinstance( self._regionDefList,  list )

      return self._regionDefList[ index ]

   def regions( self ):
      assert isinstance( self._completeString, str  )
      assert isinstance( self._namedRegions,   dict )
      assert isinstance( self._regionDefList,  list )

      return self._namedRegions

   def iterIndexInfoList( self ):
      assert isinstance( self._completeString, str  )
      assert isinstance( self._namedRegions,   dict )
      assert isinstance( self._regionDefList,  list )

      return iter( self._regionDefList )


class StructuredStringBuilder( object ):
   def __init__( self ):
      # What we're constructing
      self._str          = ''

      # Things to assist in the construction
      self._nextName     = 0
      self._map          = { }     # map of id : <index into self._position>

      self._initialize( )

   def _initialize( self ):
      assert isinstance( self._str,      str  )
      assert isinstance( self._nextName, int  )
      assert isinstance( self._map,      dict )

      self._str          = ''
      self._map          = { }

   def beginRegion( self, name=None ):
      """Mark the beginning of a region.
      Category:      Mutator.
      Returns:       (str) The name used to mark the region.
      Side Effects:  Update the map with information on a new region.
      Preconditions: [AssertionError] name must be a string (the name of the region) or None.
                        If None, a name is generated sequentially.
      """
      assert isinstance( name,           str  ) or ( name is None )

      assert isinstance( self._str,      str  )
      assert isinstance( self._nextName, int  )
      assert isinstance( self._map,      dict )

      theCurrentPos = len(self._str)

      if name is None:
         name = str( self._nextName )
         self._nextName += 1

      self._map[ name ] = StructuredStringRegion( '', [ -1, -1 ], [ theCurrentPos, -1 ] )

      return name

   def endRegion( self, name ):
      """Mark the terminating point of the named region.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Modify the map to include the retions's temination information.
      Preconditions: [AssertionError] name must be a str.
      """
      assert isinstance( name,           str  )

      assert isinstance( self._str,      str  )
      assert isinstance( self._nextName, int  )
      assert isinstance( self._map,      dict )

      theCurrentPos = len(self._str)

      self._map[ name ].regionIndecies( )[ 1 ] = theCurrentPos

   def beginDominantMember( self, name ):
      """Mark the beginning of a region's dominant member.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Updates the map.
      Preconditions: [AssertionError] name must be a string (the name of the region).
      """
      assert isinstance( name,           str  )

      assert isinstance( self._str,      str  )
      assert isinstance( self._map,      dict )
      assert isinstance( self._nextName, int  )

      theCurrentPos = len(self._str)

      self._map[ name ].dominantIndecies( )[ 0 ] = theCurrentPos

   def endDominantMember( self, name ):
      """Mark the terminating point of the named region's dominant member.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Modify the map.
      Preconditions: [AssertionError] name must be a str.
      """
      assert isinstance( name,           str  )

      assert isinstance( self._str,      str  )
      assert isinstance( self._map,      dict )
      assert isinstance( self._nextName, int  )

      currentPos = len(self._str)

      entry = self._map[ name ]
      entry.dominantIndecies( )[1] = currentPos
      entry._primaryString = self._str[ entry.dominantIndecies( )[0] : ]

   def append( self, val ):
      """Append text to the end of the string being built & mapped.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Modify the string.
      Preconditions: [AssertionError] string must be an str.
      """
      assert isinstance( val,            str  )

      assert isinstance( self._str,      str  )
      assert isinstance( self._map,      dict )
      assert isinstance( self._nextName, int  )

      self._str += val

   def appendDominant( self, name, val ):
      """Append text to the end of the string being built & mapped, mark this the dominant member of the region named by 'name'.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Modify the string.
      Preconditions: [AssertionError] string must be an str.
      """
      assert isinstance( name,           str  )
      assert isinstance( val,            str  )

      assert isinstance( self._str,      str  )
      assert isinstance( self._map,      dict )
      assert isinstance( self._nextName, int  )

      self.beginDominantMember( name )
      self.append( val )
      self.endDominantMember( name )

   def setClientData( self, name, clientData ):
      """Sets the client data for a named region.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Modifies the map.
      Preconditions: [AssertionError] name must be an str.
      """
      assert isinstance( name,           str  )

      assert isinstance( self._str,      str  )
      assert isinstance( self._map,      dict )
      assert isinstance( self._nextName, int  )

      self._map[ name ].setClientData( clientData )

   def peekString( self ):
      """Returns the string constructed so far.
      Category:      View.
      Returns:       str.  Reference to the constructed string.
      Side Effects:  None.
      Preconditions: [AssertionError] name must be an str.
      """
      assert isinstance( self._str,      str  )
      assert isinstance( self._map,      dict )
      assert isinstance( self._nextName, int  )

      return self._str

   def diag( self ):
      for name, rgn in self._map.items():
         primaryStr     = rgn._primaryString
         domIndecies    = rgn._dominantIndecies
         regionIndecies = rgn._regionIndecies
         clientData     = rgn._clientData
         print( '''{0:5} : DOM: {1:10} /{2:5}/  -- RGN {3:10} /{4}/'''.format( name, domIndecies, primaryStr, regionIndecies, clientData ) )

   def structuredString( self ):
      """Return the structured string and clear the StructuredStringBuilder.
      Category:      Mutator.
      Returns:       (StructuredString) a structured string instance contained in this builder.
      Side Effects:  Update the map with information on a new region.
      Preconditions: [Exception] The builder must be in a valid construction state...
                     e.g. all 'begins' must have corresponding ends, etc.
      """
      # Validate the underlying data.
      for name,regionDef in self._map.items():
         regionDef.validate( self._str )

      # Create the region info list to be parallel to the string
      theCompleteString = self._str
      theIndexMap       = self._map
      theIndexInfoList  = [ None for x in range(len(self._str)) ]

      for name, regionDef in self._map.items():
         dominantFirstIndex, dominantLastIndex = regionDef.dominantIndecies( )
         for dominantIndex in range( dominantFirstIndex, dominantLastIndex ):
            if theIndexInfoList[ dominantIndex ] is not None:    # Insure that no dominants overlap
               raise InvalidRegionException( 'Dominants may not overlap.' )

            theIndexInfoList[ dominantIndex ] = regionDef

      structuredString = StructuredString( self._str, self._map, theIndexInfoList )

      self._initialize( )

      return structuredString


if __name__ == "__main__":
   # Construct a structured string for "-A ^ B"
   ms = StructuredStringBuilder( )

   # Construct by depth-first traversal of the syntax tree
   ms.beginRegion( '^' )               # enter root node '^',  beginRegion
   ms.beginRegion( '-' )               # enter node '-',       beginRegion
   ms.appendDominant( '-', '-' )       # node '-' is prefix,   append substring
   ms.beginRegion( 'A' )               # enter node 'A',       beginRegion
   ms.appendDominant( 'A', 'A' )       # node is leaf,         append substring
   ms.endRegion( 'A' )                 # leave node 'A',       endRegion
   ms.endRegion( '-' )                 # leave node '-'        endRegion
   ms.append( ' ' )                    # add spacing to the internal string
   ms.appendDominant( '^', '^' )       # continue root node '^' as infix, append substring
   ms.append( ' ' )                    # add spacing to the internal string
   ms.beginRegion( 'B' )               # enter node 'B',       beginRegion
   ms.appendDominant( 'B', 'B' )       # node is leaf,         append substring
   ms.endRegion( 'B' )                 #
   ms.endRegion( '^' )

   ss = StructuredString( ms )
   print( 'Done!' )

   #val = u'\u00ACA \u2227 B'

   #map = [
         ## name, keySymIdx, region slice, clientData
         #( '^',  3,         (0,6),        []    ),         # Click & Mark region for operator ^
         #( '-',  0,         (0,2),        [1]   ),         # Click & Mark region for operator -
         #( 'A',  1,         (1,2),        [1,1] ),         # Click & Mark region for symbol   A
         #( 'B',  5,         (5,6),        [2]   )          # Click & Mark region for symbol   B
         #]
