from flask import Flask, render_template, request
import requests

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


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


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
    except requests.exceptions.RequestException as e:
        # If fetching the full list fails, print an error and use an empty list
        print(f"Error fetching all Pokémon names for autocomplete: {e}")
        pokemon_list = [] 
    except KeyError:
        # Handle cases where 'results' might be missing in a malformed response
        print("API response for all Pokémon names did not contain 'results' key.")
        pokemon_list = [] 
    

    if request.method == 'POST':
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

@app.route('/guess_pokemon') 
def guess_pokemon():
    return render_template('guess_pokemon')

@app.route('/pokemon_quiz') 
def pokemon_quiz():
    return render_template('pokemon_quiz')
        
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")