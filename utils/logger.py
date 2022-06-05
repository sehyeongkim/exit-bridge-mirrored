import sys
import os
import loguru


debugger = loguru.logger


def init_logger(config_obj, log_filename):
    log_format = '[{time:YYYY-MM-DD HH:mm:ss.SSS}] [{process: >5}] [{level.name:>5}] <level>{message}</level>'
    loguru.logger.configure(
        handlers=[
            dict(sink=sys.stdout,
                 format=log_format,
                 level=config_obj['log']['level'].upper(),
                 colorize=True),
            dict(sink=os.path.join(config_obj['log']['directory'], log_filename),
                 format=log_format,
                 enqueue=True,
                 level=config_obj['log']['level'].upper(),
                 # serialize=True,
                 rotation='%s MB' % config_obj['log']['max_mbytes'],
                 retention=int(config_obj['log']['backup_count']),
                 )
        ],
    )

