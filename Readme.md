# Full Stack Capstone Project

## Concierge App Backend

This is my final project for Udacity Full Stack Developer course. I worked in a big hotel as a Concierge for 2 years. As a hotel concierge I was required to have a good knowledge of the restaurants, events, entertainment places, activities etc. in the city. It is usually difficult to memorize all of the information. Therefore, I decided to write this project so that the concierge agents can easily create and look up the information about restaurants they reserve. This project only focuses on the restaurants in Dubai.

The project is currently deployed in Heroku: https://atp-concierge.herokuapp.com/

## Getting Started

### Installing Dependencies

#### Python 3.8.1

The dependencies for the project can be installed with pip:
```bash
pip install -r requirements.txt
```

### Key Dependencies 
- [Flask](http://flask.pocoo.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)

## Deployment

To deploy the code in heroku, follow the below instructions:

### Install Heroku CLI
https://devcenter.heroku.com/categories/command-line 

### Log in with command line 
```bash
heroku login
```

### Create your app
```bash
heroku create your_app_name
```

### Add database to your app
```bash
heroku addons:create heroku-postgresql:hobby-dev --app your_app_name
```

### Get your remote database URI
```bash
heroku config --app your_app_name

# Update URI in your code
```

### Deploy your code
`cd` to your project repository and run:
```bash
git init
git add .
git commit -m 'first commit'
git push heroku master
```

### Add tables to your remote database
```bash
heroku run python
>>> from app import db
>>> db.create_all()
>>> exit()
```

## API Documentation

- To see API endpoints navigate to [API Endpoints](endpoints.md)

### Role Based Access
- Public endpoint - No authorization is required
- Concierge agent - Can view the detailed info of the restaurants and post/patch/delete notes. The concierge agent does not have access to post/patch/delete restaurants
- Chief Concierge - Has full access 
- Access tokens for both roles are provided in the [setup](setup.sh)

### Error Handlers

API returns the following errors in the JSON format:

- 400: Bad request
- 401: Unauthorized
- 403: Forbidden
- 404: Page not found
- 500: Internal Server Error

```
{
  "error": 404,
  "message": "Page not found",
  "success": false
}
```

### Testing

To run python unittest, run:
```
createdb test_concierge
psql test_concierge < concierge_db.psql
python3 test_app.py
```

To run tests with RBAC, import [collection](concierge-app-test.postman_collection.json) in [Postman](https://www.postman.com/)

