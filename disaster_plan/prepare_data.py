import osmnx as ox
import pandas as pd
from osmnx.distance import nearest_nodes
import pickle
from pathlib import Path
import argparse

def prepare_shibuya_data(shelter_data_path: str):
    # Higher resolution
    ox.settings.use_cache = True
    ox.settings.log_console = True
    # Shibuya road network (driveable roads only)
    G = ox.graph_from_place("Shibuya, Tokyo, Japan", network_type="drive")

    shelters_data_path = Path(shelter_data_path)
    # Shibuya Shelters data
    shelters = pd.read_csv(shelter_data_path, encoding="utf-8")
    shelters.rename(columns={"経度": "longitude", "緯度": "latitude"}, inplace=True)

    # Shelters to nearest graph nodes
    shelters["nearest_node"] = shelters.apply(
        lambda row: nearest_nodes(G, row["longitude"], row["latitude"]),
        axis=1
    )
    shelters["name"] = shelters[["名称","名称_カナ","名称_英字"]].apply(
        lambda row: row.dropna().values[0], axis=1
    )

    # depot(s): Shibuya City Fire Station
    depot_node = nearest_nodes(G, 139.68812, 35.6648)  # Shibuya Fire Station
    bundle = {
        "graph": G,
        "shelters": shelters[["name", "nearest_node"]],
        "depot_node": depot_node,
    }

    save_path = shelters_data_path.parent / "shibuya_bundle.pkl"
    with open(save_path, "wb") as f:
        pickle.dump(bundle, f)

    print("Saved data/shibuya_bundle.pkl")

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--shelter_data_path", type=str, default="disaster_plan/data/shibuya_shelters.csv")
    args = argparser.parse_args()


    prepare_shibuya_data(args.shelter_data_path)
