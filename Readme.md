# OKTA LOGIN AUTOMATION GUIDE

1. Clone this repo on your machine 
2. Enter the value of base_url in OktaAutomation.py, which is okta url for your organisation for ex https://xyz.okta.com
3. Run the script it will ask you for your username and password , after that it will show you all of your 2 factor auth methods , select the method of your choice
4. A session token will be generated 

Using the session token , you can login to any app present in your okta dashboard. Send a get request at below url to access your okta enabled app .

```{base_url}/sessionCookieRedirect?checkAccountSetupComplete=true&token={session_token}&redirectUrl={okta_enabled_app_url}```

To find the value of okta_enabled_app_url , open your okta dashboard and copy the url of app you want to access. your okta_enabled_app_url will look something like this `base_url/home/appname/xx/xxxxx`