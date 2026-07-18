import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from typing import List
from main_app.models import ArtworkGallery, ChessPlayer, Meal, Dungeon, Workout, Laptop
from main_app.choices import LaptopChoices, OSChoices, MealTypeChoices, DifficultyChoices, WorkoutTypeChoices
from django.db.models import F, Case, When, Value, QuerySet


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
    ArtworkGallery.objects.bulk_create([first_art, second_art])


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
    # SELECT
    #   *
    # FROM
    #   meals
    # WHERE
    #   meal_type = 'Breakfast'
    #           OR
    #   meal_type = 'Dinner';
    Meal.objects.filter(meal_type__in=[MealTypeChoices.BREAKFAST, MealTypeChoices.DINNER]).update(calories=400)
    # Solution with Q objects
    # Meal.objects.filter(Q(meal_type=MealTypeChoices.BREAKFAST) | Q(meal_type=MealTypeChoices.DINNER))

def update_high_calorie_meals() -> None:
    Meal.objects.filter(meal_type__in=[MealTypeChoices.LUNCH, MealTypeChoices.SNACK]).update(calories=700)
    # Solution with Q objects
    #Meal.objects.filter(Q(meal_type=MealTypeChoices.LUNCH) | Q(meal_type=MealTypeChoices.SNACK)).update(calories=700)

def delete_lunch_and_snack_meals() -> None:
    Meal.objects.filter(meal_type__in=[MealTypeChoices.LUNCH, MealTypeChoices.SNACK]).delete()
    # Solution with Q objects
    #Meal.objects.filter(Q(meal_type=MealTypeChoices.LUNCH) | Q(meal_type=MealTypeChoices.SNACK)).delete()



def show_hard_dungeons() -> str:
    hard_dungeons = Dungeon.objects.filter(difficulty=DifficultyChoices.HARD).order_by('-location')

    return '\n'.join(
        f"{h.name} is guarded by {h.boss_name} who has {h.boss_health} health points!"
                     for h in hard_dungeons)

def bulk_create_dungeons(args: List[Dungeon]) -> None:
    Dungeon.objects.bulk_create(args)

def update_dungeon_names() -> None:
    Dungeon.objects.update(
        name=Case(
            When(difficulty=DifficultyChoices.EASY, then=Value("The Erased Thombs")),
            When(difficulty=DifficultyChoices.MEDIUM, then=Value("The Coral Labyrinth")),
            When(difficulty=DifficultyChoices.HARD, then=Value("The Lost Haunt")),
            # else:
            default=F('name')
        ),
    )

def update_dungeon_bosses_health() -> None:
    """
    UPDATE
        dungeon
    SET
        boss_health = 500
    WHERE
        difficulty != 'Easy';
    """
    # Solution with filter()
    # Dungeon.objects.filter(difficulty__in=["Medium", "Hard"]).update(boss_health=500)

    # Solution with exclude()
    Dungeon.objects.exclude(difficulty=DifficultyChoices.EASY).update(boss_health=500)

    # Solution with filter(difficulty__ne=)
    # Dungeon.objects.filter(difficulty__ne=DifficultyChoices.EASY).update(boss_health=500)

def update_dungeon_recommended_levels() -> None:
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty=DifficultyChoices.EASY, then=Value(25)),
            When(difficulty=DifficultyChoices.MEDIUM, then=Value(50)),
            When(difficulty=DifficultyChoices.HARD, then=Value(75)),
            # else:
            default=F('recommended_level')
        ),
    )

def update_dungeon_rewards() -> None:
    Dungeon.objects.update(
        reward=Case(
            When(boss_health=500, then= Value("1000 Gold")),
            # LIKE 'E%'
            When(location__startswith='E', then= Value("New dungeon unlocked")),
            # LIKE '%s'
            When(location__endswith='s', then= Value("Dragonheart Amulet")),
            # else:
            default=F('reward')
        ),
    )

def set_new_locations() -> None:
    Dungeon.objects.update(
        location=Case(
            When(recommended_level=25, then=Value("Enchanted Maze")),
            When(recommended_level=50, then=Value("Grimstone Mines")),
            When(recommended_level=75, then=Value("Shadowed Abyss")),
            # else:
            default=F('location')
        ),
    )



def show_workouts() -> str:
    workouts = (Workout.objects.filter(
        workout_type__in=[WorkoutTypeChoices.CALISTHENICS, WorkoutTypeChoices.CROSSFIT])
                .order_by('id')
                )

    return '\n'.join(f"{w.name} from {w.workout_type} type has {w.difficulty} difficulty!" for w in workouts)

def get_high_difficulty_cardio_workouts() -> QuerySet[Workout]:
    """
    WHERE
        difficulty = 'Hard'
                AND
        workout_type = 'Cardio';
    """
    return Workout.objects.filter(difficulty='High', workout_type='Cardio').order_by('instructor')


def set_new_instructors() -> None:
    Workout.objects.update(
        instructor=Case(
            When(workout_type=WorkoutTypeChoices.CARDIO, then=Value("John Smith")),
            When(workout_type=WorkoutTypeChoices.STRENGTH, then=Value("Michael Williams")),
            When(workout_type=WorkoutTypeChoices.YOGA, then=Value("Emily Johnson")),
            When(workout_type=WorkoutTypeChoices.CROSSFIT, then=Value("Sarah Davis")),
            When(workout_type=WorkoutTypeChoices.CALISTHENICS, then=Value("Chris Heria")),
            default=F('instructors')
        )
    )

def set_new_duration_times() -> None:
    Workout.objects.update(
        duration=Case(
            When(instructor="John Smith", then=Value("15 minutes")),
            When(instructor="Sarah Davis", then=Value("30 minutes")),
            When(instructor="Chris Heria", then=Value("45 minutes")),
            When(instructor="Michael Williams", then=Value("1 hour")),
            When(instructor="Emily Johnson", then=Value("1 hour and 30 minutes")),
            default=F('duration')
        ),
    )

def delete_workouts() -> None:
    Workout.objects.exclude(workout_type__in=[WorkoutTypeChoices.STRENGTH, WorkoutTypeChoices.CALISTHENICS]).delete()