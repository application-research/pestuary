import inspect
import os
import click
import pestuary

dir, fname = os.path.split(__file__)
fns = [name for name, val in pestuary.__dict__.items() if callable(val)]

#wrote magic to automate some things that clck doesnt do, i didnt want to have to specify each argument to click for each method when it can be done automatically using decorators
def magic(fn_name):
    fn = pestuary.__dict__[fn_name]
    argspec = inspect.getfullargspec(fn)
    arguments = argspec.args
    defaults = argspec.defaults
    if not arguments:
        arguments = []
    if not defaults:
        defaults = []
    requireds = [index < len(arguments) - len(defaults)  for index in range(len(arguments)) ]
    for i in range( len(arguments) - 1, -1, -1) :
        fn = click.argument(arguments[i], required=requireds[i])(fn)
    fn = cli.command()(fn)
    return fn

def main():
    for line in open(os.path.join(dir, "pestuary.py")):
        if line.startswith("def "):
            if line.startswith("def main") or line.startswith("def _"):
                continue
            fn_name = line.split("def ")[1].split("(")[0]
            magic(fn_name)
    cli()

@click.group()
def cli():
    pass

@cli.result_callback()
def process_result(result):
    print(json.dumps(result, default=lambda x: x.to_dict()))
    return result

if __name__ == "__main__":
    main()
