from pytest import mark, fixture


@mark.functional
class TestEndToEnd:
    @fixture
    def setup(self):
        db_name = "postgres"
        db_type = "postgres"
        install(db_name, db_type)
        df = DbFactory(db_type)
        db = df.get_db(db_name)
        clear(db)
        fields = "url, description"
        db.salva_registro("positions", fields, "'https://test.com', 'test'")
        db.salva_registro("positions", fields, "'https://rabbit.com', 'rabbit'")
        db.salva_registro("positions", fields, "'https://cat.com', 'cats dogs cows'")
        db.salva_registro(
            "positions", fields, "'https://administrar.com', 'administraca'"
        )
        db.salva_registro(
            "positions",
            fields,
            "'https://andcondition.com', 'cat dog rabbit cow cucumber'",
        )
