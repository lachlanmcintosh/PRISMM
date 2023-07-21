import logging

def log_simulation_parameters(
    pre: int, 
    mid: int, 
    post: int, 
    p_up: float, 
    p_down: float, 
    rate: float
) -> None:
    """
    Logs some information about simulation parameters.
    """
    logging.info("SIMULATION PARAMETERS ARE:")
    logging.info("pre: %s", pre)
    logging.info("mid: %s", mid)
    logging.info("post: %s", post)
    logging.info("p_up: %s", p_up)
    logging.info("p_down: %s", p_down)
    logging.info("rate: %s", rate)
    logging.info("")
