# Aristotle

# Roadmap
# =======

# PC: Pr (Proof of Concept: Propositional Logic)
#
# - Figure out some way to implement inferences from equivalences (and definitions).
# - Implement Calculus classes.
# - Combine Proof and ProofBuilder classes -OR- combine ProofBuilder and Calculus classes.
# - Fill in isinstance assertions from base casses into derived classes
# - Add a 'Save As Rule' button to the Gui to save proofs as new inference rules.
# - Implement a feature to save work to a file, and reload work.
# - Provide more interaction between the proof and the sequent
#      - click a button to begin proving the sequent form by beginning a new proof and automatically adding the premise as the first steps.
#      - Have something happen when the GUI recognizes that the sequent has been successfully proven.
# - Add a way for user to specify semantics of logics (truth valuations, etc.)
# - The scanner is not currently truely customizable.  Redesign it so that it is.  Probably have to discern symbols by spaces, parens, commas, etc.
# - Need a way to define truth-functional semantics in the language definition.
# - Need to get GUI to display the unicode character rep for wffs.

# PC: Pd (Proof of Concept: Predicate Logic)
#
# - Predicate Logic
#      - Parse predicate WFFs
#      - Parse predicate sequents
#      - Get proof to recognize active object symbols

# PC: QL (Proof of Concept: Quantified Logic)
#
# - Quantified Logic
#      - Parse and validate quantified WFFs
#      - Parse quantified sequents with object introduction notation
#      - Get proof system to allow introduction of new (unused) object symbols.

# PC: ML (Proof of Concept: Modal Logic)
#
# - Modal Logics
#      - Parse and validate quantified WFFs
#      - Invent sequent form for describing possible world semantics
#      - Parse modal sequents for working with this new sequent notation
#      - Get proof system to allow introduction of new (unused) world prefixes.

# Proof Builder Verions 1


# Other Tools

# - Term Logic
# - Tree Builder
# - Table Builder
# - Refuation Proofs
# - Venn diagramming
# - Translation Assistant (help in building wffs)
# - Formal Definitions
# - Dictionaries
# - Mathematical Induction
# - Theory Development Tools

# - Tools for doing induction
#      - Probabilities and Probability Calculus
#      - Causal Reasoning
#      - Sample/Population Reasoning


from Proof import Proof
from Calculus import Resolver, Inference, RegularInference, EquivalenceInference
from Form import *
from Logic import Logic, Gentzen, Gensler, Fitch


from tkinter import tix, messagebox
from GUITools import *


TCL_ALL_EVENTS          = 0


class CancelOperation( Exception ):
   """Exception to cancel out of the current operation."""

# #######
# Widgets

class ProofWidget( tix.ScrolledHList ):
   INDENTATION_UNIT = '|       '

   def __init__( self, master, **ops ):
      """Initialize a new instance of the class.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Initializes an instance.
      Preconditions: [AssertionError] set must be a list or None.
      """
      tix.ScrolledHList.__init__( self, master, options='hlist.columns 4 hlist.header 1 selectMode single', **ops )

      self.proofBox = self.hlist

      self.proofBox.bind( '<ButtonRelease-1>',     self.onEntryClicked )

      # Create the title for the HList widget
      #       >> Notice that we have set the hlist.header subwidget option to true
      #      so that the header is displayed
      #boldfont=self.proofBox.tk.call('tix','option','get','boldfont')

      # Create the headers for the proof
      stepNumHeaderStyle = tix.DisplayStyle(tix.TEXT, refwindow=self.proofBox,
                              anchor=tix.CENTER, padx=8, pady=2 )#, font=boldfont )
      propHeaderStyle    = tix.DisplayStyle(tix.TEXT, refwindow=self.proofBox,
                              anchor=tix.CENTER, padx=80, pady=2)#, font=boldfont )
      reasonHeaderStyle  = tix.DisplayStyle(tix.TEXT, refwindow=self.proofBox,
                              anchor=tix.CENTER, padx=10, pady=2)#, font=boldfont )

      self.proofBox.header_create( 0, itemtype=tix.TEXT, text='',
                            style=stepNumHeaderStyle )
      self.proofBox.header_create( 1, itemtype=tix.TEXT, text='Step',
                            style=propHeaderStyle )
      self.proofBox.header_create( 2, itemtype=tix.TEXT, text='Reason',
                            style=reasonHeaderStyle )

      self.proofBox.column_width( 0, chars=8 )

      self.proofBox.column_width(3,0)

      self._selectionList = [ ]
      self._proof         = Proof( )

   def onEntryClicked( self, event ):
      idx = int(self.proofBox.nearest(event.y))

      for entry in self._selectionList:
         if isinstance( entry[0], int ) and ( entry[0] == idx+1 ):
            entry[1] = not entry[ 1 ]
         elif isinstance( entry[0], tuple ) and ( entry[0][0] <= (idx+1) <= entry[0][1] ):
            entry[1] = not entry[ 1 ]

      self.after( 5, self.drawProof )

   def wrapProof( self, proof ):
      self.proof = proof

      self._selectionList = [ ]
      selectable = self.proof.availablePremises( )
      for entry in selectable:
         self._selectionList.append( [ entry, False ] )

      self.drawProof( )

   def drawProof( self ):
      self.proofBox.delete_all( )

      numberStyle        = tix.DisplayStyle(tix.TEXT, refwindow=self.proofBox, padx=10, anchor=tix.E)
      propStyle          = tix.DisplayStyle(tix.TEXT, refwindow=self.proofBox)

      # Draw the Proof Steps
      num = None
      for num,step in enumerate(self.proof):
         s = ProofWidget.indentString(step.level, step.prop)
         self.proofBox.add( str(num), itemtype=tix.TEXT, text=str(num+1) + '.', style=numberStyle)
         self.proofBox.item_create( str(num), 1, itemtype=tix.TEXT, text=s,
                             style=propStyle )
         self.proofBox.item_create( str(num), 2, itemtype=tix.TEXT, text=step.justificationString(),
                             style=propStyle )

      # Draw the 'Ghost' next step
      ghostStyle         = tix.DisplayStyle(tix.TEXT, refwindow=self.proofBox)

      if num is None:
         num = 0
      else:
         num += 1

      s = ProofWidget.indentString(self.proof.currentLevel(), '__')
      self.proofBox.add( str(num), itemtype=tix.TEXT, text=str(num+1) + '.', style=numberStyle )
      self.proofBox.item_create( str(num), 1, itemtype=tix.TEXT, text=s,
                          style=propStyle )
      self.proofBox.item_create( str(num), 2, itemtype=tix.TEXT, text='',
                          style=propStyle )

      # Indicate the selections
      for entry in self._selectionList:
         if entry[1]:
            if isinstance( entry[0], int ):
               self.proofBox.selection_set( entry[0]-1 )
            elif isinstance( entry[0], tuple ):
               for idx in range( entry[0][0]-1, entry[0][1] ):
                  self.proofBox.selection_set( idx )

   def getSelection( self ):
      selectionList = [ ]
      for entry in self._selectionList:
         if entry[1]:
            selectionList.append( entry[0] )

      return selectionList

   @staticmethod
   def indentString( level, string ):
      assert isinstance( level,  int )

      return (ProofWidget.INDENTATION_UNIT * level) + str(string)


class InferenceRuleListWidget( tix.ScrolledHList ):
   def __init__( self, master, **ops ):
      """Initialize a new instance of the class.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Initializes an instance.
      Preconditions: [AssertionError] set must be a list or None.
      """
      tix.ScrolledHList.__init__( self, master, options='hlist.columns 4 hlist.header 1 selectMode single', **ops )
      self.ruleBox = self.hlist

      #boldfont=self.ruleBox.tk.call('tix','option','get','bold_font')

      # Create the headers for Rule List
      ruleNameHeaderStyle = tix.DisplayStyle(tix.TEXT, refwindow=self.ruleBox,
                              anchor=tix.CENTER, padx=10, pady=2 )#, font=boldfont )

      self.ruleBox.header_create( 0, itemtype=tix.TEXT, text='Rule Name',
                            style=ruleNameHeaderStyle )
      self.ruleBox.header_create( 1, itemtype=tix.TEXT, text='Abbrev',
                            style=ruleNameHeaderStyle )
      self.ruleBox.header_create( 2, itemtype=tix.TEXT, text='Sequent',
                            style=ruleNameHeaderStyle )

      self.ruleBox.column_width( 3, 0 )

   def update( self, ruleList ):
      ruleStyle        = tix.DisplayStyle(tix.TEXT, refwindow=self, padx=10, anchor=tix.W)
      for rule in ruleList:
         self.ruleBox.add( rule.name, itemtype=tix.TEXT, text=rule.name, style=ruleStyle )
         self.ruleBox.item_create( rule.name, 1, itemtype=tix.TEXT, text=rule.abbrev )
         self.ruleBox.item_create( rule.name, 2, itemtype=tix.TEXT, text=rule.sequent )


class SubwffSelectorWidget( tix.Frame ):
   def __init__( self, master, aStructuredString, **options ):
      assert isinstance( aStructuredString, StructuredString )

      Frame.__init__( self, master, options )

      self._formStruct = aStructuredString
      self._sel        = None

      w = len(self._formStruct)-1

      self._textWidget = Text( master, exportselection=0, height=1, width=w, font=( "Lucida Sans Unicode", 15, 'bold' ) )
      self._textWidget.pack( expand=1, fill=BOTH )
      self._textWidget.insert( '1.0', str(self._formStruct) )

      for rgnName, rgnInfo in self._formStruct.regions( ).items( ):
         rgnSlc = rgnInfo.regionIndecies( )
         self._textWidget.tag_add( rgnName, '1.%d' % rgnSlc[0], '1.%d' % rgnSlc[1] )

      self._textWidget.bind( '<ButtonRelease-1>', self.onClick )
      self._textWidget.configure( state=DISABLED )

   def onClick( self, event ):
      if self._sel:
         self._textWidget.tag_config( self._sel[0],   background='White' )
         self._sel = None

      for key,rgnInfo in self._formStruct.regions( ).items( ):
         #rgnSlc, domSlc, clientData = val
         domSlc = rgnInfo.dominantIndecies( )
         if self._textWidget.compare( ('@%d,%d' % (event.x, event.y)), '==', '1.%d' % domSlc[0] ):
            self._textWidget.tag_raise( key )
            self._textWidget.tag_config( key, background='Gray' )

            self._sel = ( key, rgnInfo )
            break

   def getSelectionInfo( self ):
      return self._sel



# ############
# Dialog Boxes

class FreeAtomDialog( BasicDialog ):
   def __init__( self, master, rule, unmappedSymbolList ):
      self._sequent           = rule.sequent
      self.unmappedSymbolMap  = { name:None for name in unmappedSymbolList }
      self._entries           = [ ]
      self.canceled           = True

      BasicDialog.__init__( self, master )

   def body( self, master ):
      message = """Proof Builder has determined that the conclusion
      contains atomic forms not found in any of the premises.  To
      continue with this inference provide values for these forms."""

      label1 = tix.Label( master, text=message )
      label1.grid( row=0, column=0, columnspan=2 )

      label2 = tix.Label( master, text='sequent' )
      label2.grid( row=1, column=0 )

      label3 = tix.Label( master, text=str(self._sequent), relief=tix.SUNKEN )
      label3.grid( row=1, column=1 )

      for row, pair in enumerate( self.unmappedSymbolMap ):
         label4 = tix.Label( master, text=(pair[0] + ':') )
         label4.grid( row=row+2, column=0 )

         entry = tix.Entry( master )
         entry.grid( row=row+2, column=1 )

         self._entries.append( ( pair[0], entry ) )

   def apply( self ):
      self.canceled  = False
      for name, entry in self._entries:
         self.unmappedSymbolMap[ name ] = entry.get( )


class ConclusionSelectionDialog( BasicDialog ):
   def __init__( self, master, conclusionList ):
      self._conclList = conclusionList
      self._box       = None
      self._selection = None

      BasicDialog.__init__( self, master )

   def body( self, master ):
      msg       = tix.Label( master, text="Multiple conclusion forms are possible.  Select the desired form." )
      msg.pack( side=tix.TOP )

      self._box = tix.Listbox( master, height=4, width=60, selectmode=tix.SINGLE )
      self._box.insert( tix.END, *tuple( self._conclList ) )
      self._box.pack( side=tix.TOP )

   def apply( self ):
      selSet = self._box.curselection( )
      self._selection = selSet[ 0 ]


class SubWFFSelectorDialog( BasicDialog ):
   def __init__( self, master, aStructuredString ):
      assert isinstance( aStructuredString,   StructuredString )

      self._structuredString   = aStructuredString    # the wff to display for selection of a subwff
      self._selW   = None

      BasicDialog.__init__( self, master )

   def body( self, master ):
      assert isinstance( self._structuredString,    StructuredString )

      self._selW = SubwffSelectorWidget( master, self._structuredString )

      self._selW.pack( )

   def apply( self ):
      assert isinstance( self._structuredString,    StructuredString )

      self._selection = self._selW.getSelectionInfo( )

   def getSelection( self ):
      assert isinstance( self._structuredString,    StructuredString )

      return self._selection


# ###########
# Main Window

class ProofView( object ):
   def __init__( self, w, aLogic ):
      self.logic        = aLogic
      self.currentSequent = ''
      self.currentProof = Proof( )
      self.sequentEntry = None
      self.proofBox     = None
      self.ruleBox      = None

      self.selectSet    = [ ]     # The list of items currently selected

      self.root = w
      self.exit = -1

      z = w.winfo_toplevel()
      z.wm_protocol( "WM_DELETE_WINDOW", lambda self=self: self.quit() )

      w.title( "Proof Builder" )
      top = tix.Frame( w, relief=tix.RAISED, bd=1 )

      self.sequentEntryBox( top )
      self.workAreaBox( top )
      self.buttonBox( top )

      top.pack( fill=tix.BOTH, expand=1, padx=10, pady=10 )

      self.updateProof( )

   def sequentEntryBox( self, parent ):
      seqFrame = tix.Frame( parent )

      label = tix.Label( seqFrame, text='Sequent' )
      label.grid( row=0, column=0, padx=5, pady=5 )

      self.sequentEntry = tix.Entry( seqFrame, width=100 )
      self.sequentEntry.grid( row=0, column=1, padx=5, pady=5 )

      self.proveBtn = tix.Button( seqFrame, text='Prove', command=self.onProveButton )
      self.proveBtn.grid( row=0, column=2, padx=5, pady=5 )

      seqFrame.pack( fill=tix.X, ipadx=5, padx=40, pady=15 )

   def workAreaBox( self, parent ):
      # Put a simple hierachy into the HList (two levels). Use colors and
      # separator widgets (frames) to make the list look fancy
      workPane = tix.PanedWindow( parent, orientation='horizontal' )
      proofPane = workPane.add( 'proof', min=100 )
      rulePane  = workPane.add( 'rule',  min=100 )

      self.proofWidget = ProofWidget( proofPane, width=375 )
      self.proofWidget.pack( expand=1, fill=tix.BOTH, padx=5 )

      seqLst = InferenceRuleListWidget( rulePane )
      seqLst.pack( expand=1, fill=tix.BOTH, padx=5 )

      workPane.pack( fill=tix.BOTH, expand=1 )

      self.proofBox = self.proofWidget.proofBox
      self.ruleBox = seqLst.hlist


      seqLst.update( self.logic.calculus().ruleList() )

   def buttonBox( self, parent ):
      box= tix.ButtonBox(parent, orientation=tix.HORIZONTAL )

      box.add( 'infer', text='Infer', underline=0, width=6,
               command=self.onInferButton )

      box.add( 'infer-equiv', text='Infer Equivalence', underline=0, width=15,
               command=self.onInferEquivButton )

      box.add( 'begin', text='Begin', underline=0, width=6,
               command=self.onBeginButton )

      box.add( 'end', text='End', underline=0, width=6,
               command=self.onEndButton )

      box.add( 'del', text='<<', underline=0, width=6,
               command=self.deleteStep )

      box.add( 'close',  text='Close', underline=0,  width=6,
               command=self.quit )

      self.infer = box.infer

      box.pack( fill=tix.X )

   def onProveButton( self ):
      # Get the sequent typed by the user
      seqStr = self.sequentEntry.get( )
      self.currentSequent = self.logic.language().parseSeq( seqStr )

      # Get the inference rule for asserting premises into a proof
      rule = self.logic.calculus().premiseAssertionRule()
      
      # Determine the symbol used by the assertion rule for a premise
      assertionVar  = rule.sequent.conclusionAdditions( )[ 0 ]

      # Create a new proof
      self.currentProof = Proof( )

      # Insert each premise from the sequent into the proof as a premise
      for premise in self.currentSequent.premiseFormSet():
         premiseCitationList = [ ]
         premiseSet          = FormSet( )
         additionalSymbolMappings = { assertionVar : premise }

         # Infer
         #inferenceRule = self.logic.calculus().rule( assertionRule.abbrev )
         #inference = inferenceRule.inferFrom( premiseSet, additionalMappings )

         inference = RegularInference( FormSet( ), rule, additionalSymbolMappings )
         conclusionFormList = inference.resolve( Resolver() )    # dummy resolver.  There should be nothing to resolve.

         # Select the desired conclusion
         conclusionIndex = 0
         conclusionForm = conclusionFormList[ conclusionIndex ]

         # Add a new step to the proof
         self.currentProof.addStep( conclusionForm, premiseCitationList, rule, additionalSymbolMappings, conclusionIndex )

      self.updateProof( )

   def onInferButton( self ):
      try:
         # get the inference rule
         ruleList = self.ruleBox.info_selection( )
         if len(ruleList) == 0:
            raise Exception( "No inference rule selected." )
         ruleName = ruleList[0]
         rule = self.logic.calculus().rule( ruleName )

         # Assemble the list of selected premises
         premiseCitList = self.proofWidget.getSelection( )
         premiseSet     = self.currentProof.buildPremiseSet( premiseCitList )

         # Deal with any symbols in the Rule's conclusion forms, NOT also in the premise forms.
         conclusionOnlySymbols    = rule.conclusionOnlySymbols( )
         additionalSymbolMappings = None
         if len(conclusionOnlySymbols) > 0:
            additionalSymbolMappings = self._assignUnmappedSymbols( conclusionOnlySymbols, rule )

         # Infer
         inference = RegularInference( premiseSet, rule, additionalSymbolMappings )
         conclusionFormList = inference.resolve( self )

         # Select the desired conclusion
         conclusionIndex = 0
         if len(conclusionFormList) > 1:
            conclusionIndex = self._selectConclusionForm( conclusionFormList )

         conclusionForm = conclusionFormList[ conclusionIndex ]

         # Add a new step to the proof
         self.currentProof.addStep( conclusionForm, premiseCitList, rule, inference.additionalSymbolMappings, conclusionIndex )

         # Update the view of the proof
         self.updateProof( )

      except CancelOperation:
         pass

      except SequentApplicationError:
         messagebox.showerror( 'Inference Error', 'Cannot map the inference rule to the selected premises.' )

      except Exception as msg:
         if msg is None:
            msg = 'An unknown error occured.'

         messagebox.showerror( "Inference Error", msg )

      self.ruleBox.selection_clear( )

   def onInferEquivButton( self ):
      try:
         # get the inference rule
         ruleList = self.ruleBox.info_selection( )
         if len(ruleList) == 0:
            raise Exception( "No inference rule selected." )
         ruleName = ruleList[0]
         rule = self.logic.calculus().rule( ruleName )

         # Assemble the list of selected premises
         premiseCitList = self.proofWidget.getSelection( )
         premiseSet     = self.currentProof.buildPremiseSet( premiseCitList )

         # Infer
         inference = EquivalenceInference( premiseSet, rule )
         inference.resolve( self )
         self.currentProof.addStep( inference.getConclusionForm(), premiseCitList, rule, inference.additionalSymbolMappings, inference.conclusionIndex )

         # Update the view of the proof
         self.updateProof( )

      except CancelOperation:
         pass

      except SequentApplicationError:
         messagebox.showerror( 'Inference Error', 'Cannot map the inference rule to the selected premises.' )

      except Exception as msg:
         if msg is None:
            msg = 'An unknown error occured.'

         messagebox.showerror( "Inference Error", msg )

      self.ruleBox.selection_clear( )

   def onBeginButton( self ):
      try:
         self.currentProof.beginHypo( )
         self.updateProof( )

      except Exception as msg:
         if msg is None:
            msg = 'An unknown error occured.'

         messagebox.showerror( "Nesting Error", msg )

   def onEndButton( self ):
      try:
         self.currentProof.endHypo( )
         self.updateProof( )

      except Exception as msg:
         if msg is None:
            msg = 'An unknown error occured.'

         messagebox.showerror( "Nesting Error", msg )

   def deleteStep( self ):
      self.currentProof.deleteStep( )
      self.updateProof( )

   def updateProof( self ):
      sv = tix.StringVar( )
      sv.set( str(self.currentSequent) )
      self.sequentEntry.config( textvariable=sv )

      self.proofWidget.wrapProof( self.currentProof )

   def destroy (self):
      self.root.destroy()

   def _selectSubWFF( self, wff ):
      '''Return a sub-WFF of wff.  Return False to cancel the operation.'''
      assert isinstance( wff, Form )

      ss = wff.structuredString()
      d = SubWFFSelectorDialog( self.root, ss )
      selection = d.getSelection()
      return selection[1]._clientData

   def _assignUnmappedSymbols( self, unmappedSymbolList, rule ):
      '''Modify symbolMap.  Each symbol must be mapped to a valid WFF. Return False to cancel the operation.'''
      d = FreeAtomDialog( self.root, rule, unmappedSymbolList )
      symbolMapping = d.unmappedSymbolMap

      for name, val in symbolMapping.items():
         symbolMapping[ name ] = self.logic.language().parseProp( val )

      return symbolMapping

   def _selectConclusionForm( self, conclusionFormList ):
      '''Return an index into conclusionFormList.  Return False to cancel the operation.'''
      # Select the desired conclusion
      d = ConclusionSelectionDialog( self.root, conclusionFormList )
      return int(d._selection)

   def quit( self ):
      self.exit = 0

   def mainloop(self):
      while self.exit < 0:
         self.root.tk.dooneevent(TCL_ALL_EVENTS)


if __name__== '__main__' :
   AVAILABLE_LOGICS = {
                      'Gentzen': Gentzen,
                      'Gensler': Gensler,
                      'Fitch':   Fitch
                      }

   DEFAULT_LOGIC    = 'Gentzen'

   root = tix.Tk( )
   pv = ProofView( root, Fitch )

   pv.mainloop( )
   pv.destroy( )
