import json
import click

from typing import List

from gameoflife.Life import Life
from gameoflife.Grid import GridType, GridFactory


def mode_convert(_, __: click.Option, value: str) -> GridType:
    if value == "escaping":
        return GridType.ESCAPING
    elif value == "wrapping":
        return GridType.WRAPPING


def input_convert(_, __, value: str) -> List[List[int]]:
    print (f"value = {value}")

    return json.loads(value)


pulsar_g1 = """[
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]"""


@click.command()
@click.argument("generations", type=int)
@click.option("-f", "--file", default="out.gif", help="output file")
@click.option("-m", "--mode",
              type=click.Choice(['wrapping', 'escaping'], case_sensitive=False),
              default="escaping", callback=mode_convert)
@click.option("-g", "--gen_zero", default=pulsar_g1, callback=input_convert)
@click.option("-i", "--interpret_as",
              type=click.Choice(['grid', 'list'], case_sensitive=False),
              default="list")
def cli(generations, file, mode, gen_zero, interpret_as):

    factory = GridFactory(mode)
    if interpret_as == 'grid':
        g_zero = factory.from_list(gen_zero)
    else:
        all_x = [x[0] for x in gen_zero]
        all_y = [x[1] for x in gen_zero]

        g_zero = factory.from_xy(max(all_x)+3, max(all_y)+3)
        for cell in gen_zero:
            g_zero.set(cell[0]+1, cell[1]+1, 1)

    resultant_generations = []
    generations = Life.evaluate_n_generations(g_zero, generations, resultant_generations)
    print(generations)

    frames = []
    for generation in resultant_generations:
        frames.append(generation.render())

    frame_one = frames[0]
    frame_one.save(file, format="GIF", append_images=frames, save_all=True, duration=200, loop=0)


if __name__ == "__main__":
    cli()



