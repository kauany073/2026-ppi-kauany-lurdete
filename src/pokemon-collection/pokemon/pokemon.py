from flask import Blueprint, render_template, request, redirect, url_for

from .db import get_db


bp = Blueprint("pokemon", __name__)


@bp.route("/")
def index():
    db = get_db()

    pokemons = db.execute(
        "SELECT id, name, type, level, power FROM pokemon"
    ).fetchall()

    return render_template("pokemon/index.html", pokemons=pokemons)


@bp.route("/create", methods=("GET", "POST"))
def create():

    if request.method == "POST":
        name = request.form["name"]
        type = request.form["type"]
        level = request.form["level"]
        power = request.form["power"]

        db = get_db()

        db.execute(
            """
            INSERT INTO pokemon (name, type, level, power)
            VALUES (?, ?, ?, ?)
            """,
            (name, type, level, power)
        )

        db.commit()

        return redirect(url_for("pokemon.index"))

    return render_template("pokemon/create.html")

@bp.route("/<int:id>/update", methods=("GET", "POST"))
def update(id):
    db = get_db()

    pokemon = db.execute(
        "SELECT * FROM pokemon WHERE id = ?",
        (id,)
    ).fetchone()

    if request.method == "POST":
        name = request.form["name"]
        type = request.form["type"]
        level = request.form["level"]
        power = request.form["power"]

        db.execute(
            """
            UPDATE pokemon
            SET name = ?, type = ?, level = ?, power = ?
            WHERE id = ?
            """,
            (name, type, level, power, id)
        )

        db.commit()

        return redirect(url_for("pokemon.index"))

    return render_template("pokemon/update.html", pokemon=pokemon)

@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    db = get_db()

    db.execute(
        "DELETE FROM pokemon WHERE id = ?",
        (id,)
    )

    db.commit()

    return redirect(url_for("pokemon.index"))