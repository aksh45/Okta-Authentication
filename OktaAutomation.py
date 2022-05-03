import requests
import getpass
from AuthCodeGenerator import totp
import os

base_url = ""

def primaryAuthentication(username,password):
    authentication_payload = {
    "username": username,
    "password": password,
    "options": {
        "multiOptionalFactorEnroll": "true",
        "warnBeforePasswordExpired": "true"
    }}

    primary_authentication_response = requests.post(f"{base_url}/api/v1/authn",json = authentication_payload )
    return primary_authentication_response.json()
def findAvailable2FactorMethods(json_primary_authentication):
    count = 0
    methods = []
    for factor in json_primary_authentication['_embedded']['factors']:
        count += 1
        methods.append([factor["factorType"],factor["id"]])
        print(f'{count}\nAuthentication Type: {factor["factorType"]}\nProvider: {factor["provider"]}\n')
    return methods
def generateToken(state_token,factor_id,selected_method):
    if(selected_method == 'push'):
        verify_and_poll_push_factor_response = requests.post(f"{base_url}/api/v1/authn/factors/{factor_id}/verify", json = {"stateToken": state_token})
        push_sent = input('Enter 1 after confirming the push notification ')
        verify_and_poll_push_factor_response = requests.post(f"{base_url}/api/v1/authn/factors/{factor_id}/verify", json = {"stateToken": state_token})
        token_obj = verify_and_poll_push_factor_response.json()
    elif(selected_method == 'sms' ):
        send_sms_challenge_res = requests.post(f"{base_url}/api/v1/authn/factors/{factor_id}/verify", json = {"stateToken": state_token})
        sms_inp = input('Enter SMS recieved at your registered mobile number ')
        verify_sms = requests.post(f"{base_url}/api/v1/authn/factors/{factor_id}/verify", json = {"stateToken": state_token,"passCode": sms_inp})
        token_obj = verify_sms.json()
    elif (selected_method == 'token:software:totp' ):
        totp = input("Enter Temporary OTP from your Authenticator ")
        verify_totp_res = requests.post(f"{base_url}/api/v1/authn/factors/{factor_id}/verify", json = {"stateToken": state_token,"passCode": totp })
        token_obj = verify_totp_res.json()
    return token_obj

def generateAutomatedToken(state_token,factor_id,selected_method):
    t_otp = totp(os.getenv('AUTH_KEY_ZS'))
    verify_totp_res = requests.post(f"{base_url}/api/v1/authn/factors/{factor_id}/verify", json = {"stateToken": state_token,"passCode": t_otp })
    token_obj = verify_totp_res.json()
    return token_obj





username = input('Enter Your Username ')
password = getpass.getpass()


json_primary_authentication = primaryAuthentication(username,password)
print("Please Select One Of Your 2 factor Authentication Method")

available_methods = findAvailable2FactorMethods(json_primary_authentication)
selected_method_pos = int(input('Enter Method Number Of your Choice '))
print(available_methods[selected_method_pos - 1])

selected_method = available_methods[selected_method_pos - 1][0]
state_token = json_primary_authentication['stateToken']
factor_id = available_methods[selected_method_pos - 1][1]
session_token = generateToken(state_token,factor_id,selected_method)['sessionToken']
print(session_token)
