def login(self):
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify!', 401, {'WWWW-authenticate': 'Basic realm="login required!"'})

    print(utenti.get_password_hash(str(auth.username)))

    password = 'pbkdf2:sha256:150000$yE0tZv5Z$a597a06cfb9c522b1e85679404bb0ae050654ffbdbdd0f25507a777fbe63f7d1'
    print(password)

    if not password:
        return make_response('Could not verify!', 401, {'WWWW-authenticate': 'Basic realm="login required!"'})

    if check_password_hash(password, auth.password):
        token = self.sign_token(auth.username)

        return jsonify({'token': token})

    return make_response('Could not verify!', 401, {'WWWW-authenticate': 'Basic realm = login required'})
