import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dash_table, dcc, html

from mqtt2db.config import Config
from mqtt2db.database.database import Database


def main():
    config = Config("config.yml")
    database = Database(config.get("database"))

    app = Dash()
    app.layout = [
        html.H1(children="Mongo DB Dash", style={"textAlign": "center"}),
        dcc.Interval(
            id="update-component",
            interval=1.0 * 60 * 1000,  # in milliseconds
            n_intervals=0,
        ),
    ]

    db_names = database.getDatabasesNames()
    app.layout.append(
        html.Div(
            [
                "Database: ",
                dcc.Dropdown(db_names, db_names[0], id="db-names-selector-dropdown"),
            ]
        ),
    )

    app.layout.append(html.Div(children="", id="db-static-table"))
    app.layout.append(html.Div(children="", id="db-timed-data"))

    @callback(
        Output("db-static-table", "children"),
        Input("db-names-selector-dropdown", "value"),
        Input("update-component", "n_intervals"),
    )
    def update_database_table(db_name, update_intervals):
        collection_names = database.getCollectionNames(db_name, "static")
        table_layout = []
        for collection in collection_names:
            values = pd.DataFrame(database.getAllDataFrom(db_name, collection))
            table_layout.append(html.H2(children=collection))
            table_layout.append(dash_table.DataTable(values.to_dict("records")))
        return table_layout

    @callback(
        Output("db-timed-data", "children"),
        Input("db-names-selector-dropdown", "value"),
        Input("update-component", "n_intervals"),
    )
    def update_timed_data(db_name, update_intervals):
        timestamp_name = config.get("database")["timed"]["time_field_name"]
        collection_names = database.getCollectionNames(db_name, "timed")
        table_layout = []
        for collection in collection_names:
            df = pd.DataFrame(database.getAllTimedDataFrom(db_name, collection))
            data_names = list(df.columns)
            data_names = [
                name
                for name in data_names
                if name not in [timestamp_name, "index", "_id"]
            ]
            table_layout.append(html.H2(children=collection))
            table_layout.append(
                dcc.Graph(
                    figure=px.line(
                        df,
                        x=timestamp_name,
                        y=data_names,
                    )
                )
            )
        return table_layout

    app.run(debug=True)


if __name__ == "__main__":
    main()
