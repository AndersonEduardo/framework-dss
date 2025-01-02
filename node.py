import copy
import re


class Node:

    def __init__(self, name:str, rules:list):
    
        self.name = name.strip().lower()
        self.root = None
        self.rules = rules


    def _get_stretched_rule(self, rule):

        if ' not in ' in rule:

            raise Exception('RULE SYNTAX ERROR: the logical operand `not` is only admitted at the beginning of the rule.')

        else:

            if ' in ' in rule:

                split_tag = ' in '

            else:

                return rule

        rule_splited = rule.split(split_tag)
        first_part = rule_splited[0]

        if first_part.strip().startswith('not '):

            negation_tag = 'not ('

            first_part = first_part.replace(negation_tag, '')

        else:

            negation_tag = ''

        if rule_splited[1].endswith(')'):

            second_part = rule_splited[1].replace(rule_splited[1][-1], '')
            rule_closing_guarantee = ')'

        else:

            second_part = rule_splited[1]
            rule_closing_guarantee = ''

        if ',' in first_part:

            query_parameters = eval(first_part).split(',')
            rule_stretched = ' ' + negation_tag + '(' + ' or '.join([f'"{p.strip()}"' + split_tag + second_part for p in query_parameters]) + ')' + rule_closing_guarantee

            return rule_stretched

        else:

            return rule


    def get_stretched_rule(self, rule):

        rulex_split = re.split(r'or|and', rule)
        rule_dict = dict()
        rule_parsed = None

        for rule_i in rulex_split:

            rule_dict[rule_i] = self._get_stretched_rule(rule_i)


        for k in rule_dict.keys():

            if rule_parsed is None:

                rule_parsed = rule.replace(k, rule_dict.get(k))
            
            else:

                rule_parsed = rule_parsed.replace(k, rule_dict.get(k))

        return rule_parsed


    def _rule_parser(self, query_parameters):

        rules = copy.deepcopy(self.rules)

        print('\n\t*Node name:', str(self.name).upper())
        print('\t*Node rule:', self.rules[0][0])
        print('\t\tIf True: go to', '&'.join([x.upper() if 'output:' not in x.lower() else x for x in  str(self.rules[0][1]).split('&')]))
        print('\t\tIf False: go to', '&'.join([x.upper() if 'output:' not in x.lower() else x for x in  str(self.rules[0][2]).split('&')]))

        output = list()

        for i in range(len(rules)):

            for (k,v) in query_parameters.items():

                if isinstance(v, str):

                    v = f'"{v}"'

                if k.strip().lower() in rules[i][0]:

                    rules[i][0] = rules[i][0]\
                        .replace('variable:' + k, str(v).strip().lower())

            logical_expression = rules[i][0].strip().lower().replace('  ', ' ')
            # logical_expression = ' and '.join(['(' + x.strip() + ')' for x in logical_expression.split('and')])
            logical_expression_eval_list = list()
            logical_expression_output_for_true = rules[i][1].lower().replace('  ', ' ')
            logical_expression_output_for_false = rules[i][2].lower().replace('  ', ' ')

            if 'not in' in logical_expression:

                raise Exception('RULE SYNTAX ERROR: the logical operand `not` is only admitted at the beginning of the rule.')
            
            if logical_expression.strip().lower().startswith('not '):

                negation_tag = True
            
            else:

                negation_tag = False


            for argument in logical_expression.split(' or '):

                if ('variable:' in argument):

                    logical_expression_eval_list.append(

                        None

                    )

                    print('\t*Parsed rule:', argument, '-->', None)

                else:

                    argument = argument.strip().lower()\
                        .replace('not (', '')\
                        .replace('not(', '')


                    if argument.strip().lower().startswith('('):

                        argument = argument.replace('(', '', 1)


                    if argument.strip().endswith(')'):

                        argument = argument.strip().rsplit(')', 1)[0]

                    argument_streched = self.get_stretched_rule(argument)

                    argument_streched_output = eval(argument_streched)

                    print('\t*Parsed rule:', argument_streched, '-->', argument_streched_output)

                    logical_expression_eval_list.append(argument_streched_output)

            logical_expression_eval_bool = any(logical_expression_eval_list)

            logical_expression_eval_bool = logical_expression_eval_bool if negation_tag is False else not logical_expression_eval_bool

            output.append(
                (logical_expression_eval_bool, logical_expression_output_for_true, logical_expression_output_for_false)
            )

        return output


    def eval_rule(self, query_parameters:dict):

        parsed_rules = self._rule_parser(query_parameters)
        output = list()

        for (rule, next_step_name_for_true, next_step_name_for_false) in parsed_rules:

            if rule is True:

                output.append(next_step_name_for_true)


        if len(output) > 1:

            raise Exception(f'The rules for each decision step must be mutually exclusive.')

        elif len(output) == 1:

            return next_step_name_for_true

        else:

            return next_step_name_for_false
