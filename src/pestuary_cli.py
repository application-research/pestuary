import pestuary
import instantcli
import json

instantcli.filter_function_name = lambda name: not name.startswith("main") and not name.startswith("_")
instantcli.post_call = lambda result: print(json.dumps(result, default=lambda x: x.to_dict()))


def main():
    instantcli.instantcli(pestuary)

if __name__ == "__main__":
    main()
