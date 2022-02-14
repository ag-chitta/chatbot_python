from widgets import SplitBasedOn, SendWaitForReply, MakeHttpRequest, SendMessage 
from texts import texts

field = 'https://nbkmpn6z0m.execute-api.ap-south-1.amazonaws.com/stage/field'
asyncRequest = 'https://nbkmpn6z0m.execute-api.ap-south-1.amazonaws.com/stage/asyncRequest'
size = 'https://nbkmpn6z0m.execute-api.ap-south-1.amazonaws.com/stage/size'

def registerFields(language):
  argument = '{{{{widgets.{}.inbound.Body}}}}'.format('WalkToField_' + language)
  sizeArgument = '{{{{widgets.{}.inbound.Body}}}}'.format('VerifySize_' + language)
  fetchResultArguments = '{{{{widgets.{}.parsed.data}}}}'.format('fetchResult_' + language)
  detectfield2Arguments = '{{{{widgets.{}.parsed.data}}}}'.format('detectfield2_' + language)
  isRepresentativeArgumentInMessage = '{{widgets.inMessage.parsed.FoF}}'
  isRepresentativeArgumentInRequest = "{{flow.data.FoF}}"
  SelectedRepArgument = '{{{{widgets.{}.inbound.Body}}}}'.format('selectRepresentedFarmer_' + language)
  CancelArgument = '{{{{widgets.{}.inbound.Body}}}}'.format('fieldName_' + language)

  CancelFlowCondition = [
    { 'next': 'isRepresentative_' + language, 'friendly_name': 'cancel', 'type': 'does_not_match_any_of', 'value': 'exit, cancel, no, stop, back, Exit, Cancel, No, Stop, Back, EXIT, CANCEL, NO, STOP, BACK, N, Ex','argument': CancelArgument }
  ]

  CanWalkToFieldConditions = [
    { 'next': 'fieldName_' + language, 'friendly_name': 'start', 'type': 'matches_any_of', 'value': texts('yes_', language),'argument': argument },
    { 'next': 'notAble_' + language, 'friendly_name': 'wait', 'type': 'matches_any_of', 'value': texts('no_', language),'argument': argument },
    { 'next': 'help_' + language, 'friendly_name': 'help', 'type': 'equal_to', 'value': texts('HelpCallout_', language),'argument': argument }
  ]

  FieldParams2Conditions = [
    { 'next': 'VerifySize_' + language, 'friendly_name': 'check', 'type': 'equal_to', 'value': 'check','argument': detectfield2Arguments },
    { 'next': 'nextCorner_' + language, 'friendly_name': 'pending', 'type': 'equal_to', 'value': 'pending','argument': detectfield2Arguments },
    { 'next': 'GPSerror_' + language, 'friendly_name': 'GPSnotUpdated_' + language, 'type': 'equal_to', 'value': 'GPSnotUpdated','argument': detectfield2Arguments },
    { 'next': 'cannotFindField_' + language, 'friendly_name': 'cannotFindField_' + language, 'type': 'equal_to', 'value': 'cannotFindField','argument': detectfield2Arguments },
  ] 

  FetchResultConditions = [
    { 'next': 'VerifySize_' + language, 'friendly_name': 'check', 'type': 'equal_to', 'value': 'check','argument': fetchResultArguments },
    { 'next': 'nextCorner_' + language, 'friendly_name': 'pending', 'type': 'equal_to', 'value': 'pending','argument': fetchResultArguments },
    { 'next': 'GPSerror_' + language, 'friendly_name': 'GPSnotUpdated_' + language, 'type': 'equal_to', 'value': 'GPSnotUpdated','argument': fetchResultArguments },
    { 'next': 'cannotFindField_' + language, 'friendly_name': 'cannotFindField_' + language, 'type': 'equal_to', 'value': 'cannotFindField','argument': fetchResultArguments },
  ] 

  CorrectSizeConditions = [
    { 'next': 'saveVerified_' + language, 'friendly_name': 'complete', 'type': 'matches_any_of', 'value': texts('yes_', language),'argument': sizeArgument },
    { 'next': 'cannotFindField_' + language, 'friendly_name': 'addcorner', 'type': 'matches_any_of', 'value': texts('no_', language),'argument': sizeArgument }
  ] 

  IsRepConditions = [ 
    { 'next': 'selectRepresentedFarmer_' + language, 'friendly_name': 'isFriendOfFarmer', 'type': 'not_equal_to', 'value': '[], null','argument': isRepresentativeArgumentInMessage },
    { 'next': 'selectRepresentedFarmer_' + language, 'friendly_name': 'isFriendOfFarmer', 'type': 'not_equal_to', 'value': '[], null','argument': isRepresentativeArgumentInRequest },
  ]

  SelectedRepConditions = [ 
    { 'next': 'OwnerNotInList_' + language, 'friendly_name': 'ifNotInList', 'type': 'matches_any_of', 'value': texts('notInList_', language),'argument': SelectedRepArgument },
  ]

  DetectFieldParams = [
    { 'key' : 'phoneNumber', 'value': '{{contact.channel.address}}'},
    { 'key' : 'fieldName', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','fieldName_' + language,'}')},
    { 'key' : 'lat', 'value': '{{{}widgets.{}.inbound.Latitude{}}}'.format('{','sendLocation_' + language,'}')},
    { 'key' : 'lng', 'value': '{{{}widgets.{}.inbound.Longitude{}}}'.format('{','sendLocation_' + language,'}')},
    { 'key' : 'activity', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','currentActivity_' + language,'}')},
    { 'key' : 'fieldOwner', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','selectRepresentedFarmer_' + language,'}')},
    { 'key' : 'first', 'value': 'True' },
    ]

  DetectFieldParams2 = [
    { 'key' : 'phoneNumber', 'value': '{{contact.channel.address}}'},
    { 'key' : 'fieldName', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','fieldName_' + language,'}')},
    { 'key' : 'lat', 'value': '{{{}widgets.{}.inbound.Latitude{}}}'.format('{','nextCorner_' + language,'}')},
    { 'key' : 'lng', 'value': '{{{}widgets.{}.inbound.Longitude{}}}'.format('{','nextCorner_' + language,'}')},
    { 'key' : 'activity', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','currentActivity_' + language,'}')},
    { 'key' : 'fieldOwner', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','selectRepresentedFarmer_' + language,'}')},
    { 'key' : 'first', 'value': 'False' },
  ]

  SaveVerifiedParams = [
    { 'key' : 'result', 'value': '{{{}widgets.{}.inbound.Body{}}}'.format('{','VerifySize_' + language,'}')},
    { 'key' : 'id', 'value': '{{{}widgets.{}.parsed.id{}}}'.format('{','fetchResult_' + language,'}')},
    { 'key' : 'size', 'value': '{{{}widgets.{}.parsed.size{}}}'.format('{','fetchResult_' + language,'}')},
    { 'key' : 'id2', 'value': '{{{}widgets.{}.parsed.id{}}}'.format('{','detectfield2_' + language,'}')},
    { 'key' : 'size2', 'value': '{{{}widgets.{}.parsed.size{}}}'.format('{','detectfield2_' + language,'}')},
    { 'key' : 'pk', 'value': '{}{}'.format('{{flow.data.PK}}','{{widgets.inMessage.parsed.PK}}')},

  ]
  AA = SendMessage('InfoRep_' + language,'','',texts('InfoRep_', language)),
  # Great. Chitta is your market assistant. We try to find buyers for your crop, give credit and insurance, and help to improve your income. Type *help* to find out more about Chitta 
  A = SendMessage('Goal_' + language,'WalkToField_' + language,'',texts('Goal_', language)), 
  # To join, go to a field you own that is larger than 25 cents. We will use satellites to track what happens on the field. We sometimes ask you about the crops you grow. *Are you able to walk to your fields now? If so type "Yes" otherwise type "No"
  B = SendWaitForReply('WalkToField_' + language,'waitforReply_' + language,'','',texts('WalkToField_', language),7200), #walkToField
  C = SplitBasedOn('waitforReply_' + language,'fieldName_' + language,CanWalkToFieldConditions), #responds
  #IF NO
  # Ok, no problem. Type *add field* to register your fields another time.
  D = SendMessage('notAble_' + language,'','',texts('notAble_', language)), #notAble 
  #IF YES
  # 'Ok. *Give a name to your field*. It is important to remember the name, so please use a recognizable field feature, such as big tree, left-well. Do not use numbers, as they often confuse. *What is the name of the field? Type your field name here to register*
  E = SendWaitForReply('fieldName_' + language,'CancelFlowRegField_' + language,'fourOfour_' + language,'fourOfour_' + language,texts('fieldName_', language),18000), #fieldName
  F = SplitBasedOn('CancelFlowRegField_' + language,'help_' + language, CancelFlowCondition), #CancelFlowCondition
  # Check for friend of farmer status.
  G = SplitBasedOn('isRepresentative_' + language,'currentActivity_' + language, IsRepConditions),
  # ask to select a farmer from the list, 
  H = SendWaitForReply('selectRepresentedFarmer_' + language,'incaseNotInList_' + language,'currentActivity_' + language,'currentActivity_' + language,texts('selectRepresentedFarmer_', language),3000),
  I = SplitBasedOn('incaseNotInList_' + language,'currentActivity_' + language, SelectedRepConditions),
    # see if there is a representativelist, if so selectFriend it otherwise skip to VerifySize
  J = SendMessage('OwnerNotInList_' + language,'','',texts('OwnerNotInList_', language)),
  
  K = SendWaitForReply('currentActivity_' + language,'sendLocation_' + language,'','',texts('currentActivity_', language),3600), #walkToField
  #  When you arrived to your field, Please *walk to a corner* and *share your current location* on Whatsapp.
  L = SendWaitForReply('sendLocation_' + language,'detectfield_' + language,'','',texts('sendLocation_', language),3600), #walkToField

  M = MakeHttpRequest('detectfield_' + language,'nextCorner_' + language,'fourOfour_' + language,'POST',DetectFieldParams,field), #detectFields
  # ask to register another field side
  N = SendWaitForReply('nextCorner_' + language,'detectfield2_' + language,'','',texts('nextCorner_', language),3600), #nextcorner 
  # analyse 2nd point, split for GPS signal or failed, send to fetch async
  O = MakeHttpRequest('detectfield2_' + language,'HTTPResponds_' + language,'WaitAMoment_' + language,'POST',DetectFieldParams2,field), #detectFields
  P = SendMessage('WaitAMoment_' + language,'fetchResult_' + language,'',texts('WaitAMoment_', language)), #Goal
  Q = MakeHttpRequest('fetchResult_' + language,'HTTPResponds_' + language,'fourOfour_' + language,'POST',DetectFieldParams2,asyncRequest), #asyncRequest
  R = SplitBasedOn('HTTPResponds_' + language,'SecondaryResponds_' + language, FetchResultConditions ), #compare responds to conditions from async and detectFields2 request
  S = SplitBasedOn('SecondaryResponds_' + language,'cannotFindField_' + language, FieldParams2Conditions ), #compare responds to conditions from async and detectFields2 request
  # GPSnotUpdated
  T = SendMessage('GPSerror_' + language,'','',texts('GPSerror_', language)), #GPSerror, stop execution.
  
  # Check if size is correct
  U = SendWaitForReply('VerifySize_' + language,'successSize_' + language,'','',texts('VerifySize_', language),9000), #verifySize
  V = SplitBasedOn('successSize_' + language,'cannotFindField_' + language, CorrectSizeConditions), #successSize 
  W = MakeHttpRequest('saveVerified_' + language,'Completed_' + language,'cannotFindField_' + language,'POST',SaveVerifiedParams,size), #pingToSaveVerified
  X = SendMessage('Completed_' + language,'','',texts('Completed_', language)), #completed
  Y = SendMessage('cannotFindField_' + language,'','',texts('cannotFindField_', language)), #cannotFindField
  # When something has gone wrong
  Z = SendMessage('AnalysisError_' + language,'','',texts('AnalysisError_', language)), #analysisError 

  return *AA,*A,*B,*C,*D,*E,*F,*G,*H,*I,*J,*K,*L,*M,*N,*O,*P,*Q,*R,*S,*T,*U,*V,*W,*X,*Y,*Z
