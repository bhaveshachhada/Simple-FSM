# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 20:23:18 2020

@author: BhaveshAchhada
"""


from simple_fsm import fsm


class fsm_user:

    def __init__(self):
        
        self.username = 'bhavesh'
        self.password = 'PI@3.1415926'
        
        self.uname_input = None #= input('Enter username: ')
        self.pswd_input = None #= input('Enter password: ')
    
    def take_username_password(self,cargo=None):
        
        self.uname_input = input('Enter username: ')
        self.pswd_input = input('Enter password: ')
        return ('check_username',self.uname_input)
    
    def check_username(self,cargo):
        
        if self.username == cargo:
            return ('check_password',self.pswd_input)
        return ('error','You entered wrong Username.')
    
    def check_password(self, cargo):
        
        if self.password == cargo:
            return ('success','Logged in successfully.')
        return ('error','You entered wrong password.')
    
    def success(self,cargo):
        print(str(cargo))
    
    def error(self,cargo):
        print(str(cargo))

if __name__ == '__main__':
    
    user = fsm_user()
    m = fsm()
    
    m.add_state('take_username_password', user.take_username_password)
    m.add_state('check_username',user.check_username)
    m.add_state('check_password',user.check_password)
    m.add_state('success',user.success,True)
    m.add_state('error',user.error,True)
    
    m.run(None)