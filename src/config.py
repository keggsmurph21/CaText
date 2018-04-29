import os

# default values


# functions
def get_path(*paths):
    ''' get path under project root '''
    return os.path.join(root, *paths)


# objects
api = None
api_logger = None
app_logger = None
cli = None
cli_logger = None
current_user = None
env = None
root = None
root_logger = None
