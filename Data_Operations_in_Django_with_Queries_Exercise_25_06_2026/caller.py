import os
import django
from decimal import Decimal

from typing_extensions import Optional

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import QuerySet, F, Case, When, Value
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


def create_pet(name: str, species: str) -> str:
    """
    INSERT INTO
        pets("name", "species")
    VALUES
        ("Buddy", "Dog")
    RETURNING * ;
    """

    # pet = Pet(name=name, species=species) # No save in the db so far
    # pet.save()

    pet = Pet.objects.create(
        name= name,
        species= species,
    )
    return f"{pet.name} is a very cute {pet.species}!"



def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )
    return f"The artifact {name} is {age} years old!"

def rename_artifact(artifact: Artifact, new_name: str) -> None:
    """
    UPDATE
        artifacts
    SET
        name = new_name
    WHERE
        id = artifact.id;
    """
    if artifact.age > 250 and artifact.is_magical:
        artifact.name = new_name # No save to the db at this point
        artifact.save() # Real save happens here

def delete_all_artifacts() -> None:
    """ DELETE FROM artifacts """
    Artifact.objects.all().delete()



def show_all_locations() -> str:
    """
    SELECT * FROM locations
    ORDER BY id DESC;
    """
    locations = Location.objects.all().order_by('-id')
    return '\n'.join(f"{l.name} has a population of {l.population}!" for l in locations)

def new_capital() -> None:
    """
    SELECT * FROM locations LIMIT 1;

    UPDATE
        locations
    SET
        is_capital = True
    WHERE
        id = some_id;
    """
    # Solution 1
    first_location = Location.objects.first() # Can return silently None, doesn't return QuerySet
    first_location.is_capital = True
    first_location.save()

    # Solution 2
    # Location.objects.filter(pk=Location.objects.first().id).update(is_capital=True)

def get_capitals() -> QuerySet:
    """
    SELECT
        name
    FROM
        locations
    WHERE
        is_capital = True ;
    """
    return Location.objects.filter(is_capital=True).values('name')

def delete_first_location() -> None:
    Location.objects.first().delete()



def apply_discount() -> None:
    """
    SELECT * FROM cars;

    FOR LOOP
        UPDATE car...
    """
    for car in Car.objects.all():
        # 2008 -> "2008" -> 2 + 0 + 0 + 8 -> 10 / 100 -> 0.10
        percentage_off = Decimal(str(sum(int(d) for d in str(car.year)) / 100))
        # 10 000 * 0.10 -> 1 000
        discount = car.price * percentage_off
        car.price_with_discount = car.price - discount
        car.save()
        # Not the most optimal since we are making a request on every iteration

    # Option 2
    # Use bulk_update

    # Option 3
    # Get rid of the python loop

def get_recent_cars() -> QuerySet:
    """
    SELECT
        model, price_with_discount
    FROM
        cars
    WHERE
        year > 2020 ;
    """
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')

def delete_last_car() -> None:
    # last() could be None
    Car.objects.last().delete()



def show_unfinished_tasks() -> str:
    tasks = Task.objects.filter(is_finished=False)

    return '\n'.join(
        f"Task - {t.title} needs to be done until {t.due_date}!"
        for t in tasks
    )

def complete_odd_tasks() -> None:
    # TODO: research a better way
    all_tasks = Task.objects.all()
    complete_tasks = []

    for t in all_tasks:
        if t.id % 2 != 0:
            t.is_finished = True
            complete_tasks.append(t)

    Task.objects.bulk_update(complete_tasks, ['is_finished'])

def encode_and_replace(text: str, task_title: str) -> None:
    encoded_text = ''.join(chr(ord(l) - 3) for l in text)

    # Option 1: worst case
    # for t in Task.objects.filter(title=task_title):
    #     t.description = encoded_text
    #     t.save()

    # Option 2: Use bulk_update

    # Option 3: Direct update
    """
    UPDATE
        tasks
    SET 
        description = encoded_text
    WHERE 
        title = task_title;
    """
    Task.objects.filter(title=task_title).update(description=encoded_text)


def get_deluxe_rooms() -> str:
    deluxe_rooms = HotelRoom.objects.filter(room_type=HotelRoom.RoomType.DELUXE)
    # Try to do it in the filter
    even_rooms = [r for r in deluxe_rooms if r.id % 2 == 0]

    return '\n'.join(
        f"Deluxe room with number {r.room_number} costs {r.price_per_night}$ per night!"
        for r in even_rooms
    )

def increase_room_capacity() -> None:
    reserved_rooms = HotelRoom.objects.filter(is_reserved=True).order_by('id')
    previous_room: Optional[HotelRoom] = None

    # TODO: can be optimized with bulk_update()
    for r in reserved_rooms:
        if previous_room:
            r.capacity += previous_room.capacity
        else:
            r.capacity += r.id

        previous_room = r
        r.save()

def reserve_first_room() -> None:
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()

def delete_last_room() -> None:
    last_room = HotelRoom.objects.last()

    if not last_room.is_reserved:
        last_room.delete()



def grand_dexterity() -> None:
    """
    UPDATE
        character
    SET
        dexterity = 30;
    """
    Character.objects.update(dexterity=30)

def grand_intelligence() -> None:
    Character.objects.update(intelligence=40)

def grand_strength() -> None:
    Character.objects.update(strength=50)

def delete_characters() -> None:
    text = Character.objects.filter(inventory='The inventory is empty')
    if text:
        text.delete()



def update_characters_1() -> None:
    # Retrieve each group separately and save each object in a loop.
    mages = Character.objects.filter(class_name=Character.NameType.MAGE)
    warriors = Character.objects.filter(class_name=Character.NameType.WARRIOR)
    # Where class_name IN (..., ...);
    special_characters = Character.objects.filter(
        class_name__in=[Character.NameType.ASSASSIN, Character.NameType.SCOUT]
    )

    for m in mages:
        m.level += 3
        m.intelligence -= 7
        m.save()

    for w in warriors:
        w.hit_points //= 2
        w.dexterity += 4
        w.save()

    for sc in special_characters:
        sc.inventory = "The inventory is empty"
        sc.save()

def update_characters_2() -> None:
    Character.objects.filter(class_name=Character.NameType.MAGE).update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7,
    )
    Character.objects.filter(class_name=Character.NameType.WARRIOR).update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4,
    )
    Character.objects.filter(class_name__in=[Character.NameType.ASSASSIN, Character.NameType.SCOUT]).update(
        inventory="The inventory is empty"
    )

def update_characters_3() -> None:
    Character.objects.update(
        level=Case(
            When(class_name=Character.NameType.MAGE, then=F('level') + 3),
            default=F('level'),
        ),
        intelligence=Case(
            When(class_name=Character.NameType.MAGE, then=F('intelligence') - 7),
            default=F('intelligence'),
        ),
        hit_points=Case(
            When(class_name=Character.NameType.WARRIOR, then=F('hit_points') / 2),
            default=F('hit_points'),
        ),
        dexterity=Case(
            When(class_name=Character.NameType.WARRIOR, then=F('dexterity') + 4),
            default=F('dexterity'),
        ),
        inventory=Case(
            When(class_name__in=[Character.NameType.ASSASSIN, Character.NameType.SCOUT],
                 then=Value("The inventory is empty")),
            default=F('inventory')
        ),
    )

def fuse_characters(first_character: Character, second_character: Character) -> None:
    inventory = None

    if first_character.class_name in [Character.NameType.MAGE, Character.NameType.SCOUT]:
        inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom'
    elif first_character.class_name in [Character.NameType.WARRIOR, Character.NameType.ASSASSIN]:
        inventory = 'Dragon Scale Armor, Excalibur'

    Character.objects.create(
        name=first_character.name + ' ' + second_character.name,
        class_name=Character.NameType.FUSION,
        level=(first_character.level + second_character.level) // 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory=inventory
    )
    first_character.delete()
    second_character.delete()
