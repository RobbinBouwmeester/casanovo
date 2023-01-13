from gooey import Gooey, GooeyParser
from casanovo import casanovo
import os
from datetime import datetime

def parse_arguments():
    """Read arguments from the CLI or GUI."""
    parser = GooeyParser(
        prog="casanovo",
        description=(
            "casanovo")
    )

    input_args = parser.add_argument_group("Input data and models")

    input_args.add_argument(
        "--mode",
        nargs="+",
        required=True,
        choices=["denovo","train","eval"],
        #default=None,
        metavar="Data sets to fit models",
        widget="Dropdown",
        help=(
            "The mode in which to run Casanovo:"
        ),
    )

    input_args.add_argument(
        "--model",
        nargs="+",
        required=False,
        metavar="Model",
        widget="FileChooser",
        help=(
            "The file name of the model weights (.ckpt file)."
        ),
    )

    input_args.add_argument(
        '--peak_path',
        metavar="MGF file for predictions",
        type=str,
        required=True,
        widget="FileChooser"
    )

    input_args.add_argument(
        '--peak_path_val',
        metavar="MGF file for validation (when training)",
        type=str,
        required=False,
        widget="FileChooser"
    )

    input_args.add_argument(
        "--config",
        nargs="+",
        required=True,
        widget="FileChooser",
        help=(
            "The file name of the configuration file with custom options."
        ),
    )

    input_args.add_argument(
        '--output',
        type=str,
        required=True,
        widget="DirChooser"
    )

    results = parser.parse_args()

    return results


@Gooey(
    program_name="Casanovo",
    default_size=(720, 790),
    monospace_display=True
)
def main_gui():
    argu = parse_arguments()
    #print(vars(argu))
    argu_pass = list(vars(argu).items())
    argu_list = []
    for a,b in argu_pass:
        if b == None:
            continue
        argu_list.append("--"+a)
        if a == "output":
            now = datetime.now()
            y = now.strftime("%Y")
            m = now.strftime("%m")
            d = now.strftime("%d")
            t = now.strftime("%H%M%S")
            fname = f"results{y}{m}{d}_{t}"
            argu_list.append(os.path.join(b,fname))
        elif type(b) == list:
            argu_list.append(b[0])
        else:
            argu_list.append(b)
    print(argu_list)
    casanovo.main(argu_list)
    

if __name__ == "__main__":
    print(dir(casanovo))
    main_gui()