import requests
base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info (pokemon_name):
    url =f'{base_url}/pokemon/{pokemon_name}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}")
        
pokemon_name = input("Enter the name of the pokemon: ")
pokemon_info = get_pokemon_info(pokemon_name)


if pokemon_info:
    name = pokemon_info["name"]
    height = pokemon_info["height"]
    weight = pokemon_info["weight"]
    types = [t["type"]["name"] for t in pokemon_info["types"]]
    moves = sorted([move["move"]["name"] for move in pokemon_info["moves"]])

    print(f'Name: {name.capitalize()}')
    print(f"Height: {height}")
    print(f"weight: {weight}")
    print(f"Types: {' , '.join(types)}")
    print("Moves:")
  
    for i,move in enumerate(moves, start = 1):
        print(f"{i} : {move}")