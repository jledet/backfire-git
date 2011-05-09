#!/usr/bin/env python

import socket
import cPickle

host = ''
port = 9988

def recv_obj(sock):
    try:
        f = sock.makefile('rb')
        obj = cPickle.load(f)
        f.close()
    except Exception:
        return None

    return obj

def send_obj(sock, obj):
    try:
        f = sock.makefile('wb')
        cPickle.dump(obj, f, cPickle.HIGHEST_PROTOCOL)
        f.close()
    except Exception:
        return

def serve():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)

    while True:
        conn, addr = s.accept()
        cmd = recv_obj(conn)

        if not cmd or not cmd.has_key('action'):
            pass
        elif cmd['action'] == 'write':
            try:
                f = open(cmd['path'], 'w')
                f.write(cmd['value'])
                f.close()
                send_obj(conn, "OK")
            except Exception as error:
                send_obj(conn, error)
        elif cmd['action'] == 'read':
            try:
                f = open(cmd['path'], 'r')
                val = f.read()
                f.close()
                send_obj(conn, val)
            except Exception as error:
                send_obj(conn, error)
        elif cmd['action'] == 'exec':
            try:
                val = os.popen(cmd['cmd'], 'r').read()
                send_obj(conn, val)
            except Exception as error:
                send_obj(conn, error)
        elif cmd['action'] == 'close':
            print("Received quit")
            send_obj(conn, "Quit")
            conn.close()
            break

    conn.close()

try:
    serve()
except KeyboardInterrupt:
    print("Quit")
