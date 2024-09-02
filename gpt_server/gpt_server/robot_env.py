import numpy as np



def Robot(func, checker=None):
    """ primitive flag, no practical effect. """

    def Robot_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return Robot_wrapper


class MedicalEnv(PosCtrlEnv):
    def __init__(self):
        super().__init__()


    @Robot
    def initialize_robot(self):
        self.initialize_robot()

    @Robot
    def grab_pipette(self, pipette_type):
        self.grab_pipette(pipette_type)
        

    @Robot
    def attach_tip(self, tip_position):
        self.attach_tip(tip_position)


    @Robot
    def aspirate_liquid(self, medical_position):
        self.aspirate_liquid(medical_position)

    @Robot
    def transfer_to_mix(self):
        self.transfer_to_mix()

    @Robot
    def shake(self):
        self.shake()

    @Robot
    def shake(self):
        self.shake()
        
    @Robot
    def dispense_to_dish(self, method):
        self.dispense_to_dish(method)
        
    @Robot
    def dispose_tip(self):
        self.dispose_tip()
        
    @Robot
    def complete_task(self):
        self.complete_task()

def make_env():
    env = MedicalEnv()
    return env
