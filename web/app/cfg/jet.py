'''
Option JET_DEFAULT_THEME was taken from:
https://jet.readthedocs.io/en/latest/config_file.html#jet-default-theme
'''
#JET_DEFAULT_THEME = 'light-blue'
JET_DEFAULT_THEME = 'my-default-theme'

'''
Option JET_THEMES was taken from:
https://jet.readthedocs.io/en/latest/config_file.html#jet-themes
'''
JET_THEMES = [
 {
   'theme': 'default', # theme folder name
   'color': '#47bac1', # color of the theme's button in user menu
   'title': 'Predeterminado' # theme title
 },
 {
   'theme': 'green',
   'color': '#44b78b',
   'title': 'Verde'
 },
 {
   'theme': 'light-green',
   'color': '#2faa60',
   'title': 'Verde claro'
 },
 {
   'theme': 'light-violet',
   'color': '#a464c4',
   'title': 'Violeta claro'
 },
 {
  'theme': 'light-blue',
   'color': '#5EADDE',
   'title': 'Azul claro'
 },
 {
   'theme': 'light-gray',
   'color': '#222',
   'title': 'Gris claro'
 },
 # {
 #   'theme': 'my-default-theme',
 #   'color': 'black',
 #   'title': 'Default Theme'
 # }
]
'''
JET_SIDE_MENU_ITEMS = [
  {
  	'app_label': 'auth', 
  	'items': [
      {'name': 'users.users'},
      {'name': 'group'},
  	]
	},
  {
    'app_label': 'catalogues', 
  	'items': [
      {'name': 'country'},
      {'name': 'city'},
      {'name': 'region'},
  	]
	},
  {
  	'app_label': 'tests', 
  	'items': [
  		{'name': 'tests'},
      {'name': 'params'},
      {'name': 'testsparams'},
      {'name': 'testsgroups'},
      {'name': 'testsrequests'},
      {'name': 'testsresults'},
  	]
	},
  {
    'app_label': 'labs', 
    'items': [
      {'name': 'labs'}
    ]
  },
  {
    'app_label': 'customers', 
    'items': [
      {'name': 'customers'}
    ]
  },
]
'''
#JET_SIDE_MENU_COMPACT = True

# Taken from: https://jet.readthedocs.io/en/latest/dashboard_custom.html
#JET_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'
JET_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'