import json
import os
from collections import OrderedDict
from model_base.behavior_model import *


class model_manager(object):
    def __init__(self):
        pass

    def export_model(self, model, path=".", name="model.json"):
        entity_data = OrderedDict()
        entity_data["name"] = model.get_name()
        entity_data["model"] = model.serialize()

        f = open(os.path.join(path, name), "w")
        f.write(json.dumps(entity_data, ensure_ascii=False, indent="\t"))
        f.close()

    def import_model(self, path=".", name="model.json"):
        json_data = open(os.path.join(path, name)).read()
        data = json.loads(json_data)
        name = data["name"]
        _model = BehaviorModel(name)
        _model.deserialize(data["model"])
        return _model
