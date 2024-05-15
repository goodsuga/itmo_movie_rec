docker run --rm -it \
    -v /home/a/Desktop/ИТМО/itmo_movie_rec/:/app_root \
    -v /home/a/Desktop/ИТМО/itmo_movie_rec/data_pull_service/data_requests/:/app_root/data_pull_service/data_requests/ \
    -v /home/a/Desktop/ИТМО/itmo_movie_rec/movie_data/:/app_root/movie_data/ \
    -v /home/a/Desktop/ИТМО/itmo_movie_rec/configurations/:/app_root/configurations/ \
    movie-rec-server-service
