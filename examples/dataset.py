#!/usr/bin/env python
from typing import Dict, List

from cihai.core import Cihai
from cihai.extend import Dataset

data = {}  # any data source, internal, a file, on the internet, in a database...


class MyDataset(Dataset):
    def bootstrap(self) -> None:  # automatically ran with .add_dataset, if exists
        # Use this to setup your dataset, check if updates are needed, etc.
        data.update({"好": "Good", "好好": "Hello"})

    def givemedata(self, key: str) -> str:
        return data[key]

    def search(self, needle: str) -> Dict[str, str]:
        return {k: v for k, v in data.items() if needle in k}

    def backwards(self, needle: str) -> List[str]:
        return [k for k, v in data.items() if needle in v]


def run() -> None:
    c = Cihai(unihan=False)

    c.add_dataset(MyDataset, namespace="moo")
    c.moo.bootstrap()

    print("Definitions exactly for 好", c.moo.givemedata("好"))

    print("Definitions matching with 你好:", ", ".join(c.moo.search("好")))

    print("Reverse definition with Good:", ", ".join(c.moo.backwards("Good")))


if __name__ == "__main__":
    run()
