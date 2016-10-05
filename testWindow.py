from tkinter.tix import *
from GUITools import *


from StructuredString import *


class SubwffSelector( Frame ):
   def __init__( self, master, mappedStr, **options ):
      assert isinstance( mappedStr, StructuredString )

      Frame.__init__( self, master, options )

      self._wffMap   = mappedStr
      self._sel      = None

      w = len(mappedStr)-1

      self._textWidget = Text( master, exportselection=0, height=1, width=w, font=( "Lucida Sans Unicode", 15, 'bold' ) )
      self._textWidget.pack( expand=1, fill=BOTH )
      self._textWidget.insert( '1.0', str(mappedStr) )

      for rgnName, rgnInfo in self._wffMap.regions( ).items( ):
         rgnSlc = rgnInfo.regionIndecies( )
         self._textWidget.tag_add( rgnName, '1.%d' % rgnSlc[0], '1.%d' % rgnSlc[1] )

      self._textWidget.bind( '<ButtonRelease-1>', self.onClick )
      self._textWidget.configure( state=DISABLED )

   def onClick( self, event ):
      if self._sel:
         self._textWidget.tag_config( self._sel[0],   background='White' )
         self._sel = None

      for key,rgnInfo in self._wffMap.regions( ).items( ):
         #rgnSlc, domSlc, clientData = val
         domSlc = rgnInfo.dominantIndecies( )
         if self._textWidget.compare( ('@%d,%d' % (event.x, event.y)), '==', '1.%d' % domSlc[0] ):
            self._textWidget.tag_raise( key )
            self._textWidget.tag_config( key, background='Gray' )

            self._sel = ( key, rgnInfo )
            break

   def getSelectionInfo( self ):
      return self._sel


class SubWFFSelectorDialog( BasicDialog ):
   def __init__( self, master, wff ):
      #assert isinstance( wff,   WFF )

      self._wff    = wff
      self._selW   = None

      BasicDialog.__init__( self, master )

   def body( self, master ):
      #assert isinstance( self._wff,    WFF )

      self._selW = SubwffSelector( master, self._wff )

      self._selW.pack( )

   def getSelection( self ):
      #assert isinstance( self._wff,    WFF )

      return self._selW.getSelectionClientData( )


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


#val = u'\u00ACA \u2227 B'

#map = [
      ## name, keySymIdx, region slice, clientData
      #( '^',  3,         (0,6),        []    ),         # Click & Mark region for operator ^
      #( '-',  0,         (0,2),        [1]   ),         # Click & Mark region for operator -
      #( 'A',  1,         (1,2),        [1,1] ),         # Click & Mark region for symbol   A
      #( 'B',  5,         (5,6),        [2]   )          # Click & Mark region for symbol   B
      #]



root = Tk( )

#mainFrame = SubwffSelector( root, ms )

#mainFrame.pack( )

D = SubWFFSelectorDialog( root, ss )

root.mainloop( )
