from dotenv import load_dotenv
import sys
if len(sys.argv) > 1:
    load_dotenv("." + sys.argv[1])
else:
    load_dotenv()

from registry import Registry, db
from flare import app
import json
import os
import core_models
__import__("apps." + os.environ["app"])
os.environ["app_path"] = os.path.abspath(os.path.join("apps", os.environ["app"]))
print("App path", os.environ["app_path"])

db.init(os.environ["db_name"],
    user=os.environ["db_user"],
    password=os.environ["db_pass"],
    host=os.environ["db_host"],
    port=os.environ["db_port"])
db_interactive_evolve = True if os.environ.get("db_interactive_evolve",'') == 'True' else False
db.evolve(interactive=db_interactive_evolve)
port = os.environ.get("port", 6800)
host = os.environ.get("host", "0.0.0.0")
flask_debug = True if os.environ.get("flask_debug",'') == 'True' else False
print(Registry)

Meta = Registry["FlrMeta"]

#Initialize empty database
if Registry["FlrUser"].read([], count=True) == 0:
    #Create administrator
    if not os.environ.get("admin_pass"):
        admin_passwd = input("Superuser password: ")
    else:
        admin_passwd = os.environ["admin_pass"]
    gid = Registry["FlrGroup"].flr_create(name="Administrator")
    uid = Registry["FlrUser"].flr_create(
        name="Administrator",
        login="admin",
        email="admin",
        password=admin_passwd,
        groups=[gid])
    Meta.flr_create(
        meta_id="flgroup_admin",
        model="FlrGroup",
        rec_id=gid
    )
    Meta.flr_create(
        meta_id="fluser_admin",
        model="FlrUser",
        rec_id=uid
    )

with db.atomic() as transaction:
#Load records from "data" directory
    try:
        all_meta_ids = set()
        for meta in Meta.select(Meta.meta_id):
            all_meta_ids.add(meta.meta_id)
        read_meta_ids = set()
        files_initial = []
        files_custom  = []
        initial_data = "data"
        custom_data = os.path.join("apps", os.environ["app"], "data")
        for files, data_directory in ((files_initial,initial_data), (files_custom,custom_data)):
            if os.path.exists(data_directory):
                for fname in os.listdir(data_directory):
                    if fname.endswith(".json"):
                        fullpath = os.path.join(data_directory, fname)
                        files.append(fullpath)
        for fullpath in sorted(files_initial) + sorted(files_custom):
            print("Loading", fullpath)
            with open(fullpath) as f:
                records = json.load(f)
                for record in records:
                    if not record.get("meta_id"):
                        raise Exception("%s\nmeta:id missing"%record)
                    if not record.get("model"):
                        raise Exception("%s\nModel missing"%record)
                    if not record.get("data"):
                        raise Exception("%s\nData missing"%record)
                    model_name = record["model"]
                    Model = Registry[model_name]
                    meta_id = record["meta_id"]
                    read_meta_ids.add(meta_id)
                    existing = Meta.get_or_none(
                        Meta.model==model_name,
                        Meta.meta_id==meta_id
                    )
                    data = record["data"]
                    for field in data:
                        if field.endswith("_META_ID"):
                            if type(data[field]) == str:
                                meta_ids = [data[field]]
                                m2m = False
                            elif type(data[field]) == list:
                                meta_ids = data[field]
                                m2m = True
                            else:
                                raise Exception("%s expected string or list"%field)
                            res_ids = []
                            for meta_id_search in meta_ids:
                                ref = Meta.get_or_none(
                                    Meta.meta_id==meta_id_search
                                )
                                if ref is None:
                                    raise Exception("%s: meta_id does not exist"%meta_id_search)
                                res_ids.append(ref.rec_id)
                            if not m2m:
                                data[field] = res_ids[0]
                            else:
                                data[field] = res_ids
                    data = {
                        k.replace("_META_ID",""): data[k]
                        for k in data
                    }
                    if existing is None:
                        created_id = Model.flr_create(**data)
                        Meta.flr_create(
                            model=model_name,
                            rec_id=created_id,
                            meta_id=meta_id
                        )
                    else:
                        Model.flr_update(data, [('id','=',existing.rec_id)])
        #Delete records that are in the meta table but are not present in the files (were deleted from the file)
        for meta_id in all_meta_ids:
            if meta_id not in read_meta_ids and meta_id not in ("fluser_admin","flgroup_admin"):
                print("deleting", meta_id)
                meta_rec = Meta.get_or_none(Meta.meta_id==meta_id)
                if meta_rec:
                    meta_rec.delete_instance()
                    rec = Registry[meta_rec.model].get_by_id(meta_rec.rec_id)
                    rec.delete_instance()
    except:
        transaction.rollback()
        raise

app.run(port=port, host=host, debug=flask_debug)