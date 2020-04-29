from mpt import create_app

database_name = "mpt_test"
database_path = "postgresql://{}/{}".format(
    'postgres@localhost:5433',
    database_name
)

app = create_app(database_path=database_path)
