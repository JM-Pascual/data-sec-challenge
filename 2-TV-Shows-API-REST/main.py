from tv_shows_api_rest import best_in_genre, best_in_genre_spark

if __name__ == '__main__':
    best_show = best_in_genre("Action")
    print(f"Best show in genre 'Action': {best_show}")

    best_show_spark = best_in_genre_spark("Action")
    print(f"Best show in genre 'Action' (Using Spark): {best_show_spark}")

    best_show = best_in_genre("CrImE")
    print(f"Best show in genre 'Crime': {best_show}")

    best_show_spark = best_in_genre_spark("comedy")
    print(f"Best show in genre 'Comedy' (Using Spark): {best_show_spark}")

    best_show_not_found = best_in_genre("Not Found")
    print(f"Best show in genre 'Not Found': {best_show_not_found}")