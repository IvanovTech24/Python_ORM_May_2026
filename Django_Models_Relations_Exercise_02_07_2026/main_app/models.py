from django.db import models


class Author(models.Model):
    name = models.CharField(
        max_length=40,
    )

class Book(models.Model):
    """
    CREATE TABLE book(
        id ...,
        title VARCHAR(40),
        price DECIMAL(5, 2),
        author INT FOREIGN KEY (author)
                REFERENCES author(id)
                ON DELETE CASCADE
    );
    """

    title = models.CharField(
        max_length=40,
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )
    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
    )


class Song(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True,
    )

class Artist(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    songs = models.ManyToManyField(
        to=Song,
        related_name="artists",
    )