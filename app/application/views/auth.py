from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_mail import Mail, Message
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user
from ..objects.char_claim_token import confirm_password_token, generate_account_token, generate_password_token, generate_token, confirm_token, confirm_account_token
from ..models.models import Business, Roleplaying, User, PlayerCharacter, db
from .forms.forms import PasswordChange, PasswordReset, UserLogin, UserRegistration

login_manager = LoginManager()
mail_manager = Mail()

auth = Blueprint("auth", __name__, template_folder="templates")


# Not a endpoint for convinience of use in main_page blueprint
def register_user(email: str, char_id: str, password: str):
    """Registers a new user based on their character id and password input, sends a confirmation email once complete. Returns True if successfully completed, returns False any issues occurr"""

    # create confirmation token first
    confirmation_token = generate_account_token(email, current_app)

    retrieved = db.session.execute(db.select(User).where(and_(User.char_id == char_id,
                                                              User.enabled == True))).scalar()
    # print(confirmation_token) # Temp workaround for email
    # If we can't find a disabled one existing, create a new user
    if retrieved is None:
        new_business = Business()
        new_roleplaying = Roleplaying()
        new_char = PlayerCharacter()
        new_char.char_id = char_id
        new_char.business = new_business
        new_char.roleplaying = new_roleplaying
        db.session.add(new_char)

        new_user = User()
        new_user.char_id = char_id
        new_user.email = email
        new_user.password = generate_password_hash(password)
        new_user.character = new_char
        db.session.add(new_user)
        db.session.commit()

    # send email
    html_mail = f"""You are recieving this email because you have registered and claimed your account for the Adventurer's Guild Card. Please click the link below to confirm your account and character creation.
    <br><br>
    <a href="{"http:/localhost:5000/"+url_for("auth.validate_new_user", token=confirmation_token)}">Click here to verify your email and immediately jump into your new card</a>.
    <br><br>
    If you did not use this email to register for this, please ignore this message and contact ..., do not reply to this email address as it is not being monitored."""
    confirmation_email = Message(
        subject="Adventurer's Guild Card Email Verification",
        recipients=[email],
        html=html_mail
    )
    mail_manager.send(confirmation_email)
    return True


@auth.route("/verify", methods=["GET", "POST"])
def validate_new_user():
    """Shows a page for either the successful usage of a confirmation link sent out in a email or a error page with the appropriate message"""
    retrieved_token = confirm_account_token(request.args.get("token"), current_app)
    retrieved_user = db.session.execute(db.select(User).where(User.email == retrieved_token)).scalar()

    if retrieved_token is None:
        flash("This link is either invalid or has expired. Please try claiming your character and registering again")
        return render_template("failed-verify.html")
    else:
        # set enabled to true, log user in and redirect to char page
        retrieved_user.enabled = True
        db.session.commit()
        login_user(retrieved_user)
        return redirect(url_for("card_maker.retrieve_char_details", char_id=retrieved_user.char_id, mode="edit"))


@auth.route("/login", methods=["POST"])
def login_char():
    userform = UserLogin()
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


@auth.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    """Sends a request to reset the user's password, and issues the user's email with a link"""
    resetform = PasswordReset()
    if resetform.validate_on_submit():
        # Retrieve user
        retrieved = db.session.execute(db.select(User).where(and_(User.char_id == resetform.char_id.data,
                                                                  User.email == resetform.email.data))).scalar()
        # If retrieve is none, flash "No account exists"
        if retrieved is None:
            flash("No account found for provided details")
            return render_template("reset-password.html", form=resetform, state="request")
        else:
            # Else Generate account token with email+char_id
            password_token = generate_password_token(retrieved.email, retrieved.char_id, current_app)
            # Structure reset password email
            html_mail = f"""You have recieved this email because a request was sent to us for a password reset on for Character ID {retrieved.char_id}. This link will be valid for 5 minutes. If you have not made this request, you should ignore this email.
            <br><br>
            <a href="{"http://localhost:5000"+url_for("auth.confirm_password_reset", token=password_token)}">Click here to verify your request and change your password</a>"""
            # Send email
            reset_email = Message(
                subject="Adventurer's Guild Card Password Reset",
                recipients=[retrieved.email],
                html=html_mail
            )
            mail_manager.send(reset_email)
            # Render email-sent page
            return render_template("email-success.html", mode="password")
    elif resetform.errors:
        # Form errors here
        return render_template("reset-password.html", errors=resetform.errors, form=resetform, state="request")
    return render_template("reset-password.html", form=resetform, state="request")


@auth.route("/confirm-reset", methods=["GET", "POST"])
def confirm_password_reset():
    """Recieved the token from the link and checks it for validity, then allows user to input a new password and submit it"""
    retrieved_token = confirm_password_token(request.args.get("token"), current_app)

    passwordform = PasswordChange()

    if retrieved_token == "":
        flash("This link is invalid, please try again")
        return render_template("invalid-link.html")
    elif passwordform.validate_on_submit():
        retrieved_user = db.session.execute(db.select(User).where(and_(User.char_id == retrieved_token[0],
                                                                   User.email == retrieved_token[1])))
        retrieved_user.password = passwordform.password.data
        db.session.commit()
        return render_template("reset-password.html", state="success")
    elif passwordform.errors:
        return render_template("reset-password.html", errors=passwordform.errors, form=passwordform, state="change")

    return render_template("reset-password.html", form=passwordform, state="change")
