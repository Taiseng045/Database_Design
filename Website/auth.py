from flask import Blueprint,render_template, request,flash,redirect,url_for
auth = Blueprint('auth', __name__)
# from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required,logout_user,current_user
import os
from . import get_db,User
from .view import insert_log

# all the admin
APPROVED_ADMIN_EMAILS = ['taiseng66666@gmail.com']

@auth.route("/login", methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, username, password, role, status, description, delete_at,created_at,updated_at FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            # Check if the user status is 'Active' and validate password
            if user_data[5] == 'Active':  # Check if user status is active
                if check_password_hash(user_data[3], password):  # Validate password hash
                    # Create a simple user object or dictionary (or use User class if you have one)
                    print("almost")
                    user = User(user_data[0], user_data[1],user_data[2], user_data[3], user_data[4],user_data[5],user_data[6],user_data[7],user_data[8],user_data[9])
                    login_user(user, remember=True)
                    flash("Login successful", category='success')
                    insert_log(user_id=current_user.id, action='Login', detail='User log in.')
                    return redirect(url_for('views.dashboard'))  # Redirect to home page after successful login
                else:
                    print("nopeeew")
                    flash("Login failed: Incorrect password", category='error')
            else:
                print("nopedd")
                flash("Account is inactive", category='error')
        else:
            print("nopeff")
            flash("Login failed: Email not found", category='error')
        print("nope")
    return render_template('login.html', user=current_user)

@auth.route("/logout")
@login_required
def logout():
    insert_log(user_id=current_user.id, action='Logout', detail='User log out.')
    logout_user()
    return redirect(url_for('auth.login'))
# @auth.route("/sign-up", methods=['POST','GET'])
# def signUp():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         fname = request.form.get('fname')
#         lname = request.form.get('lname')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')
#         if email in APPROVED_ADMIN_EMAILS:
#             role = 'admin'
#         else:
#             role = 'customer'
#         user = User.query.filter_by(email=email).first()
#         if user:
#             flash('Email is already exists',category='error')
#         elif password1 != password2:
#             flash('Invalid password',category='error')
#         else:
#             new_user = User(email=email,fname=fname,lname=lname,password=generate_password_hash(password1,method='pbkdf2:sha256'),role=role)
#             db.session.add(new_user)
#             db.session.commit()
#             flash('Account is created successfully',category='success')
#             # login_user(user,remember=True)
#             return redirect(url_for('views.home'))
#     return render_template('sign_up.html', user= current_user)

# @auth.route("/admin")
# @login_required
# def admin():
#     if current_user.role == 'admin':
#         from .models import Product
#         products = Product.query.all()  # Fetch all products from the database
#     return render_template('admin.html',user = current_user, products=products)

# @auth.route("/admin/edit-stock", methods=['GET', 'POST'])
# @login_required
# def editstock():
#     if current_user.role == 'admin':
#         from flask import Flask
#         app = Flask(__name__)
#         UPLOAD_FOLDER = os.path.join(os.getcwd(), "Website", "static", "uploads")
#         os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist
#         app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
#         if request.method == 'POST':
#         # Get product details from the form
#             pname = request.form['pname']
#             price = float(request.form['price'])
#             stock = request.form['stock']
#             image = request.files['image']  # Image file from the form

#         # Save the image to the upload folder
#             if image:
#                 filename = secure_filename(image.filename)
#                 image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 image.save(image_path)
#                 image_url = os.path.join('uploads', filename)
#                 # Save product details to the database
#                 from .models import Product
#                 new_product = Product(name=pname, price=price,stock = stock, image_url=image_url)
#                 db.session.add(new_product)
#                 db.session.commit()

#                 return redirect(url_for('auth.admin'))
#     return render_template('EditStock.html', user=current_user)