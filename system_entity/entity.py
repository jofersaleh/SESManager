# from system_entity.attribute import *
from system_entity.structure_attribute import *
from system_entity.runtime_attribute import *
import copy


class Entity(object):
    def __init__(self, _name):
        self.entity_name = _name
        self.core_attribute = None
        self.attribute_list = []

    def __str__(self):
        fmt = "{0: <10}{name: <10}\t{arity: <5}\t{opt: <5}"
        _str = ""
        _str += "Name: " + self.entity_name + "\n"
        _str += fmt.format("Entities: ", name="Name", arity="Arity", opt="Optional") + "\n"
        entities = self.core_attribute.retrieve_entities()

        for idx, entity in enumerate(entities):
            _str += "\t" + fmt.format(idx+1, name=entity[0], arity=entity[1], opt=entity[2]) + "\n"

        return _str

    def set_name(self, name):
        self.entity_name = name

    def get_name(self):
        return self.entity_name

    def get_type(self):
        return self.core_attribute.get_type()

    def get_core_attribute(self):
        return self.core_attribute

    def set_core_attribute(self, attr):
        self.core_attribute = attr

    def insert_attribute(self, attr):
        self.attribute_list.append(attr)

    def get_attribute_list(self):
        return self.attribute_list

    def serialize_attributes(self):
        attribute_map = {}
        for attribute in self.attribute_list:
            attribute_map[AttributeType.resolve_type_from_enum(attribute.get_type())] = attribute.serialize()

        return attribute_map
 #   def serialize_core_attribute(self):
 #       return self.core_attribute.serialize()

    def deserialize_attributes(self, jsons):
        #print(jsons["RUNTIME"])
        #pass
        for key, json in jsons.items():
            if key == "RUNTIME":
                ra = RuntimeAttribute()
                ra.deserialize(json)
                self.insert_attribute(ra)

    def clone(self):
        return copy.deepcopy(self)

    def check_validity(self):
        return self.core_attribute.check_validity()

    def prune(self, _sub_entity):
        self.core_attribute.prune(_sub_entity)