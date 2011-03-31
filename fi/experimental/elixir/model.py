import elixir
import random

elixir.metadata.bind = "sqlite:///:memory:"

elixir.options_defaults['shortnames'] = True

Model = elixir.Entity

Field = elixir.Field

Integer = elixir.Integer
String = elixir.String
DateTime = elixir.DateTime

def commit():
    elixir.session.commit()
    
class Todd(Model):
    thing = Field(Integer, primary_key=True)
    second_thing = Field(Integer, primary_key=True)
    elixir.using_options(order_by=('thing', 'second_thing'))

    def __repr__(self):
        return "<Todd(%d)>" % self.thing

elixir.setup_all()
elixir.create_all()

first = range(10)
random.shuffle(first)
second = range(10)
random.shuffle(second)
for i in first:
    for j in second:
        Todd(
            thing=i,
            second_thing=j
        )

elixir.session.commit()

for todd in Todd.query.filter(Todd.thing != 5):
    print todd.thing, todd.second_thing