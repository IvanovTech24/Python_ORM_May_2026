import os
from typing import List

import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import ArtworkGallery, ChessPlayer, Meal, Dungeon, Workout, Laptop
from main_app.choices import LaptopChoices, OSChoices
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
