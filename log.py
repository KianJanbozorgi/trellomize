import logging

if __name__ == "__main__":
    
    logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.INFO)
    
    logging.debug('This message should go to the log file')
    logging.info('So should this')
    logging.warning('And this, too')
    logging.error('And non-ASCII stuff, too, like Øresund and Malmö')