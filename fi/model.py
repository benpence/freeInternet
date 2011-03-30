import os

import elixir

import fi

# Make connection to sqlite
elixir.metadata.bind = "sqlite:///%s" % fi.DATABASE_PATH

# Global options
elixir.options_defaults['shortnames'] = True

# Model
Model = elixir.Entity
Field = elixir.Field

# Datatypes for models
Integer = elixir.Integer
String = elixir.String
DateTime = elixir.DateTime
PickleType = elixir.PickleType
ManyToOne = elixir.ManyToOne

def mapTables():
    elixir.setup_all()

def createDatabaseTables():
    elixir.create_all()

def commit():
    elixir.session.commit()