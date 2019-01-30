import os
import sys
from logging import ERROR, INFO, DEBUG
from transonic.dist import get_logger, ParallelBuildExt

FLUIDDYN_DEBUG = os.environ.get("FLUIDDYN_DEBUG", False)
PARALLEL_COMPILE = not FLUIDDYN_DEBUG

if "egg_info" in sys.argv:
    level = ERROR
elif FLUIDDYN_DEBUG:
    level = DEBUG
else:
    level = INFO

logger = get_logger("fluidsht")
logger.setLevel(level)


class FluidSHTBuildExt(ParallelBuildExt):
    def initialize_options(self):
        super().initialize_options()
        self.logger_name = "fluidsht"
        self.num_jobs_env_var = "FLUIDDYN_NUM_PROCS_BUILD"

    def get_num_jobs(self):
        if PARALLEL_COMPILE:
            return super().get_num_jobs()
        else:
            # Return None which would in turn retain the `self.parallel` in its
            # default value
            return None
