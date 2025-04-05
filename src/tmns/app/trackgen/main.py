
#  Python Standard Libraries
import logging

#  Project Libraries
from tmns.app.trackgen.Options  import Options
from tmns.app.trackgen.sim      import run_simulation
from tmns.sim.missile import Missile

def main():
    
    #  Parse the configuration
    options = Options.parse()

    logger = logging.getLogger( 'trackgen' )

    #  Load missile profiles
    missiles = Missile.load_configs( options.cfg_args )

    for missile in missiles:
        print( missile.to_log_string() )

    #  Run the simulation
    run_simulation( options,
                    missiles,
                    logger )


if __name__ == '__main__':
    main()

def run_command():
    main()