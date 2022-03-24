import click

from parsing.parsing import parser, insert_satellites
from sql.database import connect_to_db, create_tables, create_schema


@click.group()
def cli1():
    pass


@cli1.command(help='Import Data From Json')
def import_json():
    clean_data = parser()
    click.echo(insert_satellites(clean_data))


@click.group()
def cli2():
    pass


@cli2.command(help='Delle Al Rows')
def delete_all_rows():
    connection = connect_to_db()
    cursor = connection.cursor()
    sql = "DELETE FROM blue.starlink_ts"
    try:
        with connection:
            cursor.execute(sql)
            connection.commit()
            click.echo("All Rows Deleted")
    except Exception as e:
        click.echo(e.args)


@click.group()
def cli3():
    pass


@cli3.command()
def init_db():
    """Create Schema 'blue', and create table 'starlink_ts'"""
    create_schema()
    create_tables()


cli = click.CommandCollection(sources=[cli1, cli2, cli3])


if __name__ == '__main__':
    cli()
