CLIENT_ID = "a65c7274-60fd-48a5-99ef-bc9e504e4c78" #the client's id (i.e. my microsoft group)
AUTHORITY = "https://login.microsoftonline.com/dad6a21d-1de3-4e35-a608-7522149b112b" #the id of an authority
CLIENT_SECRET = "CUD5MyI37NwA-mUFO~21_DGG2jQ2A6_Ipz" #the secret that determines whether the communication of information is 
ENDPOINT = 'https://graph.microsoft.com/v1.0/users' #sends the the users endpoint, so it can send back that information
SCOPE = ["User.ReadBasic.All"] #the information that the app is able to read
SESSION_TYPE = "filesystem"  