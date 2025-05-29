from flask import Flask, render_template, request
import requests

app = Flask(__name__)

base_url = "https://pokeapi.co/api/v2/"

# Function to fetch Pokémon info
def Pokeverse(pokemon_name):
    url = f'{base_url}pokemon/{pokemon_name}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}")
        return None

# Function to fetch the Pokémon type info
def get_pokemon_type(pokemon_name):
    url = f"{base_url}pokemon/{pokemon_name}"
    response = requests.get(url)
    if response.status_code == 200:
        pokemon_data = response.json()
        primary_type = pokemon_data['types'][0]['type']['name']
        return primary_type
    else:
        return 'normal' 


@app.route('/home')
def home():
    return render_template('home.html')

    
@app.route('/pokedex', methods=['GET', 'POST'])
def pokedex():
    pokemon_info = None
    primary_type = 'normal'  
    
    # Get the list of all Pokémon for autocomplete
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=10000')
    data = response.json()
    pokemon_list = [pokemon['name'] for pokemon in data['results']]
      
    if request.method == 'POST':
        name = request.form['pokemon_name'].lower()
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        poke_response = requests.get(pokemon_url)
        
        if poke_response.status_code == 200:
            pokemon_info = poke_response.json()
            primary_type = get_pokemon_type(name)

    return render_template('pokedex.html', 
                         pokemon_info=pokemon_info, 
                         pokemon_list=pokemon_list, 
                         primary_type=primary_type)

@app.route('/games')
def games():
    return render_template("games.html ")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")