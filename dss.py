import os
import copy
import pickle
import datetime as dt
from dotenv import load_dotenv
import pandas as pd
# from datetime import datetime
from decisiontree import *
from parameters import *
from awss3 import AwsS3 as aws

load_dotenv()


class DecisionSupportSystem:

    def __init__(self):

        self.decision_tree_list = list()
        self.__bucket = self.__set_bucket()
        self.__filename = self.__set_filename()
        self.__filename_backup = self.__set_filename_backup()
        self.__default_context = self.__set_default_context()


    def __set_filename(self):

        return  PERSISTENCE_FILEPATH


    def __set_filename_backup(self):

        return PERSISTENCE_BACKUP_FILEPATH


    def __set_bucket(self):
        
        return S3_BUCKET


    def __set_default_context(self):

        return DEFAULT_CONTEXT


    def __check_existence(self, tree_name:str, node_name:str = None, context:str = None):

        context = self.__default_context if context is None else context.strip().lower()
        tree_name = tree_name.strip().lower()
        node_name = None if node_name is None else node_name.strip().lower()

        for item in self.decision_tree_list:

            if item['context'] == context.strip().lower() and\
               item['tree'].name == tree_name.strip().lower():

                if node_name is None:
                    
                    return True

                else:

                    if node_name in [x['node_name'].strip().lower() for x in item['tree'].get_node_list()]:

                        return True

        return False


    def build_decision_tree(self, name:str, target_field:str, context:str = None, **kwargs):


        if not isinstance(name, str):

            raise TypeError('The parameter "name" must be a Python str.')

        if not isinstance(target_field, str):

            raise TypeError('The parameter "target_field" must be a Python str.')

        if (context is not None) and not isinstance(context, str):

            raise TypeError('The parameter "context" must be a Python str.')


        context = self.__default_context if context is None else str(context).strip().lower()
        name = name.strip().lower()
        target_field = target_field.strip().lower()

        offline = kwargs.get('offline')
        offline = False if offline is None else offline

        if not isinstance(offline, bool):

            raise TypeError('The parameter "offline" must be a Python bool (i.e., either True or False).')

        force = kwargs.get('force')
        force = False if force is None else force

        if not isinstance(force, bool):

            raise TypeError('The parameter "force" must be a Python bool (i.e., either True or False).')


        pre_existence_check = self.__check_existence(
            context = context, 
            tree_name = name
        )

        if pre_existence_check is True and force is False:

            raise Exception(f'A Tree named {name} (context {context}) already exists (in order to force the creation, consider the parameter force=True).')

        else:

            self.delete_tree(
                context = context,
                decision_tree_name = name,
                offline = offline,
                silence = True
            )

            dt = DecisionTree(name, target_field)

            self.decision_tree_list.append({'context':context, 'tree':dt})


            if offline is True:

                pass
            
            elif offline is False or offline is None:

                self._save()

            else:

                raise ValueError('The offline special parameter must be either True or False.')


    def rule_parser(self, context:str, user_input:str, **kwargs):
        '''Processa input do usuário para a regras dos nós.'''

        if not isinstance(context, str):

            raise TypeError('The parameter "context" must be a Python str.')

        if not isinstance(user_input, str):

            raise TypeError('The parameter "user_input" must be a Python str.')


        if (' and ' in user_input.lower()) and (' or ' in user_input.lower()):

            raise Exception('Too complex node rule detected. Consider break up you rule into more than one tree node.')

        bundles = kwargs.get('bundles')

        if bundles is not None:

            user_input = bundles.bundle_injection(context=context, rule=user_input)

        user_input = user_input\
            .replace(': ', ':')\
            .replace(' :', ':')\
            .replace('  ', ' ')
        user_input = [x.split(';') for x in user_input.strip().lower().split('|')]

        parsed_rule = [[x.strip() for x in y] for y in user_input]
        parsed_rule = [[x.replace(' true', ' "true"') for x in y] for y in parsed_rule]
        parsed_rule = [[x.replace(' false', ' "false"') for x in y] for y in parsed_rule]
        parsed_rule = [[x.replace('=true', ' "true"') for x in y] for y in parsed_rule]
        parsed_rule = [[x.replace('=false', ' "false"') for x in y] for y in parsed_rule]


        return parsed_rule


    def add_tree_node(self, context:str, decision_tree_name:str, node_name:str, 
                      node_rules:str, **kwargs):

        if context is not None and not isinstance(context, str):

            raise TypeError('The parameter "context" must be a Python str.')

        if not isinstance(decision_tree_name, str):

            raise TypeError('The parameter "decision_tree_name" must be a Python str.')

        if not isinstance(node_name, str):

            raise TypeError('The parameter "node_name" must be a Python str.')

        if not isinstance(node_rules, str):

            raise TypeError('The parameter "node_rules" must be a Python str.')


        if context is not None and context.strip().lower() == 'none':

            raise Exception('The name "nano" (as a string) is not allowed.')

        bundles = kwargs.get('bundles')

        context = self.__default_context if context is None else context.strip().lower()
        decision_tree_name = decision_tree_name.strip().lower()
        node_name = node_name.strip().lower()

        force = kwargs.get('force')
        force = False if force is None else force

        if not isinstance(force, bool):

            raise TypeError('The parameter "force" must be a Python bool (i.e., either True or False).')

        offline = kwargs.get('offline')
        offline = False if offline is None else offline

        if not isinstance(offline, bool):

            raise TypeError('The parameter "offline" must be a Python bool (i.e., either True or False).')


        found = False

        for item in self.decision_tree_list:

            if item['context'] == context and\
               item['tree'].name.strip().lower() == decision_tree_name:
                
                pre_existence_check = self.__check_existence(
                    context = context,
                    tree_name = decision_tree_name, 
                    node_name = node_name
                )

                if pre_existence_check is True and force is False:

                    raise Exception(f'A Node named {node_name} already exists for the Tree {decision_tree_name} (context {context}) (in order to force the creation, consider the parameter force=True).')

                else:

                    self.delete_node(
                        context = context,
                        decision_tree_name = decision_tree_name,
                        node_name = node_name,
                        offline = offline
                    )

                    node_rules = self.rule_parser(context=context, user_input=node_rules, bundles=bundles)
                    node_new = Node(node_name, node_rules)

                    item['tree'].add(node_new)

                    found = True


        if found is False:

            raise Exception(f'Tree {decision_tree_name} (context {context}) not found.')


        if offline is True:

            pass
        
        elif offline is False or offline is None:

            self._save()

        else:

            raise ValueError('The offline special parameter must be either True or False.')


    def rooting(self, context:str, decision_tree_name:str):

        context = self.__default_context if context is None else context.strip().lower()

        for item in self.decision_tree_list:

            if item['context'] == context.strip().lower() and\
               item['tree'].name.strip().lower() == decision_tree_name.strip().lower():
            
                item['tree'].rooting()


    def query(self, context:str, decision_tree_name:str, user_input:dict):

        context = self.__default_context if context is None else context.strip().lower()

        found = False

        for item in self.decision_tree_list:

            if item['context'] == context.strip().lower() and\
               item['tree'].name.strip().lower() == decision_tree_name.strip().lower():
                
                found = True

                return item['tree'].query(user_input)
            
        if found is False:

            raise Exception(f'Tree "{decision_tree_name}" or context "{context}" not found.')
        
        else:

            raise Exception('Some inconsistency found at DecisionSupportSystem.query')


    def delete_node(self, context:str, decision_tree_name:str, node_name:str, **kwargs):

        context = self.__default_context if context is None else context.strip().lower()

        found = False

        for item in self.decision_tree_list:

            if item['context'] == context.strip().lower() and\
               item['tree'].name.strip().lower() == decision_tree_name.strip().lower():

                item['tree'].delete_node(node_name.strip().lower())

                found = True

        if found is False:

            raise Exception(f'Node {node_name} (at Tree {decision_tree_name}, context {context}) not found.')

        offline = kwargs.get('offline')

        if offline is True:

            pass
        
        elif offline is False or offline is None:

            self._save()

        else:

            raise ValueError('The offline special parameter must be either True or False.')


    def delete_tree(self, context:str, decision_tree_name:str, **kwargs):

        context = self.__default_context if context is None else context.strip().lower()
        decision_tree_name = decision_tree_name.strip().lower()

        silence = kwargs.get('silence')
        silence = False if silence is None else silence

        if not isinstance(silence, bool):

            raise TypeError('The parameter "silence" must be a Python bool (i.e., either True or False).')

        offline = kwargs.get('offline')
        offline = False if offline is None else offline

        if not isinstance(offline, bool):

            raise TypeError('The parameter "offline" must be a Python bool (i.e., either True or False).')

        found = False

        idx_for_pop = list()

        for i in range(len(self.decision_tree_list)):

            if self.decision_tree_list[i]['context'] == context and\
               self.decision_tree_list[i]['tree'].name.strip().lower() == decision_tree_name:

                idx_for_pop.append(i)

                found = True

        for idx in idx_for_pop:

            self.decision_tree_list.pop(idx)

        if found is False and silence is False:

            raise Exception(f'Tree {decision_tree_name} (context {context}) not found.')

        if offline is True:

            return None
        
        elif offline is False or offline is None:

            self._save()

        else:

            raise ValueError('The offline special parameter must be either True or False.')


    def get_tree_list(self, context:str = None):

        if context is None:

            context = self.__default_context

        elif context.strip().lower() == 'all':

            context = None

        else:

            context = context.strip().lower()


        if context is None:

            return [
                {'id':id, 'context':item['context'], 'tree_name':item['tree'].name, 'target_field':item['tree'].target_field} \
                for (id, item) in enumerate(self.decision_tree_list)
            ]
        
        else:

            return [
                {'id':id, 'context':item['context'], 'tree_name':item['tree'].name, 'target_field':item['tree'].target_field} \
                for (id, item) in enumerate(self.decision_tree_list) if item['context'] == context.strip().lower()
            ]


    def get_node_list(self, context:str, decision_tree_name:str):

        context = self.__default_context if context is None else context.strip().lower()

        for item in self.decision_tree_list:

            if item['context'] == context.strip().lower() and\
               item['tree'].name.strip().lower() == decision_tree_name.strip().lower():

                return item['tree'].get_node_list()


    def get_rule_list(self, context:str, decision_tree_name:str):

        context = self.__default_context if context is None else context.strip().lower()

        for item in self.decision_tree_list:

            if item['context'] == context.strip().lower() and\
               item['tree'].name.strip().lower() == decision_tree_name.strip().lower():
    
                return item['tree'].get_rule_list()


    def update_rule(self, context:str, new_rule:str, decision_tree_name:str, node_name:str, **kwargs):

        if not isinstance(context, str) and context is not None:

            raise TypeError('The parameter "context" must be a Python str.')

        if not isinstance(new_rule, str):

            raise TypeError('The parameter "new_rule" must be a Python str.')

        if not isinstance(decision_tree_name, str):

            raise TypeError('The parameter "decision_tree_name" must be a Python str.')

        if not isinstance(node_name, str):

            raise TypeError('The parameter "node_name" must be a Python str.')


        bundles = kwargs.get('bundles')

        context = self.__default_context if context is None else context.strip().lower()

        offline = kwargs.get('offline')

        for item in self.decision_tree_list:

            if item['context'] == context.strip().lower() and\
               item['tree'].name.strip().lower() == decision_tree_name.strip().lower():

                for i in range(len(item['tree'].node_list)):

                    if item['tree'].node_list[i].name.strip().lower() == node_name.strip().lower():

                        new_rule = self.rule_parser(context=context, user_input=new_rule, bundles=bundles)
                        item['tree'].node_list[i].rules = new_rule


                        if offline is True:

                            pass
                        
                        elif offline is False or offline is None:

                            self._save()

                        else:

                            raise ValueError('The offline special parameter must be either True or False.')


                        return None

        raise Exception('Decision Tree or Node not found.')


    def s3_file_exists(self):

        try:

            aws.load_from_s3(self.__bucket, self.__filename)

            print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}] ...DSS source file found and successfully loaded...')

            return True
        
        except:

            print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}] WARNING! Not able to load the DSS source file.')

            return False


    def s3_backup_exists(self):

        try:

            aws.load_from_s3(self.__bucket, self.__filename_backup)

            return True
        
        except:

            return False


    def _save(self):

        # TODO: ideia: salvar modificações do dia no diretório local. No
        # fim do dia (e.g., meia noite), rodar um processo que faz o
        # update no S3.

        if self.s3_file_exists():

            if self.s3_backup_exists():
 
                aws.delete_on_s3(self.__bucket, self.__filename_backup)
            
            new_backup = aws.load_from_s3(self.__bucket, self.__filename)

            aws.save_on_s3(new_backup, self.__bucket, self.__filename_backup)

        else:

            pass

        aws.save_on_s3(obj=self.decision_tree_list, bucket=self.__bucket, file_name=self.__filename)


    @classmethod
    def _clean_persistence_files(cls):

        cls.__clean_persistence_files_on_s3()


    def __clean_persistence_files_on_s3(self):
        
        aws.delete_on_s3(self.__bucket, self.__filename)
        aws.delete_on_s3(self.__bucket, self.__filename_backup)


    def load_backup_from_s3(self):

        # a arvore mais atual está no __file_name. A __filename_backup é
        # a "penultima", ou seja, é um backup de emergencia, de fato.
        if self.s3_file_exists():

            trees_from_backup = aws.load_from_s3(self.__bucket, self.__filename)

            self.decision_tree_list.extend(trees_from_backup)

        else:

            # print('\n load_backup_from_s3: RETORNANDO O SELF')

            return None


    def _build_tree_from_excel(self, context:str, excel_filepath:str = None, **kwargs):

        if context is not None and context.strip().lower() == 'none':

            raise Exception('The name "none" (as a string) is not allowed.')

        bundles = kwargs.get('bundles')

        if 'FileStorage'.lower() in str(type(excel_filepath)).lower():

            pass

        else:

            if excel_filepath is None or not os.path.exists(excel_filepath):

                raise FileNotFoundError(f'File {excel_filepath} not found.')
            
            else:

                pass


        xl = pd.ExcelFile(excel_filepath)


        sheet_name_for_config = [x for x in xl.sheet_names if 'TREE' in x.strip().upper()]

        if len(sheet_name_for_config) != 1:

            raise Exception('Inconsistency found in sheet names: a unique sheet named "TREE" is mandatory.')
        
        else:

            sheet_name_for_config = sheet_name_for_config[0]


        parameters_table = pd.read_excel(xl, sheet_name_for_config)

        parameters_table.columns = [x.strip().upper() for x in parameters_table.columns]

        if not all([x in SHEET_TREE_COLUMNS for x in parameters_table.columns]):

            raise Exception(f'The sheet "TREE" must be the following columns (mandatory): { ", ".join(SHEET_TREE_COLUMNS)}.')


        ## context ##
        context = parameters_table['CONTEXT'].dropna().to_list()

        if len(context) > 1:

            raise Exception('Only one value for the parameter "context" is allowed.')
        
        elif len(context) == 0:

            context = None
        
        else:
            
            context = str(context[0]).strip().lower()
            context = None if context is None else (None if context == 'none' else context)

        ## decision tree name ##
        decision_tree_name = parameters_table['TREE'].dropna().to_list()

        if len(decision_tree_name) > 1:

            raise ValueError('Only one tree name is allowed.')
        
        elif len(decision_tree_name) == 0:

            raise ValueError('Tree name not found.')

        else:

            decision_tree_name = decision_tree_name[0].strip().lower()

        if not isinstance(decision_tree_name, str) and not isinstance(decision_tree_name, int):

            raise TypeError('The field "TREE" at the excel sheet "TREE" must be either a python int or a python str.')


        ## target field ##
        target = parameters_table['TARGET'].dropna().to_list()

        if len(target) > 1:

            raise ValueError('Only one tree name is allowed.')
        
        elif len(target) == 0:

            raise ValueError('Target name not found.')

        else:

            target = target[0].strip().lower()

        if not isinstance(target, str) and not isinstance(target, int):

            raise TypeError('The field "target" at the excel sheet "TREE" must be either a python int or a python str.')
        

        ## tree nodes ##
        nodes = [x.strip().lower() for x in parameters_table['NODE'].dropna().to_list()]

        if len(nodes) == 0:

            raise ValueError('Node names not found.')
        

        ## tree rules ##
        rules = [x.strip().lower() for x in parameters_table['RULE'].dropna().to_list()]

        if len(rules) == 0:

            raise ValueError('Node names not found.')
        
        if len(nodes) != len(rules):

            raise Exception('The number of node names and node rules should be the same.')

    
        ## outputs ##
        outputs_true = parameters_table['TRUE'].dropna().to_list()
        outputs_false = parameters_table['FALSE'].dropna().to_list()

        if len(outputs_true) == 0 or len(outputs_false) == 0:

            raise ValueError('Values for TRUE or FALSE were not found.')

        if len(outputs_true) != len(rules) or len(outputs_false) != len(rules):

            raise Exception('The number of values for columns TRUE and FALSE should be equal to the number of node rules.')


        ## offline ##
        # user_choice = kwargs.get('offline')


        ## force the overwriting of a tree (with the same name) ##
        force = kwargs.get('force')
        force = False if force is None else force

        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] Tree context (and data type):", context, type(context))

        # building the new tree
        self.build_decision_tree(
            context = context,
            name = decision_tree_name,
            target_field = target,
            offline = True, #user_choice,  # deixando True pois tudo será atualizado no S3 no _save mais abaixo.
            force = force
        )

        new_decision_tree = [
            decision_tree 
            for decision_tree in self.decision_tree_list
            if (decision_tree['context'] == context) and (decision_tree['tree'].name == decision_tree_name)
        ][0]

        ## add the rules ##
        for (node, rule,  output_true, output_false) in zip(nodes, rules, outputs_true, outputs_false):

            node_name = node.strip().lower()
            node_rules = f'{rule}; {output_true}; {output_false}'
            context = self.__default_context if context is None else context.strip().lower()

            pre_existence_check = self.__check_existence(
                    context = context,
                    tree_name = decision_tree_name, 
                    node_name = node_name
                )

            if pre_existence_check is True and force is False:

                raise Exception(f'A Node named {node_name} already exists for the Tree \
                                {decision_tree_name} (context {context}) (in order to \
                                force the creation, consider the parameter force=True).')

            else:

                node_rules = self.rule_parser(context=context, user_input=node_rules, bundles=bundles)
                node_new = Node(node_name, node_rules)

                new_decision_tree['tree'].add(node_new)


        if len(new_decision_tree['tree'].node_list) > 0:

            self.rooting(context = context, decision_tree_name = decision_tree_name)

            self._save()

        else:

            raise Exception(f'Tree {decision_tree_name} (context {context}) have no nodes.')
