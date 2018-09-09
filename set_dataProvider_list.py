'''
set_dataProvider_list.py
'''
import sys
import dpla_utils
import getopt, dpla_config
import csv
def set_dataProvider_list():
        api_key = dpla_config.API_KEY
        #set_provider_list.set_provider_list()
        #csv_reader = csv.reader(open('files/provider_list.csv'))
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
        output_file, input_file = "",""
        for op, value in opts:
                if op == "-o":
                        output_file = value
                elif op == "-i":
                        input_file = value
        try:
                csv_reader = csv.reader(open(input_file))
                header = True
                count = 0
                for row in csv_reader:
                        if header:
                                header = False
                                continue
                        else:
                                current_provider = row[0]
                                condition = {'provider.name': current_provider}
                                condition['facets'] = 'dataProvider'
                                response = dpla_utils.dpla_fetch_facets_remote(api_key, **condition)
                                current_dataprovider_list = []
                                sub_dict = response['dataProvider']
                                dataprovider_result_list = sub_dict['terms']
                                count += len(dataprovider_result_list)
                                #with open(output_file + current_provider + '.csv', 'w')
                                try:
                                        with open(output_file + current_provider + '.csv', 'w') as file_open:
                                                header = ['term', 'count']
                                                writer = csv.DictWriter(file_open, header)
                                                writer.writeheader()
                                                writer.writerows(dataprovider_result_list)
                                        #header = ['dataProvider.name', 'count']
                                        #writer.writeheader()

                                        with open(output_file + current_provider + '.csv') as file1:
                                                f_csv = csv.DictReader(file1)
                                                for index, row in enumerate(f_csv):
                                                        key = 'provider'
                                                        value = 'current_provider'
                                                        row[key] = value

                                        #print("There are " + str(count) + " dataProviders contribute data for DPLA")
                                except IOError as f:
                                        print("please enter a valid output_file")
                                        sys.exit()
                print("There are " + str(count) + " dataProviders contribute data for DPLA")

        except IOError as e:
                print("Please enter a valid input file name. ")
                #logging.exception(e)
set_dataProvider_list()


