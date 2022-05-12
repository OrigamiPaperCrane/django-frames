from django.test import TestCase
import pandas as pd
import os

from example_app.example_app.settings import BASE_DIR


class BasicApplicationTest(TestCase):
    def setUp(self):
        raw_members = pd.read_csv(os.path.join(BASE_DIR.parent, 'members0.csv'))

        def test_insert_clubs():
            """create entities from the raw data"""
            pass

        def test_insert_members():
            """create the membership relation"""
            pass