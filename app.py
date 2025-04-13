from flask import Flask , render_template , request
import requests

app = Flask(__name__)

base_url = "https://pokeapi.co/api/v2/"

def Pokeverse(pokemon_name):
    url = f'{base_url}pokemon/{pokemon_name}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    pokemon_info = None
    if request.method == "POST":
        pokemon_name = request.form["pokemon_name"].lower()
        pokemon_info = Pokeverse(pokemon_name)
        pokemon_types = [t["type"]["name"] for t in pokemon_info["types"]]
        primary_type = pokemon_types[0] if pokemon_types else "normal"
    return render_template("home.html", pokemon_info=pokemon_info,primary_type=primary_type )

    

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")