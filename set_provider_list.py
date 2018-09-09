'''
set_provider_list.py
This fuction is used for getting all the providers in DPLA with the format {id, name, count}
'''
import dpla_utils
import sys, getopt
import csv

def get_pvd():
        api_key = "00cab391260d2c1862c8673dd5651a53"
        condi = {'facets': 'provider'}
        _dict = dpla_utils.dpla_fetch_facets_remote(api_key,"items",  **condi)
        result_list = []
        #travers subarray key: id or name
        for key, value in _dict.items():
                _key = key
                _list = value['terms'] # type: list
                # treaverse the list of id and name
                for index in range(len(_list)):
                        i = index
                        sub_dict = _list[i]
                        length = len(result_list)
                        if i + 1 > length:
                                unit_dict = {'count': sub_dict['count'], _key: sub_dict['term']}
                                #print(unit_dict)
                                result_list.append(unit_dict)
                        else:
                                unit_dict = result_list[i]
                                unit_dict[_key] = sub_dict['term']
                                result_list[i] = unit_dict

        #print(result_list)
        #print("The amount of Providers: " + str(len(result_list)))
        return result_list

def set_provider_list():
        
        opts, args = getopt.getopt(sys.argv[1:], "ho:")
        output_file = ""
        for op, value in opts:
                if op == "-o":
                        output_file = value
                else:
                        print("please enter a valid output file")
                        sys.exit()

        #provider_list = get_pvd()
        try:
                provider_list = get_pvd()
                with open(output_file, 'w') as file_open:
                        file_header = ['provider.name', 'provider.@id', 'count']
                        writer = csv.DictWriter(file_open, file_header)
                        writer.writeheader()
                        writer.writerows(provider_list)
       
                        print("List of providers has been successfully written to files as provider_list.csv")
                        print("The amount of Providers: " + str(len(provider_list)))
        except IOError as e:
                print("please enter a valid output file")

set_provider_list()
