'''
set_collection_list.py
with input: files/provider_list.csv
with output: files/collection_list.csv
'''
import sys
import dpla_utils
import getopt, dpla_config
import csv
import argparse

PROVIDER_HEADER_PROVIDER_NAME = 'provider.name' 
PROVIDER_HEADER_ITEMS_COUNT = 'count_of_items'
PROVIDER_HEADER_DATAPROVIDER_PATH = 'dataProvider_file_path'

def set_collection_list():
        api_key = dpla_config.API_KEY


        #read input output files
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', action='append', dest = 'input_file_list')
        parser.add_argument('-o', action = 'append', dest = 'output_file_list')
        results = parser.parse_args()

        input_file = results.input_file_list[0]
        output_file = results.output_file_list[0]

        try:
                # process_provider_list, add dataProvider_list_path
                process_provider_list(input_file)

                #open input file, traverse it, and get each dataProvider list path
                with open(input_file) as input_file:
                        provider_csv_reader = csv.reader(input_file)

                        #skip header
                        next(provider_csv_reader, None)
                        collections_result_list = []
                        for provider_information_row in provider_csv_reader:

                                print("Calm down and keep patient... Process: ",  int(len(collections_result_list)/ 65), " %")
                                #print(provider_information_row)
                                dataProvider_file_path = provider_information_row[2]# 2 or 3???

                                #open dataProvider file
                                print(dataProvider_file_path)
                                with open(dataProvider_file_path) as dataProvider_input_file:
                                        dataProvider_csv_reader = csv.reader(dataProvider_input_file)

                                        #skip the header

                                        next(dataProvider_csv_reader, None)
                                        for dataProvider_information_row in dataProvider_csv_reader:
                                                #print(dataProvider_information_row[0] )
                                                dataProvider_name = dataProvider_information_row[0] 

                                                #query collections by faceting dataProvider.name
                                                query_term = {'dataProvider': dataProvider_name}
                                                query_term['facets'] = 'sourceResource'
                                                print(dataProvider_name)
                                                collection_query_response = dpla_utils.dpla_fetch_facets_remote(api_key, **query_term)
                                                print(collection_query_response)
                                                #process query response

                                                # collection_query_response['sourceResource.collection.id']['terms'] is a list
                                                '''
                                                for single_collection_information in collection_query_response['sourceResource.collection.id']['terms']:
                                                        collection_single_row = [provider_information_row[0], dataProvider_name]
                                                        collection_single_row.append(single_collection_information['term'])
                                                        collection_single_row.append(single_collection_information['count'])

                                                        #print(collection_single_row)
                                                        collections_result_list.append(collection_single_row)

                                                try:
                                                        #write collection information into files
                                                        with open(output_file, 'w') as collection_file:
                                                                collection_file_writer = csv.writer(collection_file)
                                                                collection_file_writer.writerow(['provider.name', 'dataProvider.name', 'collection.id', 'count_of_items'])
                                                                collection_file_writer.writerows(collections_result_list)

                                                        collection_file.close()

                                                except IOError as output_file_error:
                                                        print("could not write to this output file")
                                                '''
                                dataProvider_input_file.close()
                input_file.close()                              
                        
        except IOError as input_file_error:
                print("couldn`t read the input file ") 

def process_provider_list(provider_file):
        provider_rows = []

        #read provider_list and store it into a list, append dataProvider document path

        with open(provider_file, 'r') as provider_list_input:

                provider_reader = csv.reader(provider_list_input)

                reader_row = next(provider_reader, None)
                for provider_information in provider_reader:
                        provider_information.append('files/dataProvider/' + provider_information[0] + '.csv')
                        provider_rows.append(provider_information)
        provider_list_input.close()
        #print(provider_rows)
        #re-write the list into file, added dataProvider_file_path
        with open(provider_file, 'w', newline = '') as provider_list_output:
                provider_writer = csv.writer(provider_list_output, lineterminator='\n')
                
                provider_writer.writerow([PROVIDER_HEADER_PROVIDER_NAME, PROVIDER_HEADER_ITEMS_COUNT, PROVIDER_HEADER_DATAPROVIDER_PATH])
                provider_writer.writerows(provider_rows)
      
      
def main():
        set_collection_list()

main()
