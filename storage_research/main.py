import logging

from storage_research.service.generator import Generator
from storage_research.service.handler import handler_result
from storage_research.service.loader_mango import LoaderMongo
from storage_research.service.loader_pg import LoaderPostgres
from storage_research.settings.config import LOGGING, mongo_config, pg_config


def main():
    log.info("start_pg")
    with LoaderPostgres(generator=Generator(), config=pg_config) as pg:
        pg.run()
    log.info("start_mongo")
    with LoaderMongo(generator=Generator(), config=mongo_config) as mongo:
        mongo.run()
    handler_result()


if __name__ == "__main__":
    logging.basicConfig(**LOGGING)
    log = logging.getLogger(__name__)
    log.info("start")
    main()
    log.info("end")
