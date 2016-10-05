"""This module contains all that's needed for constructing proofs."""

from Form import *
from Calculus import InferenceRule, Resolver, Inference, RegularInference, EquivalenceInference


class Step( object ):
   """Implementation of a single step of a proof."""
   def __init__( self, level, prop, premiseCitationList, inferenceRule, mapping, conclusionIndex ):
      """Initialize a new instance of the class.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Initialize the new instance.
      Preconditions: [AssertionError] 'level' must be an int, 0 represents the top level,
                        1 is the first nested subproof level.
                     [AssertionError] 'prop' must be a WFF.
                     [AssertionError] 'premiseCitationList' list of step numbers.
                     [AssertionError] 'inferenceRule' the Inference rule.
                     [AssertionError] 'mapping' mapping of rule sequent symbols to WFFs.
                     [AssertionError] 'conclusionForm' (int).
      """
      assert isinstance( level,               int           )
      assert isinstance( prop,                WFF           )
      assert isinstance( premiseCitationList, list          )
      assert isinstance( inferenceRule,       InferenceRule )
      assert isinstance( mapping,             dict          )
      assert isinstance( conclusionIndex,     int           )

      self.level               = level
      self.prop                = prop
      self.citationList        = premiseCitationList
      self.inferenceRule       = inferenceRule
      self.mapping             = mapping
      self.conclusionIndex     = conclusionIndex

      self.citationListStr        = self._buildPremiseCitationListString( )
      self.ruleApplicationTypeStr = self._buildRuleApplicationTypeString( )
      self.ruleNameStr            = self._buildRuleNameString( )

      self._buildPremiseCitationListString( )

   def __str__( self ):
      """Implement the str() operation.
      Category:       Pure Function.
      Returns:        (str) A string representation of this instance.
      Side Effects:   None.
      Preconditions:  None.
      """
      assert isinstance( self.level,              int       )
      assert isinstance( self.prop,               WFF       )
      assert isinstance( self.justification,      Inference )

      return "Step( %d, %s, %s )" % ( self.num, repr( self.prop ), repr( self.justification ) )

   def __repr__( self ):
      """Return a string representation of the wff.
      Category:      Function.
      Returns:       str.
      Side Effects:  None.
      Preconditions: None.
      """
      assert isinstance( self.level,              int       )
      assert isinstance( self.prop,               WFF       )
      assert isinstance( self.justification,      Inference )

      return str( self )

   def justificationString( self ):
      if len(self.ruleApplicationTypeStr) > 0:
         return '{0} {1} {2}'.format( self.citationListStr, self.ruleApplicationTypeStr, self.ruleNameStr )
      else:
         return '{0} {1}'.format( self.citationListStr, self.ruleNameStr )

   def _buildPremiseCitationListString( self ):
      result = ""

      isFirst = True
      for cit in self.citationList:
         if not isFirst:
            result += ','

         if isinstance( cit, int ):
            result += str( cit )
         elif isinstance( cit, (list,tuple) ):
            result += '%d-%d' % tuple(cit)

         isFirst = False

      if len(result) != 0:
         result += ' '

      return result

   def _buildRuleApplicationTypeString( self ):
         # TODO: adjust for 'Theorem Introduction'
         return ''

   def _buildRuleNameString( self ):
      return self.inferenceRule.abbrev


class Env( object ):
   """The environment stack tracks which steps, objects, possible worlds, etc.
   are currently active and available for use."""
   def __init__( self, level, outter = None ):
      """Initialize a new instance of the class.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Initialize the new instance.
      Preconditions: [AssertionError] 'level' must be an int.  Represents the
                        scope level.  0 is top-level.  1 is the first nested subproof.
                     [AssertionError] 'outter' must be Env or None.  If provided,
                        'outter' must be a reference to the Env for the enclosing scope.
      """
      assert isinstance( level,  int )
      assert isinstance( outter, Env ) or ( outter is None )

      self._level   = level
      self._steps   = []
      self._outter  = outter

   def level( self ):
      """Return the current nesting level.  0 is the top level, 1 is the first
         nested proof level.
      Category:      Pure Function.
      Returns:       (int)
      Side Effects:  None.
      Preconditions: [AssertionError] 'level' must be an int.
                     [outter] 'outter' must be None (for the top-level scope)
                        or an Env representing the enclosing scope (sub-proof).
      """
      assert isinstance( self._level,  int  )
      assert isinstance( self._steps,  list )
      assert isinstance( self._outter, Env  ) or ( self._outter is None )

      return self._level

   def outter( self ):
      """Returns the Env for the enclosing scope (subproof).
      Category:      Pure Function.
      Returns:       (Env)
      Side Effects:  None.
      Preconditions: None.
      """
      assert isinstance( self._level,  int  )
      assert isinstance( self._steps,  list )
      assert isinstance( self._outter, Env  ) or ( self._outter is None )

      return self._outter

   def addStep( self, stepNum ):
      """Add a step number to this Env instance.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Adds 'stepNum' to the Env instance.
      Preconditions: [AssertionError] 'stepNum' must be an int.
      """
      assert isinstance( stepNum, (int, tuple) )

      assert isinstance( self._level,  int  )
      assert isinstance( self._steps,  list )
      assert isinstance( self._outter, Env  ) or ( self._outter is None )

      self._steps.append( stepNum )

   def __contains__( self, citation ):
      """Does the Env stack contain the citation?

      Category:      Predicate.
      Returns:       (bool) True if 'citation' is somewhere in the Env stack.
      Side Effects:  None.
      Preconditions: [AssertionError] 'citation' is an in or tuple citation.
      """
      assert isinstance( citation, (int,tuple)  )

      assert isinstance( self._level,  int  )
      assert isinstance( self._steps,  list )
      assert isinstance( self._outter, Env  ) or ( self._outter is None )

      lst = self.availableSteps( )
      return citation in lst

   def range( self ):
      """Returns the range of steps covered by the subproof as a tuple.

      Category:      Pure Function
      Returns:       (tuple) First and last step numbers.
      Parameters:    None.
      Side Effects:  None.
      Preconditions: None.
      """
      assert isinstance( self._level,  int  )
      assert isinstance( self._steps,  list )
      assert isinstance( self._outter, Env  ) or ( self._outter is None )

      return ( self._steps[0], self._steps[-1] )

   def availableSteps( self ):
      """Returns the complete list of valid citations.

      Category:      Pure Function.
      Returns:       Nothing.
      Parameters:    None.
      Side Effects:  None.
      Preconditions: None.
      """
      assert isinstance( self._level,  int  )
      assert isinstance( self._steps,  list )
      assert isinstance( self._outter, Env  ) or ( self._outter is None )

      lst = [ ]
      self._availableSteps( lst )
      return lst

   def _availableSteps( self, lst, includeSubproofs=True ):
      """Implementation for the public method availableSteps( )."""
      assert isinstance( lst,              list )
      assert isinstance( includeSubproofs, bool )

      assert isinstance( self._level,      int  )
      assert isinstance( self._steps,      list )
      assert isinstance( self._outter,     Env  ) or ( self._outter is None )

      if self._outter:
         self._outter._availableSteps( lst, False )

      for entry in self._steps:
         if isinstance( entry, tuple ):
            if includeSubproofs:
               lst.append( entry )
         else:
            lst.append( entry )


class Proof( object ):
   """The actual proof."""
   def __init__( self ):
      """Initialize a new instance of the class.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Initialize the new instance.
      Preconditions: [AssertionError] 'steps' must be None or a list of Step
                        instances which represents a valid proof.
      """
      self._env          = None
      self._steps        = None

      self._initialize( )

   def _initialize( self, steps=None ):
      """Initialize or reinitializes a Proof instance.  .

      Category:      Mutator
      Returns:       Nothing.
      Side Effects:  Reinitializes the instance.
      Preconditions: [AssertionError] 'steps' must either be None or a list of
                        Step instances which constitutes a valid proof.
      """
      assert isinstance( steps, list ) or ( steps is None )

      self._env         = Env( 0 )
      self._steps       = [ ]

      if not steps:
         return

      currentLevel = 0

      for step in steps:
         if step.level > currentLevel:
            self.beginHypo( )
            currentLevel += 1
         elif step.level < currentLevel:
            self.endHypo( )
            currentLevel -= 1

         self.addStep( step.prop, step.rsn )

   def currentLevel( self ):
      """Return the current nesting level.  0 represents the top level, 1
      represents the first nested subproof.

      Category:      Pure Function
      Returns:       (int)
      Side Effects:  None.
      Preconditions: None.
      """
      assert isinstance( self._env,         Env  )
      assert isinstance( self._steps,       list )

      return self._env.level( )

   def availablePremises( self ):
      """Return a list of valid step citations for a next step.  .

      Category:      Pure Function
      Returns:       (list)
      Side Effects:  None.
      Preconditions: None.
      """
      assert isinstance( self._env,           Env    )
      assert isinstance( self._steps,         list   )

      return self._env.availableSteps( )

   def addStep( self, prop, premiseCitationList, inferenceRule, mapping, conclusionIndex ):
      """Add a new step to the end of the proof.
      Category:      Mutator
      Returns:       Nothing.
      Side Effects:  Add a new step to the proof.
      Preconditions: [AssertionError] 'prop' must be a WFF.
                     [AssertionError] 'reason' must be a Reason.
                     [AssertionError] 'conclusionForm' must be an int.
                        A rule application returns a list of all valid conclusion forms.
                        'conclusionForm' is an index into this list to specify the
                        correct form.
                     [AssertionError] 'AdditionalMappings' must be None or a dict.
                        The conclusion form of some inference rules contains contain
                        Atomic WFF not found in the premises.  So they cannot be
                        mapped to WFFs when the premise forms are mapped to a set
                        of premises.  This map should go from these atomic wffs
                        to instance wffs.
      """
      # Add the step to the Proof
      assert isinstance( prop,                WFF           )
      assert isinstance( premiseCitationList, list          )
      assert isinstance( inferenceRule,       InferenceRule )
      assert isinstance( mapping,             dict          )
      assert isinstance( conclusionIndex,      int           )

      assert isinstance( self._env,           Env       )
      assert isinstance( self._steps,         list      )

      self._steps.append( Step( self._env.level( ), prop, premiseCitationList, inferenceRule, mapping, conclusionIndex ) )

      self._env.addStep( len(self._steps) )

   def deleteStep( self ):
      """Remove the last tesp from the proof.  .

      Category:      Mutator
      Returns:       Nothing.
      Side Effects:  None.
      Preconditions: None.
      """
      assert isinstance( self._env,         Env  )
      assert isinstance( self._steps,       list )

      # Save the stuff we need
      oldSteps = self._steps
      oldSteps.pop( )

      # Reinitialize this instance
      self._initialize( oldSteps )

   def buildPremiseSet( self, citList ):
      """Expand a list of citations into a list of premises.  .

      Category:      Pure Function
      Returns:       Nothing.
      Side Effects:  None.
      Preconditions: [AssertionError] 'citList' must be a list.
      """
      assert isinstance( citList,           list )

      assert isinstance( self._env,         Env  )
      assert isinstance( self._steps,       list )

      premiseSet = FormSet( )

      if len( citList ) > 0:
         for cit in citList:
            if isinstance( cit, int ):
               if cit not in self._env:
                  return FormSet( )
               else:
                  premiseSet.append( self._steps[ cit - 1 ].prop )
            else:
               if cit not in self._env:
                  return FormSet( )
               else:
                  hypoPremises   = FormSet( [ self._steps[ cit[0] - 1 ].prop ] )
                  hypoConclusion = FormSet( [ self._steps[ cit[1] - 1 ].prop ] )
                  premiseSet.append( Sequent( hypoPremises, hypoConclusion ) )
      else:
         return FormSet( )

      return premiseSet

   def beginHypo( self ):
      """Begin a hypothetical proof.  .

      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Adds a new Env to the environment stack.
      Preconditions: None.
      """
      assert isinstance( self._env,         Env  )
      assert isinstance( self._steps,       list )

      if len(self._steps) == 0:
         prevStepLevel = 0
      else:
         prevStepLevel = self._steps[ len(self._steps) - 1 ].level

      if self._env.level() not in ( prevStepLevel, prevStepLevel - 1 ):
         raise Exception( 'Cannot nest more than one level in a single step.' )

      self._env = Env( self._env.level() + 1, self._env )

   def endHypo( self ):
      """End the most current hypothetical proof.

      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  Pop one Env off from the environment stack.
      Preconditions: [Exception] At least one hypothetical proof must be started.
      """
      assert isinstance( self._env,         Env  )
      assert isinstance( self._steps,       list )

      if len(self._steps) == 0:
         prevStepLevel = 0
      else:
         prevStepLevel = self._steps[ len(self._steps) - 1 ].level

      if self._env.level() == 0:
         raise Exception( 'No more levels to exit.' )

      if self._env.level() not in ( prevStepLevel, prevStepLevel + 1 ):
         raise Exception( 'Cannot exit more than one level in a single step.' )

      if self._env.level() == prevStepLevel:
         # Then the env is not empty.
         subproofRange = self._env.range( )

         self._env = self._env.outter( )
         self._env.addStep( subproofRange )
      else:
         self._env = self._env.outter( )

   def __iter__( self ):
      """Implement the public function iter( )."""
      assert isinstance( self._env,         Env  )
      assert isinstance( self._steps,       list )

      return iter( self._steps )

   def __getitem__( self, stepNum ):
      """Implementation of rvalue subscript operator.  .

      Category:      Pure Function
      Returns:       (Step) the step.
      Side Effects:  None.
      Preconditions: [AssertionError] 'StepNum' must be an int.
      """
      assert isinstance( stepNum,           int  )

      assert isinstance( self._env,         Env  )
      assert isinstance( self._steps,       list )

      return self._steps[ stepNum - 1 ]

   def __len__( self ):
      """Returns the number of steps in the proof.

      Category:      Pure Function
      Returns:       Nothing.
      Side Effects:  None.
      Preconditions: None.
      """
      assert isinstance( self._env,         Env  )
      assert isinstance( self._steps,       list )

      return len( self._steps )

