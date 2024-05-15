import logging
from bs4 import BeautifulSoup
import requests
from pprint import pprint, pformat
from tqdm import tqdm
import polars as pl
from pathlib import Path
import yaml

from pull_movie_data import pull_data

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)

from time import sleep

if __name__ == "__main__":
    loc_str = "[data_pull_service/data_pull_service.py]:"
    logger.info(
        f"{loc_str} Starting data pull service... "
        "Waiting for requests to appear in data_requests folder"
    )
    
    # Отслеживаем появление запросов на выгрузку данных
    data_requests_folder = Path("/app_root/data_pull_service/data_requests")
    data_requests_folder.mkdir(exist_ok=True)

    while True:
        data_requests_folder.mkdir(exist_ok=True)

        data_pull_requests = list(data_requests_folder.glob("*.yaml"))
        if len(data_pull_requests) == 0:
            sleep(5)
            continue
        
        logger.info(
            f"{loc_str} found {len(data_pull_requests)} data pull requests!"
            " Processing..."
        )
        for data_pull_request in data_pull_requests:
            logger.info(
                f"{loc_str} Processing data pull request at {data_pull_request}"
            )
            with open(data_pull_request, "r") as r:
                config = yaml.safe_load(r)
            logger.info(f"{loc_str} Obtained data pull config: {pformat(config)}")

            outpath = config["outpath"]
            pull_data(outpath)
            data_pull_request.unlink()
