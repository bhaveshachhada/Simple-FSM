# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 19:26:02 2020

@author: BhaveshAchhada
"""


class fsm:
    
    def __init__(self):
        
        self.start_state = None
        self.end_states = []
        self.num_states = 0
        self.current_state = None
        self.state_handlers = {}
    
    def add_state(self,state,handler,is_end_state = False):
        
        state = state.lower()
        if self.num_states == 0:
            self.start_state = state
            self.current_state = state
        
        self.state_handlers[state] = handler
        
        if is_end_state:
            self.end_states.append(state)
        
        self.num_states += 1
    
    def run(self, cargo):
        
        try:
            handler = self.state_handlers[self.start_state]
        except:
            raise Exception("There must be at least one state.")
        
        if len(self.end_states) == 0:
            raise Exception("There must be at least one end state.")
        
        while True:
            
            (newState , cargo) = handler(cargo)
            newState = newState.lower()
            
            if newState in self.end_states:
                print( str(newState) + "reached.")
                break
            else:
                handler = self.state_handlers[newState]
    
