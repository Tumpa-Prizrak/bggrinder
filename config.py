import json5
from dataclasses import dataclass


@dataclass
class Config:
    target_fps: int
    time: int
    output_folder: str
    images_folder: str


def parse():
    data = json5.load(open("config.jsonc"))
    return Config(
        data["target_fps"],
        data["time"],
        data["output_folder"],
        data["images_folder"]
    )
