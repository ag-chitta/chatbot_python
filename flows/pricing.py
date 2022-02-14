from widgets import MakeHttpRequest, SendMessage 
from texts import texts

mandi = 'https://k14y5popkj.execute-api.ap-south-1.amazonaws.com/stage/commodities'

def Pricing(language):  
  #LOCATION = '{{widgets.inMessage.parsed.location}}'
  #result = '{{{{widgets.{}.parsed.data.value}}}}'.format('RequestPricing_' + language)

  APMCParams = [
    { 'key' : 'place', 'value': '{{widgets.inMessage.parsed.location}}'},
    { 'key' : 'radius', 'value': '60'},
    { 'key' : 'language', 'value': '{{widgets.inMessage.parsed.language}}'},
    { 'key' : 'type', 'value': 'current'},
    { 'key' : 'commodities', 'value': '-'},
    # use output = string to return apmc:modalprice:date as string
    { 'key' : 'output', 'value': 'String'},
  ]

    # request current prices for all apmcs and all commodities in a 20km radius  returns a string
  A = MakeHttpRequest('RequestPricing_' + language,'PricingResult_' + language,'fourOfour_' + language,'GET',APMCParams,mandi),
  # show string results and end conversation
  B = SendMessage('PricingResult_' + language,'','',texts('APMCprices_', language)),

  return *A,*B