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
invalid_dataProvider_list = ['C']

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
                entire_collection_list = []
                collection_count = 0

                #open input file, traverse it, and get each dataProvider list path
                with open(input_file) as input_file:
                        provider_csv_reader = csv.reader(input_file)

                        #skip header
                        next(provider_csv_reader, None)
                        collections_result_list = []
                        for provider_information_row in provider_csv_reader:

                                print("*************  Calm down and keep patient... Process: ",  int(collection_count/ 365), " %     *******************")
                                #print(provider_information_row[0])
                                dataProvider_file_path = provider_information_row[2]

                                #open dataProvider file
                                #print(dataProvider_file_path)
                                with open(dataProvider_file_path) as dataProvider_input_file:
                                        dataProvider_csv_reader = csv.reader(dataProvider_input_file)

                                        #skip the header

                                        next(dataProvider_csv_reader, None)
                                        for dataProvider_information_row in dataProvider_csv_reader:
                                                item_collection_id_dict = {'@id': 'collection_id'} # keep track of collection.id of each item
                                                item_collection_title_dict = {'@id', 'title'}
                                                item_belongs_to_no_collection_count = 0
                                                item_belongs_to_multi_collections_list = []
                                                collection_list = [] #record collection.title, collection.id, count
                                                #print(dataProvider_information_row[0] )
                                                dataProvider_name = dataProvider_information_row[0] 
                                                
                                                if dataProvider_name in invalid_dataProvider_list:
                                                        continue
                                                dataProvider_name = process_dataProvider_name(dataProvider_name)
                                                #query collections by faceting dataProvider.name
                                                query_term = {'dataProvider': dataProvider_name}#dataProvider_name
                                                #query_term['facets'] = 'sourceResource.subject.@id'
                                                query_term['fields'] = 'sourceResource.collection,@id'
                                                query_term['count'] = 10 # need to be larger
                                                #print(provider_information_row[0])
                                                #print(dataProvider_name)
                                                collection_query_response = dpla_utils.dpla_fetch_remote(api_key, **query_term)
                                                #print(' here is the response ::::::::::::')
                                                #print(collection_query_response)
                                                for index in range(len(collection_query_response)):
                                                        #if current item belongs to no collection
                                                        if not 'sourceResource.collection' in collection_query_response[index]:
                                                                item_belongs_to_no_collection_count = item_belongs_to_no_collection_count + 1
                                                        else:
                                                                current_item = collection_query_response[index]['@id']
                                                                current_collection = collection_query_response[index]['sourceResource.collection']
                                                                #check if this item belongs to multiple collection
                                                                if (current_item in item_collection_id_dict) or (current_item in item_collection_title_dict):
                                                                        item_belongs_to_multi_collections_list.append(current_item)
                                                                else:
                                                                        # record this item - collection mapping
                                                                        if 'title' in current_collection:
                                                                                item_collection_title_dict.update({current_item: current_collection['title']})
                                                                                #item_collection_title_dict[current_item] = current_collection['title']
                                                                        if 'id' in current_collection:
                                                                                item_collection_id_dict.update({current_item: current_collection['id']})
                                                                                #item_collection_id_dict[current_item] = current_collection['id']

                                                                        # check if need a new collection ro record this collection - item mapping
                                                                        collection_already_exist = False
                                                                        for collection_index in range(len(collection_list)):
                                                                                current_collection_entry = collection_list[collection_index]
                                                                                #print('current_collection_entry[collection.title] is ', current_collection_entry['collection.title'])
                                                                                if (('title' in current_collection) and (current_collection['title'] == current_collection_entry['collection.title'])) or (('id' in current_collection) and (current_collection['id'] == current_collection_entry['collection.id'])):
                                                                                        # run this when current collection already exists
                                                                                        collection_list[collection_index]['count'] = collection_list[collection_index]['count'] + 1
                                                                                        collection_already_exist = True;
                                                                                        break; # so this works when current_collection is only one collection

                                                                        # we really need a new collection entry!!
                                                                        #print(" going to enter new collection creation")
                                                                        if collection_already_exist == False:
                                                                                #print(" going to enter new collection creation")
                                                                                #initialize
                                                                                new_collection_entry = {'collection.title': None, 'collection.id': None, 'count': 1, 'provider.name': provider_information_row[0], 'dataProvider.name': dataProvider_name}
                                                                                #new_collection_entry['collection.id'] = None
                                                                                #new_collection_entry['count'] = 1;
                                                                                if 'title' in current_collection:
                                                                                        new_collection_entry['collection.title'] = current_collection['title']
                                                                                if 'id' in current_collection:
                                                                                        new_collection_entry['collection.id'] = current_collection['id']
                                                                                #print(" this is new collection entry ::::::::::::::::::::::::::::::")
                                                                                #print(new_collection_entry)
                                                                                if not (new_collection_entry['collection.title'] is None) and (new_collection_entry['collection.id'] is None):
                                                                                        collection_list.append(new_collection_entry)
                                                #print(" This is collection list : : : : : : : : : \n")
                                                #print(collection_list)
                                                print(dataProvider_name, " contributes items with no collection :::::", item_belongs_to_no_collection_count)
                                                collection_count = collection_count + len(collection_list)
                                                entire_collection_list.append(collection_list)

                                                #process query response

                                                # collection_query_response['sourceResource.collection.id']['terms'] is a list
                                dataProvider_input_file.close()               
                        
                        try:
                                #write collection information into files
                                with open(output_file, 'w') as collection_file:
                                        collection_file_writer = csv.writer(collection_file)
                                        header = ['provider.name', 'dataProvider.name', 'collection.id', 'collection.title', 'count']
                                        collection_file_writer.writerow(header)
                                        collection_csv_writer = csv.DictWriter(collection_file, header)
                                        #collection_file_writer.writerows(collections_result_list)
                                        for index in range(len(entire_collection_list)):
                                                if len(entire_collection_list[index]) == 0:
                                                        continue
                                                print("current list :::::::::::::::::::", entire_collection_list[index])
                                                collection_csv_writer.writerows(entire_collection_list[index])

                                collection_file.close()

                        except IOError as output_file_error:
                                print("could not write to this output file")
                                                
                                #dataProvider_input_file.close()
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
      
def process_dataProvider_name(dataProvider_name):
        if "[" in dataProvider_name:
                dataProvider_name = dataProvider_name.replace("[", "\[")

        if "]" in dataProvider_name:
                dataProvider_name = dataProvider_name.replace("]", "\]")

        if "/" in dataProvider_name:
                dataProvider_name = dataProvider_name.replace("/", "\/")

        return dataProvider_name
      
def main():
        set_collection_list()

main()
