#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

2012/11/14 - Juan Font (juanfontalonso@gmail.com) 

This script generates the json-formatted data used for http://politikon.es/14N/

"""

import suds   

EXPECTED_FILE = "/tmp/data.json"
COMPARED_FILE ="/tmp/data_past.json"
HARDCODED_STRIKES_FILE = "/tmp/strikes.json"

YESTERDAY = '2012-11-13'
TODAY = '2012-11-14'

def get_programed_demand(date):
  url = "https://demanda.ree.es/WSVisionaV01/wsDemandaMovService?wsdl"    
  client = suds.client.Client(url)
  response = client.service.prevProgMov(date)
  if response:
    return response[0]
  else: 
    None 

def get_detailed_demand(date):
  url = "https://demanda.ree.es/WSVisionaV01/wsDemandaMovService?wsdl"
  client = suds.client.Client(url)
  response = client.service.demandaGeneracionCO2Mov(date)
  if response:
    return response[0] 
  else: 
    None 

def generate_realvsexpec_json(yst_expected, yst_demand, expected, demand):
  result = '['
              
  for ex in yst_expected:
    if YESTERDAY in ex['timeStamp']:
      result = result + ('{ "date": "' + ex['timeStamp'] + '", "demand": null, "expected": ' + str(ex['prevista']) + '},')

  for d in yst_demand:
    if YESTERDAY in d['timeStamp']:
      result = result.replace('"demand": null', '"demand": ' + str(d['demanda']), 1) 
              
  for ex in expected:
    if TODAY in ex['timeStamp']:
      result = result + ('{ "date": "' + ex['timeStamp'] + '", "demand": null, "expected": ' + str(ex['prevista']) + '},')

  for d in demand:
    if TODAY in d['timeStamp']:
      result = result.replace('"demand": null', '"demand": ' + str(d['demanda']), 1) 
  result = result[:-1] + ']'
  
  with open(EXPECTED_FILE, 'w') as f:
    f.write(result)

def generate_comparison_json(demand):
  result='['

  h29M = get_detailed_demand('2012-03-29')
  h29S = get_detailed_demand('2010-09-29')

  for e in h29M:
    if '2012-03-29' in e['timeStamp']:
      result = result + ('{ "date": "' + e['timeStamp'] + '", "29S": null, "29M": ' + str(e['demanda']) + ', "14N": null },')

  for e in h29S:
    if '2010-09-29' in e['timeStamp']:
      result = result.replace('"29S": null', '"29S": ' + str(e['demanda']), 1)
  for e in demand:
    if TODAY in e['timeStamp']:
      result = result.replace('"14N": null', '"14N": ' + str(e['demanda']), 1)
          
  result = result[:-1] + ']'
  with open(COMPARED_FILE, 'w') as f:
    f.write(result)
    
def generate_impact_json(expected, demand):
  impact = 0.0
  count = 0
  exp_values = {}
  dem_values = {}
  for e in expected:
    if TODAY in e['timeStamp']:
          exp_values[e['timeStamp']] = e['prevista']
  for d in demand:
    if TODAY in d['timeStamp']:
      dem_values[d['timeStamp']] = d['demanda']

  for k in dem_values.iterkeys():
    poll =  abs(dem_values[k]-exp_values[k])/float(exp_values[k])
    impact = impact + poll
    count = count + 1
  impact = (impact/float(count))*100

  result = '[{ "h": "14-12-1988 (mie) - PSOE", "d": 34 }, { "h": "27-01-1994 (jue) - PSOE", "d": 27.5 }, { "h": "20-06-2002 (jue) - PP", "d": 20.8 }, { "h": "29-09-2010 (jue) - PSOE", "d": 13.5 }, { "h": "29-03-2012 (jue) - PP", "d": 14.3 }, {"h": "14-11-2012 (mie) - PP", "d": ' + str(impact) + '} ]'

  with open(HARDCODED_STRIKES_FILE, 'w') as f:
    f.write(result)  

if __name__ == '__main__':
  
  yst_expected = get_programed_demand(YESTERDAY)
  yst_demand = get_detailed_demand(YESTERDAY)
  expected = get_programed_demand(TODAY)
  demand = get_detailed_demand(TODAY)
  
  generate_realvsexpec_json(yst_expected, yst_demand, expected, demand)  
  generate_comparison_json(demand)
  generate_impact_json(expected, demand)
  
  
  
   
  
              









