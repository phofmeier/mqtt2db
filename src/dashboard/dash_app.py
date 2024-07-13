from dash import Dash, Input, Output, callback, dash_table, dcc, html

from mqtt2db.config import Config
from mqtt2db.database.database import Database


def main():
    config = Config("config.yml")
    database = Database(config.get("database"))

    app = Dash()
    app.layout = [
        html.H1(children="Mongo DB Dash", style={"textAlign": "center"}),
    ]

    db_names = database.getDatabasesNames()
    app.layout.append(
        dcc.Dropdown(db_names, db_names[0], id="db-names-selector-dropdown"),
    )

    app.layout.append(html.Div(children="", id="db-table"))

    @callback(
        Output("db-table", "children"),
        Input("db-names-selector-dropdown", "value"),
    )
    def update_database_table(db_name):
        collection_names = database.getCollectionNames(db_name)
        values = []
        table_layout = []
        for collection in collection_names:
            values = database.getAllDataFrom(db_name, collection)
            table_layout.append(html.H2(children=collection))
            table_layout.append(dash_table.DataTable(values))
        return table_layout

    app.run(debug=True)


if __name__ == "__main__":
    main()
