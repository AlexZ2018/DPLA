'''
import sys
import dpla_utils
#import get_provider_list
#import set_provider_list
import csv
def set_dataProvider_list():
        api_key = "00cab391260d2c1862c8673dd5651a53"
        #set_provider_list.set_provider_list()
        #csv_reader = csv.reader(open('files/provider_list.csv'))
        try:
                csv_reader = csv.reader(open(sys.argv[1]))
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

                                with open('files/' + current_provider + '_dataProvider_list.csv', 'w') as file_open:
                                        header = ['term', 'count']
                                        writer = csv.DictWriter(file_open, header)
                                        writer.writeheader()
                                        writer.writerows(dataprovider_result_list)
                                        #header = ['dataProvider.name', 'count']
                                        #writer.writeheader()

                                with open('files/' + current_provider + '_dataProvider_list.csv') as file1:
                                        f_csv = csv.DictReader(file1)
                                        for index, row in enumerate(f_csv):
                                                key = 'provider'
                                                value = 'current_provider'
                                                row[key] = value
                print("There are " + str(count) + " dataProviders contribute data for DPLA")

        except IOError as e:
                print("Please enter a valid file name. ")
                #logging.exception(e)
set_dataProvider_list()
