import elixir

elixir.metadata.bind = "sqlite:///test.db"

elixir.options_defaults['shortnames'] = True

Model = elixir.Entity

Field = elixir.Field

Integer = elixir.Integer
String = elixir.String
DateTime = elixir.DateTime

def commit():
    elixir.setup_all()
    elixir.create_all()
    elixir.session.commit()