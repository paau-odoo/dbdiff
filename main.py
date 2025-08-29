from DatabaseConnection import DatabaseConnection
from utils import (
    a_not_in_b,
    print_list,
    print_alterations,
    term,
    body_height,
    footer_height,
    clr_body,
    pfs,
)
import utils
from magicprompt import prompt


def quick_compare(db_a: DatabaseConnection, db_b: DatabaseConnection) -> dict:
    a_tables = db_a.table_info.keys()
    b_tables = db_b.table_info.keys()

    # Identify any DELETED tables from A & NEW tables in B
    deleted_tables = a_not_in_b(a_tables, b_tables)
    new_tables = a_not_in_b(b_tables, a_tables)

    # Identify any ALTERED tables in B
    altered = {}

    for av, ak in db_a.table_info.items():
        if av not in deleted_tables and ak["records"] != db_b.table_info[av]["records"]:
            altered[av] = db_b.table_info[av]["records"] - ak["records"]

    return {
        "new_tables": new_tables,
        "deleted_tables": deleted_tables,
        "altered_tables": altered,
    }


db_a = DatabaseConnection("odoo-soup")
db_b = DatabaseConnection("snap_odoo-soup")


a_ids = db_a.get_ids("cheese7")
b_ids = db_b.get_ids("cheese7")


# def something():
#     summary = quick_compare(db_a, db_b)

#     print("New Tables:")
#     print_list(summary["new_tables"])
#     print("Deleted Tables:")
#     print_list(summary["deleted_tables"])
#     print("Record Changes:")
#     print_alterations(summary["altered_tables"])


def create_snapshot():
    dbs = utils.list_dbs()
    print(dbs)
    pfs("Select a database")


def main():
    with term.fullscreen():
        with term.location(0, 0):
            print(term.on_black(" " * term.width))
            print(
                term.bold
                + term.mediumorchid1
                + term.on_black("DBDIFF".center(term.width))
                + term.normal
            )
            print(term.on_black(term.mediumorchid + "_" * term.width + term.normal))

        with term.location(0, body_height):
            print("1. Create DB snapshot")
            print("2. Restore DB snapshot")
            print("3. Compare DB snapshot")

        ans = pfs("Select an option")

        clr_body()
        match ans:
            case 1:
                create_snapshot()
            case _:
                pass


main()
