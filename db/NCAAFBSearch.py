import sys
import os
import csv

from sqlalchemy import create_engine



def search(conn, name):
    records = conn.execute(
        f"SELECT school, mascot, t.abbreviation FROM\
        teams t INNER JOIN conferences c ON t.conference_id = c.id where lower(c.name) = LOWER('{name}')"
    ).fetchall()

    print(f"Teams in Conference: {name}")
    for row in records:
        print(f"{row[0]}: ({row[1]}) - {row[2]}")


def report(conn):
    records = conn.execute(
        f"SELECT c.name, count(t.conference_id) AS numbers FROM conferences c INNER JOIN teams t ON t.conference_id = c.id GROUP BY name ORDER BY COUNT(*) DESC, name"
    )
    print(f"# \tConference \tCount")
    for idx, row in enumerate(records):
        print(f"{idx} \t{row[0]} \t\t{row[1]}")


def main():
    engine =create_engine("postgresql://jay:pass@localhost:5432/itse2302")
    conn = engine.connect()
    # Not suer if you need a function call here or you want to take user input with 'input' function
    search(conn, "ACC")
    report(conn)
    return 0




if __name__ == "__main__":
    sys.exit(main())
