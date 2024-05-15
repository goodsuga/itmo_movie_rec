docker run --rm -it \
    -v /home/a/Desktop/ИТМО/itmo_movie_rec/:/app_root \
    -v /home/a/Desktop/ИТМО/itmo_movie_rec/data_pull_service:/app_root/data_pull_service/ \
    -v /home/a/Desktop/ИТМО/itmo_movie_rec/movie_data:/app_root/movie_data/ \
    movie-rec-data-pull-service
