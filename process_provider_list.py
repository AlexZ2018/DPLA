'''
process_provider_list.py
for adjusting provider_list.csv, add dataProvider_document_path
called by set_collection_list, 
'''
import sys
import dpla_utils
import getopt, dpla_config
import csv
import argparse

PROVIDER_NEW_HEADER_PROVIDER_NAME = 'provider.name'
PROVIDER_NEW_HEADER_ITEMS_COUNT = 'count_of_items'
PROVIDER_NEW_HEADER_DATAPROVIDER_PATH = 'dataProvider_file_path'

def process_provider_list(provider_file):
        provider_rows = []

        #read provider_list and store it into a list, append dataProvider document path

        with open(provider_file, 'r') as provider_list_input:

                provider_reader = csv.reader(provider_list_input)

                reader_row = next(provider_reader)
                for provider_information in provider_reader:
                        provider_information.append('files/dataProvider/' + provider_information[0] + '.csv')
                        provider_rows.append(provider_information)
        provider_list_input.close()

        #re-write the list into file, added dataProvider_file_path
        with open(provider_file, 'w', newline = '') as provider_list_output:
                provider_writer = csv.writer(provider_list_output, lineterminator='\n')
                
                provider_writer.writerow([PROVIDER_NEW_HEADER_PROVIDER_NAME, PROVIDER_NEW_HEADER_ITEMS_COUNT, PROVIDER_NEW_HEADER_DATAPROVIDER_PATH])
                provider_writer.writerows(provider_rows)
      

process_provider_list(provider_file)
