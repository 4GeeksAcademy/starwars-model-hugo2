from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favourites: Mapped[List["Favourite"]] = relationship(
        "Favourite",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def serialize(self):
        return {"id": self.id,
                "email": self.email
                }


class Favourite(db.Model):
    __tablename__ = "favourite"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="favourites")

    character_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("character.id"), nullable=True)
    planet_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("planet.id"), nullable=True)
    vehicle_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("vehicle.id"), nullable=True)

    character: Mapped[Optional["Character"]] = relationship("Character")
    planet: Mapped[Optional["Planet"]] = relationship("Planet")
    vehicle: Mapped[Optional["Vehicle"]] = relationship("Vehicle")

    __table_args__ = (
        CheckConstraint(
            "(CASE WHEN character_id IS NOT NULL THEN 1 ELSE 0 END + "
            " CASE WHEN planet_id IS NOT NULL THEN 1 ELSE 0 END + "
            " CASE WHEN vehicle_id IS NOT NULL THEN 1 ELSE 0 END) = 1",
            name="ck_favourite_exactly_one_target",
        ),
    )


class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    climate: Mapped[Optional[str]] = mapped_column(String(50))
    diameter: Mapped[Optional[int]] = mapped_column(Integer)
    population: Mapped[Optional[int]] = mapped_column(Integer)

    character: Mapped[Optional["Character"]] = relationship(
        "Character",
        back_populates="homeland"
    )


class Character(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(50))
    skin_color: Mapped[Optional[str]] = mapped_column(String(50))
    hair_color: Mapped[Optional[str]] = mapped_column(String(50))
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"), nullable=False)

    homeland: Mapped["Planet"] = relationship(
        "Planet", back_populates="character", uselist=False)
    vehicles: Mapped[List["Vehicle"]] = relationship(
        "Vehicle", back_populates="character")


class Vehicle(db.Model):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    passengers: Mapped[Optional[int]] = mapped_column(Integer)
    cargo_capacity: Mapped[Optional[int]] = mapped_column(Integer)
    crew: Mapped[Optional[int]] = mapped_column(Integer)

    character_id: Mapped[int] = mapped_column(
        ForeignKey("character.id"), nullable=False)
    character: Mapped["Character"] = relationship(
        "Character", back_populates="vehicles")
