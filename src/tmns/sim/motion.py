
#  Python Standard Libraries
import logging
import math

#  Numerical Python
import numpy as np

#  Project Libraries
from tmns.geo.coordinate import ( ecf_to_geographic,
                                  geographic_to_ecf,
                                  get_ecf_forward_vector )
from tmns.math.rotations import ( Axis, Quaternion )
from tmns.math.physics   import ( position, velocity )

class Motion_Model:

    def to_log_string():
        raise NotImplementedError()
    

class Straight_Model(Motion_Model):

    def __init__(self, position_geog,
                       mass_kg: float,
                       radius_m: float,
                       thrust_kN: float,
                       air_mass_density: float,
                       drag_coefficient: float,
                       pitch_rad: float,
                       yaw_rad: float,
                       start_time_offset_sec: float,
                       burn_time_sec: float ):
        self.position_geog         = position_geog
        self.mass_kg               = mass_kg
        self.radius_m              = radius_m
        self.thrust_kN             = thrust_kN
        self.air_mass_density      = air_mass_density
        self.drag_coefficient      = drag_coefficient
        self.pitch_rad             = pitch_rad
        self.yaw_rad               = yaw_rad
        self.start_time_offset_sec = start_time_offset_sec
        self.burn_time_sec         = burn_time_sec

        self.t_cur = 0

        #  Vehicle position in ECEF
        self.position_geog_t0 = np.copy( self.position_geog )
        self.position_ecf_t0  = geographic_to_ecf( coord = self.position_geog_t0 )
        self.forward_ecf_t0   = self.get_ecf_forward( self.position_geog_t0 )
        self.down_ecf_t0      = self.get_ecf_down( self.position_geog_t0 )

        #  Physics variables
        self.g_e = 9.807

        #  Components
        self.P_init = np.copy( self.position_ecf_t0 )
        self.V_init = np.zeros( (3,1) )

        self.P_cur = np.copy( self.P_init )
        self.V_cur = np.copy( self.V_init )


    def current_position_geog(self):
        self.position_geog

    def get_ecf_forward( self, position_lla ):
        '''
        Create a forward vector but in ECF space.
        This is needed to handle the forward in a non-trivial coordinate system.
        '''

        #  update the body quaternion
        body_quat = Quaternion.from_euler_angles( Axis.Y, self.pitch_rad,
                                                  Axis.X, 0,
                                                  Axis.Z, self.yaw_rad )
        
        forward_lla = np.array( [[1],[0],[0]], dtype = np.float64 )

        forward_rot_lla = body_quat.to_rotation_matrix() @ forward_lla

        return get_ecf_forward_vector( position_lla, forward_rot_lla )
    
    def get_ecf_down( self, position_lla ):

        logging.info( f'aaaaaaaaaaaaaaaaa: {position_lla.T}' )
        position1_ecf = geographic_to_ecf( position_lla )

        logging.info( f'bbbbbbbbbbbbbbbbb: {position1_ecf.T}' )
        position_lla_minus1 = np.copy( position_lla )
        position_lla_minus1[2] -= 1
        logging.info( f'cccccccccccccccc: {position_lla_minus1.T}' )
        position2_ecf = geographic_to_ecf( position_lla_minus1 )

        logging.info( 'dddddddddddddddd' )
        delta = position2_ecf - position1_ecf
        logging.info( f'eeeeeeeeeeeeeeee: {delta.T}' )

        return delta / np.linalg.norm( delta )


    def info(self):

        #  Populate dictionary
        output = { 'position': self.current_position_geog() }

        return output
    
    def update(self, t_delta: float ):
        '''
        Increment the time and update the position/velocity info
        '''
        self.t_cur += t_delta

        logging.info( 'AAAAAAAAAAAAAAAA' )

        #  if before the start time, do nothing
        if self.t_cur < self.start_time_offset_sec:
            return

        logging.info( 'BBBBBBBBBBBBBBB' )

        #  Default thrust is no accelleration
        A_thrust = np.zeros( (3,1), dtype = np.float64 )

        logging.info( 'CCCCCCCCCCCCCCC' )

        #  if thruster is actively running 
        if self.t_cur > (self.start_time_offset_sec + self.burn_time_sec):
            
            #  Accelleration due to thrust
            boost_thrust_acc = self.thrust_kN / self.mass_kg
            A_thrust = self.get_ecf_forward() * boost_thrust_acc

        #  if we have run out of fuel
        else:  pass

        logging.info( 'DDDDDDDDDDDDD' )

        # Accelleration due to drag
        A_drag = self.accelleration_from_drag( self.V_init )

        logging.info( 'EEEEEEEEEEEEE' )

        # Accelleration due to gravity
        A_g = self.get_ecf_down(self.P_init) * self.g_e

        logging.info( 'FFFFFFFFFFFFF' )

        #  Full Accelleration
        self.A_cur = A_g + A_thrust - A_drag

        logging.info( 'GGGGGGGGGGGGGG' )

        #  Compute velocity
        self.V_init = np.copy( self.V_cur )
        self.V_cur = velocity( t_delta, self.V_init, self.A_cur )

        logging.info( 'HHHHHHHHHHHHHH' )

        #  Compute position
        self.P_init = np.copy( self.P_cur )
        self.P_cur = position( t_delta, self.P_init, self.V_cur )

        logging.info( 'IIIIIIIIIIIIII' )

    def accelleration_from_drag( self, V ):
        '''
        F_d = 0.5 * rho * v^2 * C_d
        '''

        # Surface area
        A = math.pi * (self.radius_m ** 2)
        return 0.5 * self.air_mass_density * V * V * self.drag_coefficient * A / self.mass_kg

    def to_log_string(self, offset: int ):

        gap = ' ' * offset
        output  = f'{gap}Straight_Model:\n'
        output += f'{gap} - position_geog: {self.position_geog}\n'
        output += f'{gap} - mass_kg: {self.mass_kg}\n'
        output += f'{gap} - radius_m: {self.radius_m}\n'
        output += f'{gap} - thrust_kN: {self.thrust_kN}\n'
        output += f'{gap} - air_mass_density: {self.air_mass_density}\n'
        output += f'{gap} - drag_coefficient: {self.drag_coefficient}\n'
        output += f'{gap} - pitch_rad: {self.pitch_rad}\n'
        output += f'{gap} - yaw_rad: {self.yaw_rad}\n'
        output += f'{gap} - start_time_offset_sec: {self.start_time_offset_sec}\n'
        output += f'{gap} - burn_time_sec: {self.burn_time_sec}\n'
        return output
    
    @staticmethod
    def parse( section, cfg_args ):

        #  Parse launch position
        launch_pos = [ cfg_args.getfloat( section, 'launch_position_longitude' ),
                       cfg_args.getfloat( section, 'launch_position_latitude' ),
                       cfg_args.getfloat( section, 'launch_position_elevation' ) ]
        
        mass_kg   = cfg_args.getfloat( section, 'missile_mass_kg' )
        radius_m  = cfg_args.getfloat( section, 'missile_radius_m' )
        thrust_kN = cfg_args.getfloat( section, 'missile_thrust_kN' )

        pitch_rad = cfg_args.getfloat( section, 'launch_pitch_degrees' ) * math.pi / 180.0
        yaw_rad   = cfg_args.getfloat( section, 'launch_yaw_degrees' ) * math.pi / 180.0

        start_time_offset_sec = cfg_args.getfloat( section, 'start_time_offset_sec' )
        burn_time_sec = cfg_args.getfloat( section, 'burn_time_sec' )

        air_density   = cfg_args.getfloat( section, 'air_mass_density' )
        drag_coeff    = cfg_args.getfloat( section, 'missile_drag_coefficient' )

        return Straight_Model( position_geog = np.array( launch_pos, dtype = np.float64 ),
                               mass_kg = mass_kg,
                               radius_m = radius_m,
                               thrust_kN = thrust_kN,
                               air_mass_density=air_density,
                               drag_coefficient=drag_coeff,
                               pitch_rad = pitch_rad,
                               yaw_rad = yaw_rad,
                               start_time_offset_sec = start_time_offset_sec,
                               burn_time_sec = burn_time_sec )


def get_motion_model( section, model_type, cfg_args ):

    if model_type == 'straight':
        return Straight_Model.parse( section, cfg_args )
    else:
        raise Exception( f'Unsupported model type: {model_type}' )