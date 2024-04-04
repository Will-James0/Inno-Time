# h_a = "8:45"
# h_m = h_a.split(':')
# h=int(h_m[0])
# m=int(h_m[1])
# print(f"{h} {m}")

# import pyzk
# from django.contrib import messages

# def connect_zkteco(request):
#     zk = pyzk.ZK('192.168.1.100', port=4370)  # Remplacez l'adresse IP et le port par ceux de votre appareil ZKTeco
#     try:
#         conn = zk.connect()
#         messages.success(request, 'Connexion réussie à l\'appareil ZKTeco')
        
#         # Effectuez ici les opérations souhaitées avec l'appareil ZKTeco
        
#     except pyzk.ZKErrorResponse as e:
#         messages.error(request, f'Erreur de connexion à l\'appareil ZKTeco: {e}')
    
#     conn.disconnect()

from zk import ZK, const

conn = None
# create ZK instance
zk = ZK('192.168.1.201', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
try:
    # connect to device
    conn = zk.connect()
    # disable device, this method ensures no activity on the device while the process is run
    conn.disable_device()
    # another commands will be here!
    # Example: Get All Users
    users = conn.get_users()
    for user in users:
        privilege = 'User'
        if user.privilege == const.USER_ADMIN:
            privilege = 'Admin'
        print ('+ UID #{}'.format(user.uid))
        print ('  Name       : {}'.format(user.name))
        print ('  Privilege  : {}'.format(privilege))
        print ('  Password   : {}'.format(user.password))
        print ('  Group ID   : {}'.format(user.group_id))
        print ('  User  ID   : {}'.format(user.user_id))

    # Test Voice: Say Thank You
    conn.test_voice()
    # re-enable device after all commands already executed
    conn.enable_device()
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()
