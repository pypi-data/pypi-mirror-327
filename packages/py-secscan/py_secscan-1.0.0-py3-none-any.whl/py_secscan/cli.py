from py_secscan import settings
from py_secscan import stdx
from py_secscan.scan import scan
from py_secscan.view import view

import argparse
import os


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PySecScan")
    parser.add_argument(
        "-v",
        action=stdx.StoreVerbosityParser,
        type=str,
        nargs=0,
        help="Debug verbosity level",
    )

    parser.add_argument(
        "-vv",
        action=stdx.StoreVerbosityParser,
        type=str,
        nargs=0,
        help="Debug with traceback verbosity level",
    )

    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    view_parser = subparsers.add_parser("view", help="Start webapp")
    view_parser.set_defaults(func=view.main)

    scan_parser = subparsers.add_parser("scan", help="Scan the project")
    scan_parser.add_argument(
        "-c",
        "--config-filename",
        required=False,
        help="Path to the configuration file",
        default=os.environ["PY_SECSCAN_CONFIG_FILENAME"],
    )

    return parser.parse_args()


def main() -> bool:
    try:
        settings.load_env()

        args = parse_args()

        if args.command == "view":
            args.func()
            return 0

        if args.command == "scan":
            builder = scan.ScanBuilder(args.config_filename)
            builder.execute()
            return 0

        stdx.exception(ValueError(f"Command {args.command} not found. Run with --help for more information"))
    except KeyboardInterrupt:
        stdx.warning("Manual interruption")
    except Exception as e:
        stdx.exception(e)

    return 0
