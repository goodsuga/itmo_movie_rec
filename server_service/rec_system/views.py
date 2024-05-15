from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import polars as pl
import yaml
from pathlib import Path

from uuid import uuid4

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Create your views here.
def index(request):
    # ~DEBUG~
    # Идем в папку configurations, ищем там конфиг, где хранятся все пути
    root_dir = Path("/app_root")
    configs_dir = root_dir / "configurations"

    path_config = configs_dir / "data_paths.yaml"
    with open(path_config, "r") as r:
        config = yaml.safe_load(r)

    path_to_movie_data = root_dir / config["movie_data"]

    data_pull_requests_dir = Path("/app_root/data_pull_service/data_requests/")
    request_file = data_pull_requests_dir / f"{uuid4}.yaml"

    request = {"outpath": str(path_to_movie_data)}
    with open(request_file, "w") as w:
        yaml.safe_dump(request, w)
    # ~DEBUG~!!!

    template = loader.get_template("rec_system/index.html")
    return HttpResponse(template.render())


def view_all_movies(request):
    # Идем в папку configurations, ищем там конфиг, где хранятся все пути
    root_dir = Path("/app_root")
    configs_dir = root_dir / "configurations"

    path_config = configs_dir / "data_paths.yaml"
    with open(path_config, "r") as r:
        config = yaml.safe_load(r)

    path_to_movie_data = root_dir / config["movie_data"]

    movie_data = pl.read_parquet(path_to_movie_data).to_dicts()
    template = loader.get_template("rec_system/view_all_movies.html")
    context = {
        "movie_data_rows": movie_data
    }
    return HttpResponse(template.render(context, request))