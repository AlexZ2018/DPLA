import json

FILE_path = "output/"
FILE_SUFFIX_provider_coll_info = "-providerColl.json"
CCD_PROP_LBL_noCollectionItemCount = "noCollectionItemCount"

def cal():
    countItemsNoColl = 0
    providers = ['HathiTrust', 'National Archives and Records Administration', 'Smithsonian Institution', 'The New York Public Library', 'University of Southern California. Libraries', 'The Portal to Texas History', 'Mountain West Digital Library', 'California Digital Library', 'Minnesota Digital Library', 'Digital Library of Georgia', 'Recollection Wisconsin', 'Empire State Digital Network', 'North Carolina Digital Heritage Center', 'Digital Commonwealth', 'Internet Archive', 'Missouri Hub', 'PA Digital', 'United States Government Publishing Office (GPO)', 'Digital Library of Tennessee', 'Indiana Memory', 'University of Washington', 'Kentucky Digital Library', 'Biodiversity Heritage Library', 'South Carolina Digital Library', 'ARTstor', 'J. Paul Getty Trust', 'David Rumsey', 'University of Virginia Library', 'University of Illinois at Urbana-Champaign', 'Harvard Library']
    for providerName in providers:
        provider_filename = providerName.replace(' ','-') + FILE_SUFFIX_provider_coll_info
        with open(FILE_path + provider_filename) as data_file:
            data = json.load(data_file)
            countItemsNoColl += data[CCD_PROP_LBL_noCollectionItemCount]

    print(countItemsNoColl)
    
cal()
