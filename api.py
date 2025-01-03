import os
import pickle
import time
import datetime as dt
import dotenv

from flask import Flask, jsonify, request, make_response, render_template
from flask_cors import CORS

from dss import *
from decisiontree import *
from node import *
from bundles import *
from awss3 import AwsS3 as s3

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False


print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] Building Decision Support System...")

bds = Bundles()
bds.load_backup_from_s3()

dss = DecisionSupportSystem()
dss.load_backup_from_s3()

print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ...done.")


@app.route('/')
def home():

    return jsonify('## DSSF: DECISION SUPPORT SYSTEM FRAMEWORK - COCKPIT - TMDA/SBIBAE ##')


@app.route('/create-decision-tree', methods=['GET', 'POST'])
def create_decision_tree():

    if request.is_json:

        data = request.json
        name = data.get('name')
        target_field = data.get('target-field')
        context = data.get('context')
        offline = data.get('offline')
        force = data.get('force')

        context = None if context is None else(None if context.strip().lower() == 'none' else context)
        offline = False if offline is None else(False if offline.strip().lower() == 'none' else (True if offline.strip().lower() == 'true' else False))
        force = False if force is None else(False if force.strip().lower() == 'none' else (True if force.strip().lower() == 'true' else False))

        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ## Creating a new Decision Tree ##")
        print(
            f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] User input:\n\t-name={context} {type(context)}\n\t-name={name} {type(name)}\n\t-target_field={target_field} {type(target_field)}"
        )
        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] Instantiation of a new Decision Tree...")
        dss.build_decision_tree(
            context = context, 
            name = name, 
            target_field = target_field,
            offline = offline,
            force = force
        )
        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ...done.")

        response = {"message": "Done."}
        response = make_response(response)
        response.status = 200

        return response

    else:

        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] - ouptut: Content type not supported ('application/json' needed, but {request.headers.get('Content-Type')} was found).")

        response = {"status": 415, "message": "Content type not supported."}
        response = make_response(response)
        response.status = 415

        return response


@app.route('/add-tree-node', methods=['GET', 'POST'])
def add_tree_node():

    if request.is_json:

        data = request.json
        context = data.get('context')
        decision_tree_name = data.get('decision-tree-name')
        node_name = data.get('node-name')
        rule = data.get('rule')
        if_true = data.get('if-true')
        if_false = data.get('if-false')
        offline = data.get('offline')
        force = data.get('force')

        context = None if context is None else(None if context.strip().lower() == 'none' else context)
        offline = False if offline is None else(False if offline.strip().lower() == 'none' else (True if offline.strip().lower() == 'true' else False))
        force = False if force is None else(False if force.strip().lower() == 'none' else (True if force.strip().lower() == 'true' else False))

        node_rules = f'{rule}; {if_true}; {if_false}'


        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ## Creating a new tree Node ##")
        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] User inputs:")
        print('\t-context:', context)
        print('\t-decision_tree_name:', decision_tree_name)
        print('\t-offline:', offline)
        print('\t-node_name:', node_name)
        print('\t-node_rule:', node_rules)

        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] Add a new node ({node_name}) to {decision_tree_name}...")
        dss.add_tree_node(
            context = context,
            decision_tree_name = decision_tree_name, 
            node_name = node_name, 
            node_rules = node_rules,
            bundles = bds,
            offline = offline,
            force = force
        )

        dss.rooting(
            context = context,
            decision_tree_name = decision_tree_name
        )
        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ...done.")

        response = {"message": "Done."}
        response = make_response(response)
        response.status = 200

        return response

    else:

        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] - ouptut: Content type not supported ('application/json' needed, but {request.headers.get('Content-Type')} was found).")

        response = {"status": 415, "message": "Content type not supported."}
        response = make_response(response)
        response.status = 415

        return response


@app.route('/update-tree-node', methods=['GET', 'POST'])
def update_tree_node():

    if request.is_json:

        data = request.json
        context = data.get('context')
        decision_tree_name = data.get('decision-tree-name')
        focal_node_name = data.get('focal-node-name')
        new_rule = data.get('rule')
        if_true = data.get('if-true')
        if_false = data.get('if-false')
        offline = data.get('offline')

        new_node_rule = f'{new_rule}; {if_true}; {if_false}'
        context = None if context is None else(None if context.strip().lower() == 'none' else context)
        offline = False if offline is None else(False if offline.strip().lower() == 'none' else (True if offline.strip().lower() == 'true' else False))

        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ## Update for a tree Node ##")
        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] User inputs:")
        print('\t-context:', context)
        print('\t-decision_tree_name:', decision_tree_name)
        print('\t-focal_node_name:', focal_node_name)
        print('\t-new_node_rule:', new_node_rule)


        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] Updating {focal_node_name} node...")
        update_output = dss.update_rule(
            context = context,
            decision_tree_name = decision_tree_name,
            node_name = focal_node_name,
            new_rule = new_node_rule,
            bundles = bds,
            offline = offline
        )

        # dss.rooting(decision_tree_name)
        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ...done.")

        if update_output is None:

            response = {"message": "Done."}
            response = make_response(response)
            response.status = 200
        
        else:

            response = {"message": "Decision tree name or node name not found."}
            response = make_response(response)
            response.status = 422

        return response

    else:

        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] - ouptut: Content type not supported ('application/json' needed, but {request.headers.get('Content-Type')} was found).")

        response = {"status": 415, "message": "Content type not supported."}
        response = make_response(response)
        response.status = 415

        return response


@app.route('/query', methods=['GET', 'POST'])
def query():

    if request.is_json:

        data = request.json
        decision_tree_name = data.get('decision_tree_name')
        user_input = data.get('parameters')
        context = data.get('context')

        context = None if context is None else(None if context.strip().lower() == 'none' else context)

        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ## Decision Tree Query ##")
        print(
            f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] User input: \n\t-context={context} \n\t-decision_tree_name={decision_tree_name} {type(decision_tree_name)}\n\t-parameters={user_input} {type(user_input)}"
        )

        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] Querying Decision Tree...")
        response = dss.query(
            context = context,
            decision_tree_name = decision_tree_name, 
            user_input = user_input
        )
        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] Response:", response)
        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ...done.")

        response = {"message": "Done.", "response": response}
        response = make_response(response)
        response.status = 200

        return response

    else:

        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] - ouptut: Content type not supported ('application/json' needed, but {request.headers.get('Content-Type')} was found).")

        response = {"status": 415, "message": "Content type not supported."}
        response = make_response(response)
        response.status = 415

        return response


@app.route('/delete-tree-node', methods=['DELETE',])
def delete_tree_node():

    if request.is_json:

        data = request.json
        decision_tree_name = data.get('decision-tree-name')
        node_name = data.get('node-name')
        context = data.get('context')
        offline = data.get('offline')

        context = None if context is None else(None if context.strip().lower() == 'none' else context)
        offline = False if offline is None else(False if offline.strip().lower() == 'none' else (True if offline.strip().lower() == 'true' else False))

        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ## Node Deleting ##")
        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] User inputs:")
        print('\context:', context)
        print('\tdecision_tree_name:', decision_tree_name)
        print('\tnode_name:', node_name)

        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] Deleting a Node ({node_name}) from {decision_tree_name} (context '{context}')...")
        dss.delete_node(
            context = context,
            decision_tree_name = decision_tree_name, 
            node_name = node_name,
            offline = offline
        )
        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ...done.")

        response = {"message": "Done."}
        response = make_response(response)
        response.status = 200

        return response

    else:

        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] - ouptut: Content type not supported ('application/json' needed, but {request.headers.get('Content-Type')} was found).")

        response = {"status": 415, "message": "Content type not supported."}
        response = make_response(response)
        response.status = 415

        return response


@app.route('/delete-tree', methods=['DELETE',])
def delete_tree():

    if request.is_json:

        data = request.json
        decision_tree_name = data.get('decision-tree-name')
        context = data.get('context')
        offline = data.get('offline')

        context = None if context is None else(None if context.strip().lower() == 'none' else context)
        offline = False if offline is None else(False if offline.strip().lower() == 'none' else (True if offline.strip().lower() == 'true' else False))

        print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}] ## Decision Tree Deleting ##')
        print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  User inputs: \n\t-context: {context} \n\t-decision_tree_name: {decision_tree_name}')
        print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  Deleting the Decision Tree {decision_tree_name} (context "{context}")...')
        dss.delete_tree(
            context = context,
            decision_tree_name = decision_tree_name,
            offline = offline
        )
        print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  ...done.')

        response = {"message": "Done."}
        response = make_response(response)
        response.status = 200

        return response

    else:

        print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  - ouptut: Content type not supported ("application/json" needed, but {request.headers.get("Content-Type")} was found).')

        response = {"status": 415, "message": "Content type not supported."}
        response = make_response(response)
        response.status = 415

        return response


@app.route('/list-trees')
def list_trees():

    context = request.args.get('context', type=str, default=None)

    context = None if context is None else(None if context.strip().lower() == 'none' else context)

    print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  ## Decision Tree Listing ##')
    print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  Decision trees in the system (context = {context}):')
    response = dss.get_tree_list(
        context = context
    )
    print(response)
    print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}] ...done.')

    response = {"message": "Done.", "response": response}
    response = make_response(response)
    response.status = 200

    return response


@app.route('/list-tree-nodes')
def list_tree_nodes():

    decision_tree_name = request.args.get('decision-tree-name', type=str, default=None)
    context = request.args.get('context', type=str, default=None)

    context = None if context is None else(None if context.strip().lower() == 'none' else context)

    print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  ## Node Listing ##')
    print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  User inputs: \n\t-context: {context}\n\t-decision_tree_name: {decision_tree_name}')
    print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  List of Nodes for the Decision Tree {decision_tree_name}:')
    response = dss.get_node_list(
        context = context,
        decision_tree_name = decision_tree_name
    )
    print(response)
    print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  ...done.')

    response = {"message": "Done.", "response": response}
    response = make_response(response)
    response.status = 200

    return response


@app.route('/list-tree-rules')
def list_tree_rules():

    decision_tree_name = request.args.get('decision-tree-name', type=str, default=None)
    context = request.args.get('context', type=str, default=None)

    context = None if context is None else(None if context.strip().lower() == 'none' else context)

    print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  ## Node Listing ##')
    print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  User inputs: \n\t-context: {context}\n\t-decision_tree_name: {decision_tree_name}')
    print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}] List of Rules for the Decision Tree {decision_tree_name}:')
    response = dss.get_rule_list(
        context = context,
        decision_tree_name = decision_tree_name
    )
    print(response)
    print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  ...done.')

    response = {"message": "Done.", "response": response}
    response = make_response(response)
    response.status = 200

    return response


@app.route('/create-bundles', methods=['GET', 'POST'])
def create_bundles():

    if request.is_json:

        data = request.json
        context = str(data.get('context')).strip().lower()
        bundle_name = str(data.get('bundle-name')).strip().lower()
        bundle_values = str(data.get('bundle-values')).strip().lower()
        offline = str(data.get('offline')).strip().lower()

        context = None if context is None else(None if context == 'none' else context)
        offline = None if offline is None else(None if offline == 'none' else offline)


        if offline not in [None, 'true', 'false']:

            raise TypeError('The parameter "offline" must be either True or False.')
        
        else:

            if offline == 'true':

                offline = True
            
            else:

                offline = False


        print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  ## Bundle ##')
        print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  \t-context: {context}')
        print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  \t-bundle name: {bundle_name}')
        print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  \t-bundle values: {bundle_values}')
        print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  \t-offline: {offline}')
    
        print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  Running parser...')
        parsed = bds.input_parser(bundle_name, bundle_values)
        bds.append(context=context, bundle=parsed, offline=offline)    
        print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  ...done.')

        response = {"message": "Done."}
        response = make_response(response)
        response.status = 200

        return response

    else:

        print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  - ouptut: Content type not supported ("application/json" needed, but {request.headers.get("Content-Type")} was found).')

        response = {"status": 415, "message": "Content type not supported."}
        response = make_response(response)
        response.status = 415

        return response


@app.route('/list-bundles')
def list_bundles():

    print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  ## Bundles Listing ##')
    print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  Current bundles in the system:')
    response =  bds.get_bundles_list()
    print(response)
    print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}] ...done.')

    response = {"message": "Done.", "response": response}
    response = make_response(response)
    response.status = 200

    return response


@app.route('/delete-bundle', methods=['DELETE',])
def delete_bundle():

    if request.is_json:

        data = request.json
        bundle_name = str(data.get('bundle-name')).strip().lower()
        context = str(data.get('context')).strip().lower()
        offline = str(data.get('offline')).strip().lower()
        all_bundles = str(data.get('all')).strip().lower()

        context = None if context is None else(None if context == 'none' else context)
        offline = None if offline is None else(None if offline == 'none' else offline)
        all_bundles = None if all_bundles is None else(None if all_bundles == 'none' else all_bundles)


        if offline not in [None, 'true', 'false']:

            raise TypeError('The parameter "offline" must be either True or False.')
        
        else:

            if offline == 'true':

                offline = True
            
            else:

                offline = False

        if all_bundles not in [None, 'true', 'false']:

            raise TypeError('The parameter "all_bundles" must be either True or False.')

        else:

            if all_bundles == 'true':

                all_bundles = True
            
            else:

                all_bundles = False


        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ## Bundle Deleting ##")
        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] User inputs:")
        print('\tcontext:', context)
        print('\tbundle_name:', bundle_name)
        print('\toffline:', offline)
        print('\tall_bundles:', all_bundles)


        if all_bundles in [True, 'true']:
            print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] Deleting all Bundles...")            
        else:
            print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] Deleting Bundle {bundle_name} (context {context}')...")

        bds.delete(
            context = context,
            name = bundle_name, 
            offline = offline,
            all = all_bundles
        )
        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ...done.")

        response = {"message": "Done."}
        response = make_response(response)
        response.status = 200

        return response

    else:

        print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] - ouptut: Content type not supported ('application/json' needed, but {request.headers.get('Content-Type')} was found).")

        response = {"status": 415, "message": "Content type not supported."}
        response = make_response(response)
        response.status = 415

        return response


# @app.route('/treeuploader', methods=['GET', 'POST'])
# def uploader():

#     if request.method == 'POST':

#         # bundles
#         bds._load_from_excel(
#             excel_filepath = request.files.get('file') # input_value
#         )

#         # # decision tree
#         # dss._build_tree_from_excel(
#         #     context = None,
#         #     excel_filepath = request.files.get('file'), # input_value,
#         #     bundles = bds,
#         #     # offline = False,
#         #     force = False
#         # )

#         return render_template('done.html')
    
#     return render_template('uploader.html')


@app.route('/bundle-uploader', methods=['POST'])
def bundle_uploader():

    offline =  "true" if s3.check_s3_availability() is False else "false"

    print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ## Bundle Uploader ##")
    print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] User inputs:")
    print('\trequest method:', request.method)
    print('\trequest is json:', request.is_json)
    print('\toffline:', offline)


    if offline not in [None, 'true', 'false']:

        raise TypeError('The parameter "offline" must be either True or False.')
    
    else:

        if offline == 'true':

            offline = True
        
        else:

            offline = False


    print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] Uploading Bundle file...")

    file = request.files['file']

    if file.filename == '':
        response = {"message": "No file selected."}
        response = make_response(response)
        response.status = 400

        return response

    file = BytesIO(file.read())
    bds._load_from_excel(
        excel_filepath = file, # input_value
        offline = offline
    )

    print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ...done.")

    response = {"message": "Done."}
    response = make_response(response)
    response.status = 200

    return response


@app.route('/refresh', methods=['GET'])
def refresh():

    global bds, dss

    del bds, dss

    dotenv.load_dotenv(override=True)

    print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] Refreshing Decision Support System...")

    bds = Bundles()
    bds.load_backup_from_s3()

    dss = DecisionSupportSystem()
    dss.load_backup_from_s3()

    print(f"[API STATUS - {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%s')}] ...done.")

    return jsonify({"status": 200, "message": "Decision Support System refreshing concluded."})


@app.route('/healthcheck', methods=['GET'])
def healthCheck():

    print(f'[API STATUS - {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%s")}]  ## Health check ##')

    return {
        "STATUS": 200,
        "detailed": True,
        "message": "Health is fine for deploy on ECS."
    }


if __name__ == '__main__':

    app.run(host="0.0.0.0", debug=False)
