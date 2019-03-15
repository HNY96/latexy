#!/usr/bin/env python3

import argparse
import json
import re


def readFile(path):
	with open(path) as fp:
		content = fp.read()
	return content


# the return dict is like {markdown:latex}, {"*":"textit"}
def readConfig(path):
	with open(path) as fp:
		content = json.load(fp)
	return content


def writeFile(content, path):
	with open(path, mode="w") as fp:
		fp.write(content)


def parseArgs():
	parser = argparse.ArgumentParser(description="Describe your config!")
	parser.add_argument("-i", help="The input file path.")
	parser.add_argument("-o", help="The output file path. Default is same as input file path.")
	parser.add_argument("-c", help="The config file path.")
	args = parser.parse_args()

	return args.i, args.o, args.c


def translate(content, config_dict):
	pass


def main():
	input_path, output_path, config_path = parseArgs()

	# read the file from designated path
	if not input_path:
		print("Please give me the source.")
		exit()
	content = readFile(input_path)

	# read config file from designated path
	if not config_path:
		print("Please give me the config file.")
		exit()
	config_dict = readConfig(config_path)

	# translate from markdown to latex source
	content_translated = translate(content, config_dict)

	# output the file
	if not output_path:
		output_path = input_path.replace("md", "txt")
	writeFile(content_translated, output_path)

	print("Done!")


if __name__ == '__main__':
	main()