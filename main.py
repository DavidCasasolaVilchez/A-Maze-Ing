from Utils.ArgsParser import ArgsParser
from Model import Panel


def main() -> None:
    args: ArgsParser = ArgsParser("amazing/config.txt")
    print(
        f"height {args.height}\n"
        f"width {args.width}\n"
        f"seed {args.seed}\n"
        f"exit {args.exit}\n"
        f"entry {args.entry}\n"
        f"perfect {args.perfect}\n"
        f"display_mode {args.display_mode}\n"
        f"output_file {args.output_file}\n\n"
    )
    p: Panel = Panel.create_base(
        (args.height, args.width),
        args.perfect,
        args.entry,
        args.exit,
        args.seed,
    )
    p.display_ascii()
    print("\n")
    p.generate42()
    p.display_ascii()


if __name__ == "__main__":
    main()
