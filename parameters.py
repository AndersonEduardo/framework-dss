S3_BUCKET = 'framework-dss-bucket'
PERSISTENCE_FOLDER = 'persistence'

PERSISTENCE_FILEPATH = 'persistence/tree.pkl'
PERSISTENCE_BACKUP_FILEPATH = 'persistence/tree_BACKUP.pkl'

PERSISTENCE_BUNDLE_FILEPATH = 'persistence/bundles.pkl'
PERSISTENCE_BUNDLE_BACKUP_FILEPATH = 'persistence/bundles_BACKUP.pkl'

DEFAULT_CONTEXT = 'dev'

RESERVED_SHEETS = ['BUNDLES', 'TREE']

SHEET_TREE_COLUMNS = ['CONTEXT', 'TREE', 'TARGET', 'NODE', 'RULE', 'TRUE', 'FALSE']

LINEBREAK = '[LINEBREAK]'
INNERLINEBREAK = '[INNERLINEBREAK]'
SEMICOLON = '[SEMICOLON]'


MENU_OPERATIONS = ['>', '>=', '<', '<=', '==', '!=', 'in']
MENU_PARAMETERS_TYPE = ['Number', 'Bundle', 'Text']
MENU_ACTION = ['Go to', 'Output', 'Output & Go to', 'End']

API_DSSF_CREATE_TREE = 'http://localhost:5000/create-decision-tree'
API_DSSF_ADD_NODE = 'http://localhost:5000/add-tree-node'
API_DSSF_BUNDLES = 'http://localhost:5000/list-bundles'