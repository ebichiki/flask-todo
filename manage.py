from __future__ import print_function
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from todo import app, db

# manager = Manager(app)
#
# @manager.command
# def init_db():
#     db.create_all()

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()