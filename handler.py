import json
from widgets import trigger, SplitBasedOn, SendWaitForReply, MakeHttpRequest, SendMessage, SetVariables 
from flows.pay import Pay
from flows.credit import Credit
from flows.registerfield import registerFields
from flows.status import Status
from flows.pricing import Pricing
from texts import texts
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)
member = 'https://nbkmpn6z0m.execute-api.ap-south-1.amazonaws.com/stage/member'
receive = 'https://fzfeh4kgbc.execute-api.ap-south-1.amazonaws.com/dev/receive'  # used in SOS,EOS but not created..

def SOS(language):
  # Question asked: Hi {{1}} are you preparing a new cultivation?
  RequestMessageArg = '{{{{widgets.{}.inbound.Body}}}}'.format('sendRequestMessage_' + language)
  sendRequestResponds = [
      { 'next': 'SOSYes_' + language, 'friendly_name': 'SOSYes_' + language, 'type':  'matches_any_of', 'value': texts('yes_', language), 'argument': RequestMessageArg},
      { 'next': 'SOSHTTP_' + language, 'friendly_name': 'SOSNo_' + language, 'type':  'matches_any_of', 'value': texts('no_', language), 'argument': RequestMessageArg}
  ]
  SOSHTTPParams = [
    { 'key' : 'croptype', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','SOSYes_' + language,'}')},
    { 'key' : 'variety', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','SeedType_' + language,'}')},
    { 'key' : 'fields_checked', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','CheckFields_' + language,'}')},
    { 'key' : 'fields', 'value': "{{flow.data.fields}}"},
    { 'key' : 'analysisDate', 'value': "{{flow.data.analysisDate}}"},
    { 'key' : 'type', 'value': 'SOS'},
    { 'key' : 'phonenumber', 'value': '{{contact.channel.address}}'},
  ]
  A = SplitBasedOn('SOSCheck_' + language,'fourOfour_' + language,sendRequestResponds),
  # follow-up question on YES
  B = SendWaitForReply('SOSYes_' + language,'SeedType_' + language,'','fourOfour_' + language,texts('SOSYes_', language),300),
  C = SendWaitForReply('SeedType_' + language,'CheckFields_' + language,'','fourOfour_' + language,texts('SeedType_', language),300),
  D = SendWaitForReply('CheckFields_' + language,'SOSHTTP_' + language,'','fourOfour_' + language,texts('CheckFields_', language),300),
  E = SendMessage('SOSNo_' + language,'','',texts('SOSNo_', language)),
  F = MakeHttpRequest('SOSHTTP_' + language,'SOSNo_' + language,'fourOfour_' + language,'POST',SOSHTTPParams,receive),
  return *A,*B,*C,*D,*E,*F

def Cultivation(language):
  # Question asked: Hi {farmername}, are you growing {paddy}?  
  RequestMessageArg = '{{{{widgets.{}.inbound.Body}}}}'.format('sendRequestMessage_' + language)
  sendRequestResponds = [
      { 'next': 'cultYes_' + language, 'friendly_name': 'cultYes_' + language, 'type':  'matches_any_of', 'value': texts('yes_', language), 'argument': RequestMessageArg},
      { 'next': 'cultNo_' + language, 'friendly_name': 'cultNo_' + language, 'type':  'matches_any_of', 'value': texts('no_', language), 'argument': RequestMessageArg}
  ]
  cultHTTPParams = [
    { 'key' : 'response', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','cultNo_' + language,'}')},
    { 'key' : 'type', 'value': 'Cultivation'},
  ]
  A = SplitBasedOn('CultivationCheck_' + language,'fourOfour_' + language,sendRequestResponds),
  # follow-up question on NO
  B = SendMessage('cultYes_' + language,'','',texts('cultYes_', language)),
  C = SendWaitForReply('cultNo_' + language,'cultHTTP_' + language,'','fourOfour_' + language,texts('cultNo_', language),300),
  D = MakeHttpRequest('cultHTTP_' + language,'cultYes_' + language,'fourOfour_' + language,'POST',cultHTTPParams,receive),
  return *A,*B,*C,*D

def EOS(language):  
  #Hi {{1}}, harvest is coming soon. Do you expect to harvest within 2 weeks?
  RequestMessageArg = '{{{{widgets.{}.inbound.Body}}}}'.format('sendRequestMessage_' + language)
  sendRequestResponds = [
      { 'next': 'EOSYes_' + language, 'friendly_name': 'EOSYes_' + language, 'type':  'matches_any_of', 'value': texts('yes_', language), 'argument': RequestMessageArg},
      { 'next': 'EOSNo_' + language, 'friendly_name': 'EOSNo_' + language, 'type':  'matches_any_of', 'value': texts('no_', language), 'argument': RequestMessageArg}
  ]
  EOSHTTPParams = [
    { 'key' : 'response', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','EOSNo_' + language,'}')},
    { 'key' : 'type', 'value': 'EOS'},
  ]
  A = SplitBasedOn('EOSCheck_' + language,'fourOfour_' + language,sendRequestResponds),
  # follow-up question on NO
  B = SendWaitForReply('EOSNo_' + language,'EOSHTTP_' + language,'','fourOfour_' + language,texts('EOSNo_', language),300),
  C = SendMessage('EOSYes_' + language,'','',texts('EOSYes_', language)),
  D = MakeHttpRequest('EOSHTTP_' + language,'EOSYes_' + language,'fourOfour_' + language,'POST',EOSHTTPParams,receive),
  return *A,*B,*C,*D

def selectLanguage(language):
    startArgument = '{{widgets.{}.message}}'.format('sendRequestMessage_' + language) 
    action_conditions = [
      { 'next': 'InfoRep_' + language, 'friendly_name': 'RegisterfieldsRep_' + language, 'type': 'equal_to', 'value': 'RegisterFieldsRep', 'argument': '{{flow.data.type}}'},
      { 'next': 'Goal_' + language, 'friendly_name': 'Registerfields_' + language, 'type': 'equal_to', 'value': 'RegisterFields', 'argument': '{{flow.data.type}}'},
      { 'next': 'PayAmount_' + language, 'friendly_name': 'Pay_' + language, 'type': 'equal_to', 'value': 'Pay', 'argument': '{{flow.data.type}}'},
      { 'next': 'Status_CheckWallet_' + language, 'friendly_name': 'Status_' + language, 'type': 'equal_to', 'value': 'Status', 'argument': '{{flow.data.type}}'},
      { 'next': 'SOSCheck_' + language, 'friendly_name': 'SOS_' + language, 'type': 'equal_to', 'value': 'SOS', 'argument': '{{flow.data.type}}'},
      { 'next': 'CultivationCheck_' + language, 'friendly_name': 'Cultivation_' + language, 'type': 'equal_to', 'value': 'Cultivation', 'argument': '{{flow.data.type}}'},
      { 'next': 'EOSCheck_' + language, 'friendly_name': 'EOS_' + language, 'type': 'equal_to', 'value': 'EOS', 'argument': '{{flow.data.type}}'},
    ]
    one = SendWaitForReply('sendRequestMessage_' + language,'waitforMessageReply_' + language,'fourOfour_' + language,'fourOfour_' + language,'{{flow.data.message}}',72000) #sendRequestMessage 
    two = SplitBasedOn('waitforMessageReply_' + language,'fourOfour_' + language,action_conditions) #waitforReply
    three = SendMessage('fourOfour_' + language,'','',texts('fourOfour_', language))
    four = registerFields(language)
    five = SOS(language)
    six = Cultivation(language)
    seven = EOS(language)
    eight = Status(language)
    nine = Pay(language)
    ten = Credit(language)
    eleven = Pricing(language)

    return one,two,three,*four,*five,*six,*seven,*eight,*nine,*ten,*eleven

def menu(language):
    TriggerMessageArgument = '{{trigger.message.Body}}' 
    TriggerMessageCons = [
      { 'next': 'fieldName_' + language, 'friendly_name': 'Add field', 'type': 'matches_any_of', 'value': texts('addField_', language),'argument' : TriggerMessageArgument },
      { 'next': 'Status_CheckWallet_' + language, 'friendly_name': 'Status', 'type': 'matches_any_of', 'value': "Status, status, satus, statu, 2",'argument': TriggerMessageArgument },
      { 'next': 'FindPK_' + language, 'friendly_name': 'Pay', 'type': 'matches_any_of', 'value': texts('pay_', language),'argument': TriggerMessageArgument },
      { 'next': 'Credit_CheckWallet_' + language, 'friendly_name': 'Credit', 'type': 'matches_any_of', 'value': "Loan, Credit, Borrow, 4",'argument': TriggerMessageArgument },  
      { 'next': 'RequestPricing_' + language, 'friendly_name': 'Pricing', 'type': 'matches_any_of', 'value': "Price, mandi, Mandi, CropPricing, 5",'argument': TriggerMessageArgument },
      { 'next': 'grade_' + language, 'friendly_name': 'Grade', 'type': 'matches_any_of', 'value': "Grade, grade, 6",'argument': TriggerMessageArgument },
      { 'next': 'sell_' + language, 'friendly_name': 'Sell', 'type': 'matches_any_of', 'value': "Sell, future, sell, 6",'argument': TriggerMessageArgument },
      { 'next': 'weather_' + language, 'friendly_name': 'Weather', 'type': 'matches_any_of', 'value': "Weather, weather, 7",'argument': TriggerMessageArgument },
      { 'next': 'advice_' + language, 'friendly_name': 'Advice', 'type': 'matches_any_of', 'value': "Crop Advice, advice, crop help, crop advice, 8",'argument': TriggerMessageArgument }
    ] 
    A = SplitBasedOn('Request_' + language,'help_' + language, TriggerMessageCons), #request
    B = SendMessage('help_' + language,'','',texts('Menu_', language)),    
    C = SendMessage('grade_' + language,'','',texts('Grade_', language)),   
    D = SendMessage('sell_' + language,'','',texts('Sell_', language)),   
    E = SendMessage('weather_' + language,'','',texts('Weather_', language)), 
    F = SendMessage('advice_' + language,'','',texts('Advice_', language)),
    # chat   
    return *A,*B,*C,*D,*E,*F

def main():
    language_Request = [
        { 'next': 'sendRequestMessage_EN', 'friendly_name': 'English', 'type': 'does_not_match_any_of', 'value': '(Tamil), (Hindi), (Kannadam), (Telugu)', 'argument': "{{flow.data.language}}"}, #sendRequestMessage_EN
        { 'next': 'sendRequestMessage_TN', 'friendly_name': 'Tamil', 'type': 'equal_to', 'value': '(Tamil)', 'argument': "{{flow.data.language}}"}, #sendRequestMessage_TM
        { 'next': 'sendRequestMessage_HI', 'friendly_name': 'Hindi', 'type': 'equal_to', 'value': '(Hindi)', 'argument': "{{flow.data.language}}"}, #sendRequestMessage_HI
        { 'next': 'sendRequestMessage_KN', 'friendly_name': 'Kannada', 'type': 'equal_to', 'value': '(Kannadam)', 'argument': "{{flow.data.language}}"}, #sendRequestMessage_KN
        { 'next': 'sendRequestMessage_TG', 'friendly_name': 'Telugu', 'type': 'equal_to', 'value':'(Telugu)', 'argument': "{{flow.data.language}}"}, #sendRequestMessage_TG
    ]
    language_Incoming = [
        { 'next': 'Request_EN', 'friendly_name': 'English', 'type': 'does_not_match_any_of', 'value': '(Tamil), (Hindi), (Kannadam), (Telugu)', 'argument': '{{widgets.inMessage.parsed.language}}'},
        { 'next': 'Request_TN', 'friendly_name': 'Tamil', 'type': 'equal_to', 'value': '(Tamil)', 'argument': '{{{{widgets.inMessage.parsed.language}}}}'},
        { 'next': 'Request_HI', 'friendly_name': 'Hindi', 'type': 'equal_to', 'value': '(Hindi)', 'argument': '{{{{widgets.inMessage.parsed.language}}}}'},
        { 'next': 'Request_KN', 'friendly_name': 'Kannada', 'type': 'equal_to', 'value': '(Kannadam)', 'argument': '{{{{widgets.inMessage.parsed.language}}}}'},
        { 'next': 'Request_TG', 'friendly_name': 'Telugu', 'type': 'equal_to', 'value': '(Telugu)', 'argument': '{{{{widgets.inMessage.parsed.language}}}}'}
    ]      
    inMessageParams = [{ 'key' : "phoneNumber", 'value': '{{contact.channel.address}}'}]    
    try: 
        flow = { "states": [ 
                  trigger('Trigger','inMessage','','inRequest'), # trigger               
                  SplitBasedOn('inRequest','fourOfour_EN',language_Request), #select language
                  *selectLanguage('EN'),
                  *selectLanguage('TN'),
                  *selectLanguage('HI'),
                  *selectLanguage('KN'),
                  *selectLanguage('TG'),            
                  MakeHttpRequest('inMessage','incomingLanguage','noUser','POST',inMessageParams,member), #getUserParams
                  SendMessage('noUser','','','Ues, did you already register at Chitta? If not, please go to https://chitta.network, create a wallet and register yourself as a farmer. Otherwise, please try again later.'),
                  SplitBasedOn('incomingLanguage','noUser',language_Incoming), #select language
                  *menu('EN'),
                  *menu('TN'),
                  *menu('HI'),
                  *menu('KN'),
                  *menu('TG')
                  ]
                }        
        # add parameters to JSON object  
        flow['description'] = "ChittaBot"
        flow['initial_state'] = "Trigger"
        flow['flags'] = { "allow_concurrent_calls": True }     
        with open('flow.json', 'w') as f:
            json.dump(flow, f, ensure_ascii=False, indent=4)
        f.close()
        #with open('flow.json') as r:
        #    data = json.load(r)
        jsonDump = json.dumps(flow)
        #print('final json object:', jsonDump)
        flow_validate = client.studio.flow_validate.update(
                               commit_message='ADD RELEASE STAGE HERE', 
                               definition=jsonDump, 
                               friendly_name='',
                               status='published')    
        print(flow_validate.valid) 
        flow = client.studio.flows('ADD YOUR FLOW ID HERE').update(
                            commit_message='ADD RELEASE STAGE HERE',  
                            definition=jsonDump, 
                            status='published')
        print(flow.friendly_name)

    except TwilioRestException as e: 
        print(e.details)
        print('------------------------')
        return "Error"
    
if __name__ == "__main__":
   main()
