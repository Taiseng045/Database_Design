from flask import Blueprint,abort, render_template,request,flash,jsonify,redirect,url_for,session
from flask_login import login_required,current_user
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required,logout_user,current_user
import os
import json
from flask import current_app as app
from flask import Flask, render_template
import plotly.express as px
from . import get_db;
from datetime import timedelta;
views = Blueprint('views', __name__)
# define when it a / it is routed to home
@views.route('/',endpoint="dashboard")
@login_required
def dashboard():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cases;")
    TotalCase = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM cases WHERE status = 'Under Investigation'")
    active_cases = cursor.fetchone()[0]
    # Near Deadline (arrest_date within next 7 days)
    cursor.execute("""
            SELECT COUNT(*) FROM cases 
            WHERE arrest_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
        """)
    near_deadline = cursor.fetchone()[0]

        # Closed Cases
    cursor.execute("SELECT COUNT(*) FROM cases WHERE status IN ('Guilty', 'Innocent')")
    closed_cases = cursor.fetchone()[0]

    # Recent cases table
    cursor.execute("""
            SELECT case_number, category AS case_type, arrest_date AS date
            FROM cases ORDER BY arrest_date DESC LIMIT 5
        """)
    recent_cases_table = cursor.fetchall()

        # Near deadline cases
    cursor.execute("""
            SELECT case_number, category AS case_type, arrest_date AS date
            FROM cases
            WHERE arrest_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 14 DAY)
            ORDER BY arrest_date ASC LIMIT 5
        """)
    near_deadline_cases_table = cursor.fetchall()

        # Closed cases
    cursor.execute("""
            SELECT case_number, category AS case_type, arrest_date AS date,status
            FROM cases
            WHERE status IN ('Guilty', 'Innocent')
            ORDER BY arrest_date DESC LIMIT 5
        """)
    closed_cases_table = cursor.fetchall()

    conn.close()
    # pie chart
    labels = ['Apples', 'Bananas', 'Cherries', 'Dates']
    values = [30, 15, 45, 10]
    fig = px.pie(names=labels, values=values, hole=0)
    fig.update_traces(textinfo='label+percent', hoverinfo='label+value+percent')
    fig.update_layout(plot_bgcolor='#D6F4F7',paper_bgcolor='#D6F4F7' )
    plot_html = fig.to_html(full_html=False)

    # bar chart
    bar_fig = px.bar(x=labels, y=values)
    bar_fig.update_layout(
        plot_bgcolor='#D6F4F7',  # Background color for the plot area
        paper_bgcolor='#D6F4F7'  # Background color for the entire chart
    )
    bar_plot_html = bar_fig.to_html(full_html=False)

    return render_template('dashboard.html',user= current_user,plot=plot_html, bar_plot=bar_plot_html,TotalCase=TotalCase,active_cases=active_cases,near_deadline=near_deadline,closed_cases=closed_cases,recent_cases_table=recent_cases_table,near_deadline_cases_table=near_deadline_cases_table,closed_cases_table=closed_cases_table)
@views.route('/admin/user',endpoint="user")
@login_required
def user():
    if not current_user.role =='Admin':
        abort(404)  # Check if user is an admin
        flash("You do not have permission to access this page.", "warning")
        return redirect(url_for('views.dashboard'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('user.html',user= current_user,users=users)
@views.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.role =='Admin':
        abort(404)  # Check if user is an admin
        flash("You do not have permission to access this page.", "warning")
        return redirect(url_for('views.dashboard'))
    if request.method == 'POST':
        # try:
            # -------------Personal information------------
            name = request.form['name']
            gender = request.form['gender']
            dob = request.form['dob']
            nationality = request.form['nationality']
            idNumber = request.form['idNumber']
            occupation = request.form['occupation']
            MaritalStatus = request.form['MaritalStatus']
            workplace = request.form['workplace']
            email = request.form['email']
            # -------------Birth Address------------
            bCity = request.form['bCity']
            bDistrict = request.form['bDistrict']
            bCommune = request.form['bCommune']
            bVillage = request.form['bVillage']
            bStreetAdd = request.form['bStreetAdd']
            bCountry = request.form['bCountry']
            bPostal = request.form['bPostal']
            # -------------Current Address------------
            cCity = request.form['cCity']
            cDistrict = request.form['cDistrict']
            cCommune = request.form['cCommune']
            cVillage = request.form['cVillage']
            cStreetAdd = request.form['cStreetAdd']
            cCountry = request.form['cCountry']
            cPostal = request.form['cPostal']
            # -------------Case Detail------------
            caseNumber = request.form['caseNumber']
            caseType = request.form['caseType']
            caseStatus = request.form['caseStatus']
            caseArrestDate = request.form['caseArrestDate']
            caseArrestTime = request.form['caseArrestTime']
            caseArrestingOfficer = request.form['caseArrestingOfficer']
            caseDescription = request.form['caseDescription']
            # -------------Current Address------------
            CLcity = request.form['CLcity']
            CLdistrict = request.form['CLdistrict']
            CLcommune = request.form['CLcommune']
            CLvillage = request.form['CLvillage']
            CLstreetAdd = request.form['CLstreetAdd']
            CLcountry = request.form['CLcountry']
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cases WHERE case_number = %s", (caseNumber,))
            existing_case = cursor.fetchone()
            # Raw SQL insert
            if existing_case:
                case_id = existing_case[0]
                cursor.execute("""
                    INSERT INTO addresses (city, district, commune, village, street_address, country, postal_code)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (bCity, bDistrict, bCommune, bVillage, bStreetAdd, bCountry, bPostal))
                birth_place_id = cursor.lastrowid
                # --------- Insert into addresses ---------
                cursor.execute("""
                    INSERT INTO addresses (city, district, commune, village, street_address, country, postal_code)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (cCity, cDistrict, cCommune, cVillage, cStreetAdd, cCountry, cPostal))
                current_location_id = cursor.lastrowid
                # --------- Insert into charged_persons ---------
                cursor.execute("""
                INSERT INTO charged_persons (
                    card_number, name, gender, dob,nationality,occupation,MaritalStatus,workplace, contact_info, birth_place,current_location, created_by, modified_by
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    idNumber, name, gender, dob,nationality,occupation,MaritalStatus,workplace, email, birth_place_id,current_location_id, current_user.id, current_user.id
                ))
                charged_person_id = cursor.lastrowid
                # Insert into case_charged_persons to link charged person to the existing case
                cursor.execute("""
                    INSERT INTO case_charged_persons (case_number, charged_person_id)
                    VALUES (%s, %s)
                """, (caseNumber, charged_person_id))
            else:

                # --------- Insert into addresses ---------
                cursor.execute("""
                    INSERT INTO addresses (city, district, commune, village, street_address, country, postal_code)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (bCity, bDistrict, bCommune, bVillage, bStreetAdd, bCountry, bPostal))
                birth_place_id = cursor.lastrowid
                # --------- Insert into addresses ---------
                cursor.execute("""
                    INSERT INTO addresses (city, district, commune, village, street_address, country, postal_code)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (cCity, cDistrict, cCommune, cVillage, cStreetAdd, cCountry, cPostal))
                current_location_id = cursor.lastrowid
                # --------- Insert into charged_persons ---------
                cursor.execute("""
                INSERT INTO charged_persons (
                    card_number, name, gender, dob,nationality,occupation,MaritalStatus,workplace, contact_info, birth_place,current_location, created_by, modified_by
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    idNumber, name, gender, dob,nationality,occupation,MaritalStatus,workplace, email, birth_place_id,current_location_id, current_user.id, current_user.id
                ))
                charged_person_id = cursor.lastrowid
                # --------- Insert into addresses ---------
                cursor.execute("""
                    INSERT INTO addresses ( city, district, commune, village, street_address, country)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, ( CLcity, CLdistrict, CLcommune, CLvillage, CLstreetAdd, CLcountry))
                arrest_location_id = cursor.lastrowid
                # --------- Insert into cases ---------
                cursor.execute("""
                    INSERT INTO cases (case_number, category, status, arrest_date, arrest_agency, arrest_location, arrest_time, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (caseNumber, caseType, caseStatus, caseArrestDate, caseArrestingOfficer, arrest_location_id ,caseArrestTime, caseDescription))
                case_id = cursor.lastrowid
                # --------- Insert into case_charged_persons ---------
                cursor.execute("""
                    INSERT INTO case_charged_persons (case_number, charged_person_id)
                    VALUES (%s, %s)
                """, (
                    caseNumber, charged_person_id,
                ))
            # --------- Finalize ---------
            conn.commit()
            cursor.close()
            conn.close()
            insert_log(user_id=current_user.id, action='Create', detail='User register a charged person of a case.')
            return redirect('/cases')
        # except Exception as e:
        #     return f"An error occurred: {e}"
    return render_template('register.html',user= current_user)
@views.route('/cases')
@login_required
def cases():
    if not current_user.role =='Admin':
        abort(404)  # Check if user is an admin
        flash("You do not have permission to access this page.", "warning")
        return redirect(url_for('views.dashboard'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases")
    cases = cursor.fetchall()
    conn.close()
    return render_template('cases.html',user= current_user,cases=cases)
@views.route('/chargedPerson')
@login_required
def chargedPerson():
    if not current_user.role =='Admin':
        abort(404)  # Check if user is an admin
        flash("You do not have permission to access this page.", "warning")
        return redirect(url_for('views.dashboard'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM charged_persons")
    charged_persons = cursor.fetchall()
    conn.close()
    return render_template('chargedperson.html',user= current_user,charged_persons=charged_persons)
@views.route('/get_case_fill',methods=['GET'])
def get_case_fill():
    case_number = request.args.get('case_number')
    print(case_number)
    if not case_number:
        return jsonify({'error': 'No case number provided'}), 400
    conn = get_db()
    cursor = conn.cursor()
    query = """
            SELECT * FROM cases WHERE case_number = %s;
        """
    cursor.execute(query, (case_number,))
    case_data = cursor.fetchone()
    conn.close()
    if not case_data:
        return jsonify({'found': False})
    case_data_serializable = []
    for item in case_data:
        if isinstance(item, timedelta):
            print("appended")
            case_data_serializable.append(str(item))  # Convert timedelta to string
        else:
            print("other case")
            case_data_serializable.append(item)
    print(case_data_serializable)
    return jsonify({'found': True,
        'data': case_data_serializable})
@views.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.role =='Admin':
        abort(404)  # Check if user is an admin
        flash("You do not have permission to access this page.", "warning")
        return redirect(url_for('views.dashboard'))
    if request.method == 'POST':
        name = request.form['UserFullName']
        username = request.form['UserEmail']
        password = request.form['UserPassword']
        password2 = request.form['UserPassword2']
        role = request.form['UserRole']
        status = request.form['UserStatus']
        if password != password2:
                flash("Passwords do not match!", "Error")
                return render_template('add.html')
        else:
            hashed_password = generate_password_hash(password)
            conn = get_db()
            cursor = conn.cursor()
            try:
                cursor.execute('''INSERT INTO users (name, username, password, role, status)
                                VALUES (%s, %s, %s, %s, %s)''', 
                                (name, username, hashed_password, role, status))
                conn.commit()
                insert_log(user_id=current_user.id, action='Create', detail='User created '+name)
                flash("User registered successfully!", "success")
                return redirect('user') 
            except Exception as e:
                conn.rollback()  # Rollback if there is an error
                flash(f"Error: {e}", "danger")
        cursor.close()
        conn.close()
    return render_template('add.html',user= current_user)
@views.route('/admin/update_user/<int:id>', methods=['GET', 'POST'])
@login_required
def user_update(id):
    if not current_user.role == 'Admin':
        abort(404)  # Check if the user is an admin
        flash("You do not have permission to access this page.", "warning")
        return redirect(url_for('user.html'))  # Assuming you have a dashboard route

    conn = get_db()
    cursor = conn.cursor()
    # Fetch the user to update
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    TheUser = cursor.fetchone()
    
    if request.method == 'POST':
        name = request.form['UserFullName']
        username = request.form['UserEmail']
        password = request.form['UserPassword']
        password2 = request.form['UserPassword2']
        role = request.form['UserRole']
        status = request.form['UserStatus']
        
        # Check if password and confirm password match
        if password != password2:
            flash("Passwords do not match!", "danger")
            return render_template('user_update.html', user=current_user)  # Stay on the same page
        
        # Hash the new password if provided (only hash if password is changed)
        hashed_password = generate_password_hash(password) if password else TheUser[2]  # Keep the current password if not changing
        
        try:
            # Update the user in the database
            cursor.execute('''UPDATE users SET name = %s, username = %s, password = %s, role = %s, status = %s 
                            WHERE id = %s''', 
                            (name, username, hashed_password, role, status, id))
            conn.commit()
            insert_log(user_id=current_user.id, action='Update', detail='User updated information of '+name)
            flash("User updated successfully!", "success")
            return redirect(url_for('views.user',user=current_user))  # Redirect to view updated user page (or user list)
        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}", "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template('user_update.html',user= current_user,TheUser= TheUser)
@views.route('/admin/delete_user/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    if not current_user.role == 'Admin':
        abort(404)  # Check if user is an admin
        flash("You do not have permission to access this page.", "warning")
        return redirect(url_for('views.user'))  # Redirect to dashboard or another page
    
    # Fetch the user to delete
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    cursor.close()

    try:
        conn = get_db()
        cursor = conn.cursor()
        insert_log(user_id=current_user.id, action='Delete', detail='User deleted a user, '+user[1])
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        conn.commit()
        flash(f"User {user[1]} deleted successfully!", "success")
    except Exception as e:
        conn.rollback()  # Rollback if there is an error
        flash(f"Error: {e}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('views.user'))  # Redirect to the user list page after deletion
@views.route('/user_detail/<int:id>', methods=['GET'])
@login_required
def user_detail(id):
    if not current_user.role == 'Admin':
        abort(404)  # Check if the user is an admin
        flash("You do not have permission to access this page.", "warning")
        return redirect(url_for('dashboard'))  # Redirect to dashboard or another page
    
    # Fetch the user details from the database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        return render_template('user_detail.html', user=user)  # Pass user data to the template
    else:
        flash("User not found", "danger")
        return redirect(url_for('views.user'))
@views.route('/admin/delete_case/<int:case_number>', methods=['POST'])
@login_required
def delete_case(case_number):
    if not current_user.role == 'Admin':
        abort(404)  # Check if user is an admin
        flash("You do not have permission to access this page.", "warning")
        return redirect(url_for('views.cases'))  # Redirect to dashboard or another page
    
    # Fetch the user to delete
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases WHERE case_number = %s", (case_number,))
    TheCase = cursor.fetchone()

    try:
        conn = get_db()
        cursor = conn.cursor()
        insert_log(user_id=current_user.id, action='Delete', detail='User deleted case: '+TheCase[0])
        cursor.execute("DELETE FROM cases WHERE case_number = %s", (case_number,))
        conn.commit()
        flash(f"User {TheCase[0]} deleted successfully!", "success")
    except Exception as e:
        conn.rollback()  # Rollback if there is an error
        flash(f"Error: {e}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('views.cases'))
@views.route('/admin/chargedperson_update/<int:ChargedPersonId>', methods=['GET', 'POST'])
@login_required
def chargedperson_update(ChargedPersonId):
    # ,CaseNumber,ChargedPersonBA,ChargedPersonCA,ArrestLocation
    if not current_user.role == 'Admin':
        abort(404)  # Check if the user is an admin
        flash("You do not have permission to access this page.", "warning")
        return redirect(url_for('chargedperson.html'))  # Assuming you have a dashboard route

    conn = get_db()
    cursor = conn.cursor()
    # Fetch the user to update
    cursor.execute("SELECT * FROM charged_persons WHERE id = %s", (ChargedPersonId,))
    TheChargedperson = cursor.fetchone()
    cursor.execute("SELECT c.* FROM cases c WHERE c.case_number IN (SELECT cp.case_number FROM case_charged_persons cp WHERE cp.charged_person_id = %s)", (ChargedPersonId,))
    TheCaseNumber = cursor.fetchone()
    cursor.execute("SELECT * FROM addresses WHERE id = %s", (TheChargedperson[10],))
    ChargedPersonBAdd = cursor.fetchone()
    cursor.execute("SELECT * FROM addresses WHERE id = %s", (TheChargedperson[11],))
    ChargedPersonCAdd = cursor.fetchone()
    cursor.execute("SELECT * FROM addresses WHERE id = %s", (TheCaseNumber[5],))
    ArrestAdd = cursor.fetchone()
    arrest_time = TheCaseNumber[9]
    hours, remainder = divmod(arrest_time.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    formatted_time = f"{arrest_time.days * 24 + hours:02}:{minutes:02}"
    if request.method == 'POST':
            # -------------Personal information------------
            name = request.form['name']
            gender = request.form['gender']
            dob = request.form['dob']
            nationality = request.form['nationality']
            idNumber = request.form['idNumber']
            occupation = request.form['occupation']
            MaritalStatus = request.form['MaritalStatus']
            workplace = request.form['workplace']
            email = request.form['email']
            # -------------Birth Address------------
            bCity = request.form['bCity']
            bDistrict = request.form['bDistrict']
            bCommune = request.form['bCommune']
            bVillage = request.form['bVillage']
            bStreetAdd = request.form['bStreetAdd']
            bCountry = request.form['bCountry']
            bPostal = request.form['bPostal']
            # -------------Current Address------------
            cCity = request.form['cCity']
            cDistrict = request.form['cDistrict']
            cCommune = request.form['cCommune']
            cVillage = request.form['cVillage']
            cStreetAdd = request.form['cStreetAdd']
            cCountry = request.form['cCountry']
            cPostal = request.form['cPostal']
            # -------------Case Detail------------
            caseNumber = request.form['caseNumber']
            caseType = request.form['caseType']
            caseStatus = request.form['caseStatus']
            caseArrestDate = request.form['caseArrestDate']
            caseArrestTime = request.form['caseArrestTime']
            caseArrestingOfficer = request.form['caseArrestingOfficer']
            caseDescription = request.form['caseDescription']
            # -------------Case location Address------------
            CLcity = request.form['CLcity']
            CLdistrict = request.form['CLdistrict']
            CLcommune = request.form['CLcommune']
            CLvillage = request.form['CLvillage']
            CLstreetAdd = request.form['CLstreetAdd']
            CLcountry = request.form['CLcountry']
            print(caseArrestTime)
            try:
                cursor.execute("""
                    UPDATE addresses
                    SET city = %s, district = %s, commune = %s, village = %s, street_address = %s, country = %s, postal_code = %s
                    WHERE id = %s
                """, (bCity, bDistrict, bCommune, bVillage, bStreetAdd, bCountry, bPostal, ChargedPersonBAdd[0]))  # Assuming ChargedPersonBAdd is the address object retrieved

                # Update the current address (Charged Person's Current Address)
                cursor.execute("""
                    UPDATE addresses
                    SET city = %s, district = %s, commune = %s, village = %s, street_address = %s, country = %s, postal_code = %s
                    WHERE id = %s
                """, (cCity, cDistrict, cCommune, cVillage, cStreetAdd, cCountry, cPostal, ChargedPersonCAdd[0]))  # Assuming ChargedPersonCAdd is the address object retrieved
                cursor.execute("""
                        UPDATE addresses
                        SET city = %s, district = %s, commune = %s, village = %s, street_address = %s, country = %s
                        WHERE id = %s
                    """, (CLcity, CLdistrict, CLcommune, CLvillage, CLstreetAdd, CLcountry, ArrestAdd[0]))
                # Update the charged_persons record
                cursor.execute("""
                    UPDATE charged_persons
                    SET card_number = %s, name = %s, gender = %s, dob = %s, nationality = %s, occupation = %s, 
                        MaritalStatus = %s, workplace = %s, contact_info = %s, birth_place = %s, current_location = %s, 
                        modified_by = %s
                    WHERE id = %s
                """, (
                    idNumber, name, gender, dob, nationality, occupation, MaritalStatus, workplace, email, 
                    ChargedPersonBAdd[0], ChargedPersonCAdd[0], current_user.id, TheChargedperson[0]  # Assuming TheChargedperson is the person object
                ))
                # Update the case record
                cursor.execute("""
                    UPDATE cases
                    SET case_number = %s,category = %s, status = %s, arrest_date = %s, arrest_agency = %s, arrest_location = %s, 
                        arrest_time = %s, description = %s
                    WHERE case_number = %s
                """, (caseNumber, caseType, caseStatus, caseArrestDate, caseArrestingOfficer, ArrestAdd[0], caseArrestTime, caseDescription, TheCaseNumber[0]))

                # Update the case_charged_persons record
                cursor.execute("""
                    UPDATE case_charged_persons
                    SET case_number = %s
                    WHERE case_number = %s AND charged_person_id = %s
                """, (caseNumber,TheCaseNumber[0],ChargedPersonId))

                
                
                insert_log(user_id=current_user.id,action="Update", detail="User Updated the charged person and cases "+TheChargedperson[2])
                # Commit the transaction
                conn.commit()
                flash("Charged Person updated successfully!", "success")
                return redirect(url_for('views.chargedPerson',user=current_user))  # Redirect to view updated user page (or user list)
            except Exception as e:
                    conn.rollback()
                    flash(f"Error: {e}", "danger")
            finally:
                    cursor.close()
                    conn.close()
    return render_template('chargedperson_update.html',user= current_user,TheChargedperson= TheChargedperson,ChargedPersonBAdd=ChargedPersonBAdd,ChargedPersonCAdd=ChargedPersonCAdd,ArrestAdd=ArrestAdd,TheCaseNumber=TheCaseNumber,formatted_time=formatted_time)
@views.route('/courts')
@login_required
def courts():
    if not current_user.role =='Admin':
        abort(404)  # Check if user is an admin
        flash("You do not have permission to access this page.", "warning")
        return redirect(url_for('views.dashboard'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courts")
    courts = cursor.fetchall()
    conn.close()
    return render_template('court.html',user= current_user,courts=courts)
@views.route('/ActivityLogs')
@login_required
def ActivityLogs():
    if not current_user.role =='Admin':
        abort(404)  # Check if user is an admin
        flash("You do not have permission to access this page.", "warning")
        return redirect(url_for('views.dashboard'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    logs = cursor.fetchall()
    conn.close()
    return render_template('activityLog.html',user= current_user,logs=logs)
def insert_log(user_id, action, detail):
    conn = get_db()
    cursor = conn.cursor()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO logs (user_id, action, detail) VALUES (%s, %s, %s)",
                (user_id, action, detail)
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        conn.close()