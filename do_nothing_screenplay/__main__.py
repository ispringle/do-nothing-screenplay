import click
import jinja2
import yaml


def step_factory(global_context):
    def step_template(instructions, local_context):
        context = global_context | local_context
        for instruction in instructions:
            if type(instruction) is dict and instruction.get('prompt', None):
                template = jinja2.Template(instruction['prompt'])
                s = template.render(context)
                global_context[instruction["context_key"]] = input(s)
            elif instruction == "await":
                wait_for_enter()
            else:
                template = jinja2.Template(instruction)
                s = template.render(context)
                print(s)
    return step_template


def wait_for_enter():
    input("Press Enter to continue...")


def load_yml(yml_file):
    with open(yml_file, 'r') as f:
        return yaml.safe_load(f)


@click.command()
@click.option("--script-path", "-s",
              help="The do-nothing-screenplay Script to run.")
def main(script_path):
    script = load_yml(script_path)
    step_maker = step_factory(script['global_context'])
    for step in script['script']:
        step_maker(step['steps'], step.get('context', {}))
    print("Done.")


if __name__ == "__main__":
    main()
