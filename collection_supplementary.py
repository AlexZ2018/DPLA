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
	collection_title_list = [] # keep track of previous collection title
	collection_id_list = [] # keep track of previous collection id
	collection_multi_dataProvider = [] # record collections contributing multiple dataprovider <collection.title, collection.id, dataProvider_list[]>
	true_collection_multi_dataProvider = []
	try:
		with open(input_csv, 'r') as input_file:

			input_reader = csv.reader(input_file)

			#skip the header
			next(input_reader, None)

			# keep track of previous provider and dataProvider
			previous_provider = ''
			previous_dataProvider = ''
			collection_title_list.append('')
			collection_id_list.append('')

			for collection_info_row in input_reader:
				#print(collection_info_row)
				current_provider = collection_info_row[0]
				current_dataProvider = collection_info_row[1]
				current_collection_title = collection_info_row[3]
				current_collection_id = collection_info_row[2]

				# update provider_collection_count
				if current_provider == previous_provider:
					provider_collection_count[len(provider_collection_count) - 1]['count_of_collections'] += 1
				else:
					provider_collection_count_entry = {'provider.name': current_provider, 'count_of_collections': 1}
					provider_collection_count.append(provider_collection_count_entry)
					previous_provider = current_provider

				# update dataProvider_collection_count
				if current_dataProvider == previous_dataProvider:
					dataProvider_collection_count[len(dataProvider_collection_count) - 1]['count_of_collections'] += 1
					dataProvider_collection_count[len(dataProvider_collection_count) - 1]['count_of_items'] += collection_info_row[4]
				else:
					dataProvider_collection_count_entry = {'dataProvider.name': current_dataProvider, 'count_of_collections': 1, 'count_of_items': collection_info_row[4]}
					dataProvider_collection_count.append(dataProvider_collection_count_entry)
					previous_dataProvider = current_dataProvider

				# update collection_multi_dataProvider list, this is for decreasing time complexity so we don`t have to traverse all the time
				if (current_collection_title in collection_title_list) and (current_collection_id in collection_id_list):
					# traverse collection_multi dataProvider and update the entry
					#print(current_collection_title)
					#print(current_collection_id)
					for index in range(len(collection_multi_dataProvider)):
						if (current_collection_title == collection_multi_dataProvider[index]['collection.title']) and (current_collection_id == collection_multi_dataProvider[index]['collection.id']):
							collection_multi_dataProvider[index]['dataProvider_list'].append(current_dataProvider)
							break
				else:
					# update collection_title and collection_id lists
					if not current_collection_title == '':
						collection_title_list.append(current_collection_title)

					if not current_collection_id == '':
						collection_id_list.append(current_collection_id)

					current_dataProvider_list = []
					current_dataProvider_list.append(current_provider)
					new_collection_multi_dataProvider_entry = {'collection.title': current_collection_title, 'collection.id': current_collection_id, 'dataProvider_list': current_dataProvider_list}
					collection_multi_dataProvider.append(new_collection_multi_dataProvider_entry)
					
			#true_collection_multi_dataProvider = []
			for index in range(len(collection_multi_dataProvider)):
				collection_info = collection_multi_dataProvider[index]
				if not len(collection_info['dataProvider_list']) == 1:
					true_collection_multi_dataProvider.append(collection_info)

	except IOError as input_file_error:
		print("this input file cannot be read")

	print("**************** Q4 : How many collections is are contributed by each provider: ***************")
	print("************************ Q9 : Which providers contribute collections: *************************")
	print(provider_collection_count)

	print("**************** Q12: How many collections is are contributed by each provider: ***************")
	print("**************** Q11: How many items per dataProvider are included in collections: *************")
	print(dataProvider_collection_count)

	print("**************** Q15: How many collections include more than one dataProvider: ***************")
	print(true_collection_multi_dataProvider)


def main():
	collection_supplementary()

main()
