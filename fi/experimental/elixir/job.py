import model

class Job(model.Model):
    name = model.Field(model.String, primary_key=True)
    description = model.Field(model.String)
    
    def __repr__(self):
        return "<Job('%s','%s')>" % (self.name, self.description)

class Style(model.Model):
    name = model.Field(model.String, primary_key=True)
    description = model.Field(model.String)

    def __repr__(self):
        return "<Job('%s','%s')>" % (self.name, self.description)

Job(name="Testing", description="Just another story")
Job(name="Toasting", description="Just another toast")

model.commit()

Style(name="Testing", description="Just another story")
Style(name="Toasting", description="Just another toast")

model.commit()

print dir(Style)