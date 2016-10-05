"""This module represents all the abstract elements of a Logic."""

from Language import Language
from Calculus import Calculus
from Form import Sequent


'''
Language
   - Lexicon
   - Grammar

Inference Rule
   - Sequent
   - Proof
      - Fundamental Proof (a dummy proof)
      - True Proof

Calculus
   - Fundamental Inference Rules
   - Derived Inference Rules
      - Simple Rules
      - Theorems
         - Simple Theorems
         - Equivalences

Logic
   - Language
   - Calculus

Theory
   - Logic
   - Axioms (Postulates)
   - Definitions
   - Theorems
'''

class Logic( object ):
   """Implementation of a logic."""
   def __init__( self, language, calculus ):
      """Initialize a new instance of this class.
      Category:      Mutator.
      Returns:       Nothing.
      Side Effects:  None.
      Preconditions: [AssertionError] 'language' must be a Language instance.
                     [AssertionError] 'calculus' must be a Calculus instance.
      """
      assert isinstance( language, Language )
      assert isinstance( calculus, Calculus )

      self._language  = language
      self._calculus  = calculus

   def language( self ):
      """Returns the language.
      Category:      Pure Function.
      Retursn:       (Language)
      Side Effects:  None.
      Preconditions: None.
      """
      assert isinstance( self._language,     Language )
      assert isinstance( self._calculus,     Calculus )

      return self._language

   def calculus( self ):
      '''Returns the calculus.
      Category:      Pure Function.
      Returns:       (Calculus)
      Side Effects:  None.
      Preconditions: None.
      '''
      assert isinstance( self._language,     Language )
      assert isinstance( self._calculus,     Calculus )

      return self._calculus



GentzenLexicon = [
          ( 'Negation',       [ '~',   u'\u00AC' ],  'PREFIX OP',  [ 'no', 'not', 'non-', 'it is not the case that' ]  ),
          ( 'Conjunction',    [ '&',   u'\u2227' ],  'INFIX OP',   [ 'and', 'but', 'also' ] ),
          ( 'Disjunction',    [ 'v',   u'\u2228' ],  'INFIX OP',   [ 'or', 'unless' ]       ),
          ( 'Conditional',    [ '>',   u'\u2283' ],  'INFIX OP',   [ 'implies', 'if-then', 'only if', 'is a sufficient condition for' ] ),
          ( 'Biconditional',  [ '<->', u'\u2261' ],  'INFIX OP',   [ 'if and only if', 'iff', 'just if'  ] ),
          ( 'Necessitation',  [ 'N:',  u'\u25A1' ],  'PREFIX OP',  [ 'it is necessary that', 'it is necessarilly the case that' ] ),
          ( 'Possibility',    [ 'P:',  u'\u25C7' ],  'PREFIX OP',  [ 'it is possible that', 'it is possibly the case that' ] ),
          ( 'Entailment',     [ '|-',  u'\u22A6' ],  'ENTAILS',    [ 'entails' ] )
          ]

GentzenLanguage = Language( GentzenLexicon, [ '<->', u'\u2261' ] )

GentzenRules = [
#           Name                            Abbreviation  Form (Sequent)
#           ==============================  ============  =============================================
          ( 'Given',                        'Given',      GentzenLanguage.parseSeq( '                       |-  P'                                     ) ),

          ( 'Modus Ponens',                 'MP',         GentzenLanguage.parseSeq( 'P > Q, P               |-  Q'                                     ) ),
          ( 'Modus Tollens',                'MT',         GentzenLanguage.parseSeq( 'P > Q, ~Q              |-  ~P'                                    ) ),
          ( 'Hypothetical Syllogism',       'HS',         GentzenLanguage.parseSeq( 'P > Q, Q > R           |-  P > R'                                 ) ),
          ( 'Disjunctive Syllogism 1',      'DS1',        GentzenLanguage.parseSeq( 'P v Q, ~P              |-  Q'                                     ) ),
          ( 'Disjunctive Syllogism 2',      'DS2',        GentzenLanguage.parseSeq( 'P v Q, ~Q              |-  P'                                     ) ),
          ( 'Constructive Dilemma',         'CD',         GentzenLanguage.parseSeq( 'P v Q, P > R, Q > S    |-  R v S, S v R'                          ) ),
          ( 'Absorption',                   'Abs',        GentzenLanguage.parseSeq( 'P > Q                  |-  P > (P & Q)'                           ) ),
          ( 'Simplification',               'Simp',       GentzenLanguage.parseSeq( 'P & Q                  |-  P, Q'                                  ) ),
          ( 'Conjunction',                  'Conj',       GentzenLanguage.parseSeq( 'P, Q                   |-  P & Q, Q & P'                          ) ),
          ( 'Addition',                     'Add',        GentzenLanguage.parseSeq( 'P                      |-  P v Q, Q v P'                          ) ),

          ( 'DeMorgan\'s (Conj)',           'DM(&)',      GentzenLanguage.parseSeq( '                       |-  ~(P & Q) <-> (~P v ~Q)'                ) ),
          ( 'DeMorgan\'s (Disj)',           'DM(v)',      GentzenLanguage.parseSeq( '                       |-  ~(P v Q) <-> (~P & ~Q)'                ) ),
          ( 'Commutation (Conj)',           'Comm(&)',    GentzenLanguage.parseSeq( '                       |-  (P & Q) <-> (Q & P)'                   ) ),
          ( 'Commutation (Disj)',           'Comm(v)',    GentzenLanguage.parseSeq( '                       |-  (P v Q) <-> (Q v P)'                   ) ),
          ( 'Association (Conj)',           'Assoc(&)',   GentzenLanguage.parseSeq( '                       |-  (P & (Q & R)) <-> ((P & Q) & R)'       ) ),
          ( 'Association (Disj)',           'Assoc(v)',   GentzenLanguage.parseSeq( '                       |-  (P v (Q v R)) <-> ((P v Q) v R)'       ) ),
          ( 'Distribution (Conj)',          'Dist(&)',    GentzenLanguage.parseSeq( '                       |-  (P & (Q v R)) <-> ((P & Q) v (P & R))' ) ),
          ( 'Distribution (Disj)',          'Dist(v)',    GentzenLanguage.parseSeq( '                       |-  (P v (Q & R)) <-> ((P v Q) & (P v R))' ) ),
          ( 'Double Negation',              'DN',         GentzenLanguage.parseSeq( '                       |-  P <-> ~~P'                             ) ),
          ( 'Transposition',                'Trans',      GentzenLanguage.parseSeq( '                       |-  (P > Q) <-> (~Q > ~P)'                 ) ),
          ( 'Material Implication',         'Impl',       GentzenLanguage.parseSeq( '                       |-  (P > Q) <-> (~P v Q)'                  ) ),
          ( 'Material Equivalence (Conj)',  'Equiv(&)',   GentzenLanguage.parseSeq( '                       |-  (P <-> Q) <-> ((P & Q) v (~P & ~Q))'   ) ),
          ( 'Material Equivalence (Cond)',  'Equiv(>)',   GentzenLanguage.parseSeq( '                       |-  (P <-> Q) <-> ((P > Q) & (Q > P))'     ) ),
          ( 'Exportation',                  'Exp',        GentzenLanguage.parseSeq( '                       |-  ((P & Q) > R) <-> (P > (Q > R))'       ) ),
          ( 'Tautology (Conj)',             'Taut(&)',    GentzenLanguage.parseSeq( '                       |-  P <-> (P & P)'                         ) ),
          ( 'Tautology (Disj)',             'Taut(v)',    GentzenLanguage.parseSeq( '                       |-  P <-> (P v P)'                         ) )
          ]

GentzenCalculus = Calculus( GentzenRules,   'Given', 'Theorem Intro', 'Axiom Intro', True )

Gentzen = Logic( GentzenLanguage, GentzenCalculus )








GenslerLexicon = [
          ( 'Negation',       [ '~',   u'\u00AC' ],  'PREFIX OP',  [ 'no', 'not', 'non-', 'it is not the case that' ]  ),
          ( 'Conjunction',    [ '&',   u'\u2227' ],  'INFIX OP',   [ 'and', 'but', 'also' ] ),
          ( 'Disjunction',    [ 'v',   u'\u2228' ],  'INFIX OP',   [ 'or', 'unless' ]       ),
          ( 'Conditional',    [ '>',   u'\u2283' ],  'INFIX OP',   [ 'implies', 'if-then', 'only if', 'is a sufficient condition for' ] ),
          ( 'Biconditional',  [ '<->', u'\u2261' ],  'INFIX OP',   [ 'if and only if', 'iff', 'just if'  ] ),
          ( 'Necessitation',  [ 'N:',  u'\u25A1' ],  'PREFIX OP',  [ 'it is necessary that', 'it is necessarilly the case that' ] ),
          ( 'Possibility',    [ 'P:',  u'\u25C7' ],  'PREFIX OP',  [ 'it is possible that', 'it is possibly the case that' ] ),
          ( 'Entailment',     [ '|-',  u'\u22A6' ],  'ENTAILS',    [ 'entails' ] )
          ]

GenslerLanguage = Language( GenslerLexicon, [ '<->', u'\u2261' ] )

GenslerRules = [
#           Name                            Abbreviation  Form (Sequent)
#           ==============================  ============  =============================================
          ( 'Assumption',                   'asm.',       GenslerLanguage.parseSeq( '                       |-  P'               ) ),

          ( 'Simplification (Conj)',        'S(&)',       GenslerLanguage.parseSeq( 'P & Q                  |-  P, Q'            ) ),
          ( 'Simplification (Disj)',        'S(v)',       GenslerLanguage.parseSeq( '~(P v Q)               |-  ~P, ~Q'          ) ),
          ( 'Simplification (Impl)',        'S(->)',      GenslerLanguage.parseSeq( '~(P > Q)               |-  P, ~Q'           ) ),
          ( 'Simplification (Neg)',         'S(~)',       GenslerLanguage.parseSeq( '~~P                    |-  P'               ) ),
          ( 'Simplification (Bi)',          'S(<->)',     GenslerLanguage.parseSeq( 'P <-> Q                |-  P > Q, Q > P'    ) ),
          ( 'Simplification (~Bi)',         'S(~<->)',    GenslerLanguage.parseSeq( '~(P <-> Q)             |-  P v Q, ~(P & Q)' ) ),

          ( 'Inference (Conj 1)',           'I(&1)',      GenslerLanguage.parseSeq( '~(P & Q), P            |-  ~Q'              ) ),
          ( 'Inference (Conj 2)',           'I(&2)',      GenslerLanguage.parseSeq( '~(P & Q), Q            |-  ~P'              ) ),
          ( 'Inference (Disj 1)',           'I(v1)',      GenslerLanguage.parseSeq( 'P v Q, ~P              |-  Q'               ) ),
          ( 'Inference (Disj 2)',           'I(v2)',      GenslerLanguage.parseSeq( 'P v Q, ~Q              |-  P'               ) ),
          ( 'Inference (Cond 1)',           'I(->1)',     GenslerLanguage.parseSeq( 'P > Q, P               |-  Q'               ) ),
          ( 'Inference (Cond 2)',           'I(->2)',     GenslerLanguage.parseSeq( 'P > Q, ~Q              |-  ~P'              ) ),

          ( 'Reductio Ad Absurdum',         'RAA',        GenslerLanguage.parseSeq( '( ~P  |-  Q & ~Q )     |-  P'               ) )
          ]

GenslerCalculus = Calculus( GenslerRules, 'Assumption', 'Thm', 'Ax', True, 'Assumption' )

Gensler = Logic( GenslerLanguage, GenslerCalculus )







FitchLexicon = [
          ( 'Negation',       [ '-',   u'\u00AC' ],  'PREFIX OP',  [ 'no', 'not', 'non-', 'it is not the case that' ]  ),
          ( 'Conjunction',    [ '^',   u'\u2227' ],  'INFIX OP',   [ 'and', 'but', 'also' ] ),
          ( 'Disjunction',    [ 'v',   u'\u2228' ],  'INFIX OP',   [ 'or', 'unless' ]       ),
          ( 'Conditional',    [ '->',  u'\u2192' ],  'INFIX OP',   [ 'implies', 'if-then', 'only if', 'is a sufficient condition for' ] ),
          ( 'Biconditional',  [ '<->', u'\u2194' ],  'INFIX OP',   [ 'if and only if', 'iff', 'just if'  ] ),
          ( 'Necessitation',  [ 'N:',  u'\u25A1' ],  'PREFIX OP',  [ 'it is necessary that', 'it is necessarilly the case that' ] ),
          ( 'Possibility',    [ 'P:',  u'\u25C7' ],  'PREFIX OP',  [ 'it is possible that', 'it is possibly the case that' ] ),
          ( 'Entailment',     [ '|-',  u'\u22A6' ],  'ENTAILS',    [ 'entails' ] )
          ]

FitchLanguage = Language( FitchLexicon, [ '<->', u'\u2194' ] )

FitchRules =   [
#           Name                            Abbreviation  Form (Sequent)
#           ==============================  ============  =============================================
          ( 'Assumption',                   'A',          FitchLanguage.parseSeq( '                       |-  P'                ) ),
          ( 'Hypothesis',                   'H',          FitchLanguage.parseSeq( '                       |-  P'                ) ),

          ( 'Negation Elimination',         '-E',         FitchLanguage.parseSeq( '--P                    |-  P'                ) ),
          ( 'Negation Introduction',        '-I',         FitchLanguage.parseSeq( '( P  |-  Q ^ -Q )      |-  -P'               ) ),

          ( 'Conjunction Elimination',      '^E',         FitchLanguage.parseSeq( 'P ^ Q                  |-  P, Q'             ) ),
          ( 'Conjunction Introduction',     '^I',         FitchLanguage.parseSeq( 'P, Q                   |-  P ^ Q, Q ^ P'     ) ),

          ( 'Disjunction Elimination',      'vE',         FitchLanguage.parseSeq( 'P v Q, P -> R, Q -> R  |-  R'                ) ),
          ( 'Disjunction Introduction',     'vI',         FitchLanguage.parseSeq( 'P                      |-  P v Q, Q v P'     ) ),

          ( 'Conditional Elimination',      '->E',        FitchLanguage.parseSeq( 'P -> Q, P              |-  Q'                ) ),
          ( 'Conditional Introduction',     '->I',        FitchLanguage.parseSeq( '( P  |-  Q )           |-  P -> Q'           ) ),

          ( 'Biconditional Elimination',    '<->E',       FitchLanguage.parseSeq( 'P <-> Q                |-  P -> Q, Q -> P'   ) ),
          ( 'Biconditional Introduction',   '<->I',       FitchLanguage.parseSeq( 'P -> Q, Q -> P         |-  P <-> Q, Q <-> P' ) ),

          ( 'Demorgan\'s Rule',             'DM',         FitchLanguage.parseSeq( ' |- -(P ^ Q)  <->  (-P v -Q)'                ) )
          ]

FitchCalculus = Calculus( FitchRules, 'A', 'TI', 'AxI', True, 'H' )

Fitch = Logic( FitchLanguage, FitchCalculus )

