import logging

def set_logging_settings(args):
    if args.debug == "debug":
        level = logging.DEBUG
    elif args.debug == "info":
        level = logging.INFO
    
    logging.basicConfig(level=level)