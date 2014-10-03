import logging
from ouroboros.core.migrators import Migrator
from ouroboros.core.converters import converters
from configparser import ConfigParser

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
    logging.getLogger('sqlalchemy.orm').setLevel(logging.ERROR)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.ERROR)
    logging.getLogger('sqlalchemy.dialects').setLevel(logging.ERROR)

    config = ConfigParser()
    config.read('config.ini')
    driver = config['driver']
    if driver:
        src = driver.get('src', None)
        dst = driver.get('dst', None)

        if not src or not dst:
            raise Exception("You must set driver.src and driver.dst in your config.ini")

        migrator = Migrator(converters,
                            src,
                            dst)
        migrator.migrate()
