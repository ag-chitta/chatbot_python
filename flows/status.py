from widgets import SplitBasedOn, SendWaitForReply, MakeHttpRequest, SendMessage 
from texts import texts

status = 'https://nbkmpn6z0m.execute-api.ap-south-1.amazonaws.com/stage/status'

def Status(language):  
  HasWallet = '{{widgets.inMessage.parsed.PK}}'

  StatusParams = [
    { 'key' : 'phoneNumber', 'value': '{{contact.channel.address}}'},
    { 'key' : 'pk', 'value': '{{widgets.inMessage.parsed.PK}}'},
  ]
  HasWallet = [
    { 'next': 'Status_noWallet_' + language, 'friendly_name': 'failure', 'type': 'equal_to', 'value': '0','argument': HasWallet }, # return 0 when no PK is found, noPK_
  ]  

  # check if this user has a wallet.
  A = SplitBasedOn('Status_CheckWallet_' + language,'StatusRequest_' + language, HasWallet), 
  # flow that returns the active applications and wallet balance of the user.
  B = MakeHttpRequest('StatusRequest_' + language,'Status_print_' + language,'fourOfour_' + language,'POST',StatusParams,status),
  C = SendMessage('Status_print_' + language,'','',texts('Status_print_', language)),
  D = SendMessage('Status_noWallet_' + language,'','',texts('noPK_', language)),

  return *A,*B,*C,*D