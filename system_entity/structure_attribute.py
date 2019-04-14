from system_entity.attribute import *
from collections import OrderedDict


class ModelStructuralAttribute(ModelAttribute):
    def __init__(self):
        super(ModelStructuralAttribute, self).__init__("ASPECT")
        self.entity_list = []
        self.external_input_map = {}
        self.internal_coupling_map_tuple = {}
        self.internal_coupling_map_entity = {}
        self.external_output_map = {}
        self.priority_list = []

    def insert_entity(self, entity, arity='1'):
        # TODO: Exception Handling
        self.entity_list.append((entity, arity))

    def retrieve_entities(self):
        return self.entity_list

    def insert_coupling(self, src, dst):
        src_entity, src_port = src
        dst_entity, dst_port = dst

        if src_entity == "":
            if src_port in self.external_input_map:
                self.external_input_map[src_port].append(dst)
            else:
                self.external_input_map[src_port] = [dst]
        elif dst_entity == "":
            if dst_port in self.external_output_map:
                self.external_output_map[dst_port].append(src)
            else:
                self.external_output_map[dst_port] = [src]
        else:
            if src in self.internal_coupling_map_tuple:
                self.internal_coupling_map_tuple[src].append(dst)
                self.internal_coupling_map_entity[src_entity].append((src_port, dst))
            else:
                self.internal_coupling_map_tuple[src] = [dst]
                self.internal_coupling_map_entity[src_entity]=[(src_port, dst)]

    def retrieve_external_input_coupling(self):
        return self.external_input_map

    def retrieve_external_output_coupling(self):
        return self.external_output_map

    def retrieve_internal_coupling(self):
        return self.internal_coupling_map_entity

    def serialize(self):
        json_obj = OrderedDict()
        json_obj["type"] = "STRUCTURAL"
        json_obj["entities"] = self.retrieve_entities()
        json_obj["input_ports"] = self.retrieve_input_ports()
        json_obj["output_ports"] = self.retrieve_output_ports()
        json_obj["external_input"] = self.retrieve_external_input_coupling()
        json_obj["external_output"] = self.retrieve_external_output_coupling()
        json_obj["internal"] = self.retrieve_internal_coupling()
        return json_obj

    def deserialize(self, json):
        # Handle Entities
        for entity in json["entities"]:
            self.insert_entity(entity[0], entity[1])
        # Handle In ports
        for port in json["input_ports"]:
            self.insert_input_port(port)
        # Handle In ports
        for port in json["output_ports"]:
            self.insert_output_port(port)

        # Handle In EIC
        for k, v in json["external_input"].items():
            for t in v:
                self.insert_coupling(("", k), tuple(t))

        # Handle In EOC
        for k, v in json["external_output"].items():
            for t in v:
                self.insert_coupling(tuple(t), ("", k))

        # Handle In IC
        for k, v in json["internal"].items():
            for t in v:
                self.insert_coupling((k, t[0]), tuple(t[1]))
        pass