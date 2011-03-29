import elixir

elixir.metadata.bind = "sqlite:///test.db"

elixir.options_defaults['shortnames'] = True

Model = elixir.Entity

Field = elixir.Field

Integer = elixir.Integer
String = elixir.String
DateTime = elixir.DateTime

def commit():
    elixir.session.commit()
    
class Job(Model):
    name = Field(String, primary_key=True)
    description = Field(String)

    def __repr__(self):
        return "<Job('%s','%s')>" % (self.name, self.description)

class Style(Model):
    name = Field(String, primary_key=True)
    description = Field(String)

    def __repr__(self):
        return "<Job('%s','%s')>" % (self.name, self.description)

elixir.setup_all()

print Job.query.all()