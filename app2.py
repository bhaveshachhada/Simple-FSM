# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 22:08:42 2020

@author: BhaveshAchhada
"""


import os
import time
import cherrypy
import json
from simple_fsm import fsm
import random

class App(object):
    
    def __init__(self):
        
        
        self.is_lift_idle = True
        self.has_car_arrived = False
        self.pack_detected_by_car = False
        self.current_state = None
        self.availability = False
        self.pack_detected_by_car = False

    @cherrypy.expose
    def print_hello(self,cargo=None):
        response = {}
        response['output'] = 'Hello' if cargo == None else str(cargo)
        return json.dumps(response)
    
    def error_state(self, cargo):
        print('Error: ' + str(cargo))
        self.current_state = 'wait'
        return ('wait' , None)
    
    @cherrypy.expose
    def pack_request(self):
        if self.current_state == 'wait':
            self.current_state = 'pack_request_arrived'
        else:
            return json.dumps({'output' : 'busy'})
    
    @cherrypy.expose
    def set_pack_available_status(self, status):
        if status == 'True':
            self.availability = True
        else:
            self.availablility = False
    
    @cherrypy.expose
    def set_lift_status(self,status):
        if status == 'idle':
            self.is_lift_idle = True
        else:
            self.is_lift_idle = False
    
    def check_availability(self , cargo=None):
        
        # return ('available' , None) if self.availability > 0 else ('error' , 'Packs not available.')
        if self.availability == True:
            self.current_state = 'available'
            out = ('available' , None)
            return out
        
        self.current_state = 'error'
        return ('error', 'Packs not available')

    def check_lift_status(self, cargo=None):
        
        # return ('lift_idle' , None) if self.is_lift_idle == True else ('error', 'lift is busy')
        if self.is_lift_idle == True:
            self.current_state = 'lift_idle'
            return ('lift_idle' , None)
        self.current_state = 'error'
        return ('error' , 'lift is busy')
    
        
    def check_car_status(self, cargo=None):
        
        # return ('car_arrived' , None) if self.has_car_arrived == True else ('error' , 'Car not ready')
        if self.has_car_arrived == True:
            
            self.current_state = 'car_arrived'
            return ('car_arrived' , None)
        
        # self.current_state = 'error'
        return ('picked' , None)
    
    def pick_and_drop(self, cargo = None):
        time.sleep(5)
        self.current_state = 'dropped'
        self.has_car_arrived = False
        return ('dropped' , None)
    
    def wait(self , cargo = None):
        # print('wait')
        return (self.current_state , None)
        
    def success(self, cargo = None):
        msg = 'Pack sucessfully dropped'
        print(msg)
        response = {}
        response['status'] = msg        
        
        time.sleep(5)
        self.is_lift_idle = True
        self.current_state = 'wait'
        return ('wait' , None)
    
    @cherrypy.expose
    def change_car_status(self,status = None):
        if status == 'arrived':
            self.has_car_arrived = True
        else:
            self.has_car_arrived = False
        
        
    def pick_up_and_move(self, cargo = None):
        time.sleep(5)
        self.current_state = 'picked'
        return ('picked' , None)
    
    def drop_pack(self, cargo = None):
        time.sleep(5)
        self.current_state = 'dropped'
        return ('dropped' , None)
    
    @cherrypy.expose
    def set_pack_detection(self, status):
        if status == 'good':
            self.pack_detected_by_car = True
        else:
            self.pack_detected_by_car = False
    
    def pack_detected(self, cargo = None):
        if self.pack_detected_by_car == True:
            self.current_state = 'success'
            return ('success', None)
        else:
            self.current_state = 'error'
            return ('error' , 'Pack not dropped properly.')
    
def Start(obj):
    try:    
        # print('in start method.')
        cherrypy.config.update(
            {
                'server.socket_host': '0.0.0.0',
                'server.socket_port': 11000,
                'engine.autoreload.on': False,
                'tools.cors.on': False}
            )
        cherrypy.engine.start()
        cherrypy.tree.mount(obj, '/')
        # cherrypy.engine.block()
    except:
        print('error occurred.')
    
    obj.current_state = 'wait'
    # print('returning from start')
    return ('wait',None)

if __name__ == '__main__':
    
    #pass    
    
    obj = App()
    
    machine = fsm()
    machine.add_state('init', Start)
    machine.add_state('wait' , obj.wait)
    machine.add_state('pack_request_arrived' , obj.check_availability)    
    machine.add_state('available' , obj.check_lift_status)    
    machine.add_state('error' , obj.error_state, True)
    machine.add_state('lift_idle' , obj.pick_up_and_move)
    machine.add_state('picked' , obj.check_car_status)
    machine.add_state('car_arrived' , obj.drop_pack)
    machine.add_state('dropped' , obj.pack_detected )
    machine.add_state('success', obj.success)
    # while True:
    machine.run(obj)