import model

class Job(model.Model):
    name = model.Field(model.String, primary_key=True)
    description = model.Field(model.String)
    
    def __repr__(self):
        return "<Job('%s','%s')>" % (self.name, self.description)

model.commit()

job = Job(name="Testing", description="Just another story")
job = Job(name="Toasting", description="Just another toast")
model.commit()