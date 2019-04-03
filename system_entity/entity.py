from system_entity.attribute import *
from collections import OrderedDict

class Entity(object):
    def __init__(self, _name="None", _type="None"):
        self.entity_name = _name
        self.entity_type = AttributeType.resolve_type_from_str(_type)
        self.core_attribute = None
        self.attribute_list = []

    def __str__(self):
        return self.entity_name

    def set_name(self, name):
        self.entity_name = name

    def get_name(self):
        return self.entity_name

    def set_type(self, _type):
        self.entity_type = AttributeType.resolve_type_from_str(_type)

    def get_type(self):
        return AttributeType.resolve_type_from_enum(self.entity_type)

    def get_core_attribute(self):
        return self.core_attribute

    def set_core_attribute(self, attribute):
        self.core_attribute = attribute

    def insert_attribute(self, attribute):
        self.attribute_list.append(attribute)

    def get_attribute_list(self):
        return self.attribute_list

class StructuralEntity(Entity):
    def __init__(self, _name):
        super(StructuralEntity, self).__init__(_name)
        self.core_attribute = ModelStructuralAttribute()
        self.entity_type = self.core_attribute.get_type()
        self.attribute_list = []

    def insert_entity(self, name):
        self.core_attribute.insert_entity(name)

    def insert_input_port(self, name):
        self.core_attribute.insert_input_port(name)

    def retrieve_input_ports(self):
        return  self.core_attribute.retrive_input_ports()

    def insert_output_port(self, name):
        self.core_attribute.insert_output_port(name)

    def retrieve_output_ports(self):
        return  self.core_attribute.retrive_output_ports()

    def insert_coupling(self, src, dst):
        self.core_attribute.insert_coupling(src, dst)

    def serialize_core_attribute(self):
        to_list = []
        #attributes = self.get_attribute_list()
        #for attribute in attributes:
        json_obj = OrderedDict()
        json_obj["type"] = AttributeType.resolve_type_from_enum(self.core_attribute.get_type())
        json_obj["entities"] = self.core_attribute.retrieve_entities()
        json_obj["input_ports"] = self.core_attribute.retrieve_input_ports()
        json_obj["output_ports"] = self.core_attribute.retrieve_output_ports()
        json_obj["external_input"] = self.core_attribute.retrieve_external_input_coupling()
        json_obj["external_output"] = self.core_attribute.retrieve_external_output_coupling()
        json_obj["internal"] = self.core_attribute.retrieve_internal_coupling()
        to_list.append(json_obj)
        return to_list

    def deserialize_core_attribute(self, jsons):
        for json in jsons:
            enum = AttributeType.resolve_type_from_str(json["type"])
            if enum == AttributeType.BEHAVIOR:
                pass
            elif enum == AttributeType.STRUCTURAL:
                self.core_attribute = ModelStructuralAttribute()
                self.core_attribute.deserialize(json)
                pass
            else:
                pass
        pass

    def attribute_to_list(self): # TODO modify serialization
        to_list = []
        attributes = self.get_attribute_list()
        for attribute in attributes:
            json_obj = OrderedDict()
            json_obj["type"] = AttributeType.resolve_type_from_enum(attribute.get_type())
            json_obj["entities"] = attribute.retrive_entities()
            json_obj["input_ports"] = attribute.retrive_input_ports()
            json_obj["output_ports"] = attribute.retrive_output_ports()
            json_obj["external_input"] = attribute.retrive_external_input_coupling()
            json_obj["external_output"] = attribute.retrive_external_output_coupling()
            json_obj["internal"] = attribute.retrive_internal_coupling  ()
            to_list.append(json_obj)
        return to_list
    pass

class BehaviorEntity(Entity):
    def __init__(self, name):
        super(BehaviorEntity, self).__init__(name)
        self.core_attribute = ModelBehavioralAttribute()

    pass

### Test code ###
if __name__ == "__main__":
    entity = Entity("abc")
    entity.insert_attribute(ModelBehaviorAttribute())
    attribute : ModelBehaviorAttribute = entity.get_attribute_list()[0]
    attribute.insert_state("idle", 0)
    print(attribute.find_state("idle"))
    print(Entity("abc"))

##################