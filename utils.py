import blessed
from magicprompt import prompt
from sqlalchemy import create_engine, text

term = blessed.Terminal()
body_height = 5
footer_height = 2


def clr_body():
    with term.location(0, body_height):
        print(term.clear_eos)
        term.move_xy(0, body_height)


def pfs(text: str):
    with term.location(0, term.height - 2):
        ans = prompt(text, numOnly=1, clearAfterResponse=1)
        return ans


def a_not_in_b(lst_a: list, lst_b: list):
    not_in = []

    set_b = set(lst_b)
    for item in lst_a:
        if item not in set_b:
            not_in.append(item)

    if len(not_in):
        return not_in

    else:
        return None


def print_list(lst: any) -> None:
    if lst:
        for l in lst:
            print(f"  - {l}")
    else:
        print("  ---")


def print_alterations(altered: dict) -> None:
    if altered:
        for k, v in altered.items():
            print(f"  - {k}: {v}")
    else:
        print("  ---")


def list_dbs():
    e = create_engine("postgresql:///postgres")
    with e.connect() as conn:
        q = text("SELECT datname FROM pg_database WHERE datistemplate = false;")
        r = conn.execute(q)
        dbs = [db[0] for db in r if "snap_" not in db[0]]

        return dbs
