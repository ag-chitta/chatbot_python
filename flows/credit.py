from widgets import SplitBasedOn, SendWaitForReply, MakeHttpRequest, SendMessage 
from texts import texts

credit = 'https://nbkmpn6z0m.execute-api.ap-south-1.amazonaws.com/stage/credit'

def Credit(language):  
  PK = '{{widgets.inMessage.parsed.PK}}'
  res = '{{{{widgets.{}.parsed.data.value}}}}'.format('CreditRequest_' + language)

  CreditParams = [
    { 'key' : 'phoneNumber', 'value': '{{contact.channel.address}}'},
    { 'key' : 'pk', 'value': '{{widgets.inMessage.parsed.PK}}'},
  ]

  HasWallet = [{ 'next': 'Status_noWallet_' + language, 'friendly_name': 'failure', 'type': 'equal_to', 'value': '0','argument': PK }] # return 0 when no PK is found, noPK_  
  Result = [
      { 'next': 'Credit_unavailable_ns_' + language, 'friendly_name': 'no credit score', 'type': 'equal_to', 'value': '0','argument': res },
      { 'next': 'Credit_unavailable_np_' + language, 'friendly_name': 'no profile match', 'type': 'equal_to', 'value': '1','argument': res },
      { 'next': 'Credit_payBack_' + language, 'friendly_name': 'open credit detected', 'type': 'equal_to', 'value': '2','argument': res },
      { 'next': 'Credit_available_' + language, 'friendly_name': 'available for credit line', 'type': 'equal_to', 'value': '3','argument': res },
      ]  

  # check if this user has a wallet.
  A = SplitBasedOn('Credit_CheckWallet_' + language,'CreditRequest_' + language, HasWallet), 
  # request the credit status of this farmer, his active activity, and the credit profile of the FPO
  B = MakeHttpRequest('CreditRequest_' + language,'CreditResult_' + language,'fourOfour_' + language,'POST',CreditParams,credit),
  # get the result and decide what to do next. 
  C = SplitBasedOn('CreditResult_' + language,'fourOfour_' + language, Result), 
  # not available at this moment, noscore,
  D = SendMessage('Credit_unavailable_ns_' + language,'','',texts('Credit_unavailable_ns_', language)),
  # not available at this moment, no profile match,
  E = SendMessage('Credit_unavailable_np_' + language,'','',texts('Credit_unavailable_np_', language)),
  # open credit line, first pay off
  F = SendMessage('Credit_payBack_' + language,'','',texts('Credit_payBack_', language)),
  # available for credit, please go to your office manager 
  G = SendMessage('Credit_available_' + language,'','',texts('Credit_available_', language)),

  return *A,*B,*C,*D,*E,*F,*G