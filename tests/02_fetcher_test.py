import logging
import yaml

def test_base_fetcher(xnippet, github_repo, auth):
    logging.info(f"++ Case 1. Test BaseFetcher.")
    BaseFetcher = xnippet.fetcher.BaseFetcher
    
    logging.info(f" + Network connection test.")
    assert BaseFetcher.is_connected() == True
    logging.info(" - Connected: %s", BaseFetcher.is_connected())
    
    logging.info(f" + Walk GitHub repository and count number of plugins. auth=%s", True if auth else False)
    plugins = [i for i in BaseFetcher._walk_github_repo(**github_repo, auth=auth) if 'manifest.yaml' in i['files']]
    assert len(plugins) == 1
    file_to_download = 'manifest.yaml'
    download_url = plugins[0]['files'][file_to_download]
    logging.info(f" + Get download url of `manifest.yaml`: %s", download_url)
    
    logging.info(f" + Downloading, %s...", file_to_download)
    bff = b"".join(BaseFetcher._download_buffer(url=download_url, auth=auth))
    result = yaml.safe_load(bff)
    logging.info(" - Downloaded PlugIn: %s", result['plugin']['name'])

def test_snippets_fetcher(xnippet, github_repo, auth):
    logging.info(f"++ Case 2. Test SnippetsFetcher.")
    SnippetsFethcer = xnippet.fetcher.SnippetsFethcer
    
    
    
# def test_pluginfetcher(pytest, xnippet, presets):
#     logging.info("++ Step2. Xnippet.get_fetcher(plugin) method testing")
#     config = xnippet.XnippetManager(**presets['example'])
    
#     logging.debug(f' + Check installed plugin')
#     available = config.avail
#     logging.info(f' + List plugins')
#     logging.info(f"  -> avail plugins: {available}")
#     if len(available):
#         plugin = available[0]
#         plugin_string = f'{plugin.name}=={str(plugin.version)}'
#         logging.info(f' + Installing: {plugin_string}...')
#         with pytest.warns() as record:
#             config.install(plugin_name=plugin.name, plugin_version=str(plugin.version), yes=True)
#             assert len(record) == 1
#         logging.info(f' - Avail Remote: {config.avail} because its installed.')
#         logging.info(f' - Installed: {config.installed}')
#         installed_plugin = config.installed[0]
#         logging.info(f" - Activated? {installed_plugin._activated}")
#         result = installed_plugin._imported_object(2, 3)
#         assert result == (2+3) + (2*3)
#         result = installed_plugin._imported_object(4, 5)
#         assert result == (4+5) + (4*5)
#         logging.info(f' - Imported modules: {list(installed_plugin._include.keys())}')
#     logging.info("++ Removing config folder.")
#     config.delete_config('local', yes=True)