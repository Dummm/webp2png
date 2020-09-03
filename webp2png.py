#!/usr/bin/python

import os
import sys
import argparse

class Converter:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("directory",
                            help = "searched directory (default = '.')")
        parser.add_argument("-r", "--recursive",
                            help="recursive search",
                            action="store_true")
        parser.add_argument("-k", "--keep",
                            help="keep webp files",
                            action="store_true")
        parser.add_argument("-o", "--output",
                            help="output directory (default = same location as webp)")
        parser.add_argument("-v", "--verbose",
                            help="verbose logs")

        self.args = parser.parse_args()
        print(self.args)

    def get_all_file_paths(self):
        print("getting all files...")

        directory = self.args.directory
        directory_tree = os.walk(os.path.expanduser(directory))

        file_paths = []
        for directory_path, _directories, filenames in directory_tree:
            for filename in filenames:
                file_paths.append((directory_path, filename))

            if not self.args.recursive:
                break

        return file_paths

    def filter_webps(self, file_paths):
        print("filtering webps...")

        webps = filter(lambda path: path[1].lower().endswith("webp"), file_paths)

        return list(webps)

    def create_pngs(self, file_paths):
        print("creating pngs...")

        for i, (directory, filename) in enumerate(file_paths):
            new_filename = filename[:-len("webp")] + 'png'
            if self.args.output != None:
                new_directory = str(self.args.output)
            else:
                new_directory = directory

            old_path = os.path.join(directory, filename)
            new_path = os.path.join(new_directory, new_filename)
            command = "dwebp \"{}\" -o \"{}\"".format(old_path, new_path)

            os.system(command)
            # print()
            if self.args.verbose:
                print("\rconverting file {:>3} out of {:>3}\n".format(i + 1, len(file_paths)), end="")

    def delete_old_files(self, file_paths):
        print("deleting old files...")

        for directory, filename in file_paths:
            file_path = os.path.join(directory, filename)
            if os.path.exists(file_path):
                # print("delete {}".format(file_path))
                os.remove(file_path)
            elif self.args.verbose:
                print("file not found: {}".format(file_path))


    def webp2png(self):
        file_paths = self.get_all_file_paths()
        webps = self.filter_webps(file_paths)
        self.create_pngs(webps)
        if not self.args.keep:
            self.delete_old_files(webps)


if __name__ == "__main__":
    converter = Converter()
    converter.webp2png()