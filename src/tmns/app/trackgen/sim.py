

#  Python Standard Libraries
import logging

#  Project Libraries
from tmns.app.trackgen.Options  import Options
from tmns.app.trackgen.writer   import Track_Writer
from tmns.sim.missile           import Missile


def run_simulation( config:   Options,
                    missiles: list[Missile],
                    logger:   logging.Logger ):

    logger.info( 'Starting Simulation' )

    #  Create output track-writer
    writer = Track_Writer( config.cfg_args.get('general','output_base' ))

    # Capture the start time
    t_cur  = 0
    t_max  = config.cfg_args.getfloat( 'general', 'simulation_time_secs' )
    t_step = config.cfg_args.getfloat( 'general', 'step_time_ms' ) / 1000.0

    start_time_unix = config.cfg_args.getfloat( 'general', 'start_time_unix' )

    # Start iteration
    iterations = 0
    while t_cur < t_max:

        logger.debug( f'Start of iteration: {iterations}' )

        #  Iterate over each missile
        for missile in missiles:
            
            #  Get the information about the vehicle
            info = missile.info()
            print( info )
            logger.debug( f'Missile:{missile.id}\n', info )
            writer.add_missile_entry( midx = info['id'],
                                      unix_time = start_time_unix + t_cur,
                                       position = info['position'] )
            
            #  update the next time step
            logger.debug( 'Start of update' )
            missile.update( t_delta = t_step )
            logger.debug( 'End of update' )

        #  Increment time step
        t_cur += t_step
        iterations += 1

        break

    #  Write everything to disk
    writer.write_all()