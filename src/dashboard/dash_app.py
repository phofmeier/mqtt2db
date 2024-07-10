from dash import Dash, Input, Output, callback, dash_table, dcc, html
from pymongo import MongoClient

CONNECTION_STRING = "localhost:27017"


app = Dash()


app.layout = [
    html.H1(children="Mongo DB Dash", style={"textAlign": "center"}),
]

client = MongoClient(CONNECTION_STRING)
db_names = client.list_database_names()
app.layout.append(
    dcc.Dropdown(db_names, db_names[0], id="db-names-selector-dropdown"),
)


app.layout.append(html.Div(children="", id="db-table"))


@callback(
    Output("db-table", "children"),
    Input("db-names-selector-dropdown", "value"),
)
def update_database(value):
    return make_table(value)


def make_table(db_name):
    database = client[db_name]
    collection_names = database.list_collection_names()
    values = []
    table_layout = []
    for collection in collection_names:
        values = list(database[collection].find({}, {"_id": False}))
        table_layout.append(html.H2(children=collection))
        table_layout.append(dash_table.DataTable(values))
    return table_layout


if __name__ == "__main__":
    app.run(debug=True)
