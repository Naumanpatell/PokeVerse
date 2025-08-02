import os
from flask import Flask, render_template, request
import requests
import random
from datetime import datetime

app = Flask(__name__)

base_url = "https://pokeapi.co/api/v2/"

# Function to fetch Pokémon info
def Pokeverse(pokemon_name):
    url = f'{base_url}pokemon/{pokemon_name}'
    try:
        response = requests.get(url)
        response.raise_for_status() # Raises HTTPError for bad responses 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Pokémon info for {pokemon_name}: {e}")
        return None

# Function to fetch the Pokémon type info
#t This function implicitly uses Pokeverse but for consistency, let's keep it separae
# if its logic is slightly different (e.g., just returning the type)
def get_pokemon_type(pokemon_name):
    url = f"{base_url}pokemon/{pokemon_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        pokemon_data = response.json()
        primary_type = pokemon_data['types'][0]['type']['name']
        return primary_type
    except (requests.exceptions.RequestException, IndexError) as e:
        print(f"Error fetching Pokémon type for {pokemon_name}: {e}")
        return 'main' # Default to 'normal' on error or if no types are found

def get_pokemon_of_day():
    """Get a random Pokémon for the current day using a seeded random generator"""
    try:
        # Get all Pokémon names
        response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=10000')
        response.raise_for_status()
        data = response.json()
        pokemon_list = [pokemon['name'] for pokemon in data['results']]
        
        if not pokemon_list:
            return None
            
        # Create a daily seed for consistent random selection
        today = datetime.now()
        day_of_year = today.timetuple().tm_yday  # Day of year (1-366)
        year = today.year
        
        # Combine year and day of year for a unique daily seed
        daily_seed = year * 1000 + day_of_year
        
        # Set the random seed for today
        random.seed(daily_seed)
        
        # Get a random Pokémon
        random_pokemon = random.choice(pokemon_list)
        
        # Reset the random seed to avoid affecting other parts of the application
        random.seed()
        
        return random_pokemon
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Pokémon list for daily Pokémon: {e}")
        return None
    except Exception as e:
        print(f"Error in get_pokemon_of_day: {e}")
        return None


@app.route('/')
@app.route('/home')
def home():
    pokemon_list = []
    pokemon_of_day = None
    
    try:
        response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=10000')
        response.raise_for_status()
        data = response.json()
        pokemon_list = [pokemon['name'] for pokemon in data['results']]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching all Pokémon names for home page: {e}")
        pokemon_list = []
    except KeyError:
        print("API response for all Pokémon names did not contain 'results' key.")
        pokemon_list = []
    
    # Get the Pokémon of the Day
    pokemon_of_day_name = get_pokemon_of_day()
    if pokemon_of_day_name:
        try:
            pokemon_of_day = Pokeverse(pokemon_of_day_name)
        except Exception as e:
            print(f"Error fetching Pokémon of the Day data: {e}")
            pokemon_of_day = None
    
    return render_template('home.html', 
                         pokemon_list=pokemon_list, 
                         pokemon_of_day=pokemon_of_day)


@app.route('/pokedex', methods=['GET', 'POST'])
def pokedex():
    pokemon_info = None
    primary_type = 'main'
    pokemon_list = [] 
    
    try:
        response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=10000')
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        pokemon_list = [pokemon['name'] for pokemon in data['results']]
        print(f"Successfully loaded {len(pokemon_list)} Pokémon for autocomplete")
    except requests.exceptions.RequestException as e:
        # If fetching the full list fails, print an error and use an empty list
        print(f"Error fetching all Pokémon names for autocomplete: {e}")
        pokemon_list = [] 
    except KeyError:
        # Handle cases where 'results' might be missing in a malformed response
        print("API response for all Pokémon names did not contain 'results' key.")
        pokemon_list = [] 
    
    # Check for pokemon parameter in GET request (from homepage link)
    if request.method == 'GET' and request.args.get('pokemon'):
        name = request.args.get('pokemon').lower()
        pokemon_data = Pokeverse(name) 
        if pokemon_data: 
            pokemon_info = pokemon_data
            if pokemon_data['types']: 
                primary_type = pokemon_data['types'][0]['type']['name']
            else:
                primary_type = 'normal' 
    
    # Handle POST request (from search form)
    elif request.method == 'POST':
        name = request.form['pokemon_name'].lower()
        pokemon_data = Pokeverse(name) 
        if pokemon_data: 
            pokemon_info = pokemon_data
            if pokemon_data['types']: 
                primary_type = pokemon_data['types'][0]['type']['name']
            else:
                primary_type = 'normal' 
        else:
            pass

    return render_template('pokedex.html',
                           pokemon_info=pokemon_info,
                           pokemon_list=pokemon_list, 
                           primary_type=primary_type)

@app.route('/games')
def games():
    return render_template("games.html")

@app.route('/pokemon_guess')
def pokemon_guess():
    return render_template('pokemon_guess.html')

@app.route('/pokemon_quiz')
def pokemon_quiz():
    return render_template('pokemon_quiz.html')

        
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000))) 