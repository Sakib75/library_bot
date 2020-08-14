from firebase import firebase

firebase = firebase.FirebaseApplication("YOUR DATABASE", None)



def get_all_cred():
    result = firebase.get('YOUR DATABASE','')
    return result



    
