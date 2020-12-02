import logging

def log_level():
    #setting up log level '''
    logging.basicConfig(filename='saivision_assignment.log', filemode='w', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger(__name__)
    logger.info('Haivision Rest API Assignment Detailed Test Log \n')
