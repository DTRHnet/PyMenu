import argparse
import curses
import json
import logging
import os
import sys
from menu.dtrh_menu import DynamicMenu

def list_files(directory, extension):
    return [f for f in os.listdir(directory) if f.endswith(extension)]

def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def main(stdscr, config_file):
    with open(config_file, 'r') as file:
        json_config = json.load(file)
    menu = DynamicMenu(stdscr, json_config)
    menu.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PyTUI Application")
    parser.add_argument('-C', '--config-file', type=str, help="The JSON file to load for the menu")
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose output for real-time debugging")
    parser.add_argument('-l', '--log', type=str, nargs='?', const='pyTUI-log.log', help="Enable logging, to [file], or pyTUI-log.log")
    parser.add_argument('-V', '--version', action='store_true', help="Display version")
    parser.add_argument('-T', '--list-themes', action='store_true', help="List themes configurations")
    parser.add_argument('-M', '--list-menus', action='store_true', help="List menu configurations")
    parser.add_argument('-U', '--unit-tests', type=str, help="Run unit tests on [menu]")
    
    args = parser.parse_args()

    if args.version:
        print("PyTUI Version 1.0")
        sys.exit(0)

    if args.list_themes:
        themes = list_files('themes', '.json')
        print("Available Themes:")
        for theme in themes:
            print(f" - {theme}")
        sys.exit(0)

    if args.list_menus:
        menus = list_files('config', '.json')
        print("Available Menu Configurations:")
        for menu in menus:
            print(f" - {menu}")
        sys.exit(0)

    if args.unit_tests:
        print(f"Running unit tests on {args.unit_tests} menu")
        # You can add your unit test running code here
        sys.exit(0)

    if args.log:
        setup_logging(args.log)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose mode enabled")

    config_file = args.config_file if args.config_file else 'config/basic_menu.json'
    if not os.path.exists(config_file):
        logging.error(f"Config file {config_file} not found")
        sys.exit(1)

    logging.info(f"Loading config file: {config_file}")
    curses.wrapper(main, config_file)
