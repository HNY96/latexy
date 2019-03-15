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
	for type_key, value in config_dict.items():
		# like *itelic*
		if type_key == "pair":
			for pre, after in value.items():
				# need to be found
				my_re = re.escape(pre) + r"[\S| ]*?" + re.escape(pre)

				# I have to define here because subPair only take 1 argument
				def subPair(myobejct, pre=pre, after=after):
					tmp = myobejct.group(0).replace(pre, '{', 1)
					tmp = tmp[::-1]
					tmp = tmp.replace(pre, '}', 1)
					tmp = tmp[::-1]
					# add a \ to activate function in latex
					tmp = "\\" + after + tmp
					# add escape for _
					tmp = re.sub(r"_", r"\_", tmp)
					return tmp

				content = re.sub(my_re, subPair, content)
				# print(pre, after)
		elif type_key == "single":
			for pre, after in value.items():
				my_re = r"^" + re.escape(pre) + r" [\S| ]*"

				def subSingle(myobejct, pre=pre, after=after):
					tmp = myobejct.group(0).replace(pre, '')
					# because there may have a space between # and text
					tmp = tmp.strip()
					tmp = "\\" + after + "{" + tmp + "}"
					return tmp

				content = re.sub(my_re, subSingle, content, flags=re.MULTILINE)

		# some other change because of bug of Ulysses
		content = content.replace('’', '\'')

	return content


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