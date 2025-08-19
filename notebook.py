# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "tinydb==4.8.2",
# ]
# ///

import marimo

__generated_with = "0.14.17"
app = marimo.App(width="medium")


# init
@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
    # Database Search

    This notebook searches a database.
    """
    )
    return


# source data
@app.cell
def _(mo):
    from tinydb import TinyDB

    db = TinyDB("db.json")

    records = db.all()
    fields = set()
    for record in records:
        fields.update(record.keys())
    sorted_fields = sorted(fields)
    return db, sorted_fields


# query
@app.cell
def _(mo, sorted_fields):
    search_string = mo.ui.text(
        value="",
        label="Search string",
    )
    search_field = mo.ui.dropdown(options=sorted_fields, label="Search field")

    run_button = mo.ui.run_button(label="Search")

    mo.vstack([mo.md("### DB Search"), search_string, search_field, run_button])
    return search_string, search_field, run_button


@app.cell
def _(mo, db, search_string, search_field, run_button):
    from tinydb import Query

    results = []
    if run_button.value:
        results = db.search(Query()[search_field.value] == search_string.value)
    return results


# render results
@app.cell
def _(mo, results):
    table = mo.ui.table(data=results)
    return table


@app.cell
def _(mo, table):
    mo.vstack([table, table.value])
    return table


if __name__ == "__main__":
    app.run()
