from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        with patch('django.db.connection.ensure_connection') as ec:
            ec.return_value = True
            call_command('wait_for_db')
            self.assertEqual(ec.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        with patch('django.db.connection.ensure_connection') as ec:
            ec.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(ec.call_count, 6)
