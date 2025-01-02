import requests
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_tree_select import tree_select
from dataloader import DataLoader as dataloader
from awss3 import AwsS3 as s3

from parameters import *

bundles_data_formated = dataloader.load_data()


@st.dialog("Selecione os valores na lista", width='large')
def bundle_modal(row:int):

    return_select = tree_select(bundles_data_formated['bundles_data_formated'])

    st.write(return_select)

    if st.button("Close"):
        
        st.session_state[f'bundle_parameter_value_{row}'] = return_select
        st.session_state[f'bundle_dialog_state_{row}'] = 1
        st.rerun()


@st.dialog("Message", width='small')
def popup(text:str):

    st.write(text)

    if st.button("Ok"):
        st.session_state['warning_dialog_state'] = 1
        st.rerun()


def build_graph(input_data):

    nodes = []
    edges = []

    if len(input_data) > 2:

        with st.container(border=True):
        
            for i,item in enumerate(input_data):
            
                if i == 0:
            
                    pass
            
                else:
            
            
                    nodes.append(Node(id=item['node_name'], label=item['node_name']))
        
                    edges.append(
                        Edge(
                            source=item['node_name'], 
                            target=item['if_true'],
                            type="STRAIGHT",
                            label="Se Verdadeiro", 
                        )
                    )
        
                    edges.append(
                        Edge(
                            source=item['node_name'], 
                            target=item['if_false'],
                            type="STRAIGHT",
                            label="Se Falso", 
                        )
                    )
            
            
            config = Config(
                width=700,
                height=300,
                nodeHighlightBehavior=True,
                directed=True, 
                physics=True, 
                hierarchical=True
            )
            
            # return_value = agraph(
            return agraph(
                nodes=nodes, 
                edges=edges,
                config=config
            )


def create_tree(input_data):

        # dados para criar a árvore
        create_tree_data = {
            "context": input_data[0]['context'],
            "name": input_data[0]['tree_name'],
            "target-field": "XPTO",
            "offline": "True" if s3.check_s3_availability() is False else "False",
            # "force": True
        }

        # criando a árvore de decisão
        response = requests.post(API_DSSF_CREATE_TREE, json=create_tree_data)

        print(f'STATUS: API response for new decision tree creation:', response.status_code)
        
        
        # dados para criar os nós
        for i, node_data in enumerate(input_data):
        
            if i == 0:
        
                pass
        
            else:
            
                if node_data['value_if_true'].strip().lower() == 'output':
            
                    se_verdadeiro_rule_contents = f"output:{node_data['if_true']}"

                elif node_data['value_if_true'].strip().lower() == 'output & ir para':

                    if_true_contents = [x.strip().lower() for x in node_data['if_true'].split('&')]

                    se_verdadeiro_rule_contents = f"{if_true_contents[0]}&output:{if_true_contents[1]}"

                else:

                    se_verdadeiro_rule_contents = node_data['if_true']
            
                if node_data['value_if_false'].strip().lower() == 'output':
            
                    se_falso_rule_contents = f"output:{node_data['if_false']}"

                elif node_data['value_if_false'].strip().lower() == 'output & ir para':

                    if_false_contents = [x.strip().lower() for x in node_data['if_false'].split('&')]

                    se_falso_rule_contents = f"{if_false_contents[0]}&output:{if_false_contents[1]}"
                
                else:

                    se_falso_rule_contents = node_data['if_false']
                    

                if node_data['parameter_type'].strip().lower() == 'bundle':
                    
                    rule_contents = 'variable:' + node_data['variable_name'] + ' ' + node_data['operation'] + f' "{node_data["parameter_value"]}"'

                else:
                    
                    rule_contents = 'variable:' + node_data['variable_name'] + ' ' + node_data['operation'] + ' ' + str(node_data['parameter_value'])


                # dados do nó
                node_data = {
                    "context": input_data[0]['context'],
                    "decision-tree-name": input_data[0]['tree_name'],
                    "offline": "True" if s3.check_s3_availability() is False else "False",

                    "node-name": node_data['node_name'],
                    "rule": rule_contents,
                    "if-true": se_verdadeiro_rule_contents,
                    "if-false": se_falso_rule_contents
                }

                # criando o nó
                response = requests.post(API_DSSF_ADD_NODE, json=node_data)
        
                print('s3.check_s3_availability():', s3.check_s3_availability())

                print(f'STATUS: node {i}', response.status_code)

        
        if ('warning_dialog_state' not in st.session_state) or (st.session_state['warning_dialog_state'] == 0):
        
            popup(f'Status code: {response.status_code}')

        else:

            st.session_state['warning_dialog_state'] = 0
