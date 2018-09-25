'''
set_dataProvider_list.py
'''
import sys
import dpla_utils
import getopt, dpla_config
import csv
import argparse
# argparse
def set_dataProvider_list():
        api_key = dpla_config.API_KEY

        # put this in a seperate function
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', action='append', dest = 'input_file_list')
        parser.add_argument('-e', action = 'append', dest = 'folder_list')
        results = parser.parse_args()

        #input_file = results['i']
        #print(results)
        '''
        opts, args = getopt.getopt(sys.argv[1:], "hi:e:")
        folder, input_file = "",""
        for op, value in opts:
                if op == "-e":
                        folder = value                
                elif op == "-i":
                        input_file = value
        '''
        input_file = results.input_file_list[0]
        folder = results.folder_list[0]
        try:
                with open(input_file) as input_file:
                        provider_csv_reader = csv.reader(input_file)
                        header_boolean = True # delete
                        dataProvider_count = 0 
                
                        for provider_information_row in provider_csv_reader: 
                        
                                # this is for skiping the header, which is the first line, or we can say this variable is a flag
                                if header_boolean: 
                                        header_boolean = False
                                        continue
                                else:
                                        current_provider_name = provider_information_row[0] 

                                        # comment for query and facet
                                
                                        query_terms = {'provider.name': current_provider_name}
                                        query_terms['facets'] = 'dataProvider'
                                        dataProvider_query_response = dpla_utils.dpla_fetch_facets_remote(api_key, **query_terms)
                                        #print(response)
                                        dataprovider_result_list = dataProvider_query_response['dataProvider']['terms']
                                        dataProvider_count += len(dataprovider_result_list)
                                
                                        try:
                                                with open(folder + current_provider_name + '.csv', 'w') as dataProvider_file:
                                                        print(folder + current_provider_name + '.csv');
                                                        header = ['term', 'count'] # put in begining
                                                        dataProvider_csv_writer = csv.DictWriter(dataProvider_file, header)
                                                        dataProvider_csv_writer.writeheader()
                                                        dataProvider_csv_writer.writerows(dataprovider_result_list)

                                                dataProvider_file.close();
                                        
                                        except IOError as folder_error: 
                                                print("couldn`t create file in this folder") 
                                                sys.exit()
                        print("There are " + str(dataProvider_count) + " dataProviders contribute data for DPLA")
                        input_file.close();
        except IOError as input_file_error: 
                print("couldn`t read the input file ") 
                
set_dataProvider_list() # main funciton # close csv
