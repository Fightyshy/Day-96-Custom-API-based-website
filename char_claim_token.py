from itsdangerous import URLSafeTimedSerializer

# https://www.freecodecamp.org/news/setup-email-verification-in-flask-app/


def generate_token(charid, app):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(charid, salt=app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, app, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        charid = serializer.loads(
            token,
            salt=app.config["SECURITY_PASSWORD_SALT"],
            max_age=expiration,
        )
        return charid
    except Exception:
        return False
