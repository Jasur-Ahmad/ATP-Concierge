from flask import Flask, jsonify, request, abort
import re
from flask_migrate import Migrate

from models.models import setup_db, db, Restaurant, Location, Age_policy, Category, Cuisine, Notes, drop_and_create_all
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
migrate = Migrate(app, db)

# pagination parameters
DEFAULT_PER_PAGE = 3


@app.route('/')
def index():
    return 'Welcome to ATP-Concierge'

# Restaurants
# -------------------------------------------------------------------


# public endpoint
@app.route('/restaurants-public', methods=['GET'])
def get_restaurants_short_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', DEFAULT_PER_PAGE, type=int)
    restaurants = Restaurant.query.order_by(Restaurant.id).paginate(
        page=page, error_out=False, per_page=per_page)

    if len(restaurants.items) == 0:
        abort(404)

    formatted_restaurants = [res.public_info() for res in restaurants.items]

    return jsonify({
        'success': True,
        'total_restaurants': restaurants.total,
        'total_pages': restaurants.pages,
        'current_page': restaurants.page,
        'restaurants': formatted_restaurants
    })


@app.route('/restaurants', methods=['GET'])
@requires_auth('get:restaurants')
def get_restaurants_full():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', DEFAULT_PER_PAGE, type=int)
    restaurants = Restaurant.query.order_by(Restaurant.id).paginate(
        page=page, error_out=False, per_page=per_page)

    if len(restaurants.items) == 0:
        abort(404)

    formatted_restaurants = [res.detailed_info() for res in restaurants.items]

    return jsonify({
        'success': True,
        'total_restaurants': restaurants.total,
        'total_pages': restaurants.pages,
        'current_page': restaurants.page,
        'restaurants': formatted_restaurants
    })


@app.route('/restaurants/<int:rest_id>', methods=['GET'])
@requires_auth('get:restaurants')
def get_individual_restaurant(rest_id):
    rest = Restaurant.query.get(rest_id)
    if rest is None:
        abort(404)

    notes = Notes.query.order_by(Notes.id).filter(
        Notes.restaurant_id == rest_id).all()

    return jsonify({
        'success': True,
        'restaurant': rest.detailed_info(),
        'notes': [note.format() for note in notes]
    })


@app.route('/restaurants', methods=['POST'])
@requires_auth('post:restaurants')
def post_new_restaurant():
    data = request.get_json()
    name = data.get('name', None)
    cuisine_id = data.get('cuisine_id', None)
    location_id = data.get('location_id', None)
    age_policy_id = data.get('age_policy_id', None)
    category_id = data.get('category_id', None)
    rating = data.get('rating', 0)
    address = data.get('address', None)
    phone_number = data.get('phone_number', 'No phone number')
    prebooking_required = data.get('prebooking_required', None)

    try:
        new_restaurant = Restaurant(
            name=name, cuisine_id=cuisine_id, location_id=location_id,
            age_policy_id=age_policy_id, category_id=category_id,
            rating=rating, address=address, phone_number=phone_number,
            prebooking_required=prebooking_required)
        new_restaurant.insert()

        return jsonify({
            'success': True,
            'created': new_restaurant.id
        })

    except:
        abort(400)


@app.route('/restaurants/search', methods=['GET'])
@requires_auth('get:restaurants')
def search_restaurant():
    search_word = request.args.get('keyword', None, type=str)
    page = request.args.get('page', 1, type=int)

    if search_word is None:
        abort(400)

    result = Restaurant.query.filter(
        Restaurant.name.ilike('%' + search_word + '%')).paginate(
        page=page, error_out=False, per_page=10)

    if len(result.items) == 0 or len(re.findall('\w', search_word)) < 3:
        return jsonify({
            'success': False,
            'message': 'No result'
        })

    formatted_result = [res.detailed_info() for res in result.items]

    return jsonify({
        'success': True,
        'results': result.total,
        'total_pages': result.pages,
        'current_page': result.page,
        'restaurants': formatted_result
    })


@app.route('/restaurants/<int:rest_id>', methods=['PATCH'])
@requires_auth('patch:restaurants')
def edit_restaurant(rest_id):
    rest = Restaurant.query.get(rest_id)
    if rest is None:
        abort(404)

    try:
        data = request.get_json()
        if not data:
            abort(400)

        rest.name = data.get('name', rest.name)
        rest.cuisine_id = data.get('cuisine_id', rest.cuisine_id)
        rest.location_id = data.get('location_id', rest.location_id)
        rest.age_policy_id = data.get('age_policy_id', rest.age_policy_id)
        rest.category_id = data.get('category_id', rest.category_id)
        rest.rating = data.get('rating', rest.rating)
        rest.address = data.get('address', rest.address)
        rest.phone_number = data.get('phone_number', rest.phone_number)
        rest.prebooking_required = data.get(
            'prebooking_required', rest.prebooking_required)

        rest.update()

        return jsonify({
            'success': True,
            'restaurant': rest.detailed_info()
        })

    except:
        abort(400)


@app.route('/restaurants/<int:rest_id>', methods=['DELETE'])
@requires_auth('delete:restaurants')
def delete_restaurant(rest_id):
    rest = Restaurant.query.get(rest_id)
    if rest is None:
        abort(404)

    try:
        rest.delete()
        return jsonify({
            'success': True,
            'deleted': rest_id
        })

    except:
        abort(500)

# Categories
# -------------------------------------------------------------------


# public endpoint
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = [cat.format() for cat in categories]

    return jsonify({
        'success': True,
        'categories': formatted_categories
    })


@app.route('/categories/<int:cat_id>/restaurants', methods=['GET'])
@requires_auth('get:restaurants')
def get_rest_by_category(cat_id):
    category = Category.query.get(cat_id)
    if category is None or len(category.restaurant) == 0:
        abort(404)

    formatted_rest = [rest.detailed_info() for rest in category.restaurant]

    return jsonify({
        'success': True,
        'total_restaurants': len(formatted_rest),
        'restaurants': formatted_rest
    })


# Cuisines
# -------------------------------------------------------------------


# public endpoint
@app.route('/cuisines', methods=['GET'])
def get_cuisines():
    cuisines = Cuisine.query.order_by(Cuisine.name).all()
    formatted_cuisines = [cuisine.format() for cuisine in cuisines]

    return jsonify({
        'success': True,
        'cuisines': formatted_cuisines
    })


@app.route('/cuisines/<int:cuisine_id>/restaurants', methods=['GET'])
@requires_auth('get:restaurants')
def get_rest_by_cuisine(cuisine_id):
    cuisine = Cuisine.query.get(cuisine_id)
    if cuisine is None or len(cuisine.restaurant) == 0:
        abort(404)

    formatted_rest = [rest.detailed_info() for rest in cuisine.restaurant]

    return jsonify({
        'success': True,
        'total_restaurants': len(formatted_rest),
        'restaurants': formatted_rest
    })

# Age Policies
# -------------------------------------------------------------------


# public endpoint
@app.route('/age-policies', methods=['GET'])
def get_age_policies():
    policies = Age_policy.query.order_by(Age_policy.id).all()
    formatted_policies = [policy.format() for policy in policies]

    return jsonify({
        'success': True,
        'age-policy': formatted_policies
    })


@app.route('/age-policies/<int:policy_id>/restaurants', methods=['GET'])
@requires_auth('get:restaurants')
def get_rest_by_policy(policy_id):
    policy = Age_policy.query.get(policy_id)
    if policy is None or len(policy.restaurant) == 0:
        abort(404)

    formatted_rest = [rest.detailed_info() for rest in policy.restaurant]

    return jsonify({
        'success': True,
        'total_restaurants': len(formatted_rest),
        'restaurants': formatted_rest
    })

# Locations
# -------------------------------------------------------------------


# public endpoint
@app.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.order_by(Location.name).all()
    formatted_locations = [loc.format() for loc in locations]

    return jsonify({
        'success': True,
        'locations': formatted_locations
    })


@app.route('/locations/<int:loc_id>/restaurants', methods=['GET'])
@requires_auth('get:restaurants')
def get_rest_by_location(loc_id):
    location = Location.query.get(loc_id)
    if location is None or len(location.restaurant) == 0:
        abort(404)

    formatted_rest = [rest.detailed_info() for rest in location.restaurant]

    return jsonify({
        'success': True,
        'total_restaurants': len(formatted_rest),
        'restaurants': formatted_rest
    })

# Notes
# -------------------------------------------------------------------


@app.route('/restaurants/<int:rest_id>/notes', methods=['POST'])
@requires_auth('full-access:notes')
def create_note(rest_id):
    data = request.get_json()
    note = data.get('note', None)

    if note is None:
        abort(400)

    try:
        new_note = Notes(note=note, restaurant_id=rest_id)
        new_note.insert()
        return jsonify({
            'success': True,
            'created': new_note.id
        })
    except:
        abort(500)


@app.route('/notes/<int:note_id>', methods=['PATCH', 'DELETE'])
@requires_auth('full-access:notes')
def edit_or_delete_note(note_id):
    data = request.get_json()
    note = Notes.query.get(note_id)

    if note is None:
        abort(404)

    try:
        if request.method == 'PATCH':
            note.note = data.get('note', None)
            note.update()

        if request.method == 'DELETE':
            note.delete()

        return jsonify({
            'success': True
        })

    except:
        abort(400)

# Error handlers
# -------------------------------------------------------------------


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Page not found'
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
    }), 400


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal server error'
    })


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error
    }), error.status_code
