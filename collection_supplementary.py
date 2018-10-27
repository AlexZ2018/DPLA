'''
collection_supplementary.py
with input: files/collection_list.csv
'''
import sys
import dpla_utils
import getopt, dpla_config
import csv
import argparse

def collection_supplementary():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', action='append', dest = 'input_file_list')
	results = parser.parse_args()

	input_file = results.input_file_list[0]

def main():
	collection_supplementary()

main()
