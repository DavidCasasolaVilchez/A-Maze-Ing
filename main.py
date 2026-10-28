from Utils.ArgsParser import ArgsParser
from Model.Panel import Panel
# from Model.Resolver import start_search


def main() -> None:
    args: ArgsParser = ArgsParser("config.txt")
    p: "Panel" = Panel.create_base(
        (args.height, args.width),
        args.perfect,
        args.entry,
        args.exit,
        args.seed,
    )
    p.generate42()
    p.convert_to_base()
    p.convert_imperfect()
    p.display_ascii(args.display_mode)


if __name__ == "__main__":
    main()
