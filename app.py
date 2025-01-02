import requests
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_tree_select import tree_select

# from dssf.parameters import *
from parameters import *
from utils import *
from dataloader import DataLoader as dataloader


bundles_data_formated = dataloader.load_data()


st.title("Decision Trees")

# Armazenar os valores
if 'number_of_lines' not in st.session_state:

    st.session_state['number_of_lines'] = 1


input_data = list()

if 'session_input_data' not in st.session_state:

    st.session_state['session_input_data'] = list() #input_data



col = st.columns([1, 1])

with col[0]:

    context_name = st.text_input("Context name:", value='sandbox', key="context")

with col[1]:

    tree_name = st.text_input("Decision tree name:", value=None, key="decision_tree")

input_data.append({'context': context_name, 'tree_name': tree_name})


counter = 0

while counter < st.session_state['number_of_lines']: 

    st.write(f'**Decision node {counter+1}:**')

    with st.container():

        col1, _ = st.columns(2)

        with col1:
        
            node_name = st.text_input('Node name:', value=None, key=f"node_name_{counter}")

        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
    
            variable_name = st.text_input("Variable name:", value=None, key=f"var_{counter}")
    
        with col2:
    
            operation = st.selectbox('Operation type:', MENU_OPERATIONS, index=None, key=f"operation_{counter}")
    
        with col3:
    
            parameter_type = st.selectbox('Parameter type:', MENU_PARAMETERS_TYPE, index=None, key=f"parameter_type_{counter}")

            if str(parameter_type).strip().lower() == 'bundle':

                if (f'bundle_dialog_state_{counter}' not in st.session_state) or (st.session_state[f'bundle_dialog_state_{counter}'] == 0):

                    bundle_modal(row=counter)

            else:

                st.session_state[f'bundle_dialog_state_{counter}'] = 0

        with col4:

            if str(parameter_type).strip().lower() == 'bundle':

                selection_indexes = st.session_state.get(f'bundle_parameter_value_{counter}')

                selection_indexes = '' if selection_indexes is None else selection_indexes['checked']

                selection_indexes = [x for x in selection_indexes if x.split('_')[0].strip().lower() not in ['pathway', 'section']]

                parameter_value = [bundles_data_formated['index_list'].get(x) for x in selection_indexes]

                if len(set(x.split('_')[0] for x in selection_indexes)) > 1:

                    st.session_state[f'bundle_parameter_value_{counter}'] = None # necessário forçar None aqui, para limpar o placeholder
                    
                    popup('Mixing values from different categories (e.g., exams with medications) is not allowed.')

                    st.session_state[f'bundle_dialog_state_{counter}'] = 0

                else:

                    st.session_state['warning_dialog_state'] = 0

                    parameter_value = [str(x).title() for x in parameter_value]

                    parameter_value = '[linebreak]'.join(parameter_value)


                st.text_input("Parameter value:", disabled=True, value=None, 
                              placeholder=parameter_value.replace('[linebreak]', ', '), key=f"parameter_value_{counter}")          


            else:

                parameter_value = st.text_input("Parameter value:", disabled=False, value=None, key=f"parameter_value_{counter}")

                if (str(parameter_type).strip().lower() == 'number') and (parameter_value is not None):
            
                    parameter_value = float(parameter_value)


    with st.container():

        col1, col2 = st.columns(2)

        with col1:
    
            value_if_true = st.selectbox('If *True*:', MENU_ACTION,
                                         index=None, key=f"se_verdadeiro_{counter}")
            value_if_false = st.selectbox('If *False*:', MENU_ACTION,
                                          index=None, key=f"se_falso_{counter}")
    
        with col2:

            if value_if_true == 'Output & Go to':

                place_holder_true = 'Example: Node-02 & Obesity'

            else:

                place_holder_true = None

            if value_if_false == 'Output & Go to':

                place_holder_false = 'Example: Node-02 & Obesity'

            else:

                place_holder_false = None

            contents_if_true = st.text_input(
                "Contents:", value=None, placeholder=place_holder_true, key=f"contents_if_true_{counter}"
            )
            contents_if_false = st.text_input(
                "Contents:", value=None, placeholder=place_holder_false, key=f"contents_if_false_{counter}"
            )

            contents_if_true = None if (contents_if_true == '') or (contents_if_true == 'End') else contents_if_true
            contents_if_false = None if (contents_if_false == '') or (contents_if_true == 'End') else contents_if_false


    input_data.append(
        {
            'node_name': node_name, 'variable_name': variable_name, 
            'operation': operation, 
            'parameter_type': parameter_type, 'parameter_value': parameter_value,
            'value_if_true': value_if_true, 'value_if_false': value_if_false,
            'if_true': contents_if_true, 'if_false': contents_if_false
        }
    )
    counter +=1


col = st.columns([1, 1, 5])

with col[0]:

    if st.button("Add", key=f'button_add_{counter}'):

        st.session_state['number_of_lines'] = st.session_state['number_of_lines'] + 1
        st.rerun()

with col[1]:
    
    if st.button("Reset", key=f'button_reset_{counter}'):
    
        del st.session_state['number_of_lines']
        del st.session_state['session_input_data']
        del st.session_state['context']
        del st.session_state['decision_tree']
        del st.session_state['var_0']
        del st.session_state['operation_0']
        del st.session_state['parameter_type_0']
        del st.session_state['parameter_value_0']
        del st.session_state['node_name_0']
        del st.session_state['contents_if_true_0']
        del st.session_state['contents_if_false_0']
        del (input_data, context_name, tree_name, variable_name, operation, 
             parameter_type, parameter_value, node_name, contents_if_true, 
             contents_if_false)
        st.cache_data.clear()
        st.rerun()


########################
######## Graph #########
########################

# build_graph(input_data)

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
        agraph(
            nodes=nodes, 
            edges=edges,
            config=config
        )

########################
########################
########################


########################
###### JSON DATA #######
########################

# Exibe os valores selecionados (opcional)

# st.write("Valores Selecionados:")
# st.json(input_data)



########################
######### API ##########
########################


if st.button("Create decision tree", key='create_decision_tree'):
    
    create_tree(input_data)
