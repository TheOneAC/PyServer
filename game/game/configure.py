#!/usr/bin/python
# -*- coding: utf-8 -*-


LOGIN_HOST, LOGIN_PORT = "0.0.0.0", 9999
ACTION_HOST, ACTION_PORT = "0.0.0.0", 9998
MESSAGE_SIZE = 1024
enKey = "68b329da9893e340"
salt = ""

logFileName = 'log/logfile.txt'

RSA_PRIVATE_KEY = "\
MIICXQIBAAKBgQCY4l+8+5B6wzSh/wMTwvaj8KfGhxYRbhX5vtkVAVIICWWgsDwg\n\
lriJjFzObKenNU+k2he+jG1ZncfDI3fXS0rD34pT0PvxG3f/KoeKtnstnSOH4wEC\n\
LTVhHeKKQdP+gAzTFrbHtP+kONDIQeBFLbfxjipU2vyDbeYoPASy8iZqXwIDAQAB\n\
AoGAQ9QLTbj+fLimXUjagKX67vkSNo4wSENjFI6LmTogvtgMcqI9yueTr9LKSfsC\n\
1rhcQXNRHYUH7r6FphnSTX5mCJj/FgFG8KP+RwwzbghuLK3Jj365aRE6y9csThuH\n\
hyfYEAVdvlSyuc/i1RDdO4lvB1QV3h6v4EVKXgWuhZLfOqECQQC58hBphr14Fvc5\n\
uysgjg11zQ+1+Xj/yP1ehsMTFaCNOgdsWCAQk/555nno2vvKVSubZC5BDsav0GW3\n\
PAM/eKzzAkEA0nujyvDD1I2OGX0T8EI85FVUx3ziXIvdepyRZ/Vjn8lArrijvy1K\n\
FdzqMLYB30KlzVOjMqbaPrabUhCttqa35QJBAJJvy/UPI8+bZn+Uo1Y0CO2o3KKX\n\
IW9vPfpfbulsstAFzyrIDBiCNHqTw5ZaPskNYhYyQysBFAAJwtEW9gfaZXkCQAqe\n\
JhMUtixAv8xVXO4fyUaTb2VozVpxy8hloYgm/tGOq26k7c21ESmtLTsr00hZ6ldD\n\
QtZJSHUlbQxkvv6ZxmkCQQCx8uwYz1/WN7aA5HXA9+VLpZUUZ9vtde1ckGo0S+Be\n\
w0sxIUgQIe7KMu63Pz7MvgHXPwGG01h/NXXvG/pUP1e8\n"

RSA_PUBLIC_KEY = "\
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCY4l+8+5B6wzSh/wMTwvaj8KfG\n\
hxYRbhX5vtkVAVIICWWgsDwglriJjFzObKenNU+k2he+jG1ZncfDI3fXS0rD34pT\n\
0PvxG3f/KoeKtnstnSOH4wECLTVhHeKKQdP+gAzTFrbHtP+kONDIQeBFLbfxjipU\n\
2vyDbeYoPASy8iZqXwIDAQAB\n\
"
from M2Crypto import RSA
publicKey = 'secret/public'
privateKey = 'secret/private'
RSAPub = RSA.load_pub_key(publicKey)
RSAPri = RSA.load_key(privateKey)