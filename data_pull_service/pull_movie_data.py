import logging
from bs4 import BeautifulSoup
import requests
from pprint import pprint, pformat
from tqdm import tqdm
import polars as pl
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)


def pull_data(output_path):
    loc_str = "[pull_data_service/pull_movie_data.py]:"
    logger.info(f"{loc_str} Gathering movie data")
    top_500_movies_url = f"https://ru.wikipedia.org/wiki/250_%D0%BB%D1%83%D1%87%D1%88%D0%B8%D1%85_%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%D0%BE%D0%B2_%D0%BF%D0%BE_%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D0%B8_IMDb"

    r = requests.get(top_500_movies_url)
    logger.info(f"{loc_str} Getting URL {top_500_movies_url}: {r.status_code}")

    parser = BeautifulSoup(r.text, features='lxml')
    movie_table = parser.find("table")

    movie_rows = movie_table.find_all("tr")
    # [1:] потому что игнорируем место в топе
    columns = [th.text.replace("\n", "") for th in movie_rows[0].find_all("th")][1:]
    movie_data = {col: [] for col in columns}
    movie_data.update({
        "Ссылка на Вики": [],
        "Сюжет": [],
        "Описание": []
    })

    for row_index in tqdm(range(1, len(movie_rows)), total=len(movie_rows)-1):
        # [1:] потому что игнорируем место в топе
        tds = movie_rows[row_index].find_all("td")[1:]
        for i, td in enumerate(tds):
            link = td.find("a")
            if columns[i] == "Год":
                movie_data[columns[i]].append(
                    int(link["title"].replace(" год в кино", ""))
                )
                continue
            elif columns[i] == "Режиссёр":
                movie_data[columns[i]].append(link["title"])
                continue
            elif columns[i] == "Жанр по версии IMDb":
                movie_data[columns[i]].append(td.text.replace("\n", ""))
                continue
            
            if columns[i] != "Название фильма":
                continue

            # Парсим название фильма
            name = link["title"]
            movie_data["Название фильма"].append(name)

            movie_href = f"https://ru.wikipedia.org{link['href']}"
            movie_data["Ссылка на Вики"].append(movie_href)

            # Вытаскиваем данные по фильму
            info_request = requests.get(movie_href)
            info_parser = BeautifulSoup(info_request.text, features='lxml')

            main_block = info_parser.find("div", {"id": "mw-content-text"}).findChildren()[0]
            elements = main_block.findChildren()

            for element in elements:
                if element.name == "p":
                    movie_description = element.text.replace("\n", " ")
                    break
            
            if movie_description is None:
                movie_data["Описание"].append(None)
                movie_data["Сюжет"].append(None)
                continue

            movie_data["Описание"].append(movie_description.replace("\n", " "))
            
            found_plot = False
            plot = []
            
            for element in elements:
                # logger.info(f"{element}")

                if element.find("span", {"id": "Сюжет"}):
                    found_plot = True
                    continue

                if element.name == "h2":
                    found_plot = False
                    continue
                
                if element.name == "p" and found_plot:
                    plot.append(element.text)

            plot = ". ".join(plot).replace("\n", " ")

            movie_data["Сюжет"].append(plot)
            plot = None
            found_plot = False
            movie_description = None    

    data = pl.DataFrame(movie_data)
    data.write_parquet(output_path)
    logger.info(f"{loc_str} {data}")


# if __name__ == "__main__":
#     outdir = Path("../movie_data")
#     outdir.mkdir(exist_ok=True)
#     outpath = outdir / "movie_data.parquet"
#     pull_data(outpath)
    


    