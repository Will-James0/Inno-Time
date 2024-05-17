
def filter_and_save_attendance(request):
    users = Personnel.objects.all()

    for user in users:
        # Récupération des enregistrements de présence de l'utilisateur
        user_logs =Attendance.objects.filter(personnel_a=user.id)

        # Filtrage des enregistrements par jour
        attendance_data = {}
        for log in user_logs:
            date_key = log.heure_punch.date()

            if date_key not in attendance_data:
                attendance_data[date_key] = {'check_in': None, 'check_out': None}

            if log.type_punch == 'check_in':
                if attendance_data[date_key]['check_in'] is None or log.heure_punch < attendance_data[date_key]['check_in']:
                    attendance_data[date_key]['check_in'] = log.heure_punch
            elif log.type_punch == 'check_out':
                if attendance_data[date_key]['check_out'] is None or log.heure_punch > attendance_data[date_key]['check_out']:
                    attendance_data[date_key]['check_out'] = log.heure_punch

        # Enregistrement des enregistrements de présence filtrés dans la table Attendance
        for date_key, attendance in attendance_data.items():
            if attendance['check_in'] and attendance['check_out']:
                # Vérification si un enregistrement de présence existe déjà pour cette journée
                existing_attendance = Horaire.objects.filter(date_d=date_key, personnel=user.id).first()

                if not existing_attendance:
                    # Enregistrement de la présence dans la table Attendance
                    attendance_entry = Horaire(date_d=date_key, personnel=user.id, arrival_time=attendance['check_in'], departure_time=attendance['check_out'])
                    attendance_entry.save()
    return render(request, 'attendance_saved.html')


