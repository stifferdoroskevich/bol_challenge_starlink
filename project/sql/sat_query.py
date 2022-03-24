import click
from haversine import haversine

from database import connect_to_db


@click.group()
def cli1():
    pass


@cli1.command()
@click.option('-id', '--satellite_id', type=str, help="ID of the satellite (String)")
def get_last_position(satellite_id: str):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"""select sts.longitude, sts.latitude
                         from blue.starlink_ts sts
                         inner join (
                               select max(sts.creation_date) last_date_col 
                                 from blue.starlink_ts sts 
                                where sts.id = '{satellite_id}') last_date
                         on sts.creation_date = last_date.last_date_col 
                         where sts.id = '{satellite_id}'""")

    record = cursor.fetchone()
    if not record:
        click.echo(f"Data not found for ID: {satellite_id}")
        return
    cols = [column[0] for column in cursor. description]
    result = dict(zip(cols, record))
    click.echo(result)


@click.group()
def cli2():
    pass


@cli2.command()
@click.option('-gt', '--given_time', help="Time for the lookup (YYYY-MM-DD HH:MM:SS)")
@click.option('-lat', '--latitude', type=float, help="latitude")
@click.option('-long', '--longitude', type=float, help="longitude")
def get_closest_satellite(
        given_time: str,
        latitude: float,
        longitude: float,
):
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"""select sts.id , sts.longitude , sts.latitude 
                          from blue.starlink_ts sts 
                         where sts.creation_date =  '{given_time}'""")

    records = cursor.fetchall()
    if not records:
        click.echo("Satellite Not Found on given datetime")
        return
    cols = [column[0] for column in cursor.description]
    closest_sat = dict(zip(cols, records[0]))
    for record in records:
        satellite = dict(zip(cols, record))
        sat_pos = (satellite['latitude'], satellite['longitude'])
        closest_sat_pos = (closest_sat['latitude'], closest_sat['longitude'])
        position_on_earth = (latitude, longitude)
        if haversine(sat_pos, position_on_earth) < haversine(closest_sat_pos, position_on_earth):
            closest_sat = satellite

    click.echo(closest_sat)


cli = click.CommandCollection(sources=[cli1, cli2])

if __name__ == '__main__':
    cli()

