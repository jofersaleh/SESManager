from system_entity.attribute import *
from collections import OrderedDict


class RuntimeAttribute(Attribute):
    def __init__(self):
        super(Attribute, self).__init__("RUNTIME")
        self.entity_list = []
        self.entity_model_map = {}
        self.entity_domain_map = {}

    def retrieve_entities(self):
        return self.entity_list

    def retrieve_model_map(self):
        return self.entity_model_map

    def retrieve_domain_map(self):
        return self.entity_domain_map

    def insert_entity(self, entity):
        self.entity_list.append(entity)

    def insert_model_path(self, entity, model_path):
        self.entity_model_map[entity] = model_path

    def insert_domain_path(self, entity, domain_path):
        self.entity_domain_map[entity] = domain_path

    def serialize(self):
        json_obj = OrderedDict()
        json_obj["type"] = "RUNTIME"
        json_obj["entities"] = self.retrieve_entities()
        json_obj["model_map"] = self.retrieve_model_map()
        json_obj["domain_map"] = self.retrieve_domain_map()

        return json_obj

    def deserialize(self, json):
        # Handle Entities
        for entity in json["entities"]:
            self.insert_entity(entity)

        # Handle Model Path
        for k, v in json["model_map"].items():
            self.insert_model_path(k, v)

        # Handle Domain Object Path
        for k, v in json["domain_map"].items():
            self.insert_domain_path(k, v)

