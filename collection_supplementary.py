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

	input_csv = results.input_file_list[0]
	provider_collection_count = [] #count collections contributed by each provider
	dataProvider_collection_count = [] # count collections contributed by each dataProvider

	try:
		with open(input_csv, 'r') as input_file:

			input_reader = csv.reader(input_file)

			#skip the header
			next(input_reader, None)

			# keep track of previous provider and dataProvider
			previous_provider = ''
			previous_dataProvider = ''

			for collection_info_row in input_reader:
				#print(collection_info_row)
				current_provider = collection_info_row[0]
				current_dataProvider = collection_info_row[1]

				# update provider_collection_count
				if current_provider == previous_provider:
					provider_collection_count[len(provider_collection_count) - 1]['count'] = provider_collection_count[len(provider_collection_count) - 1]['count'] + 1
				else:
					provider_collection_count_entry = {'provider.name': current_provider, 'count': 1}
					provider_collection_count.append(provider_collection_count_entry)
					previous_provider = current_provider

				# update dataProvider_collection_count
				if current_dataProvider == previous_dataProvider:
					dataProvider_collection_count[len(dataProvider_collection_count) - 1]['count'] = dataProvider_collection_count[len(dataProvider_collection_count) - 1]['count'] + 1
				else:
					dataProvider_collection_count_entry = {'dataProvider.name': current_dataProvider, 'count': 1}
					dataProvider_collection_count.append(dataProvider_collection_count_entry)
					previous_dataProvider = current_dataProvider

	except IOError as input_file_error:
		print("this input file cannot be read")

	print("**************** Q4: How many collections is are contributed by each provider: ***************")
	print(provider_collection_count)

	print("**************** Q12: How many collections is are contributed by each provider: ***************")
	print(dataProvider_collection_count)


def main():
	collection_supplementary()

main()
