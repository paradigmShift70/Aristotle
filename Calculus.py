import Form
import copy

class InferenceRule( object ):
   """Implementation of an inference rule."""
   def __init__( self, name, abbreviation, sequent, proof='fundamental' ):
      """Initialize a new instance of this class.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  None.
      Preconditions: [AssertionError] 'name' must be a str.
                     [AssertionError] 'abbreviation' must be a str.
                     [AssertionError] 'sequent' must be a Form.Sequent.
                     [AssertionError] 'proof' must be a str or Proof.
      """
      assert isinstance( name,          str )
      assert isinstance( abbreviation,  str )
      assert isinstance( sequent,       Form.Sequent )
      #assert isinstance( proof,         (Proof.Proof,str) )

      self.name    = name
      self.abbrev  = abbreviation
      self.sequent = sequent
      self.proof   = proof

   def conclusionOnlySymbols( self ):
      return self.sequent.conclusionAdditions( )

   def mapPremiseFormsTo( self, premises ):
      assert isinstance( premises,                           FormSet )
      assert isinstance( includeUnmappableConclusionSymbols, bool    )

      assert isinstance( self.name,      str )
      assert isinstance( self.abbrev,    str )
      assert isinstance( self.sequent,   Form.Sequent )
      assert isinstance( self.proof,     ( Proof.Proof,str ) )

      premiseMap = self.sequent.mapPremisesTo( premises )

      return premiseMap

   def applyTo( self, premises, additionalMappedSymbols ):
      """Attempt to infer a list of conclusions by first mapping the premises
      of this instance onto 'set', then instatiating the conclusion set using
      those mappings.
      Category:        Pure Function.
      Returns:         (list) The list of conclusions.
                       Empty list if set is not an instance of self._premises.
      Side Effects:    None.
      Preconditions:   [AssertionError] set must be a FormSet.
                       [AssertionError] additionalMappings must be a dict or None.
                       [Exception]      set must be an instance of self._premises.
      """
      assert isinstance( premises,                Form.FormSet )
      assert isinstance( additionalMappedSymbols, dict    ) or ( additionalMappedSymbols is None )

      assert isinstance( self.name,               str     )
      assert isinstance( self.abbrev,             str     )
      assert isinstance( self.sequent,            Form.Sequent )

      if len(premises) != len(self.sequent.premiseFormSet()):
         raise Exception( '{0} premise(s) required for the selected inference rule.'.format(len(self.sequent.premiseFormSet())) )

      mapping = self.sequent.premiseFormSet().mapTo( premises, additionalMappedSymbols )
      if mapping == {}:
         raise SequentApplicationError

      return self.sequent.conclusionFormSet().makeInstance( mapping )

   def isDerivedRule( self ):
      return isinstance( self.proof, Proof )

   def isTheoremOfLogic( self ):
      pass

   def isEquivalenceTheoremOfLogic( self ):
      pass


class Resolver( object ):
   """Abstract base class for well-formed formulas."""
   # Contract
   def _selectSubWFF( self, wff ):
      '''Return a sub-WFF of wff.  Any exception will cancel the operation.'''
      raise NotImplementedError( )

   def _assignUnmappedSymbols( self, unmappedSymbols, sequent ):
      '''Return a new dict mapping unmapped symbols to WFFs (don't modify unmappedSymbols).
      Each symbol must be mapped to a valid WFF. Any exception will cancel the operation.'''
      raise NotImplementedError( )

   def _selectConclusionForm( self, conclusionFormList ):
      '''Return an index into conclusionFormList.  Any exception will cancel the operation.'''
      raise NotImplementedError( )


class Calculus( object ):
   """Implementation of Calculus."""
   DEFAULT_THEOREM_INTRODUCTION_RULE_NAME = 'Theorem Intro'
   DEFAULT_AXIOM_INTRODUCTION_RULE_NAME   = 'Axiom Intro'

   def __init__( self, inferenceRules, proofPremiseRuleName, theoremRuleName, axiomRuleName, allowBiconditionalSubstitution=False, subproofPremiseRule=None ):
      assert isinstance( inferenceRules,                 list )
      assert isinstance( proofPremiseRuleName,           str  )
      assert isinstance( theoremRuleName,                str  )
      assert isinstance( axiomRuleName,                  str  )
      assert isinstance( allowBiconditionalSubstitution, bool )
      assert isinstance( subproofPremiseRule,            str  ) or ( subproofPremiseRule is None )

      # Basic Properties
      self._logic                = None
      self._inferenceRules       = inferenceRules
      self._proofPremiseRule     = proofPremiseRuleName
      self._theoremRuleName      = theoremRuleName
      self._axiomRuleName        = axiomRuleName
      self._allowBicondSubst     = allowBiconditionalSubstitution

      # Setup Inference Rules
      self._ruleList  = [ ]
      self._ruleDict  = { }

      for ruleIndex, ruleTuple in enumerate( inferenceRules ):
         ruleName, ruleAbbrev, ruleSeq = ruleTuple

         rule = InferenceRule( ruleName, ruleAbbrev, ruleSeq )

         self._ruleList.append( rule )
         self._ruleDict[ rule.name   ] = ruleIndex
         self._ruleDict[ rule.abbrev ] = ruleIndex

      # Setup the assertion rule
      if proofPremiseRuleName not in self._ruleDict:
         raise Exception( 'Invalid premise assertion rule: rule name not defined.' )

      proofPremiseRuleIndex = self._ruleDict[ proofPremiseRuleName ]
      self._proofPremiseRule = self._ruleList[ proofPremiseRuleIndex ]
      assertionSeq  = self._proofPremiseRule.sequent

      if len(assertionSeq.premiseFormSet()) != 0:
         raise Exception( 'Invalid premise assertion rule: rule may have no premise forms.' )

      if len(assertionSeq.conclusionFormSet()) != 1:
         raise Exception( 'Invalid premise assertion rule: rule must have exactly one conclusion form.' )

      if not isinstance(assertionSeq.conclusionFormSet()[0], Form.AtomicWFF):
         raise Exception( 'Invalid premise assertion rule: conclusion form must be atomic.' )

   def hasRule( self, aRuleName ):
      """Is 'aRuleName' the name of an inference rule in the logic?
      Category:      Predicate.
      Returns:       (bool) True if 'aRuleName' is an inference rule in the logic.
      Side Effects:  None.
      Preconditions: [AssertionError] 'aRuleName' must be a str.
      """
      assert isinstance( aRuleName,      str      )

      return aRuleName in self._ruleDict

   def rule( self, aRuleName ):
      """Returns the sequent for the rule named 'aRuleName'.
      Category:      Pure Function.
      Returns:       (Sequent)
      Side Effects:  None.
      Preconditions: [AssertionError] 'aRuleName' must be a str.
      """
      assert isinstance( aRuleName,      str      )

      return self._ruleList[ self._ruleDict[ aRuleName ] ]

   def ruleList( self ):
      """Returns a list of the inference rules; idential to the 'inferenceRules' in __init__( ).
      Category:      Pure Function.
      Returns:       (list)
      Side Effects:  None.
      Preconditions: None.
      """
      return self._ruleList

   def premiseAssertionRule( self ):
      return self._proofPremiseRule

   def theoremIntroProofText( self ):
      """Returns the rule name for the Theorem Introduction.
      Category:      Pure Function.
      Returns:       (str)
      Side Effects:  None.
      Preconditions: None.
      """
      return self._theoremIntro

   def conclusionOnlySymbols( self, ruleName ):
      return self.rule( ruleName ).conclusionOnlySymbols( )
   
   def applyInference( self, ruleName, premiseSet, additionalSymbolMappings=None ):
      '''Apply the inference rule to a set of premises.
      Category:      Pure Function.
      Returns:       (list) valid conclusion forms.
      Side Effects:  None.
      Preconditions: [AssertionError] 'rule' must be the name of an inference rule.
                     [AssertionError] 'premiseSet' must be a FormSet.
                     [AssertionError] 'additionalSymbolMappings' must be 
      '''
      assert isinstance( ruleName,                 str          )
      assert isinstance( premiseSet,               Form.FormSet )
      assert isinstance( additionalSymbolMappings, dict         )
      
      if additionalSymbolMappings is None:
         additionalSymbolMappings = { }
      else:
         additionalSymbolMappings = copy.deepcopy( additionalSymbolMappings )

      rule = self.rule( ruleName )
      return rule.applyTo( premiseSet, additionalSymbolMappings )


class Inference( object ):
   def __init__( self, premiseSet, rule, additionalSymbolMappings=None ):
      """Initialize a new instance of the class.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Initialize the new instance.
      Preconditions: premiseSet (FormSet) Set of forms to apply the rule to.
                     rule (InferenceRule)
                     additionalMappings (dict)
      """
      # Inputs
      self.ruleName            = rule.name
      self.premiseSet          = premiseSet
      self.additionalSymbolMappings = copy.deepcopy(additionalSymbolMappings)

      self.rule                = rule

      if additionalSymbolMappings is None:
         self.additionalSymbolMappings = { }

   # Contract
   def resolve( self, resolver ):
      """Resolve any issues when attempting to apply an inference rule to premises.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Adjusts internal state to something valid to apply the inference rule.
      Preconditions: proofBuilder (ProofBuilder) the proof builder currently constructing the proof.
                     citeList (list) list of proof step numbers - premises for the inference.
                     ruleName (str) name of the rule being applied.
                     additionalSymbolMappings (dict) mappings to resolve unmapped symbols.
                     equivalence (bool) is this to be an inference of an equivalence?
      """
      raise NotImplementedError


class RegularInference( Inference ):
   def __init__( self, premiseSet, ruleName, additionalSymbolMappings=None ):
      super().__init__( premiseSet, ruleName, additionalSymbolMappings )

   # Specialization of Inference
   def resolve( self, resolver ):
      return self.rule.applyTo( self.premiseSet, self.additionalSymbolMappings )


class EquivalenceInference( Inference ):
   def __init__( self, premiseSet, ruleName, additionalSymbolMappings=None ):
      super().__init__( premiseSet, ruleName, additionalSymbolMappings )

      # Inputs needed to complete a direct inference
      self.subWFFSelection     = None    # Used for applying equivalences

   # Specialization of Inference
   def resolve( self, resolver ):
      # insure the correct number of premises
      if len(self.premiseSet) != 1:
         raise Exception( 'Equivalence requires exactly one premise.' )

      thePremise = self.premiseSet[0]

      # Insure the selected rule is a theorem in the form of an equivalence
      # TODO:  Fix this
      #if not self.logic.language().isEquivalenceTheorem( self.rule.sequent ):
         #raise Exception( 'An equivalence theorem must be selected to use Infer Equivalence.' )

      # Select the subwff of the premise to which to apply the equivalence.
      self.subWFFSelection = resolver._selectSubWFF( thePremise )

      # determine if the equivalence A <-> B should be applied to subWFF as A |- B or B |- A
      theASide, theBSide = self.rule.sequent.conclusionFormSet()[ 0 ].subordinates( )
      mappingASide = theASide.mapTo( self.subWFFSelection )
      mappingBSide = theBSide.mapTo( self.subWFFSelection )
      if len(mappingASide) > 0:
         # We know we need to apply equivalence A <-> B as A |- B
         premiseToRuleMap = mappingASide
         theConclusionForm = theBSide
      elif len(mappingBSide) > 0:
         # We know we need to apply equivalence A <-> B as B |- A
         premiseToRuleMap = mappingBSide
         theConclusionForm = theASide
      else:
         raise Exception( 'The selected sub-WFF must be an instance of one side of the equivalance.' )

      # Apply equivalence
      return theConclusionForm.makeInstance( premiseToRuleMap )

