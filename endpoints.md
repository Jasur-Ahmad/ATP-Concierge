## API Endpoints

## Restaurant

`GET /restaurants-public`
- Gets a list of short detailed restaurants
- Takes query strings (page & per_page) for pagination
- No authorization is required
- Sample: `curl https://atp-concierge.herokuapp.com/restaurants-public`
```
{
  "current_page": 1,
  "restaurants": [
    {
      "cuisine": "Asian",
      "id": 1,
      "location": "Palm Jumeirah",
      "name": "Saffron"
    }
  ],
  "success": true,
  "total_pages": 3,
  "total_restaurants": 7
}
```

`GET /restaurants`
- Gets a list of detailed restaurants 
- Takes query strings (page & per_page) for pagination
- Requires authorization
- Sample: `curl -X GET --header "Authorization: bearer token" https://atp-concierge.herokuapp.com/restaurants`
```
{
  "current_page": 1,
  "restaurants": [
    {
      "address": "Atlantis The Palm",
      "age_policy": 10,
      "category": "Fine Dining",
      "cuisine": "Chinese",
      "id": 2,
      "location": "Palm Jumeirah",
      "name": "Hakkasan",
      "phone_number": "97144262626",
      "prebooking_required": true,
      "rating": 5
    }
  ],
  "success": true,
  "total_pages": 3,
  "total_restaurants": 7
}
```

`GET /restaurants/<restaurant_id>`
- Gets a json object of an individual restaurant
- Requires authorization
- Sample: `curl -X GET --header "Authorization: bearer token" https://atp-concierge.herokuapp.com/restaurants/3`
```
{
  "notes": [],
  "restaurant": {
    "address": "Taj Hotel",
    "age_policy": 21,
    "category": "Bars and Lounges",
    "cuisine": "European",
    "id": 3,
    "location": "Downtown",
    "name": "Billionaire Mansion",
    "phone_number": "No phone number",
    "prebooking_required": true,
    "rating": 5
  },
  "success": true
}
```

`GET /restaurants/search`
- Gets a list of found restaurants
- Takes a query string `keyword` and ('page' for pagination)
- Sample: `curl -X GET --header "Authorization: bearer token" https://atp-concierge.herokuapp.com/restaurants/search?keyword=bread`
```
{
  "current_page": 1,
  "restaurants": [
    {
      "address": "Atlantis The Palm",
      "age_policy": 0,
      "category": "Casual Dining",
      "cuisine": "British",
      "id": 6,
      "location": "Palm Jumeirah",
      "name": "Bread Street Kitchen",
      "phone_number": "97144262626",
      "prebooking_required": true,
      "rating": 2
    }
  ],
  "results": 1,
  "success": true,
  "total_pages": 1
}
```

`POST /restaurants`
- Creates a new restaurant in the database
- Requires authorization
- Returns successful json response
- Sample: `curl https://atp-concierge.herokuapp.com/restaurants -X POST -H "Content-Type: application/json" -H "Authorization: bearer token" -d {"key": "value"}`
```
{
  "created": 20,
  "success": true
}
```

`PATCH /restaurants/<restaurant_id>`
- Edits an existing restaurant in the database
- Requires authorization
- Returns edited restaurant object
- Sample: `curl -X PATCH https://atp-concierge.herokuapp.com/restaurants/2 -H "Content-Type: application/json" -H "Authorization: bearer token" -d {"rating": 3}`
```
{
  "restaurant": {
    "address": "Atlantis The Palm",
    "age_policy": 10,
    "category": "Casual Dining",
    "cuisine": "Chinese",
    "id": 2,
    "location": "DIFC",
    "name": "Hakkasan",
    "phone_number": "97144262626",
    "prebooking_required": true,
    "rating": 3
  },
  "success": true
}
```

`DELETE /restaurants/<restaurant_id>`
- Deletes a restaurant from the database
- Returns successful json response 
- Requires authorization
- Sample: `curl -X DELETE https://atp-concierge.herokuapp.com/restaurants/20 -H "Content-Type: application/json" -H "Authorization: bearer token"`
```
{
  "deleted": 20,
  "success": true
}
```

## Category

`GET /categories`
- Gets a list of categories
- Sample: `curl https://atp-concierge.herokuapp.com/categories`
```
{
  "categories": [
    {
      "id": 1,
      "name": "Fine Dining"
    }
  ],
  "success": true
}
```

`GET /categories/<category_id>/restaurants`
- Gets a list of restaurants based on the selected category
- Requires authorization
- Sample: `curl -X GET --header "Authorization: bearer token" https://atp-concierge.herokuapp.com/categories/1/restaurants`
```
{
  "restaurants": [
    {
      "address": "Atlantis The Palm",
      "age_policy": 10,
      "category": "Fine Dining",
      "cuisine": "Japanese",
      "id": 5,
      "location": "Palm Jumeirah",
      "name": "Nobu",
      "phone_number": "97144262626",
      "prebooking_required": true,
      "rating": 5
    }
  ],
  "success": true,
  "total_restaurants": 4
}
```

## Cuisine

`GET /cuisines`
- Gets a list of cuisines
- Sample: `curl https://atp-concierge.herokuapp.com/cuisines`
```
{
  "cuisines": [
    {
      "id": 3,
      "name": "American"
    }
  ],
  "success": true
}
```

`GET /cuisines/<cuisine_id>/restaurants`
- Gets a list of restaurants based on the selected cuisine
- Requires authorization
- Sample: `curl -X GET --header "Authorization: bearer token" https://atp-concierge.herokuapp.com/cuisines/10/restaurants`
```
{
  "restaurants": [
    {
      "address": "Atlantis The Palm",
      "age_policy": 10,
      "category": "Fine Dining",
      "cuisine": "Japanese",
      "id": 5,
      "location": "Palm Jumeirah",
      "name": "Nobu",
      "phone_number": "97144262626",
      "prebooking_required": true,
      "rating": 5
    }
  ],
  "success": true,
  "total_restaurants": 8
}
```

## Age Policy

`GET /age-policies`
- Gets a list of restaurant age-policies
- Sample: `curl https://atp-concierge.herokuapp.com/age-policies`
```
{
  "age-policy": [
    {
      "age": 0,
      "id": 1
    }
  ],
  "success": true
}
```

`GET /age-policies/<policy_id>/restaurants`
- Gets a list of restaurants based on the selected age-policy
- Requires authorization
- Sample: `curl -X GET --header "Authorization: bearer token" https://atp-concierge.herokuapp.com/age-policies/2/restaurants`
```
{
  "restaurants": [
    {
      "address": "Atlantis The Palm",
      "age_policy": 10,
      "category": "Fine Dining",
      "cuisine": "Japanese",
      "id": 5,
      "location": "Palm Jumeirah",
      "name": "Nobu",
      "phone_number": "97144262626",
      "prebooking_required": true,
      "rating": 5
    }
  ],
  "success": true,
  "total_restaurants": 10
}
```
## Location

`GET /locations`
- Gets a list of locations
- Sample: `curl https://atp-concierge.herokuapp.com/locations`
```
{
  "locations": [
    {
      "id": 3,
      "name": "Dubai Marina"
    }
  ],
  "success": true
}
```

`GET /locations/<location_id>/restaurants`
- Gets a list of restaurants based on the selected location
- Requires authorization
- Sample: `curl -X GET --header "Authorization: bearer token" https://atp-concierge.herokuapp.com/locations/4/restaurants`
```
{
  "restaurants": [
    {
      "address": "Atlantis The Palm",
      "age_policy": 10,
      "category": "Fine Dining",
      "cuisine": "Japanese",
      "id": 5,
      "location": "Palm Jumeirah",
      "name": "Nobu",
      "phone_number": "97144262626",
      "prebooking_required": true,
      "rating": 5
    }
  ],
  "success": true,
  "total_restaurants": 20
}
```

## Notes

`POST /restaurants/<restaurant_id>/notes`
- Creates a new note
- Returns successful json response
- Requires authorization
- Sample: `curl https://atp-concierge.herokuapp.com/restaurants/2/notes -X POST -H "Content-Type: application/json" -H "Authorization: bearer token" -d {"note": "test note"}`
```
{
  "created": 5,
  "success": true
}
```
`PATCH /notes/<note_id>`
- Edits existing note in the database
- Returns successful json response
- Requires authorization
- Sample: `curl -X PATCH https://atp-concierge.herokuapp.com/notes/2 -H "Content-Type: application/json" -H "Authorization: bearer token" -d {"note": "just a test"}`
```
{
  "success": true
}
```

`DELETE /notes/<note_id>`
- Deletes existing note in the database
- Returns successful json response
- Requires authorization
- Sample: `curl -X DELETE https://atp-concierge.herokuapp.com/notes/2 -H "Content-Type: application/json" -H "Authorization: bearer token"`
```
{
  "success": true
}
```
