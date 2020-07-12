import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models.models import setup_db, Restaurant, Location, Age_policy, Category, Cuisine

JWT_TOKEN = 'bearer token'


class ConciergeApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.database_path = 'postgres://localhost:5432/test_concierge'
        setup_db(self.app, self.database_path)

        self.new_restaurant = {
            'name': 'Al Mahara',
            'cuisine_id': 17,
            'location_id': 9,
            'age_policy_id': 2,
            'category_id': 2,
            'rating': 5,
            'address': 'Burj Al Arab hotel',
            'phone_number': '97144555555',
            'prebooking_required': True
        }

        self.new_restaurant_error = {
            'name': 'Amazonico',
            'rating': 4,
            'address': 'DIFC'
        }

        self.edit_rest = {
            'cuisine_id': 17
        }

        self.edit_rest_error = {
            'category_id': 77
        }

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': JWT_TOKEN
        }

    def tearDown(self):
        pass

# GET method tests
# -------------------------------------------------------------------

    def test_get_restaurants_public_info(self):
        req = self.client().get('/restaurants-public')
        response = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(response['success'], True)
        self.assertTrue(response['total_restaurants'])
        self.assertTrue(response['total_pages'])
        self.assertTrue(response['current_page'])
        self.assertTrue(len(response['restaurants']))

    def test_get_restaurants_public_info_not_found(self):
        req = self.client().get('/restaurants-public?page=88&per_page=10')
        response = json.loads(req.data)

        self.assertEqual(req.status_code, 404)
        self.assertEqual(response['success'], False)
        self.assertEqual(response['error'], 404)
        self.assertEqual(response['message'], 'Page not found')

    def test_get_restaurants_detailed(self):
        req = self.client().get('/restaurants')
        response = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(response['success'], True)
        self.assertTrue(response['total_restaurants'])
        self.assertTrue(response['total_pages'])
        self.assertTrue(response['current_page'])
        self.assertTrue(len(response['restaurants']))

    def test_get_restaurants_detailed_not_found(self):
        req = self.client().get('/restaurants?page=88&per_page=10')
        response = json.loads(req.data)

        self.assertEqual(req.status_code, 404)
        self.assertEqual(response['success'], False)
        self.assertEqual(response['error'], 404)
        self.assertEqual(response['message'], 'Page not found')

    def test_search_restaurant(self):
        req = self.client().get('/restaurants/search?keyword=bread')
        response = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(response['success'], True)
        self.assertTrue(response['results'])
        self.assertTrue(response['total_pages'])
        self.assertTrue(response['current_page'])
        self.assertTrue(len(response['restaurants']))

    def test_search_not_found(self):
        req = self.client().get('/restaurants/search?keyword=shawshank')
        response = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(response['success'], False)
        self.assertEqual(response['message'], 'No result')

    def test_get_individual_rest(self):
        req = self.client().get('/restaurants/9')
        response = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(response['success'], True)
        self.assertTrue(response['restaurant'])

    def test_get_individual_rest_not_found(self):
        req = self.client().get('/restaurants/99')
        response = json.loads(req.data)

        self.assertEqual(req.status_code, 404)
        self.assertEqual(response['success'], False)
        self.assertEqual(response['error'], 404)
        self.assertEqual(response['message'], 'Page not found')

    def test_get_categories(self):
        req = self.client().get('/categories')
        response = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(response['success'], True)
        self.assertTrue(len(response['categories']))

    def test_get_restaurant_by_category(self):
        req = self.client().get('/categories/2/restaurants')
        response = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(response['success'], True)
        self.assertTrue(response['total_restaurants'])
        self.assertTrue(len(response['restaurants']))

    def test_get_restaurant_by_category_not_found(self):
        req = self.client().get('/categories/6/restaurants')
        response = json.loads(req.data)

        self.assertEqual(req.status_code, 404)
        self.assertEqual(response['success'], False)
        self.assertEqual(response['error'], 404)
        self.assertEqual(response['message'], 'Page not found')

# POST method tests
# -------------------------------------------------------------------

    def test_post_new_restaurant(self):
        req = self.client().post('/restaurants', json=self.new_restaurant)
        response = json.loads(req.data)

        restaurant = Restaurant.query.get(response['created'])

        self.assertEqual(req.status_code, 200)
        self.assertEqual(response['success'], True)
        self.assertTrue(response['created'])
        self.assertTrue(restaurant)

    def test_post_new_restaurant_error(self):
        req = self.client().post(
            '/restaurants', json=self.new_restaurant_error)
        response = json.loads(req.data)

        self.assertEqual(req.status_code, 400)
        self.assertEqual(response['success'], False)
        self.assertEqual(response['error'], 400)
        self.assertEqual(response['message'], 'Bad request')

# PATCH method tests
# -------------------------------------------------------------------

    def test_edit_existing_restaurant(self):
        req = self.client().patch('/restaurants/7', json=self.edit_rest)
        response = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(response['success'], True)
        self.assertTrue(response['restaurant'])

    def test_edit_existing_restaurant_error(self):
        req = self.client().patch('/restaurants/7', json=self.edit_rest_error)
        response = json.loads(req.data)

        self.assertEqual(req.status_code, 400)
        self.assertEqual(response['success'], False)
        self.assertEqual(response['error'], 400)
        self.assertEqual(response['message'], 'Bad request')

# DELETE method tests
# -------------------------------------------------------------------

    def test_delete_restaurant(self):
        req = self.client().delete('/restaurants/3')
        response = json.loads(req.data)

        restaurant = Restaurant.query.get(3)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(response['success'], True)
        self.assertTrue(response['deleted'])
        self.assertEqual(restaurant, None)


if __name__ == '__main__':
    unittest.main()
