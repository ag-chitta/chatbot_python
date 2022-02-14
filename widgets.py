def trigger(name,incomingMessage,incomingCall,incomingRequest): 
  widget = { 'name': name, 'type': 'trigger', "properties": {"offset": { "x": 0, "y": 0 }},
    'transitions': [ 
      { 'next': incomingMessage, 'event': "incomingMessage"},
      { 'event': "incomingCall" },
      { 'next': incomingRequest, 'event': "incomingRequest"},
    ]}
  print('Trigger')
  return widget

def SendMessage(name, nextSent, nextFailed, body):
  print(bool(nextFailed))
  if bool(nextSent) : send = {'next': nextSent, 'event': "sent"} 
  else: send = { 'event': "sent"}
  if bool(nextFailed) : failed = {'next': nextFailed, 'event': "failed"} 
  else: failed = { 'event': "failed"}
  widget = { 
    'name': name, 
    'type': 'send-message', 
    'transitions': [ 
        send,
        failed,
        ], 
        'properties': { 
          'service': "{{trigger.message.InstanceSid}}", 
          'channel': "{{trigger.message.ChannelSid}}",
          'from': '{{flow.channel.address}}',
          "offset": { "x": 0, "y": 0 },
          'body': body
    }}
  print('SendMessage', widget)
  return widget

def SendWaitForReply(name,nextIncoming,nextTimeout,nextFailure,body,waitingTime): 
  if bool(nextIncoming) : incoming = {'next': nextIncoming, 'event': "incomingMessage"} 
  else: incoming = { 'event': "incomingMessage"}
  if bool(nextTimeout) : timeout = {'next': nextTimeout, 'event': "timeout"} 
  else: timeout = { 'event': "timeout"}
  if bool(nextFailure) : failed = {'next': nextFailure, 'event': "deliveryFailure"} 
  else: failed = { 'event': "deliveryFailure"}
  widget = { 'name': name, 'type': 'send-and-wait-for-reply', 
        'transitions': [ 
          incoming,
          timeout,
          failed,
        ], 
        'properties': { 
          'service': "{{trigger.message.InstanceSid}}", 
          'channel': "{{trigger.message.ChannelSid}}",
          "offset": { "x": 0, "y": 0 },
          'from': '{{flow.channel.address}}',
          'body': body, #{{flow.data.message}}
          'timeout': waitingTime #"3600"
        }}
  print('SendWaitForReply')
  return widget

def SetVariables(name, nextWidget, variables):
    values = []
    for variable in variables:
        var = {
            'value': var['value'],
            'key': var['key']
        }
        values.append(var)

    widget = {
        'name': name,
        'type' : "split-based-on",
        "transitions": [{ "next": nextWidget, "event": "next"}],
        "properties": { "variables": values ,"offset": { "x": 0, "y": 0 }}
    }

def SplitBasedOn(name,nextNoMatch,conditions):
    Transitions = []
    for condition in conditions:
          cond = { 
              'next': condition['next'], 
              'event': "match", 
              'conditions': [{ 
                  "friendly_name": condition['friendly_name'], 
                  "arguments": [condition['argument']],
                  "type": condition['type'],
                  "value": condition['value']
                }]
          }
          Transitions.append(cond)
    Transitions.append({'next': nextNoMatch, 'event': "noMatch" })  
    print(Transitions)
    widget = {
      'name': name,
      'type' : "split-based-on",
      "properties": {
        "input": conditions[0]['argument'],
        "offset": { "x": 100, "y": 200 }
        },
      'transitions': Transitions
    }
    print('SplitBasedOn')
    return widget

def MakeHttpRequest(name,nextSuccess,nextFailed, method, parameters, url):
  if bool(nextFailed) : failed = {'next': nextFailed, 'event': "sent"} 
  else: failed = { 'event': "failed"}
  print(parameters)
  widget = {
    'name': name,
    'type' : "make-http-request",
    'transitions': [
        { 'next': nextSuccess, 'event': "success"},
        { 'next': nextFailed, 'event': "failed"},
    ],
    'properties': {
        'method': method,
        "properties": {"offset": { "x": 0, "y": 0 }},
        "Content_type": "application/json",
        "parameters": parameters,
        "url": url
        }
    }
  print('MakeHttpRequest')
  return widget
