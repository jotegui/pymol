import json
import urllib, urllib2

# VARIABLES #
# Access to the api
api_base='http://mol.cartodb.com/api/v2/sql?'

# Table names
synonym_table = 'synonyms_carsten_n10'

# FUNCTIONS #
# Query execution
def buildQuery(query):
    params = {'q': query}
    query_url = api_base+urllib.urlencode(params)
    return query_url

def executeQuery(query_url):
    content = urllib2.urlopen(query_url).read()
    data = json.loads(content)
    return data

def execute(query):
    query_url = buildQuery(query)
    data = executeQuery(query_url)
    return data

# Common taxonomy functions
# Detect if a name is valid or not
def isValidOrNot(scientific_name, synonym_table):
    query = 'select case when upper(scientificname)=upper(mol_scientificname) then TRUE else FALSE end as valid from {0} where upper(scientificname) like \'{1}\';'.format(synonym_table, scientific_name.upper())
    data = execute(query)
    try:
        TF = data['rows'][0]['valid']
    except IndexError:
        return None
    return TF

# Extract the valid name for a synonym
def validNameFor(scientific_name, synonym_table):
    query = 'select mol_scientificname as validname from {0} where upper(scientificname) like \'{1}\';'.format(synonym_table, scientific_name.upper())
    data = execute(query)
    try:
        valid = data['rows'][0]['validname']
    except IndexError:
        return None
    return valid

# Return a list of all the synonyms for a name
def listOfSynonyms(scientific_name, synonym_table):
    TF = isValidOrNot(scientific_name, synonym_table)
    if TF is True:
        query = 'select distinct scientificname from {0} where upper(mol_scientificname) like \'{1}\' order by scientificname;'.format(synonym_table, scientific_name.upper())
    elif TF is False:
        query = 'select distinct scientificname from {0} where mol_scientificname in (select mol_scientificname from {0} where upper(scientificname) like upper(\'{1}\')) order by scientificname;'.format(synonym_table, scientific_name.upper())
    else:
        return None
    data = execute(query)
    synonyms = []
    for i in data['rows']:
        if str(i['scientificname']).upper() != scientific_name.upper():
            synonyms.append(str(i['scientificname']))
    return synonyms
    
if __name__ == '__main__':
    scientific_name='Bufo bufo'
    print isValidOrNot(scientific_name, synonym_table)
    
