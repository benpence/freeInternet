import sqlite3
import commands

print commands.getoutput("rm x.db")
conn = sqlite3.connect('x.db')
c = conn.cursor()

# Create tables

tableCreation = [
          """\
          create table jobs \
          (jobID real, credit real, binary text, input real)\
          """,
          """create table status \
          (jobID real, client text, accepted text, returned text, output text)
          """,
          """\
          create table credits \
          (client real, credit real)\
          """
          ]

for t in tableCreation:
    c.execute(t)

# Insert a row of data
c.execute("""\
          insert into jobs\
          values (?,   ?,   ?,       ?)\
          """,   (1, 200, '1', '1input'))

# Save (commit) the changes
conn.commit()

c.execute("select * from jobs order by jobID")
for row in c:
    print row

# We can also close the cursor if we are done with it
c.close()
