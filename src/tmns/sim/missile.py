
#  Python Standard Libraries


#  Project Libraries
from tmns.sim.motion import get_motion_model

class Missile:

    def __init__(self, id, motion_model ):
        self.id           = id
        self.motion_model = motion_model

    def info(self):

        #  Get information from the motion model
        output = self.motion_model.info()
        output['id'] = self.id

        return output
    
    def update(self, t_delta ):

        self.motion_model.update( t_delta )

    def to_log_string(self):

        output  =  'Missile:\n'
        output += f'   - id: {self.id}\n'
        output += f'   - motion model:\n'
        output += f'{self.motion_model.to_log_string(offset=8)}\n'

        return output

    @staticmethod
    def load_configs( cfg_args ):

        #  Get the number of missiles
        num_missiles = cfg_args.getint( 'general', 'number_missiles' )
        
        #  Missile array
        missiles = []

        for idx in range( num_missiles ):

            tag = f'missile_{idx+1}'
            missiles.append( Missile.load_config( cfg_args, tag ) )

        return missiles

    @staticmethod
    def load_config( cfg_args, missile_tag ):
        
        #  Load settings
        id = cfg_args.get( missile_tag, 'id' )

        # Motion type
        motion_type = cfg_args.get( missile_tag, 'motion_type' )



        return Missile( id = id,
                        motion_model = get_motion_model( missile_tag, 
                                                         motion_type,
                                                         cfg_args ) )

