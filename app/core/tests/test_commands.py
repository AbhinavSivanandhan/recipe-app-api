"""
Test custom django management commands.
"""
from unittest.mock import patch #mock the behaviour of database

from psycopg2 import OperationalError as Psycopg2Error #operational error exception that we might face when connecting to db before it is ready

from django.core.management import call_command #allows django to call command by name
from django.db.utils import OperationalError #another exception thrown by db depending on start up stage of db
from django.test import SimpleTestCase #for unit test, as we're testing without db

@patch('core.management.commands.wait_for_db.Command.check') #uses command.check provided by BaseCommand that allows to check status of db. patch decorator essentially mocks it. this makes sure all test functions can access patched_check argument
class CommandTests(SimpleTestCase):
    def test_wait_for_db_ready(self, patched_check): #basically the patch_check object from above 
        """Test waiting for database if database is ready"""
        patched_check.return_value = True # just return True, don't do anything else

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default']) #basically checks it we call the right thing once

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check): #Note on decorators+argument is, inside decorators comes first in order of arguments, outside decorator comes later
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6) #2 times to check Psycopg2Error, 3 times to check OperationalError, final time to actually get returned value. so our code should call 6 times, make sure we do that there!
        patched_check.assert_called_with(databases=['default'])
