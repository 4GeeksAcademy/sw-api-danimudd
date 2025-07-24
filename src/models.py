from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorite_planets: Mapped[list["Planet"]] = relationship(
        "Planet", back_populates="user")

    favorite_characters: Mapped[list["Character"]] = relationship(
        "Character", back_populates="user")

    favorite_starships: Mapped[list["Starship"]] = relationship(
        "Starship", back_populates="user")

    favorite_weapons: Mapped[list["Weapon"]] = relationship(
        "Weapon", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_planets": [planet.serialize() for planet in self.favorite_planets],
            "favorite_characters": [character.serialize() for character in self.favorite_characters],
            "favorite_starships": [starship.serialize() for starship in self.favorite_starships],
            "favorite_weapons": [weapon.serialize() for weapon in self.favorite_weapons]
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    climate: Mapped[str] = mapped_column(String(), nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="favorite_planets")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(), nullable=False)
    species: Mapped[str] = mapped_column(String(), nullable=False)

    origin_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    origin: Mapped["Planet"] = relationship("Planet")

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="favorite_characters")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "species": self.species,
            "origin": self.origin.name if self.origin else None,
            "user": self.user.email if self.user else None
        }


class Starship(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    cargo_space: Mapped[str] = mapped_column(String(), nullable=False)
    speed: Mapped[int] = mapped_column(nullable=False)
    occupancy: Mapped[int] = mapped_column(nullable=False)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="favorite_starships")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "cargo_space": self.cargo_space,
            "speed": self.speed,
            "occupancy": self.occupancy,
        }


class Weapon(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    class_type: Mapped[str] = mapped_column(String(), nullable=False)
    weilder_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    weilder: Mapped["Character"] = relationship("Character")
    power_source: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    user: Mapped[Optional["User"]] = relationship(
        "User", back_populates="favorite_weapons")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "class_type": self.class_type,
            "weilder": self.weilder.name if self.weilder else None,
            "power_source": self.power_source,
        }
