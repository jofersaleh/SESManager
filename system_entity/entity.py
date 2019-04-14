# from system_entity.attribute import *
from system_entity.structure_attribute import *


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

    def serialize_core_attribute(self):
        return self.core_attribute.serialize()

    def deserialize_core_attribute(self, jsons):
        for json in jsons:
            enum = AttributeType.resolve_type_from_str(json["type"])
            if enum == AttributeType.BEHAVIOR:
                pass
            elif enum == AttributeType.ASPECT:
                self.core_attribute = ModelStructuralAttribute()
                self.core_attribute.deserialize(json)
                # TODO: add optional attributes handling
                pass
            else:
                pass
        pass

    def check_alternatives(self):
        if self.core_attribute.get_type() == AttributeType.ASPECT:
            return True
        else:
            return False
