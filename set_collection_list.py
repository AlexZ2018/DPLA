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
                #open input file, traverse it, and get each dataProvider list path
                with open(input_file) as input_file:
                        provider_csv_reader = csv.reader(input_file)

                        #skip header
                        next(provider_csv_reader, None)
                        for provider_information_row in provider_csv_reader:
                                dataProvider_file_path = provider_information_row[2]# 2 or 3???

                                #open dataProvider file
                                with open(dataProvider_file_path) as dataProvider_input_file:
                                        dataProvider_csv_reader = csv.reader(dataProvider_input_file)

                                        #skip the header
                                        next(dataProvider_csv_reader, None)
                                        for dataProvider_information_row in dataProvider_csv_reader:
                                                dataProvider_name = dataProvider_information_row[0] #0??

                                                #query collections by faceting dataProvider.name
                                                query_term = {'dataProvider.name': dataProvider_name}
                                                query_term['facets'] = 'collection.id'
                                                collection_query_response = dpla_utils..dpla_fetch_facets_remote(api_key, **query_terms)

                                                #process query response
                                                collcetions_result_list = ????

                                                try:
                                                        #write collection information into files
                                                        with open(output_file, 'w') as collection_file:
                                                                collection_file_writer = csv.writer(collection_file)
                                                                collection_file_writer.writerow(??????????)
                                                                collection_file_writer.writerows(collections_result_list)

                                                        collection_file.close()

                                                except IOError as output_file_error:
                                                        print("could not write to this output file")
                                dataProvider_input_file.close()
                input_file.close()                              
                        
        except IOError as input_file_error:
                print("couldn`t read the input file ") 
      
def main():
        set_collection_list()

main()
