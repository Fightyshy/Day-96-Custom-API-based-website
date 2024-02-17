from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_mail import Mail, Message
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user
from ..objects.char_claim_token import generate_account_token, generate_token, confirm_token, confirm_account_token
from ..models.models import User, PlayerCharacter, db
from .forms.forms import UserLogin, UserRegistration

login_manager = LoginManager()
mail_manager = Mail()

auth = Blueprint("auth", __name__, template_folder="templates")

# TODO check register functioning
@auth.route("/register", methods=["POST"])
def register_user():
    """Registers a new user based on their character id and password input, sends a confirmation email once complete"""
    email = request.get_json()["email"]
    char_id = request.get_json()["char_id"]
    password = request.get_json()["password"]

    # create confirmation token first
    confirmation_token = generate_account_token(email, current_app)

    retrieved = db.session.execute(db.select(User).where(and_(User.char_id == char_id,
                                                              User.enabled == False))).scalar()

    # If we can't find a disabled one existing, create a new user
    if retrieved is None:
        new_user = User()
        new_user.char_id = char_id
        new_user.email = email
        new_user.password = password
        new_user.character = db.session.execute(db.select(PlayerCharacter).where(PlayerCharacter.char_id == char_id)).scalar()
        db.session.add(new_user)
        db.session.commit()

    # send email
    html_mail = f"""You are recieving this email because you have registered and claimed your account for the Adventurer's Guild Card. Please click the link below to confirm your account and character creation.
    <br><br>
    <a href="{url_for()}"></a>
    <br><br>
    If you did not use this email to register for this, please ignore this message and contact ..., do not reply to this email address as it is not being monitored."""
    confirmation_email = Message(
        subject="Adventurer's Guild Card Email Validation",
        recipients=[email],
        html=html_mail
    )
    mail_manager.send(confirmation_email)

    return render_template("register_sent.html")

# TODO validate functioning
@auth.route("/validate", methods=["GET", "POST"])
def validate_new_user():
    """Shows a page for either the successful usage of a confirmation link sent out in a email or a error page with the appropriate message"""
    retrieved_token = confirm_account_token(request.args.get("token"))
    retrieved_user = db.session.execute(db.select(User).where(User.email == retrieved_token)).scalar()

    if retrieved_token is None:
        flash("This link is either invalid or has expired. Please try claiming your character and registering again")
    else:
        # set enabled to true, log user in and redirect to char page
        retrieved_user.enabled = True
        db.session.commit()
        login_user(retrieved_user)
        return redirect(url_for("card_maker.retrieve_char_details", char_id=retrieved_user.char_id, mode="edit"))


@auth.route("/login", methods=["POST"])
def login_char():
    userform = UserLogin()
    # char_id = request.args.get("char_id")
    # password = request.args.get("password")
    retrieved = db.session.execute(db.select(User).where(and_(User.char_id == userform.char_id.data,
                                                               User.enabled == True))).scalar()
    if userform.validate_on_submit():
        if not retrieved:
            flash("Character has not been claimed and account not made yet")
            return redirect(url_for("main_page.get_charid"))
        elif not check_password_hash(retrieved.password, userform.password.data):
            flash("Password is wrong")
            return redirect(url_for("main_page.get_charid"))
        else:
            login_user(retrieved)
            return redirect(url_for("card_maker.retrieve_char_details", char_id=retrieved.char_id, mode="edit"))
    
@auth.route("/logout")
def logout_char():
    logout_user()
    return redirect(url_for("main_page.get_charid"))

# TODO password reset
@auth.route("/reset-password")
def reset_password():
    """Sends a request to reset the user's password, and issues the user's email with a link"""
    pass

@auth.route("/confirm-reset")
def confirm_password_reset():
    """Recieved the token from the link and checks it for validity, then allows user to input a new password and submit it"""
    pass