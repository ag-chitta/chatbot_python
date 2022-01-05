# pychatbot

The official chitta chatbot python SDK

pyChatbot is a flow builder with a set of APIs, such as a custodial wallet service. It uses a Twilio service to let users interact via Whatsapp with Chitta labels and the Chitta network on Algorand.

- why a Whatsapp chatbot?

pychatbot was born out of the need of a low-entry level communication platform for users that have limited understanding of digital assets and are unlikely to use mobile or desktop extension wallets for the time being. 

## use

The scope of use for this SDK is to build your own flows and push them to your own cloud environment. This SDK offers the templates to get your up and running quickly. 

It does not let you use the chitta business chatbot, or any of its current users. However you can use the APIs to connect your users to Chitta predictions** (by registrating fields) and use the Chitta wallet. Other services might be offered through the chatbot in a future stage. 

 ** This lets you connect your users to the agri data pipelines, such as yield prediction, plant health signalling and other services.  

If you wish to share resources, send us a message on info@chitta.org.

## requirements

Before using the YAML cloud template and create Twilio flows, Make sure you meet the requirements set by Twilio and Meta. 

* get a Twilio account and purchase a phone number
* create a Whatsapp business profile linked to the twilio phonenumber
* approve each outgoing initiating message with Meta.

## Get started

pychatbot is a custom implementation of the Twilio studio flow. Because of the limited complexity of a Twilio studio GUI, we needed to build a workable solution to handle multilanguage and complex flows.

Clone  ```pychatbot```

Add  ```Twilio account sid``` and ```Twilio auth credentials``` to the serverless.yml file. 

Run ```$ python handler.py``` to validate and update/create the flow in Twilio.

Add any additional APIs and lambdas to the serverless.yml file. 

## Quick start
Here's a simple example of a flow to verify if the farmer has started a new cultivation

```python
def SOS(language):
  # Question asked: Hi {{1}} are you preparing a new cultivation?
  RequestMessageArg = '{{{{widgets.{}.inbound.Body}}}}'.format('sendRequestMessage_' + language)
  
  SendRequestResponds = [
   { 'next': 'SOSYes_' + language, 'friendly_name': 'SOSYes_' + language, 'type':  'matches_any_of', 'value': texts('yes_', language), 'argument': RequestMessageArg},
   { 'next': 'SOSHTTP_' + language, 'friendly_name': 'SOSNo_' + language, 'type':  'matches_any_of', 'value': texts('no_', language), 'argument': RequestMessageArg}]
   
  SOSHTTPParams = [
    { 'key' : 'croptype', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','SOSYes_' + language,'}')},
    { 'key' : 'variety', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','SeedType_' + language,'}')},
    { 'key' : 'fields_checked', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','CheckFields_' + language,'}')},
    { 'key' : 'fields', 'value': "{{flow.data.fields}}"},
    { 'key' : 'analysisDate', 'value': "{{flow.data.analysisDate}}"},
    { 'key' : 'type', 'value': 'SOS'},
    { 'key' : 'phonenumber', 'value': '{{contact.channel.address}}'},
  ]
  
  A = SplitBasedOn('SOSCheck_' + language,'fourOfour_' + language,SendRequestResponds),
  # follow-up question on YES
  B = SendWaitForReply('SOSYes_' + language,'SeedType_' + language,'','fourOfour_' + language,texts('SOSYes_', language),300),
  C = SendWaitForReply('SeedType_' + language,'CheckFields_' + language,'','fourOfour_' + language,texts('SeedType_', language),300),
  D = SendWaitForReply('CheckFields_' + language,'SOSHTTP_' + language,'','fourOfour_' + language,texts('CheckFields_', language),300),
  E = SendMessage('SOSNo_' + language,'','',texts('SOSNo_', language)),
  F = MakeHttpRequest('SOSHTTP_' + language,'SOSNo_' + language,'fourOfour_' + language,'POST',SOSHTTPParams,receive),
  
  return *A,*B,*C,*D,*E,*F

```

## License
pychatbot is licensed under a MIT license. See the LICENSE file for details.
