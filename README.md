1. RAW SQL
statement = "INSERT INTO films (title, director, year) VALUES ('Doctor Strange', 'Scott Derrickson', '2016')"
conn.execute(statement)
2. SQLAlchemy expression
statement = films.insert().values(title="Doctor Strange", director="Scott Derrickson", year="2016")
conn.execute(statement)
3. SQLAlchemy ORM
doctor_strange = Film("Doctor Strange", "Scott Derrickson", "2016")
db_session.add(doctor_strange)