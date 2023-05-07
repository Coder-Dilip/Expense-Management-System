import requests
import json
def Example(grade, names, status,counts):
  url = "https://sheet.zoho.com/api/v2/c89f4f28295112c494f26baef3e14af173978"    # yo url change garni
  paramMap = {}
  paramMap['method'] = 'range.content.get'
  paramMap['worksheet_name'] = grade  
  paramMap['start_row'] = 2
  paramMap['start_column'] = 2
  paramMap['end_row'] = 21
  paramMap['end_column'] = 3

  headers = { 
  'Content-type':'application/x-www-form-urlencoded',  
  'Authorization':"Zoho-oauthtoken 1000.e68bf40f66286e56781c09fafc6bd168.f92596177f75cf68eb1dbb9b11778fb7"
  }
  response = requests.post(url = url, headers = headers, data = paramMap)
  data=json.loads(response.text)
  counts[0]+=1
  print(counts[0])
  for el in data['range_details']:
    names.append(el['row_details'][0]['content'])
    status.append(el['row_details'][1]['content'])
#   print(data['range_details'][0]['row_details'][0]['content'],data['range_details'][0]['row_details'][1]['content'])
#   print(names)
#   print(len(status))

grades=["Nursery","Class-1","Class-10"]      # full ko lagi yo rakhni ["Nursery","Class-1","Class-2","Class-3","Class-4","Class-5","Class-6","Class-7","Class-8","Class-9","Class-10"]

names=[]
status=[]
counts=[0]
for x in range(3):
  Example(grades[x],names, status,counts)


# print(len(names))
print(len(status),len(names))
