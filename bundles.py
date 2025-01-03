import os
import copy
import pickle
import datetime as dt
import pandas as pd

from io import BytesIO
from dotenv import load_dotenv

from awss3 import AwsS3 as aws
from parameters import *

load_dotenv()


class Bundles:

    def __init__(self):

        self.excel_filepath = None
        # self.bundles = dict()
        self.bundles = self.__set_bundles()
        self.__bucket = self.__set_bucket()
        self.__filename = self.__set_filename()
        self.__filename_backup = self.__set_filename_backup()
        self.__parameters = None
        self.__default_context = self.__set_default_context()


    def __set_bundles(self):

        # if os.path.exists(PERSISTENCE_BUNDLE_FILEPATH):

        #     with open(PERSISTENCE_BUNDLE_FILEPATH, 'rb') as f:

        #         bundles = pickle.load(f)

        # else:

        #     bundles = dict()

        # return bundles

        return dict()


    def __set_bucket(self):
        
        return S3_BUCKET


    def __set_filename(self):

        return  PERSISTENCE_BUNDLE_FILEPATH


    def __set_filename_backup(self):

        return  PERSISTENCE_BUNDLE_BACKUP_FILEPATH


    def __set_default_context(self):

        return DEFAULT_CONTEXT


    def __get_parameter_names(self):

        if self.excel_filepath is None:

            return None


        xl = pd.ExcelFile(self.excel_filepath)

        sheet_name = [x for x in xl.sheet_names if x.strip().upper() == 'BUNDLES']

        if len(sheet_name) != 1:

            raise Exception('It is mandatory a (unique) sheet named "BUNDLES". See documentation.')

        sheet_bundles = pd.read_excel(xl, sheet_name[0])

        sheet_bundles.columns = [x.strip().upper() for x in sheet_bundles.columns]

        parameter_names = sheet_bundles['PARAMETER'].to_list()


        return [x.strip().lower() for x in parameter_names]



    def get_bundles_list(self):
        
        return self.bundles


    def input_parser(self, name:str, data:str):

        if not isinstance(name, str):

            raise TypeError('The parameter "name" must be a Python str.')

        if not isinstance(data, str):

            raise TypeError('The parameter "data" must be a Python str.')


        name = name.strip().lower().replace("  ", " ").replace("  ", " ")
        data = data.strip().lower().replace("  ", " ").replace("  ", " ")


        parsed_bundle = dict()

        parsed_bundle[name] = f'"{data}"'

        return parsed_bundle


    def append(self, context:str, bundle:dict, **kwargs):

        if not isinstance(bundle, dict):

            raise TypeError('The parameter "bundle" must be a Python dict.')

        if context is not None and not isinstance(context, str):

            raise TypeError('The parameter "context" must be a Python str.')


        context = self.__default_context if context is None else context.strip().lower()
        offline = kwargs.get('offline')


        if not isinstance(offline, bool) and offline is not None:

            raise TypeError('The parameter "offline" must be None, True, or False.')


        self.__append_bundle(context=context, bundle=bundle, offline=offline)


    def _update(self, context:str, bundle, **kwargs):

        if not isinstance(bundle, dict):

            raise TypeError('The parameter "bundle" must be a Python dict.')

        if context is not None and not isinstance(context, str):

            raise TypeError('The parameter "context" must be a Python str.')

        context = self.__default_context if context is None else context.strip().lower()
        offline = kwargs.get('offline')


        if not isinstance(offline, bool) and offline is not None:

            raise TypeError('The parameter "offline" must be None, True, or False.')


        if self.bundles.get(context) is None:

            raise Exception(f'Bundle context "{context}" not found.')
        
        else:

            # self.__bundle_update(context=context, bundle=bundle)
            self.bundles[context].update(bundle)


        if offline is False or offline is None:

            self.export_to_s3()

        # else:

        #     with open(PERSISTENCE_BUNDLE_FILEPATH, 'wb') as f:

        #         pickle.dump(self.bundles, f)


    def __append_bundle(self, context:str, bundle:dict, **kwargs):

        context = str(context).strip().lower()
        offline = kwargs.get('offline')

        if (not isinstance(offline, bool)) and (offline is not None):

            raise TypeError('The parameter "offline" must be None, True, or False.')


        # if self.bundles.get(context) is None and context != self.__default_context:

        #     raise Exception(f'Bundle context "{context}" not found.')
        
        # else:

        if self.bundles.get(context) is None:

            self.bundles.update({context: bundle})
        
        else:

            self.bundles[context].update(bundle)


        if (offline is False) or (offline is None):

            self.export_to_s3()

        # else:

        #     with open(PERSISTENCE_BUNDLE_FILEPATH, 'wb') as f:

        #         pickle.dump(self.bundles, f)


    def delete(self, context:str, name:str, **kwargs):

        if context is not None and not isinstance(context, str):

            raise TypeError('The parameter "context" must be a Python str.')

        if name is not None and not isinstance(name, str):

            raise TypeError('The parameter "context" must be a Python str.')


        context = self.__default_context if context is None else context.strip().lower()
        name = name.strip().lower()


        delete_all = kwargs.get('all')
        offline = kwargs.get('offline')

        if not isinstance(delete_all, bool) and delete_all is not None:

            raise TypeError('The parameter "delete_all" must be a python bool (i.e., either True or False).')

        if not isinstance(offline, bool) and offline is not None:

            raise TypeError('The parameter "offline" must be a Python bool (i.e., either True or False).')


        if delete_all is False:

            if self.bundles.get(context) is None:

                raise Exception(f'Bundle context "{context}" not found.')
            
            else:

                self.bundles[context].pop(name)
        
        elif delete_all is True:
        
            self.bundles = dict()

        else:

            raise TypeError('The "all" parameter must be a Python bool (i.e., either True or False).')


        if offline is False or offline is None:

            self.export_to_s3()


    def get(self, name:str):

        return self.bundles.get(name)


    def bundle_injection(self, context:str, rule:str):

        if not isinstance(context, str):

            raise TypeError('The parameter "context" must be a Python str.')

        if not isinstance(rule, str):

            raise TypeError('The parameter "rule" must be a Python str.')

        if 'bundles' in rule.lower():

            raise Exception('Found `bundles` intead of `bundle` in the node rule.')

        # if any([x.lower().count('bundle:') > 1 for x in rule.split(';')]):

        #     print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] Exception in `rule` found:", rule)

        #     raise Exception('Only one `bundle` statement is allowed for each rule part.')

        if 'bundle' not in rule.lower():

            return rule

        else:

            context = context.strip().lower()

            if self.bundles.get(context) is None:

                raise Exception(f'Bundle context "{context}" not found.')

            rule_raw = rule

            rule = \
                rule.strip().lower().replace('  ', ' ').replace('  ', ' ')

            rule = [x for x in rule.split(' ') if 'bundle:' in x]

            rule = ' '.join([x.split(':')[-1] for x in rule])

            for bundle_context in self.bundles.keys():
                for bundle_name in self.bundles[bundle_context].keys():

                    # print(bundle_context, bundle_name)

                    if bundle_context == context and bundle_name in rule:

                        rule_raw = rule_raw\
                            .replace(f'bundle:{bundle_name}', self.bundles[context][bundle_name])

            return rule_raw


    def s3_file_exists(self):

        try:

            aws.load_from_s3(self.__bucket, self.__filename)

            print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}] ...Bundles source file found and successfully loaded...')

            return True
        
        except:

            print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}] WARNING! Not able to load the Bundles source file.')

            return False


    def s3_backup_exists(self):

        try:

            aws.load_from_s3(self.__bucket, self.__filename_backup)

            return True
        
        except:

            return False


    def export_to_s3(self):

        if self.s3_file_exists():

            if self.s3_backup_exists():

                aws.delete_on_s3(self.__bucket, self.__filename_backup)

            new_backup = aws.load_from_s3(self.__bucket, self.__filename)

            aws.save_on_s3(new_backup, self.__bucket, self.__filename_backup)

        else:

            pass

        aws.save_on_s3(obj=self.bundles, bucket=self.__bucket, file_name=self.__filename)

    
    def load_backup_from_s3(self):

        # a arvore mais atual está no __file_name - a __filename_backup é
        # a "penultima", ou seja, é um backup de emergencia, de fato.
        if self.s3_file_exists():

            bundles_from_backup = aws.load_from_s3(self.__bucket, self.__filename)

            # self.bundles.update(bundles_from_backup)
            self.bundles = bundles_from_backup

        else:

            return None


    def _load_from_excel(self, excel_filepath:str = None, **kwargs):

        if excel_filepath is None:

            raise ValueError('The parameter "excel_filepath" is mandatory.')
        
        else:

            self.excel_filepath = excel_filepath


        offline = kwargs.get('offline')
        offline = None if offline is None else offline

        if not isinstance(offline, bool) and offline is not None:

            raise TypeError('The parameter "offline" must be a Python bool (i.e., either True or False).')


        self.__parameters = self.__get_parameter_names()

        xl = pd.ExcelFile(self.excel_filepath)

        sheet_names = [x for x in xl.sheet_names if x.strip().upper() not in RESERVED_SHEETS]

        output = dict()

        for sheet_name in sheet_names:

            df = pd.read_excel(xl, sheet_name)

            column_names = [x.strip().lower() for x in df.columns]

            df.columns = column_names

            for column_name in column_names:

                if column_name in self.__parameters:

                    values = df[column_name].dropna().to_list().copy()
                    values = [str(x).replace(';', SEMICOLON).replace('\n', INNERLINEBREAK).strip().lower() 
                              for x in values].copy()

                    if len(values) > 0:

                        bundle_name = sheet_name.strip().lower().replace(' ', '-') + '-' + column_name.replace(' ', '-')

                        bundle_values = '"' + LINEBREAK.join(values) + '"' # juntando as linhas da coluna do excel

                        bundle_parsed = {bundle_name: bundle_values}

                        output.update(bundle_parsed)  # TODO: implementar verificação de nomes duplicados


        sheet_name_for_context_parameter = [x for x in xl.sheet_names if 'TREE' in x.strip().upper()]

        if len(sheet_name_for_context_parameter) != 1:

            raise Exception('Inconsistency found in sheet names: a (unique) sheet named "TREE" is mandatory.')
        
        else:

            sheet_name_for_context_parameter = sheet_name_for_context_parameter[0]

        sheet_tree_config = pd.read_excel(xl, sheet_name_for_context_parameter)
        sheet_tree_config.columns = [x.strip().lower() for x in sheet_tree_config]
        context = sheet_tree_config['context'].dropna().to_list()


        if len(context) > 1:

            raise Exception('Only one value for the parameter "context" is allowed.')
        
        elif len(context) == 0:

            context = None
        
        else:

            context = str(context[0]).strip().lower()

        context = None if context is None else (None if context == 'none' else context)

        # self._update(context=context, bundle=output, offline=offline)
        self.append(context=context, bundle=output, offline=offline)
