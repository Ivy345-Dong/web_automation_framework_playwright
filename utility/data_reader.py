import json
import yaml
import os


def get_json_data(filename):
    """
    Read JSON test data file and return as list of tuples
    """
    data_list = []
    with open(filename, 'r', encoding='utf-8') as f:
        case_data = json.load(f)
        for case in case_data.values():
            list = case.values()
            data_list.append(tuple(list))
    return data_list

def get_env_url():
    """Get base URL from environment.yaml"""
    yaml_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'environment.yaml')
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data['web']['url']

def get_browser_config():
    """Get browser configuration from environment.yaml"""
    yaml_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'environment.yaml')
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get('browser', {})
def get_enabled_browsers():
    """Get list of enabled browsers from environment.yaml"""
    browser_config = get_browser_config()
    return browser_config.get('enabled', ['chromium'])
def is_parallel_enabled():
    """Check if parallel execution is enabled"""
    browser_config = get_browser_config()
    parallel_config = browser_config.get('parallel', {})
    return parallel_config.get('enabled', False)
def get_parallel_workers():
    """Get number of parallel workers"""
    browser_config = get_browser_config()
    parallel_config = browser_config.get('parallel', {})
    return parallel_config.get('workers', 'auto')