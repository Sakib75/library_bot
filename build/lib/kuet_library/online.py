from firebase import firebase

firebase = firebase.FirebaseApplication("https://kuetlibrary-ca0f8.firebaseio.com/", None)



def get_all_cred():
    result = firebase.get('kuetlibrary-ca0f8/Cred','')
    return result



    