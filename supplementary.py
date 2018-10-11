'''
supplementary.py
there should be 2 inputs, provider list, collection list
'''
import sys
import dpla_utils
import getopt, dpla_config
import csv
import argparse


PROVIDER_HEADER_PROVIDER_NAME = 'provider.name' 
PROVIDER_HEADER_ITEMS_COUNT = 'count_of_items'
PROVIDER_HEADER_DATAPROVIDER_PATH = 'dataProvider_file_path'

def supplementary():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', action='append', dest = 'input_file_list')
	#parser.add_argument('-e', action = 'append', dest = 'output_file_dir')
	results = parser.parse_args()
	
	provider_file = results.input_file_list[0]
	#collection_file = results.input_file_list[1] # does this work?

	#dataProvider_dir = results.output_file_dir[0] # should be 'files/dataProvider/'
	dataProvider_list = []
	repeated_dataProvider_list = []
	try:

		process_provider_list(provider_file)
		with open(provider_file) as provider_input_file:
			provider_csv_reader = csv.reader(provider_input_file)

			#skip header
			next(provider_csv_reader, None)

			for provider_information_row in provider_csv_reader:
				dataProvider_file_path = provider_information_row[2]

				#read dataProvider files
				with open(dataProvider_file_path) as dataProvider_input_file:
					dataProvider_csv_reader = csv.reader(dataProvider_input_file)

					#skip the header
					skip_header = next(dataProvider_csv_reader, None)

					print("skip_header::   ", skip_header)
					# traverse each dataProvider list
					for dataProvider_information_row in dataProvider_csv_reader:
						current_dataProvider_name = dataProvider_information_row[0]
						print(current_dataProvider_name)
						#if repeated
						if current_dataProvider_name in dataProvider_list:
							print(current_dataProvider_name)
							if not current_dataProvider_name in repeated_dataProvider_list:
								repeated_dataProvider_list.append(current_dataProvider_name)
						# if not repeated
						else:
							# Question: How many items are contributed by each dataProvider?
							print("dataProvider ", current_dataProvider_name, " contributes ", dataProvider_information_row[1], " items")

							dataProvider_list.append(current_dataProvider_name)

				dataProvider_input_file.close()
		provider_input_file.close()

		#Question: Are there any dataProviders who contribute items to more than one provider?
		print("dataProviders contributes items to more than one providers:")
		print(repeated_dataProvider_list)
	except IOError as provider_input_file_error:
		print("couldn`t read the input file ") 

def process_provider_list(provider_file):
        provider_rows = []

        #read provider_list and store it into a list, append dataProvider document path

        with open(provider_file, 'r') as provider_list_input:

                provider_reader = csv.reader(provider_list_input)

                reader_row = next(provider_reader, None)
                for provider_information in provider_reader:
                        #process provider_information[0]
                        provider_information[0] = provider_information[0].replace(' ', '_', 256)
                        
                        provider_information.append('files/dataProvider/' + provider_information[0] + '.csv')
                        provider_rows.append(provider_information)
        provider_list_input.close()
        #print(provider_rows)
        #re-write the list into file, added dataProvider_file_path
        with open(provider_file, 'w', newline = '') as provider_list_output:
                provider_writer = csv.writer(provider_list_output, lineterminator='\n')
                
                provider_writer.writerow([PROVIDER_HEADER_PROVIDER_NAME, PROVIDER_HEADER_ITEMS_COUNT, PROVIDER_HEADER_DATAPROVIDER_PATH])
                provider_writer.writerows(provider_rows)

supplementary()
