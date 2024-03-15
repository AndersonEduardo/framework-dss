from node import *
from decisiontree import *


class DecisionTree:

    def __init__(self, name:str, target_field:str):

        self.id = None
        self.name = name
        self.node_list = list()
        self.target_field = target_field


    def add(self, node:Node):

        self.node_list.append(node)


    def rooting(self):

        self.node_list[0].root = True


    def get_root(self):

        for node in self.node_list:

            if node.root is not None and node.root is True:

                return node.name


    def query(self, x:dict):

        print('\n*Decision Tree Name:', self.name.upper())

        node_root = self.get_root()
        output = self.eval_(node_root, x)

        output = list(set(output))

        return sorted(output)


    def eval_(self, node_name:str, x:dict, **kwargs):

        output = kwargs.get('output')

        if output is None:

            output = list()

        else:

            output = output

        for node_i in self.node_list:

            if node_i.name.strip().lower() == node_name.strip().lower():

                node_output = node_i.eval_rule(x)

                if '&output' in node_output.strip().lower():

                    if 'none' not in node_output.strip().lower():

                        node_output_clean = ':'.join(node_output.split(':')[1:]).strip()

                        output.append(node_output_clean)

                    next_node = node_output.strip().lower().split(':')[0].split('&')[0].strip().lower()

                    return self.eval_(next_node, x, output=output)

                elif 'output:' in node_output.strip().lower():

                    if 'none' not in node_output.lower():

                        # node_output_clean = node_output.split(':')[-1]
                        node_output_clean = ':'.join(node_output.split(':')[1:]).strip()

                        output.append(node_output_clean)

                    return output

                elif 'output&' in node_output.strip().lower():

                    if 'none' not in node_output.strip().lower():

                        # node_output_clean = node_output.split(':')[-1]
                        node_output_clean = ':'.join(node_output.split(':')[1:]).strip()

                        output.append(node_output_clean)

                    next_node = node_output.strip().lower().split(':')[0].split('&')[1].strip().lower()

                    return self.eval_(next_node, x, output=output)

                else:

                    return self.eval_(node_output, x, output=output)

        raise Exception(f'Node name "{node_name}" not found in the Tree.')


    def delete_node(self, node_name:str):

        for i in range(len(self.node_list)):

            if self.node_list[i].name.strip().lower() == node_name:

                self.node_list.pop(i)

                break


    def get_node_list(self):

        return [{'id':id, 'node_name': x.name} for (id,x) in enumerate(self.node_list)]


    def get_rule_list(self):

        return [{'id':id, 'node_name': x.name, 'node_rule': x.rules} for (id,x) in enumerate(self.node_list)]