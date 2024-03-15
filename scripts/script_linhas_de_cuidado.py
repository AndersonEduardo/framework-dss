import requests

########################################################################
print(f'[STATUS SCRIPT] Deleting previous test tree...')
requests.delete('http://localhost:5000/delete-tree', json={"decision-tree-name": "linhas-de-cuidado"})
print(f'[STATUS SCRIPT] ...done')

print(f'[STATUS SCRIPT] Creating new test tree...')
requests.post('http://localhost:5000/create-decision-tree', json={"name": "linhas-de-cuidado", "target-field": "linhas-de-cuidado-XPTO"})
print(f'[STATUS SCRIPT] ...done')
########################################################################



# URL #
api_url = 'http://localhost:5000/' 
#######



########################################################################
######################### BUNDLES ######################################
########################################################################



## Hipertensão ##
# CIAP hipertensão
bundle_ciap_hipertensao = {
    "bundle-name": "ciap-hipertensão",
    "bundle-values": "K86, K87"
}
r = requests.post(api_url + 'bundles', json = bundle_ciap_hipertensao)
print(f'[STATUS SCRIPT] Bundle {bundle_ciap_hipertensao} finished with status: {r.status_code}')

# CID hipertensão
bundle_cid_hipertensao = {
    "bundle-name": "cid-hipertensão",
    "bundle-values": "I10, I15, I11, I12, I13"
}
r = requests.post(api_url + 'bundles', json = bundle_cid_hipertensao)
print(f'[STATUS SCRIPT] Bundle {bundle_cid_hipertensao} finished with status: {r.status_code}')

# CIPE hipertensão
bundle_cipe_hipertensao = {
    "bundle-name": "cipe-hipertensão",
    "bundle-values": "12.62, 12.63, 12.65"
}
r = requests.post(api_url + 'bundles', json = bundle_cipe_hipertensao)
print(f'[STATUS SCRIPT] Bundle {bundle_cipe_hipertensao} finished with status: {r.status_code}')



## Diabetes ##
# CIAP diabetes
bundle_ciap_diabetes = {
    "bundle-name": "ciap-diabetes",
    "bundle-values": "T89, T90"
}
r = requests.post(api_url + 'bundles', json = bundle_ciap_diabetes)
print(f'[STATUS SCRIPT] Bundle {bundle_ciap_diabetes} finished with status: {r.status_code}')

# CID diabetes
bundle_cid_diabetes = {
    "bundle-name": "cid-diabetes",
    "bundle-values": "E10, E11, E12, E13, E14"
}
r = requests.post(api_url + 'bundles', json = bundle_cid_diabetes)
print(f'[STATUS SCRIPT] Bundle {bundle_cid_diabetes} finished with status: {r.status_code}')

# CIPE diabetes
bundle_cipe_diabetes = {
    "bundle-name": "cipe-diabetes",
    "bundle-values": "15.7, 15.6, 10.52"
}
r = requests.post(api_url + 'bundles', json = bundle_cipe_diabetes)
print(f'[STATUS SCRIPT] Bundle {bundle_cipe_diabetes} finished with status: {r.status_code}')



## Obesidade ##
# CIAP obesidade
bundle_ciap_obesidade = {
    "bundle-name": "ciap-obesidade",
    "bundle-values": "T82, T83, T07"
}
r = requests.post(api_url + 'bundles', json = bundle_ciap_obesidade)
print(f'[STATUS SCRIPT] Bundle {bundle_ciap_obesidade} finished with status: {r.status_code}')



# CID Obesidade
bundle_cid_obesidade = {
    "bundle-name": "cid-obesidade",
    "bundle-values": "E66, E65, E67, E68"
}
r = requests.post(api_url + 'bundles', json = bundle_cid_obesidade)
print(f'[STATUS SCRIPT] Bundle {bundle_cid_obesidade} finished with status: {r.status_code}')

# CIPE Obesidade
bundle_cipe_obesidade = {
    "bundle-name": "cipe-obesidade",
    "bundle-values": "3.37"
}
r = requests.post(api_url + 'bundles', json = bundle_cipe_obesidade)
print(f'[STATUS SCRIPT] Bundle {bundle_cipe_obesidade} finished with status: {r.status_code}')



## Pré-Natal ##
# CIAP pré-natal
bundle_ciap_prenatal = {
    "bundle-name": "ciap-pre-natal",
    "bundle-values": 'W78, W79, W01, W29, W85'
}
r = requests.post(api_url + 'bundles', json = bundle_ciap_prenatal)
print(f'[STATUS SCRIPT] Bundle {bundle_ciap_prenatal} finished with status: {r.status_code}')

# CID pré-natal
bundle_cid_prenatal = {
    "bundle-name": "cid-pre-natal",
    "bundle-values": 'O30.0, O48, Z32.1, Z33, Z34, Z35, Z64.0, O24'
}
r = requests.post(api_url + 'bundles', json = bundle_cid_prenatal)
print(f'[STATUS SCRIPT] Bundle {bundle_cid_prenatal} finished with status: {r.status_code}')

# CIPE pré-natal
bundle_cipe_prenatal = {
    "bundle-name": "cipe-pre-natal",
    "bundle-values": '7.15, 7.16, 7.17, 7.18, 7.23, 7.25, 7.28, 7.3'
}
r = requests.post(api_url + 'bundles', json = bundle_cipe_prenatal)
print(f'[STATUS SCRIPT] Bundle {bundle_cipe_prenatal} finished with status: {r.status_code}')



## Saúde Mental ##
# CIAP saúde mental
bundle_ciap_saudemental = {
    "bundle-name": "ciap-saude-mental",
    "bundle-values": 'P15, P16, P18, P19, P28, P29, P70, P71, P72, P73, P74, P76, P77, P78, P79, P80, P81, P82, P85, P86, P98, P99'
}
r = requests.post(api_url + 'bundles', json = bundle_ciap_saudemental)
print(f'[STATUS SCRIPT] Bundle {bundle_ciap_saudemental} finished with status: {r.status_code}')

# CID saúde mental
bundle_cid_saudemental = {
    "bundle-name": "cid-saude-mental",
    "bundle-values": 'F00, F01, F02, F03, F04, F05, F06, F07, F09, F10, F11 , F12, F13, F14 , F15, F16, F17 , F18 , F19 , F20, F21,F22, F23, F24, F25, F28,F29,F30,F31 ,F32,F33,F34,F38,F39,F40,F41,F42,F43, F44, F45, F48, F50, F51, F53, F54, F55, F59, F60, F61, F62, F63, F64, F65, F66, F68, F69, F70, F71, F72, F73, F78, F79, F84, F88, F89, F90, F91, F92, F93, F94, F95, F98, F99'
}
r = requests.post(api_url + 'bundles', json = bundle_cid_saudemental)
print(f'[STATUS SCRIPT] Bundle {bundle_cid_saudemental} finished with status: {r.status_code}')

# CIPE saúde mental
bundle_cipe_saudemental = {
    "bundle-name": "cipe-saude-mental",
    "bundle-values": '21.2, 21.26, 21.14, 21.66'
}
r = requests.post(api_url + 'bundles', json = bundle_cipe_saudemental)
print(f'[STATUS SCRIPT] Bundle {bundle_cipe_saudemental} finished with status: {r.status_code}')

# PHQ-9 saúde mental
bundle_phq9_saudemental = {
    "bundle-name": "phq-9-saude-mental",
    "bundle-values": 'Transtorno Depressivo Leve, Transtorno Depressivo Moderado, Transtorno Depressivo Moderadamente Grave, Transtorno Depressivo Grave'
}
r = requests.post(api_url + 'bundles', json = bundle_phq9_saudemental)
print(f'[STATUS SCRIPT] Bundle {bundle_phq9_saudemental} finished with status: {r.status_code}')

# GAD-7 saúde mental
bundle_gad7_saudemental = {
    "bundle-name": "gad-7-saude-mental",
    "bundle-values": 'Ansiedade Leve, Ansiedade Moderada, Ansiedade Grave'
}
r = requests.post(api_url + 'bundles', json = bundle_gad7_saudemental)
print(f'[STATUS SCRIPT] Bundle {bundle_gad7_saudemental} finished with status: {r.status_code}')



########################################################################
###################### DECISION TREE ###################################
########################################################################



# pergunta 01 - Puericultura
# rule_puericultura = 'variable:idade < 2'
pergunta_01 = {
    "decision-tree-name": "linhas-de-cuidado",
    "node-name": "Pergunta 01",
    # "node-rule": f"{rule_puericultura}; output&pergunta 04:Puericultura | not ({rule_puericultura}); Pergunta 02",  # opcao 1
    "node-rule": f"variable:idade < 2; output&pergunta 04:Puericultura",  # opcao 2
    "default-next-node": "Pergunta 02"
}
r = requests.post(api_url + 'add-tree-node', json = pergunta_01)
print(f'[STATUS SCRIPT] Decision Tree node {pergunta_01.get("node-name")} finished with status: {r.status_code}')
if r.status_code != 200:
    raise Exception(f'Failed to create the Tree Node {pergunta_01.get("node-name")}')



# pergunta 02 - Saúde da Criança - Adolescente
pergunta_02 = {
    "decision-tree-name": "linhas-de-cuidado",
    "node-name": "pergunta 02",
    "node-rule": "variable:idade >= 2 and variable:idade < 19; output&pergunta 04:Saúde da Criança - Adolescente | variable:idade >= 19; Pergunta 03",
    "default-next-node": None
}
r = requests.post(api_url + 'add-tree-node', json = pergunta_02)
print(f'[STATUS SCRIPT] Decision Tree node {pergunta_02.get("node-name")} finished with status: {r.status_code}')
if r.status_code != 200:
    raise Exception(f'Failed to create the Tree Node {pergunta_02.get("node-name")}')



# pergunta 03 - Saúde do Homem ou Mulher Trans
pergunta_03 = {
    "decision-tree-name": "linhas-de-cuidado",
    "node-name": "pergunta 03",
    "node-rule": "variable:idade >= 19 and variable:sexo == 'masculino'; output&pergunta 04:Saúde do Homem ou Mulher Trans | variable:idade >= 19 and variable:sexo == 'feminino'; output&pergunta 04:Saúde da Mulher ou Homem Trans",
    "default-next-node": None
}
r = requests.post(api_url + 'add-tree-node', json = pergunta_03)
print(f'[STATUS SCRIPT] Decision Tree node {pergunta_03.get("node-name")} finished with status: {r.status_code}')
if r.status_code != 200:
    raise Exception(f'Failed to create the Tree Node {pergunta_03.get("node-name")}')



# pergunta 04 - Hipertensão
pergunta_04 = {
    "decision-tree-name": "linhas-de-cuidado",
    "node-name": "pergunta 04",
    # "node-rule": "variable:ciap in bundle:ciap-hipertensão or variablecid-10 in bundle:cid-hipertensão or variable:código in bundle:cipe-hipertensão; output&pergunta 05:Hipertensão | not (variable:ciap in bundle:ciap-hipertensão or variablecid-10 in bundle:cid-hipertensão or variable:código in bundle:cipe-hipertensão); Pergunta 05",
    "node-rule": "variable:ciap in bundle:ciap-hipertensão or variable:cid-10 in bundle:cid-hipertensão or variable:código in bundle:cipe-hipertensão; output&pergunta 05:Hipertensão",
    "default-next-node": "Pergunta 05"
}
r = requests.post(api_url + 'add-tree-node', json = pergunta_04)
print(f'[STATUS SCRIPT] Decision Tree node {pergunta_04.get("node-name")} finished with status: {r.status_code}')
if r.status_code != 200:
    raise Exception(f'Failed to create the Tree Node {pergunta_04.get("node-name")}')



# pergunta 05 - Diabetes
pergunta_05 = {
    "decision-tree-name": "linhas-de-cuidado",
    "node-name": "pergunta 05",
    "node-rule": "variable:ciap in bundle:ciap-diabetes or variable:cid-10 in bundle:cid-diabetes or variable:código in bundle:cipe-diabetes;output&Pergunta 06:Diabetes| not (variable:ciap in bundle:ciap-diabetes or variable:cid-10 in bundle:cid-diabetes or variable:código in bundle:cipe-diabetes); Pergunta 06",
    "default-next-node": None
}
r = requests.post(api_url + 'add-tree-node', json = pergunta_05)
print(f'[STATUS SCRIPT] Decision Tree node {pergunta_05.get("node-name")} finished with status: {r.status_code}')
if r.status_code != 200:
    raise Exception(f'Failed to create the Tree Node {pergunta_05.get("node-name")}')

# pergunta 06 - Diabetes
pergunta_06 = {
    "decision-tree-name": "linhas-de-cuidado",
    "node-name": "pergunta 06",
    "node-rule": "variable:glicemia > 126; output&Pergunta 07:Diabetes - fator crítico | not (variable:glicemia > 126); Pergunta 07",
    "default-next-node": "Pergunta 07"
}
r = requests.post(api_url + 'add-tree-node', json = pergunta_06)
print(f'[STATUS SCRIPT] Decision Tree node {pergunta_06.get("node-name")} finished with status: {r.status_code}')
if r.status_code != 200:
    raise Exception(f'Failed to create the Tree Node {pergunta_06.get("node-name")}')



# pergunta 07 - Obesidade
pergunta_07 = {
    "decision-tree-name": "linhas-de-cuidado",
    "node-name": "pergunta 07",
    "node-rule": "variable:ciap in bundle:ciap-obesidade or variable:cid-10 in bundle:cid-obesidade or variable:código in bundle:cipe-obesidade;output&Pergunta 08:Obesidade| not (variable:ciap in bundle:ciap-obesidade or variable:cid-10 in bundle:cid-obesidade or variable:código in bundle:cipe-obesidade); Pergunta 08",
    "default-next-node": None    
}
r = requests.post(api_url + 'add-tree-node', json = pergunta_07)
print(f'[STATUS SCRIPT] Decision Tree node {pergunta_07.get("node-name")} finished with status: {r.status_code}')
if r.status_code != 200:
    raise Exception(f'Failed to create the Tree Node {pergunta_07.get("node-name")}')

# pergunta 08 - Obesidade
pergunta_08 = {
    "decision-tree-name": "linhas-de-cuidado",
    "node-name": "pergunta 08",
    "node-rule": "variable:imc > 30; output&Pergunta 09:Obesidade - fator crítico| not (variable:imc > 30); Pergunta 09",
    "default-next-node": 'Pergunta 09'  
}
r = requests.post(api_url + 'add-tree-node', json = pergunta_08)
print(f'[STATUS SCRIPT] Decision Tree node {pergunta_08.get("node-name")} finished with status: {r.status_code}')
if r.status_code != 200:
    raise Exception(f'Failed to create the Tree Node {pergunta_08.get("node-name")}')



# pergunta 09 - pre-natal
pergunta_09 = {
    "decision-tree-name": "linhas-de-cuidado",
    "node-name": "pergunta 09",
    "node-rule": "variable:sexo == 'feminino' and variable:idade >= 16; pergunta 10",
    "default-next-node": 'pergunta 13'
}
r = requests.post(api_url + 'add-tree-node', json = pergunta_09)
print(f'[STATUS SCRIPT] Decision Tree node {pergunta_09.get("node-name")} finished with status: {r.status_code}')
if r.status_code != 200:
    raise Exception(f'Failed to create the Tree Node {pergunta_09.get("node-name")}')

# pergunta 10 - pre-natal
pergunta_10 = {
    "decision-tree-name": "linhas-de-cuidado",
    "node-name": "pergunta 10",
    "node-rule": "variable:ciap in bundle:ciap-pre-natal or variable:cid-10 in bundle:cid-pre-natal or variable:código in bundle:cipe-pre-natal; output&Pergunta 11:Pré-natal",
    "default-next-node": 'pergunta 11'
}
r = requests.post(api_url + 'add-tree-node', json = pergunta_10)
print(f'[STATUS SCRIPT] Decision Tree node {pergunta_10.get("node-name")} finished with status: {r.status_code}')
if r.status_code != 200:
    raise Exception(f'Failed to create the Tree Node {pergunta_10.get("node-name")}')

# pergunta 11 - pre-natal
pergunta_11 = {
    "decision-tree-name": "linhas-de-cuidado",
    "node-name": "pergunta 11",
    "node-rule": "variable:pregnant == True; output&Pergunta 12:Pré-natal - fator crítico",
    "default-next-node": "pergunta 12"
}
r = requests.post(api_url + 'add-tree-node', json = pergunta_11)
print(f'[STATUS SCRIPT] Decision Tree node {pergunta_11.get("node-name")} finished with status: {r.status_code}')
if r.status_code != 200:
    raise Exception(f'Failed to create the Tree Node {pergunta_11.get("node-name")}')

# pergunta 12 - pre-natal
pergunta_12 = {
    "decision-tree-name": "linhas-de-cuidado",
    "node-name": "pergunta 12",
    "node-rule": "variable:gestational-age <= 293; output&Pergunta 13:Pré-natal",
    "default-next-node": 'Pergunta 13'
}
r = requests.post(api_url + 'add-tree-node', json = pergunta_12)
print(f'[STATUS SCRIPT] Decision Tree node {pergunta_12.get("node-name")} finished with status: {r.status_code}')
if r.status_code != 200:
    raise Exception(f'Failed to create the Tree Node {pergunta_12.get("node-name")}')



# pergunta 13 - saúde mental
pergunta_13 = {
    "decision-tree-name": "linhas-de-cuidado",
    "node-name": "pergunta 13",
    "node-rule": "variable:ciap in bundle:ciap-saude-mental or variable:cid-10 in bundle:cid-saude-mental or variable:código in bundle:cipe-saude-mental; output&Pergunta 14:Saúde Mental",
    "default-next-node": 'pergunta 14'
}
r = requests.post(api_url + 'add-tree-node', json = pergunta_13)
print(f'[STATUS SCRIPT] Decision Tree node {pergunta_13.get("node-name")} finished with status: {r.status_code}')
if r.status_code != 200:
    raise Exception(f'Failed to create the Tree Node {pergunta_13.get("node-name")}')

# pergunta 14 - saúde mental
pergunta_14 = {
    "decision-tree-name": "linhas-de-cuidado",
    "node-name": "pergunta 14",
    "node-rule": "variable:phq-9 in bundle:phq-9-saude-mental; output&Pergunta 15:Saúde Mental",
    "default-next-node": "Pergunta 15"
}
r = requests.post(api_url + 'add-tree-node', json = pergunta_14)
print(f'[STATUS SCRIPT] Decision Tree node {pergunta_14.get("node-name")} finished with status: {r.status_code}')
if r.status_code != 200:
    raise Exception(f'Failed to create the Tree Node {pergunta_14.get("node-name")}')

# pergunta 15 - saúde mental
pergunta_15 = {
    "decision-tree-name": "linhas-de-cuidado",
    "node-name": "pergunta 15",
    "node-rule": "variable:gad-7 in bundle:gad-7-saude-mental; output:Saúde Mental",
    "default-next-node": None
}
r = requests.post(api_url + 'add-tree-node', json = pergunta_15)
print(f'[STATUS SCRIPT] Decision Tree node {pergunta_15.get("node-name")} finished with status: {r.status_code}')
if r.status_code != 200:
    raise Exception(f'Failed to create the Tree Node {pergunta_15.get("node-name")}')



########################################################################
###################### DECISION TREE STATUS ############################
########################################################################



r = requests.get(api_url + 'list-tree-rules?decision-tree-name=linhas-de-cuidado')
print(f'[STATUS SCRIPT] Decision Tree structure:')
print(r.json())



########################################################################
########################### FINISHING ##################################
########################################################################



# mensagem de conclusão
print(f'[STATUS SCRIPT] Concluded.')
