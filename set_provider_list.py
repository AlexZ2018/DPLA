'''
set_provider_list.py
This fuction is used for getting all the providers in DPLA with the format {id, name, count}
'''
import dpla_utils
import sys, getopt, dpla_config
import csv
import argparse

DPLA_PROVIDER_HEADER_NAME = 'provider.name'
DPLA_PROVIDER_HEADER_COUNT = 'count'

def get_providers():
        api_key = dpla_config.API_KEY
        query_terms = {'facets': 'provider.name'}
        facet_response = dpla_utils.dpla_fetch_facets_remote(api_key,  **query_terms)
        provider_result_list = []

        #travers subarray key: id or name
        for key, value in facet_response.items():
                provider_list = value['terms'] # type: list
                # treaverse the list of id and name
                for index in range(len(provider_list)):
                        
                        sub_facet_response = provider_list[index]
                        
                        length = len(provider_result_list)
                        single_facet_response = {'count': sub_facet_response['count'], key: sub_facet_response['term']}
                                
                        provider_result_list.append(single_facet_response)
                        

        return provider_result_list

def set_provider_list():

        # Read output file from command line
        parser = argparse.ArgumentParser()
        parser.add_argument('-o', action='append', dest = 'output_file_list')
        results = parser.parse_args()

        output_file = results.output_file_list[0]
        
        try:
                provider_list = get_providers()
                
                with open(output_file, 'w') as provider_file_open:
                        file_header = [DPLA_PROVIDER_HEADER_NAME, DPLA_PROVIDER_HEADER_COUNT]
                        provider_writer = csv.DictWriter(provider_file_open, file_header)
                        provider_writer.writeheader()
                        provider_writer.writerows(provider_list)

                        print("List of providers has been successfully written to files as provider_list.csv")
                        print("The amount of Providers: " + str(len(provider_list)))
        except IOError as e:
                print("cannot open output file")


def main():
        set_provider_list()

main()
