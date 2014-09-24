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

    migrator = Migrator(converters, 'sqlite:///db/kawaz.db', 'sqlite:///db/kawaz3.db')
    migrator.migrate()