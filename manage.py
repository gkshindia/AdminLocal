from flask.cli import FlaskGroup
from project import create_app, db
from project.app.models import User
import click

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('create_admin')
@click.option('--fullname', required=True, default="Gourav K S", show_default=True)
@click.option('--username', required=True, default="gourav", show_default=True)
@click.option('--email', required=True, default="gourav@test.com", show_default=True)
@click.option('--pwd', required=True, default="testpass123", show_default=True)
def create_admin(fullname, username, email, pwd):
    user = User(full_name=fullname, username=username, email=email,
                password=pwd, admin=True)
    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    cli()
