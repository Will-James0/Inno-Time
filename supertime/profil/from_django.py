from django.shortcuts import render
from .models import Log
from datetime import datetime
from zk import ZK, const

def retrieve_data_from_zkteco(request):
    # Connexion au lecteur ZKTeco
    conn = None
    zk_ip = '192.168.1.100'  # Remplacez par l'adresse IP de votre lecteur ZKTeco
    zk_port = 4370

    try:
        conn = ZK(zk_ip, port=zk_port, timeout=5, password=0, force_udp=False, ommit_ping=False)
        conn.connect()

        # Récupération des enregistrements de présence
        attendance_records = conn.get_attendance()
        
        for record in attendance_records:
            user_id = record.user_id
            check_time = record.timestamp
            punch_type = record.punch

            # Convertir l'heure au format datetime si nécessaire
            heure_check = datetime.fromtimestamp(check_time)

            # Créer une instance du modèle Log avec les données récupérées
            log = Log.objects.create(id_user=user_id, type_punch=punch_type, heure_check=heure_check)
            log.save()

        conn.disconnect()

    except Exception as e:
        print("Erreur lors de la connexion au lecteur ZKTeco :", str(e))

    return render(request, 'data_retrieved.html')
#---------------------------------------------------------------------------------------------------------------------------------#
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Log, Attendance

def process_attendance(request):
    users = User.objects.all()

    for user in users:
        logs = Log.objects.filter(id_user=user.id)
        filtered_attendance = {}

        for log in logs:
            user_id = log.id_user
            check_in = log.heure_check.date()
            check_out = log.heure_check_out.date()
            type_punch = log.type_punch

            if user_id in filtered_attendance and filtered_attendance[user_id] == check_in:
                Attendance.objects.create(id_user=user_id, heure_check_in=check_in, heure_check_out=check_out)
                del filtered_attendance[user_id]
            else:
                filtered_attendance[user_id] = check_in

    return render(request, 'attendance_processed.html')
#---------------------------------------------------------------------------------------------------------------------------------#
from datetime import date
from .models import Log, Attendance

def filter_and_save_attendance(user_id):
    users = User.objects.all()
    for user in users:
        logs = Log.objects.filter(id_user=user.id).order_by('date_d','heure_check')

        attendance_records = {}
        for log in logs:
            check_date = log.heure_check.date()

            if log.type_punch == 'check-in':
                attendance_records[check_date] = {'check_in': log.heure_check, 'check_out': None}
            elif log.type_punch == 'check-out':
                if check_date in attendance_records and attendance_records[check_date]['check_out'] is None:
                    attendance_records[check_date]['check_out'] = log.heure_check

        for date, attendance_data in attendance_records.items():
            if attendance_data['check_in'] and attendance_data['check_out']:
                Attendance.objects.create(id_user=user_id, heure_check_in=attendance_data['check_in'], heure_check_out=attendance_data['check_out'])

    return

#---------------------------------------------------------------------------------------------------------------------------------#
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Log, Attendance

def process_attendance(request):
    users = User.objects.all()

    for user in users:
        logs = Log.objects.filter(id_user=user.id)
        filtered_attendance = {}

        for log in logs:
            user_id = log.id_user
            check_in = log.heure_check_in.date()
            check_out = log.heure_check_out.date()

            if user_id in filtered_attendance and filtered_attendance[user_id] == check_in:
                Attendance.objects.create(id_user=user_id, heure_check_in=check_in, heure_check_out=check_out)
                del filtered_attendance[user_id]
            else:
                filtered_attendance[user_id] = check_in

    return render(request, 'attendance_processed.html')
#---------------------------------------------------------------------------------------------------------------------------------#
from .models import Log, Attendance
from datetime import datetime, date

def filter_and_save_attendance(user_id):
    # Récupération des enregistrements de présence de l'utilisateur
    users = User.objects.all()

    for user in users:
        
        user_logs = Log.objects.filter(id_user=user.id)
        # Filtrage des enregistrements par jour
        attendance_data = {}
        for log in user_logs:
            date_key = log.heure_check.date()

            if date_key not in attendance_data:
                attendance_data[date_key] = {'check_in': None, 'check_out': None}

            if log.type_punch == 'check_in':
                attendance_data[date_key]['check_in'] = log.heure_check
            elif log.type_punch == 'check_out':
                attendance_data[date_key]['check_out'] = log.heure_check

        # Enregistrement des enregistrements de présence filtrés dans la table Attendance
        for date_key, attendance in attendance_data.items():
            if attendance['check_in'] and attendance['check_out']:
                # Vérification si un enregistrement de présence existe déjà pour cette journée
                existing_attendance = Attendance.objects.filter(date=date_key, user_id=user_id).first()

                if not existing_attendance:
                    # Enregistrement de la présence dans la table Attendance
                    attendance_entry = Attendance(date=date_key, user_id=user_id, check_in=attendance['check_in'], check_out=attendance['check_out'])
                    attendance_entry.save()
#------------------------------------------------------------------------------------------------------------------------------#
from .models import Log, Attendance
from datetime import datetime, date

def filter_and_save_attendance(user_id):
    # Récupération des enregistrements de présence de l'utilisateur
    user_logs = Log.objects.filter(id_user=user_id)

    # Filtrage des enregistrements par jour
    attendance_data = {}
    for log in user_logs:
        date_key = log.heure_check.date()

        if date_key not in attendance_data:
            attendance_data[date_key] = {'check_in': None, 'check_out': None}

        if log.type_punch == 'check_in':
            if attendance_data[date_key]['check_in'] is None or log.heure_check < attendance_data[date_key]['check_in']:
                attendance_data[date_key]['check_in'] = log.heure_check
        elif log.type_punch == 'check_out':
            if attendance_data[date_key]['check_out'] is None or log.heure_check > attendance_data[date_key]['check_out']:
                attendance_data[date_key]['check_out'] = log.heure_check

    # Enregistrement des enregistrements de présence filtrés dans la table Attendance
    for date_key, attendance in attendance_data.items():
        if attendance['check_in'] and attendance['check_out']:
            # Vérification si un enregistrement de présence existe déjà pour cette journée
            existing_attendance = Attendance.objects.filter(date=date_key, user_id=user_id).first()

            if not existing_attendance:
                # Enregistrement de la présence dans la table Attendance
                attendance_entry = Attendance(date=date_key, user_id=user_id, check_in=attendance['check_in'], check_out=attendance['check_out'])
                attendance_entry.save()
#--------------------------------------------------------------------------------------------------------------------------#
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Log, Attendance
from datetime import datetime, date
from django.db.models import Min, Max

def filter_and_save_attendance(request):
    # Récupération de tous les utilisateurs
    users = User.objects.all()

    for user in users:
        user_id = user.id
        # Récupération des enregistrements de présence de l'utilisateur
        user_logs = Log.objects.filter(id_user=user_id)

        # Filtrage des enregistrements par jour
        attendance_data = user_logs.values('heure_check__date').annotate(check_in=Min('heure_check'), check_out=Max('heure_check'))

        # Enregistrement des enregistrements de présence filtrés dans la table Attendance
        for attendance in attendance_data:
            date_key = attendance['heure_check__date']
            check_in = attendance['check_in']
            check_out = attendance['check_out']

            # Vérification si un enregistrement de présence existe déjà pour cette journée et cet utilisateur
            existing_attendance = Attendance.objects.filter(date=date_key, user_id=user_id).first()

            if not existing_attendance and check_in and check_out:
                # Enregistrement de la présence dans la table Attendance
                attendance_entry = Attendance(date=date_key, user_id=user_id, check_in=check_in, check_out=check_out)
                attendance_entry.save()

    return render(request, 'attendance_saved.html')