import json

import instantcli

import pestuary
from pestuary import pinning
from pestuary import content
from pestuary import collections
from pestuary import autoretrieve


instantcli.filter_function_name = lambda name: not name.startswith("main") and not name.startswith("_")
instantcli.post_call = lambda result: print(json.dumps(result, default=lambda x: x.to_dict()))


def main():
    instantcli.load_module(pinning)
    instantcli.load_module(content)
    instantcli.load_module(collections)
    instantcli.load_module(autoretrieve)
    instantcli.cli()


if __name__ == "__main__":
    main()
