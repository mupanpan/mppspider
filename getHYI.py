import requests
from bs4 import BeautifulSoup

def getOneRow(tr_bf):
	name = BeautifulSoup(str(tr_bf), "html.parser").find_all('td', class_="views-field views-field-nothing")
	nativename = BeautifulSoup(str(tr_bf), "html.parser").find_all('td', class_="views-field views-field-field-nativelanguagename")
	country = BeautifulSoup(str(tr_bf), "html.parser").find_all('td', class_="views-field views-field-taxonomy-vocabulary-3")
	taxonomy = BeautifulSoup(str(tr_bf), "html.parser").find_all('td', class_="views-field views-field-taxonomy-vocabulary-4")
	startenddate = BeautifulSoup(str(tr_bf), "html.parser").find_all('td', class_="views-field views-field-field-startdate")

	affi_name = ""

	name_href = gethref(name)
	name = geta_df(name)
	taxonomy = geta_df(taxonomy)

	if nativename:
		nativename = nativename[0].string.strip()
	else:
		nativename = ""

	country = geta_df(country)
	#print(name_href)
	if name_href:
		affi_name = getAffiliation(name_href)
		print(getlatlng(affi_name))

	print([name, name_href, affi_name, country, taxonomy])
		

def gethref(td_bf):
	a_bf = BeautifulSoup(str(td_bf), "html.parser").find_all('a')

	if a_bf:
		return a_bf[0].get('href')
	else:
		return []

def geta_df(td_bf):
	a_bf = BeautifulSoup(str(td_bf), "html.parser").find_all('a')
	if a_bf:
		return a_bf[0].string
	else:
		return ""

def getAffiliation(href):
    response = requests.get(url=href)
    html = response.text
    bf = BeautifulSoup(html, "html.parser")
    affi = bf.find('div', {"id": "block-cck-blocks-taxonomy-vocabulary-5"})
    a_bf = BeautifulSoup(str(affi), "html.parser").find_all('a')

    if a_bf:
    	return a_bf[0].string
    else:
    	return ""

def getlatlng(affi):
	affi = affi.replace(' ', '+')
	#country = '+' + country
	response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+affi)
	resp_json_payload = response.json()
	try:
		return resp_json_payload['results'][0]['geometry']['location']
	except IndexError:
		return {'lat': None, 'lng': None}


targets = ["https://harvard-yenching.org/alumni?program=All&field_familyname_value=&field_startdate_value%5Bvalue%5D&field_startdate_value2%5Bvalue%5D&page=" + str(i) for i in range(36)]

for target in targets:	
	#target = "https://harvard-yenching.org/alumni?program=All&field_familyname_value=&field_startdate_value%5Bvalue%5D&field_startdate_value2%5Bvalue%5D&page=35"
	response = requests.get(url=target)
	html = response.text
	bf = BeautifulSoup(html, "html.parser")
	tr_bfs = bf.find_all('tr')
	for tr_bf in tr_bfs:
		getOneRow(tr_bf)


