import sys
import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

def create_tables(conn):
    conn.execute(
    """
        CREATE TABLE IF NOT EXISTS conferences (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            short_name VARCHAR NOT NULL,
            abbreviation VARCHAR NOT NULL
        );
    """)

    conn.commit()
    # conference_id INTEGER NOT NULL,
    # FOREIGN KEY(conference_id) REFERENCES conferences(id)
    conn.execute(
    """
        CREATE TABLE IF NOT EXISTS teams (
            id SERIAL PRIMARY KEY,
            school VARCHAR NOT NULL,
            mascot VARCHAR NOT NULL,
            abbreviation VARCHAR NOT NULL,
            logos VARCHAR NOT NULL,
            conference_id INTEGER REFERENCES conferences
        );
    """)
    conn.commit()

def import_records(conn):
    # insert rows into conferences table
    with open("conferences.csv", "r", encoding="utf-8") as f:
        csv_file = csv.reader(f)
        next(csv_file) # first row is table fields
        for id, name, short_name, abbreviation in csv_file:
            query = "INSERT INTO conferences(name, short_name, abbreviation) VALUES('{name}', '{short_name}', '{abbreviation}')".format(name=name, short_name=short_name, abbreviation=abbreviation)
            conn.execute(query)

    conn.commit()

    # insert rows into teams table
    with open("teams.csv", "r", encoding="utf-8") as f:
        csv_file = csv.reader(f)
        next(csv_file) # first row is table fields
        for id, school, mascot, abbreviation, conference_id, logos in csv_file:
            query = "INSERT INTO teams(school, mascot, abbreviation, logos, conference_id, create_date) VALUES('{school}', '{mascot}', '{abbreviation}', '{logos}', {conference_id}, '{create_date}')".format(
                    school=school, mascot=mascot,
                    abbreviation=abbreviation, logos=logos,
                    conference_id=conference_id, create_date=datetime.utcnow()
            )
            conn.execute(query)

    conn.commit()



# engine = create_engine("sqlite:///python_courser.db")
# conn = engine.connect()
def main():
    engine =create_engine("postgresql://jay:pass@localhost:5432/itse2302")
    db = scoped_session(sessionmaker(bind=engine))
    create_tables(db)
    import_records(db)
    return 0


if __name__ == "__main__":
    sys.exit(main())
