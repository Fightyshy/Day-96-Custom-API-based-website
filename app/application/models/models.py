from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class PlayerCharacter(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    char_id: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(String(length=200))
    rp_checker: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # TODO parent of roleplaying, 1-1
    roleplaying: Mapped["Roleplaying"] = relationship(
        back_populates="character"
    )
    # TODO parent of hooks, 1-1
    business: Mapped["Business"] = relationship(back_populates="character")
    # TODO maybe child of flask-login user with usermixin, 1-1


class Roleplaying(db.Model):
    __tablename__ = "roleplaying"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # character ic
    alias: Mapped[str] = mapped_column(String(length=40))
    age: Mapped[str] = mapped_column(String(length=5), nullable=False)
    gender: Mapped[str] = mapped_column(String(length=20), nullable=False)
    sexuality: Mapped[str] = mapped_column(String(length=30), nullable=False)
    relationship_status: Mapped[str] = mapped_column(String(length=20))
    tagline: Mapped[str] = mapped_column(String(length=50))

    # character ooc
    twitter: Mapped[str] = mapped_column(String(length=15))
    website: Mapped[str] = mapped_column(String(length=40))
    discord: Mapped[str] = mapped_column(String(length=32))
    oc_notes: Mapped[str] = mapped_column(String(length=90))

    # relationships
    # TODO parent of hooks, 1-many
    hooks: Mapped[List["Hook"]] = relationship(back_populates="roleplaying")
    # TODO parent of traits, 1-many
    traits: Mapped[List["Trait"]] = relationship(back_populates="roleplaying")

    # TODO child of character, many-1
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    character: Mapped["PlayerCharacter"] = relationship(
        back_populates="roleplaying"
    )


class Hook(db.Model):
    __tablename__ = "rp-hooks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(length=30), nullable=False)
    body: Mapped[str] = mapped_column(String(length=240), nullable=False)

    # TODO child of roleplaying, many(3)-1
    roleplay_id: Mapped[int] = mapped_column(ForeignKey("roleplaying.id"))
    roleplaying: Mapped["Roleplaying"] = relationship(back_populates="hooks")


class Trait(db.Model):
    __tablename__ = "rp-traits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    type: Mapped[int] = mapped_column(String(length=8), nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    trait: Mapped[int] = mapped_column(String(length=20), nullable=False)

    # TODO child of roleplaying, many([1-2]<->5-10)-1
    roleplay_id: Mapped[int] = mapped_column(ForeignKey("roleplaying.id"))
    roleplaying: Mapped["Roleplaying"] = relationship(
        back_populates="traits"
    )


class Business(db.Model):
    __tablename__ = "business"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    venue_name: Mapped[str] = mapped_column(String, nullable=False)
    venue_tagline: Mapped[str] = mapped_column(String)
    venue_website: Mapped[str] = mapped_column(String)
    venue_operating_times: Mapped[str] = mapped_column(String)
    venue_discord: Mapped[str] = mapped_column(String)
    venue_twitter: Mapped[str] = mapped_column(String)

    # TODO parent of VenueAddress, 1-1
    # TODO parent of staff, 1-1
    venue_address: Mapped["VenueAddress"] = relationship(
        back_populates="business"
    )
    venue_staff: Mapped["VenueStaff"] = relationship(back_populates="business")

    # TODO child of character, 1-1
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    character: Mapped["PlayerCharacter"] = relationship(
        back_populates="business", single_parent=True
    )


class VenueAddress(db.Model):
    __tablename__ = "venue-address"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    housing_zone: Mapped[int] = mapped_column(String, nullable=False)
    is_apartment: Mapped[bool] = mapped_column(Boolean, nullable=False)
    housing_ward: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    ward_plot: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    apartment_num: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    server: Mapped[str] = mapped_column(String, nullable=False)

    # TODO child of Buisness, 1-1
    business_id: Mapped[int] = mapped_column(ForeignKey("business.id"))
    business: Mapped["Business"] = relationship(
        back_populates="venue_address", single_parent=True
    )


class VenueStaff(db.Model):
    __tablename__ = "venue-staff"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    staff_role: Mapped[str] = mapped_column(String)
    staff_discord: Mapped[str] = mapped_column(
        String(length=32), nullable=False
    )
    staff_twitter: Mapped[str] = mapped_column(
        String(length=15), nullable=False
    )
    staff_website: Mapped[str] = mapped_column(
        String(length=40), nullable=False
    )

    # TODO child of Business, 1-1
    business_id: Mapped[int] = mapped_column(ForeignKey("business.id"))
    business: Mapped["Business"] = relationship(
        back_populates="venue_staff", single_parent=True
    )
