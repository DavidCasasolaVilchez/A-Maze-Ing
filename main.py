from Utils.ArgsParser import ArgsParser
from Model.Panel import Panel
from Model.Resolver import start_search

def main() -> None:
    args: ArgsParser = ArgsParser("config.txt")
#    print(
#        f"height {args.height}\n"
#        f"width {args.width}\n"
#        f"seed {args.seed}\n"
#        f"exit {args.exit}\n"
#        f"entry {args.entry}\n"
#        f"perfect {args.perfect}\n"
#        f"display_mode {args.display_mode}\n"
#        f"output_file {args.output_file}\n\n"
#    )
    p: "Panel" = Panel.create_base(
        (args.height, args.width),
        args.perfect,
        args.entry,
        args.exit,
        args.seed,
    )
    # print("############### Laberinto base ###############\n\n")
    # p.display_ascii()
    p.generate42()
    # print("\n\n\n############### Laberinto base con 42 ###############\n\n")
    # p.display_ascii()
    print("\n\n\n############### Laberinto imperfecto ###############\n\n")
    p.convert_to_base()
    p.display_ascii()
    print(start_search(p))


if __name__ == "__main__":
    main()
