from functools import wraps
from flask import jsonify, request
import jwt

config = '=Xm*P69zUlOgwCQ*iansLf8H=&C5r@1wg&V8zWex#8m5U?*2osVGEeNph9*vBBWMB$0F01tK7BwQryyMBglYf' \
         'Cs0RfKAQQdKY^cv|rxCh^IFd$m_AyL1$EtXbbLtOst!AuwRlymjn8sUb2mdc0p8Uj#u47XV0l&Qse%@xfdVmr' \
         'mUI9!iCZz%qPZxRPRl1_KkcNza--XiYRVz1ZyYvaCXNwr%Yivl*MLNjbxK8N^ubHgXFfKW$_HKr%sskzIBGtP' \
         'jc5XU5*fr4D^_g|q8ok-5GDIljh5tSUzdl3oDe&thk=nd2d1JtI7oC@bw#|pjhU?I!7EuGwhG%&sDrB51#!Jp' \
         '43LcsU6ICVlmIAK!%!VjC07PWz!cLz_c0u^MRj+OV%ssD7=mTQGZ=cuH73fszHMxj1sUStXzgtT&bd!#QVO+!' \
         'Xi7P@CSKGTKjxl!u=#QaN!bQpgVEleKplzM!wFyXm6P^G43w54|IZlNGHCcbwh#naq@?JI|QKkwvuloGzRWYR6%'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token missing'}), 403

        try:
            data = jwt.decode(token, config, algorithms=["HS512"])
        except:
            return jsonify({'message': 'Token invalid'}), 403

        return f(*args, **kwargs)

    return decorated
