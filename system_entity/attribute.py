from system_entity.definition import AttributeType

class Attribute(object):
    def __init__(self, type):
        self.attribute_type = AttributeType.resolve_type_from_str(type)

    def get_type(self):
        return self.attribute_type

    def __str__(self):
        return "\"type\":" + self.attribute_type + ","

class ModelAttribute(Attribute):
    def __init__(self, _type):
        super(ModelAttribute, self).__init__(_type)
        # Input Ports Declaration
        self.input_ports = []
        # Output Ports Declaration
        self.output_ports = []

    def insert_input_port(self, port):
        self.input_ports.append(port)
    def retrieve_input_ports(self):
        return self.input_ports

    def insert_output_port(self, port):
        self.output_ports.append(port)
    def retrieve_output_ports(self):
        return self.output_ports

class ModelBehaviorAttribute(ModelAttribute):
    def __init__(self):
        super(ModelBehaviorAttribute, self).__init__("BEHAVIOR")
        self.states = {}
        self.external_transition_map_tuple = {}
        self.external_transition_map_state = {}
        self.internal_transition_map_tuple = {}
        self.internal_transition_map_state = {}
        #self.time_advance_map = {}

    def insert_state(self, name, deadline):
        # TODO: Exception Handling
        # TA < 0
        # Duplicated State
        self.states[name] = deadline

    def retrieve_states(self):
        return self.states

    def find_state(self, name):
        return name in self.states

    def insert_external_transition(self, pre_state, event, post_state):
        self.external_transition_map_tuple[(pre_state, event)] = post_state
        if pre_state in self.external_transition_map_state:
            self.external_transition_map_state[pre_state].append(event, post_state)
        else:
            self.external_transition_map_state[pre_state] = [(event, post_state)]

    def retrieve_external_transition(self, pre_state):
        return self.external_transition_map_state[pre_state]

    def retrieve_external_transition(self, pre_state, event):
        return self.external_transition_map_tuple((pre_state, event))

    def find_external_transition(self, pre_state):
        return pre_state in self.external_transition_map_state

    def insert_internal_transition(self, pre_state, event, post_state):
        self.internal_transition_map_tuple[(pre_state, event)] = post_state
        if pre_state in self.internal_transition_map_state:
            self.internal_transition_map_state[pre_state].append(event, post_state)
        else:
            self.internal_transition_map_state[pre_state] = [(event, post_state)]

    def retrieve_internal_transition(self, pre_state):
        return self.internal_transition_map_state[pre_state]

    def retrieve_internal_transition(self, pre_state, event):
        return self.internal_transition_map_tuple((pre_state, event))

    def find_internal_transition(self, pre_state):
        return pre_state in self.internal_transition_map_state

class ModelStructuralAttribute(ModelAttribute):
    def __init__(self):
        super(ModelStructuralAttribute, self).__init__("STRUCTURAL")
        self.entity_list = []
        self.external_input_map = {}
        self.internal_coupling_map_tuple = {}
        self.internal_coupling_map_entity = {}
        self.external_output_map = {}
        self.priority_list = []

    def insert_entity(self, entity):
        # TODO: Exception Handling
        self.entity_list.append(entity)

    def retrieve_entities(self):
        return self.entity_list

#    def find_entity(self, entity):
#        return name in self.states

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

    def deserialize(self, json):
        # Handle Entities
        for entity in json["entities"]:
            self.insert_entity(entity)
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

        #json["external_input"] = self.core_attribute.retrieve_external_input_coupling()
        #json["external_output"] = self.core_attribute.retrieve_external_output_coupling()
        #json["internal"] = self.core_attribute.retrieve_internal_coupling()
        pass