from widgets import SplitBasedOn, SendWaitForReply, MakeHttpRequest, SendMessage 
from texts import texts

payinvoice = 'https://nbkmpn6z0m.execute-api.ap-south-1.amazonaws.com/stage/invoice'
# paysend endpoint is used by html, not by chatbot. 'https://nbkmpn6z0m.execute-api.ap-south-1.amazonaws.com/stage/send'
payping = 'https://nbkmpn6z0m.execute-api.ap-south-1.amazonaws.com/stage/ping'

def Pay(language): 
  HasWallet = '{{widgets.inMessage.parsed.PK}}'
  SignStatus = '{{{{widgets.{}.parsed.data}}}}'.format('createInvoice_' + language)
  TxStatus = '{{{{widgets.{}.parsed.data}}}}'.format('ping_' + language)
  CancelArgument = '{{{{widgets.{}.inbound.Body}}}}'.format('inputAmount_' + language)

  CancelFlowCondition = [
    { 'next': 'return_pin_' + language, 'friendly_name': 'cancel', 'type': 'does_not_match_any_of', 'value': 'exit, cancel, no, stop, back, Exit, Cancel, No, Stop, Back, EXIT, CANCEL, NO, STOP, BACK, N, Ex','argument': CancelArgument }
  ]

  CreateInvoiceID = [
    { 'key' : 'phoneNumber', 'value': '{{contact.channel.address}}'},
    { 'key' : 'amount', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','inputAmount_' + language,'}')},
    { 'key' : 'pk', 'value': '{{widgets.inMessage.parsed.PK}}'},
    { 'key' : 'pin', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','return_pin_' + language,'}')},
  ]

  CreateInvoiceIDRetry = [
    { 'key' : 'phoneNumber', 'value': '{{contact.channel.address}}'},
    { 'key' : 'amount', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','inputAmount_' + language,'}')},
    { 'key' : 'pk', 'value': '{{widgets.inMessage.parsed.PK}}'},
    { 'key' : 'pin', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','InCorrectPin_' + language,'}')},
  ]

  PingForProgress = [
    { 'key' : 'phoneNumber', 'value': '{{contact.channel.address}}'},
    { 'key' : 'invoiceId', 'value': '{{{{widgets.{}.parsed.id}}}}'.format('createInvoice_' + language)},
  ]

  HasWallet = [
    { 'next': 'noPK_' + language, 'friendly_name': 'failure', 'type': 'equal_to', 'value': '0','argument': HasWallet }, # return 0 when no PK is found, noPK_
  ]  

  Sign = [
    { 'next': 'ClickURL_' + language, 'friendly_name': 'success', 'type': 'matches_any_of', 'value': '0','argument': SignStatus }, # SUCCESS, click url to scan upi
    { 'next': 'NotEnoughBalance_' + language, 'friendly_name': 'stop', 'type': 'matches_any_of', 'value': '1','argument': SignStatus }, # FAIL, send message, then stop
    { 'next': 'InCorrectPin_' + language, 'friendly_name': 'pinretry', 'type': 'matches_any_of', 'value': '2','argument': SignStatus }, # FAIL, retry pin
  ]  

  SignRetry = [
    { 'next': 'ClickURL_' + language, 'friendly_name': 'success', 'type': 'matches_any_of', 'value': '0','argument': SignStatus }, # SUCCESS, click url to scan upi
    { 'next': 'NotEnoughBalance_' + language, 'friendly_name': 'stop', 'type': 'matches_any_of', 'value': '1','argument': SignStatus }, # FAIL, send message, then stop
    { 'next': 'InCorrectPin_' + language, 'friendly_name': 'pinretry', 'type': 'matches_any_of', 'value': '2','argument': SignStatus }, # FAIL, retry pin
  ]  

  Ping = [
    { 'next': 'PaySuccess_' + language, 'friendly_name': 'success', 'type': 'matches_any_of', 'value': '0','argument': TxStatus }, 
    { 'next': 'ping_' + language, 'friendly_name': 'nonews', 'type': 'matches_any_of', 'value': '1','argument': TxStatus },  # no news, ping again
    { 'next': 'ClickURL_' + language, 'friendly_name': 'upiretry', 'type': 'matches_any_of', 'value': '2','argument': TxStatus }, # upi failure, ask for upi again
    { 'next': 'PayFailed_' + language, 'friendly_name': 'lost_connect', 'type': 'matches_any_of', 'value': '3','argument': TxStatus }, # lost connection, try again?
  ]

  ## inRequest (so WE starts the conversation)
  A = SendMessage('PayAmount_' + language,'','',texts('EnterAmount_', language)),

  ## inMessage (so user starts the conversation)
  # check if this user has a wallet.
  B = SplitBasedOn('FindPK_' + language,'inputAmount_' + language, HasWallet), 

  # tell it has to go to FPO to request a wallet.
  C = SendMessage('noPK_' + language,'','',texts('noPK_', language)),

  #Okay , Enter the amount you need to pay
  D = SendWaitForReply('inputAmount_' + language,'CancelFlow_' + language,'fourOfour_' + language,'fourOfour_' + language,texts('EnterAmount_', language),3600), #fieldName

  E = SplitBasedOn('CancelFlow_' + language,'help_' + language, CancelFlowCondition), #CancelFlowCondition
 
  # please enter pin
  F = SendWaitForReply('return_pin_' + language,'createInvoice_' + language,'fourOfour_' + language,'fourOfour_' + language,texts('PIN_request_', language),3600),
 
  # create table_item with pin, amount, invoiceID. return invoiceId in url.
  G = MakeHttpRequest('createInvoice_' + language,'Signing_' + language,'fourOfour_' + language,'POST',CreateInvoiceID,payinvoice),

  ### failed request flow ###
  # read response and act, success or failure.
  H = SplitBasedOn('Signing_' + language,'fourOfour_' + language, Sign), 

  # failed httprequest, not enough balance or other error
  I = SendMessage('NotEnoughBalance_' + language,'','',texts('InsufficientBalance_', language)),

  # failed httprequest, the pin is incorrect. we cant find a sk. please retry
  J = SendWaitForReply('InCorrectPin_' + language,'createInvoiceRetry_' + language,'fourOfour_' + language,'fourOfour_' + language,texts('InCorrectPin_', language),3600),

  # create table_item with pin, amount, invoiceID. return invoiceId in url.
  K = MakeHttpRequest('createInvoiceRetry_' + language,'SigningRetry_' + language,'fourOfour_' + language,'POST',CreateInvoiceIDRetry,payinvoice),

  # read response and act on retry, success or failure.
  L = SplitBasedOn('SigningRetry_' + language,'fourOfour_' + language, SignRetry), 
  ### end failed request flow ###

  # return url+invoiceId in text to scan UPI.
  M = SendMessage('ClickURL_' + language,'ping_' + language,'ping_' + language,texts('ClickURL_', language)),

  # ping backend to find out if the transaction was successfull.
  N = MakeHttpRequest('ping_' + language,'Sending_' + language,'Sending_' + language,'POST',PingForProgress,payping),
  
  # read response and act, success or failure.
  O = SplitBasedOn('Sending_' + language,'fourOfour_' + language, Ping), 

  # success
  P = SendMessage('PaySuccess_' + language,'','',texts('HasBeenSend_', language)),

  # failure
  Q = SendMessage('PayFailed_' + language,'','',texts('PayFailed_', language)),

  return *A,*B,*C,*D,*E,*F,*G,*H,*I,*J,*K,*L,*M,*N,*O,*P,*Q
