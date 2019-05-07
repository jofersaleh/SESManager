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

    def insert_entity(self, entity, arity='1', opt=False):
        # TODO: Exception Handling
        self.entity_list.append([entity, arity, opt])

    def remove_entity(self, entity):
        # Check External Input Coupling
        remove_list = []
        for k, v in self.external_input_map.items():
            for item in v:
                if entity[0] == item[0]:
                    remove_list.append(item)
            for item in remove_list:
                v.remove(item)

        remove_list.clear()

        # Check External Output Coupling
        for k, v in self.external_output_map.items():
            for item in v:
                if entity[0] == item[0]:
                    remove_list.append(item)

            for item in remove_list:
                v.remove(item)

        # Check Internal Coupling - Source
        if entity[0] in self.internal_coupling_map_tuple.items():
            del(self.internal_coupling_map_tuple[entity[0]])
            del(self.internal_coupling_map_entity[entity[0]])

        remove_list.clear()
        # Check Internal Coupling - Destination
        for k, v in self.internal_coupling_map_tuple.items():
            for item in v:
                if entity[0] == item[0]:
                    remove_list.append(item)

            for item in remove_list:
                v.remove(item)

        remove_list.clear()
        for k, v in self.internal_coupling_map_entity.items():
            for item in v:
                if entity[0] == item[1][0]:
                    remove_list.append(item)

            for item in remove_list:
                v.remove(item)

        self.entity_list.remove(entity)

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

    def remove_coupling(self, _src, _dst):
        src_entity, src_port = _src
        dst_entity, dst_port = _dst

        # TODO: Implement
        pass

    def retrieve_external_input_coupling(self):
        return self.external_input_map

    def retrieve_external_output_coupling(self):
        return self.external_output_map

    def retrieve_internal_coupling(self):
        return self.internal_coupling_map_entity

    def serialize(self):
        json_obj = OrderedDict()
        # json_obj["type"] = "ASPECT"
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
            self.insert_entity(entity[0], entity[1], entity[2])
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

    def check_validity(self):
        result = []
        for entity in self.entity_list:
            print(entity)
            if type(entity[1]) is not int:
                result.append(entity)
                continue
            if entity[2]:
                result.append(entity)

        return result

    def prune(self, _sub_entity):
        delete_entity = None
        for entity in self.entity_list:
            if entity[0] == _sub_entity:
                if entity[2]:
                    print("> The sub-entity {0} is optional".format(entity[0]))
                    choice = input("> Select(s), Remove(r)")
                    if choice == 's':
                        entity[2] = False
                    else:
                        delete_entity = entity
                        break
                if type(entity[1]) is str:
                    print("> The arity of {0} is {1}".format(entity[0], entity[1]))
                    entity[1] = int(input("> Enter arity:"))

        if delete_entity is not None:
            self.remove_entity(delete_entity)

