"""
Test custom django management commands.
"""
from unittest.mock import patch #mock the behaviour of database

from psycopg2 import OperationalError as Psycopg2Error #operational error exception that we might face when connecting to db before it is ready

from django.core.management import call_command #allows django to call command by name
from django.db.utils import OperationalError #another exception thrown by db depending on start up stage of db
from django.test import SimpleTestCase #for unit test, as we're testing without db

@patch('core.management.commands.wait_for_db.Command.check') #uses command.check provided by BaseCommand that allows to check status of db. patch decorator essentially mocks it
class CommandTests(SimpleTestCase):
    def test_wait_for_db_ready(self, patched_check): #basically the patch_check object from above 
        """Test waiting for database if database is ready"""
        patched_check.return_value = True # just return True, don't do anything else

        call_command('wait_for_db')

        patched_check.assert_called_once_with(database=['default']) #basically checks it we call the right thing once
