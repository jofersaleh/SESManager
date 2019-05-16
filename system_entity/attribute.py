from system_entity.definition import AttributeType



class Attribute(object):
    def __init__(self, _type):
        self.attribute_type = AttributeType.resolve_type_from_str(_type)

    def get_type(self):
        return self.attribute_type

    def __str__(self):
        return "\"type\":" + self.attribute_type + ","

    def serialize(self):
        pass

    def deserialize(self, json):
        pass


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


class AlternativeAttribute(Attribute):
    def __init__(self, _type):
        super(Attribute, self).__init__("ALTERNATIVE")
        self.alternative_type = _type

