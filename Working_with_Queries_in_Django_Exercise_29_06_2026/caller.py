import os
from typing import List

import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import ArtworkGallery, ChessPlayer, Meal, Dungeon, Workout, Laptop
from main_app.choices import LaptopChoices, OSChoices, MealTypeChoices
from django.db.models import QuerySet, Q, F, Case, When, Value
from django.db import connection, reset_queries
from pprint import pp


def show_highest_rated_art() -> str:
    """
    SELECT
        *
    FROM
        artwork_gallery
    ORDER BY
        rating DESC,
        id ASC
    LIMIT 1;
    """
    highest_rated = ArtworkGallery.objects.order_by('-rating', 'id').first()
    return f"{highest_rated.art_name} is the highest-rated art with a {highest_rated.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    """
    INSERT INTO
        artwork_gallery
    VALUES
        (...),
        (...);
    """
    ArtworkGallery.objects.bulk_create([
        first_art, second_art
    ])


artwork1 = ArtworkGallery(
    artist_name='Vincent van Gogh',
    art_name='Starry Night',
    rating=4,
    price=1200000.0
)
artwork2 = ArtworkGallery(
    artist_name='Leonardo da Vinci',
    art_name='Mona Lisa',
    rating=5,
    price=1500000.0
)


def delete_negative_rated_arts() -> None:
    """
    DELETE FROM artwork_gallery
    WHERE rating < 0;
    """
    ArtworkGallery.objects.filter(rating__lt=0).delete()



def show_the_most_expensive_laptop() -> str:
    most_expensive_laptop = Laptop.objects.order_by('-price', '-id').first()

    return f"{most_expensive_laptop.brand} is the most expensive laptop available for {most_expensive_laptop.price}$!"


def bulk_create_laptops(args: List[Laptop]) -> None:
    Laptop.objects.bulk_create(args)


def update_to_512_gb_storage() -> None:
    """
    UPDATE laptop
    SET storage = 512
    WHERE brand IN ('Asus', 'Lenovo');
    """
    Laptop.objects.filter(brand__in=[LaptopChoices.ASUS, LaptopChoices.LENOVO]).update(storage=512)


def update_to_16_gb_memory() -> None:
    (Laptop.objects.filter(brand__in=[LaptopChoices.APPLE, LaptopChoices.ACER, LaptopChoices.DELL])
     .update(memory=16))


def update_operation_systems() -> None:
    """
    -- Solution 2
    UPDATE laptop
    SET operation_system = ...
    WHERE brand IN [..., ...]; x 4

    -- Solution 3
    UPDATE laptop
    SET operation_system = CASE
        WHEN ... THEN ...
        WHEN ... THEN ...
        WHEN ... THEN ...
        WHEN ... THEN ...
    END
    """

    # Solution 1 really badd
    # for laptop in Laptop.objects.all():
    #     if laptop = Asus
    #         ...

    # Solution 2
    Laptop.objects.filter(brand=LaptopChoices.ASUS).update(operation_system=OSChoices.WINDOWS)
    Laptop.objects.filter(brand=LaptopChoices.APPLE).update(operation_system=OSChoices.MACOS)
    Laptop.objects.filter(brand=LaptopChoices.LENOVO).update(operation_system=OSChoices.CHROME_OS)
    Laptop.objects.filter(brand__in=[LaptopChoices.DELL, LaptopChoices.ACER]).update(operation_system=OSChoices.LINUX)

    # Solution 3 best
    Laptop.objects.update(
        operation_system=Case(
            When(brand=LaptopChoices.ASUS, then=Value(OSChoices.WINDOWS)),
            When(brand=LaptopChoices.APPLE, then=Value(OSChoices.MACOS)),
            When(brand=LaptopChoices.LENOVO, then=Value(OSChoices.CHROME_OS)),
            When(brand__in=[LaptopChoices.DELL, LaptopChoices.ACER], then=Value(OSChoices.LINUX)),
        )
    )


def delete_inexpensive_laptops() -> None:
    Laptop.objects.filter(price__lt=1200).delete()



def bulk_create_chess_players(args: List[ChessPlayer]) -> None:
    ChessPlayer.objects.bulk_create(args)

def delete_chess_players() -> None:
    ChessPlayer.objects.filter(title="no title").delete()

def change_chess_games_won() -> None:
    """
    UPDATE
        chess_player
    SET
        games_won = 30
    WHERE
    title = "GM";
    """
    ChessPlayer.objects.filter(title='GM').update(games_won=30)

def change_chess_games_lost() -> None:
    ChessPlayer.objects.filter(title="no title").update(games_lost=25)

def change_chess_games_drawn() -> None:
    ChessPlayer.objects.update(games_drawn=10)

def grand_chess_title_gm() -> None:
    ChessPlayer.objects.filter(rating__gte=2400).update(title="GM")

def grand_chess_title_im() -> None:
    """
    UPDATE
        chess_player
    SET
        title = "IM"
    WHERE
        rating BETWEEN 2300 AND 2399;
    """
    ChessPlayer.objects.filter(rating__range=[2300, 2399]).update(title="IM")

def grand_chess_title_fm() -> None:
    ChessPlayer.objects.filter(rating__range=[2200, 2299]).update(title="FM")

def grand_chess_title_regular_player() -> None:
    ChessPlayer.objects.filter(rating__range=[0, 2199]).update(title="regular player")



def set_new_chefs() -> None:
    Meal.objects.update(
        chef=Case(
            When(meal_type=MealTypeChoices.BREAKFAST, then=Value("Gordon Ramsay")),
            When(meal_type=MealTypeChoices.LUNCH, then=Value("Julia Child")),
            When(meal_type=MealTypeChoices.DINNER, then=Value("Jamie Oliver")),
            When(meal_type=MealTypeChoices.SNACK, then=Value("Thomas Keller")),
        ),
    )

def set_new_preparation_times() -> None:
    Meal.objects.update(
        preparation_time=Case(
            When(meal_type=MealTypeChoices.BREAKFAST, then=Value("10 minutes")),
            When(meal_type=MealTypeChoices.LUNCH, then=Value("12 minutes")),
            When(meal_type=MealTypeChoices.DINNER, then=Value("15 minutes")),
            When(meal_type=MealTypeChoices.SNACK, then=Value("5 minutes")),
        )
    )

def update_low_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=[MealTypeChoices.BREAKFAST, MealTypeChoices.DINNER]).update(calories=400)

def update_high_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=[MealTypeChoices.LUNCH, MealTypeChoices.SNACK]).update(calories=700)

def delete_lunch_and_snack_meals() -> None:
    Meal.objects.filter(meal_type__in=[MealTypeChoices.LUNCH, MealTypeChoices.SNACK]).delete()