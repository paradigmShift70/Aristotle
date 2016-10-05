from tkinter import *

import string


class BasicDialog( Toplevel ):
   def __init__( self, parent, title = None ):
      assert isinstance( title, str ) or ( title is None )

      Toplevel.__init__( self, parent )
      self.transient( parent )

      if title:
         self.title( title )

      self.parent = parent
      self.result = None

      body = Frame( self )
      self.initial_focus = self.body( body )
      body.pack( padx=5, pady=5 )

      self.buttonbox()

      self.grab_set()

      if not self.initial_focus:
         self.initial_focus = self

      self.protocol( "WM_DELETE_WINDOW", self.cancel )

      self.geometry("+%d+%d" % ( parent.winfo_rootx()+50,
                                 parent.winfo_rooty()+50 ) )

      self.initial_focus.focus_set()

      self.wait_window( self )

   # construction hooks
   def body( self, master ):
      # create dialog body.  return widget that should have
      # initial focus.  This method should be overridden.
      pass

   def buttonbox( self ):
      # add standard button box.  Override if you don't
      # want the standard buttons.
      box = Frame( self )

      w = Button( box, text="OK", width=10, command=self.ok, default=ACTIVE )
      w.pack( side=LEFT, padx=5, pady=5 )
      w = Button( box, text="Cancel", width=10, command=self.cancel )
      w.pack( side=LEFT, padx=5, pady=5 )

      self.bind( "&lt;Return>", self.ok )
      self.bind( "&lt;Excape>", self.cancel )

      box.pack()

   # standard button sematnics
   def ok( self, event=None ):
      if not self.validate( ):
         self.initial_focus.focus_set()
         return

      self.withdraw()
      self.update_idletasks()

      self.apply()

      self.wrapup()

   def cancel( self, event=None ):
      self.wrapup( )

   def wrapup( self ):
      #Put focus back to the parent windw
      self.parent.focus_set( )
      self.destroy( )

   # command hooks
   def validate( self ):
      # Override
      return 1

   def apply( self ):
      # Override
      pass


class Callback( object ):
   """Create a callback shim. Based on code by Scott David Daniels
   (which also handles keyword arguments).

   The callback passed to __init__( ) must take a single argument.
   """
   def __init__(self, callback, *firstArgs):
      self.__callback = callback
      self.__firstArgs = firstArgs

   def __call__(self, *args):
      return self.__callback (*(self.__firstArgs + args))


