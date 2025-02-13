import os
from uuid import uuid5, NAMESPACE_OID

from cognee.api.v1.visualize.visualize import visualize_graph
from cognee.shared.utils import render_graph

os.environ["BUCKET_URL"] = "./.data_storage"
os.environ["DATA_WRITER__DISABLE_COMPRESSION"] = "true"

import dlt
import requests

BASE_URL = "https://pokeapi.co/api/v2/"


# Fetch list of Pokémon (just names and URLs)
@dlt.resource(write_disposition="replace")
def pokemon_list(limit: int = 50):
    response = requests.get(f"{BASE_URL}pokemon", params={"limit": limit})
    response.raise_for_status()
    yield response.json()["results"]


@dlt.transformer(data_from=pokemon_list)
def pokemon_details(pokemons):
    """Fetches detailed info for each Pokémon"""
    for pokemon in pokemons:
        response = requests.get(pokemon["url"])
        response.raise_for_status()
        yield response.json()  # Full Pokémon details


pipeline = dlt.pipeline(
    pipeline_name="pokemon_pipeline",
    destination="filesystem",
    dataset_name="pokemon_data",
)

# Run pipeline for Pokémon list and details
info = pipeline.run([pokemon_list, pokemon_details])
print(info)


from cognee.low_level import DataPoint
from typing import List, Optional


class Abilities(DataPoint):
    name: str = "Abilities"
    metadata: dict = {"index_fields": ["name"]}


# 🎯 Ability Model
class PokemonAbility(DataPoint):
    name: str
    ability__name: str
    ability__url: str
    is_hidden: bool
    slot: int

    _dlt_load_id: str
    _dlt_id: str
    _dlt_parent_id: str
    _dlt_list_idx: str

    is_type: Abilities

    metadata: dict = {"index_fields": ["ability__name"]}


class Pokemons(DataPoint):
    name: str = "Pokemons"
    have: Abilities
    metadata: dict = {"index_fields": ["name"]}


# 🎯 Pokémon Model (Includes a List of Abilities)
class Pokemon(DataPoint):
    name: str
    base_experience: int
    height: int
    weight: int
    is_default: bool
    order: int
    location_area_encounters: str

    # Species
    species__name: str
    species__url: str

    # Cries
    cries__latest: str
    cries__legacy: str

    # Sprites
    sprites__front_default: str
    sprites__front_shiny: str
    sprites__back_default: Optional[str]
    sprites__back_shiny: Optional[str]

    _dlt_load_id: str
    _dlt_id: str

    is_type: Pokemons
    abilities: List[PokemonAbility]  # Relationship: A Pokémon has multiple abilities

    metadata: dict = {"index_fields": ["name"]}


# Read data from destination into Pydantic
from pathlib import Path
import json

# Set the path to your `dlt` filesystem storage
STORAGE_PATH = Path(".data_storage/pokemon_data/pokemon_details")

# Find the latest JSONL file (sorted by timestamp)
jsonl_pokemons = sorted(STORAGE_PATH.glob("*.jsonl"))
if not jsonl_pokemons:
    raise FileNotFoundError("No JSONL files found in the storage directory.")

latest_file = jsonl_pokemons[-1]  # Pick the latest file
print(f"📂 Loading data from: {latest_file}")

# Set the path to your `dlt` filesystem storage
STORAGE_PATH = Path(".data_storage/pokemon_data/pokemon_details__abilities")

# Find the latest JSONL file (sorted by timestamp)
jsonl_abilities = sorted(STORAGE_PATH.glob("*.jsonl"))
if not jsonl_abilities:
    raise FileNotFoundError("No JSONL files found in the storage directory.")

latest_file = jsonl_abilities[-1]  # Pick the latest file
print(f"📂 Loading data from: {latest_file}")


# Read and parse JSONL data
pokemon_abilities = []

abilities_root = Abilities()

for jsonl_ability in jsonl_abilities:
    with open(jsonl_ability, "r") as f:
        for line in f:
            ability = json.loads(line)  # Convert JSON string to dictionary
            ability["id"] = uuid5(NAMESPACE_OID, ability["_dlt_id"])
            # We add name so it's nicely shown in the graph preview
            ability["name"] = ability["ability__name"]
            ability["is_type"] = abilities_root
            pokemon_abilities.append(ability)


# Read and parse JSONL data
pokemons = []

pokemon_root = Pokemons(have=abilities_root)

for jsonl_pokemon in jsonl_pokemons:
    with open(jsonl_pokemon, "r") as f:
        for line in f:
            pokemon_data = json.loads(line)  # Convert JSON string to dictionary
            abilities = [
                ability
                for ability in pokemon_abilities
                if ability["_dlt_parent_id"] == pokemon_data["_dlt_id"]
            ]

            pokemon_data["external_id"] = pokemon_data["id"]
            pokemon_data["id"] = uuid5(NAMESPACE_OID, str(pokemon_data["id"]))
            pokemon_data["abilities"] = [PokemonAbility(**ability) for ability in abilities]
            pokemon_data["is_type"] = pokemon_root

            pokemons.append(
                Pokemon(**pokemon_data),
            )


import asyncio
import pathlib
import cognee
from cognee.low_level import setup as cognee_setup


async def main():
    data_directory_path = str(
        pathlib.Path(os.path.join(pathlib.Path(__file__).parent, ".data_storage")).resolve()
    )
    # Set up the data directory. Cognee will store files here.
    cognee.config.data_root_directory(data_directory_path)

    cognee_directory_path = str(
        pathlib.Path(os.path.join(pathlib.Path(__file__).parent, ".cognee_system")).resolve()
    )
    # Set up the Cognee system directory. Cognee will store system files and databases here.
    cognee.config.system_root_directory(cognee_directory_path)

    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    await cognee_setup()

    # Create a pipeline
    from cognee.tasks.storage import add_data_points
    from cognee.modules.pipelines.tasks.Task import Task

    tasks = [Task(add_data_points, task_config={"batch_size": 50})]

    from cognee.modules.pipelines import run_tasks

    results = run_tasks(tasks, pokemons)
    async for result in results:
        print(result)
    print("Done")

    await render_graph()
    # graph_file_path = str(
    #     pathlib.Path(
    #         os.path.join(pathlib.Path(__file__).parent, ".artifacts/graph_visualization.html")
    #     ).resolve()
    # )
    # await visualize_graph(graph_file_path)

    from cognee.api.v1.search import SearchType

    # search_results = await cognee.search(query_type=SearchType.GRAPH_COMPLETION, query_text="What is Bulbasaur?")
    search_results = await cognee.search(
        query_type=SearchType.GRAPH_COMPLETION, query_text="pokemons?"
    )
    # search_results = await cognee.search(query_type=SearchType.GRAPH_COMPLETION, query_text="What's in the data?")

    # Display results
    print("Search results:")
    for result_text in search_results:
        print(result_text)


if __name__ == "__main__":
    asyncio.run(main())
