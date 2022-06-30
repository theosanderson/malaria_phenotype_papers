import argparse
parser = argparse.ArgumentParser(description='Search for titles')
parser.add_argument('-m', '--max', type=int, default=0, help='Maximum number of results to return')

args = parser.parse_args()
# You should test that your search return results first on the web
# https://www.ncbi.nlm.nih.gov/dbvar before using them
# in your python script.  Available dbVar search terms are on the help page
# (https://www.ncbi.nlm.nih.gov/dbvar/content/help/#entrezsearch).
# For general Entrez help and boolean search see the online book
# (https://www.ncbi.nlm.nih.gov/books/NBK3837/#EntrezHelp.Entrez_Searching_Options)

# This example will make use of these eUtils History Server parameters
# usehistory, WebEnv, and query_key.  It is highly recommended you use them in
# your pipeline and script.

# /usehistory=/
# When usehistory is set to 'y', ESearch will post the UIDs resulting from the
# search operation onto the History server so that they can be used directly in
# a subsequent E-utility call. Also, usehistory must be set to 'y' for ESearch
# to interpret query key values included in term or to accept a WebEnv as input.

# /WebEnv=/
# Web environment string returned from a previous ESearch, EPost or ELink call.
# When provided, ESearch will post the results of the search operation to this
# pre-existing WebEnv, thereby appending the results to the existing
# environment. In addition, providing WebEnv allows query keys to be used in
# term so that previous search sets can be combined or limited. As described
# above, if WebEnv is used, usehistory must be set to 'y' (ie.
# esearch.fcgi?db=dbvar&term=asthma&WebEnv=<webenv string>&usehistory=y)

# /query_key=/
# Integer query key returned by a previous ESearch, EPost or ELink call. When
# provided, ESearch will find the intersection of the set specified by query_key
# and the set retrieved by the query in term (i.e. joins the two with AND). For
# query_key to function, WebEnv must be assigned an existing WebEnv string and
# usehistory must be set to 'y'.

# load python modules
# May require one time install of biopython and xml2dict.
from Bio import Entrez
import xmltodict
import re
import tqdm, sys

# initialize some default parameters
Entrez.email = 'theo@theo.io'  # provide your email address
db = 'pubmed'  # set search to dbVar database
paramEutils = {'usehistory': 'Y'}  # Use Entrez search history to cache results

# generate query to Entrez eSearch
eSearch = Entrez.esearch(db=db, term='plasmodium OR malaria', **paramEutils)

# get eSearch result as dict object
res = Entrez.read(eSearch)

retmax = 10000
count = res['Count']

paramEutils['WebEnv'] = res[
    'WebEnv']  #add WebEnv and query_key to eUtils parameters to request esummary using
paramEutils['query_key'] = res[
    'QueryKey']  #search history (cache results) instead of using IdList
paramEutils['rettype'] = 'xml'  #get report as xml
paramEutils['retstart'] = 0  #get result starting at 0, top of IdList
paramEutils['retmax'] = retmax  #get next five results

# with pro
with tqdm.tqdm(total=int(count)) as pbar:
    for retstart in range(0, int(count), retmax):
        if args.max and retstart > args.max:
            break
        # generate query to Entrez eSearch
        print(retstart, file=sys.stderr)
        paramEutils['retstart'] = retstart
        eSearch = Entrez.esummary(db=db, **paramEutils)

        # get eSearch result as dict object
        list_of_results = Entrez.read(eSearch)
        first = 1

        for result in list_of_results:
            if first:
                # print to stderr
                print(result['Id'], file=sys.stderr)
                first = 0
            pbar.update(1)
            # print PMID then title
            title = result['Title']
            #strip all html tags
            title = re.sub('<[^<]+?>', '', title)

            print(result['Id'] + "\t" + title)
