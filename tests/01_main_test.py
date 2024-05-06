import logging

def test_xnippy__init__(pytest, xnippy, presets, default_config):
    logging.info('++ Step1. Xnippy.__init__ test.')
    logging.info(' + Xnippy initiate without config file.')
    with pytest.warns() as record_1:
        xnippy_empt = xnippy.XnippyManager(**presets['empty'])
        assert len(record_1) == 1, "Warning related to the config file not exists in config directory"
        assert xnippy_empt.config == default_config, "Check the loaded config is one in the default inside package"
    logging.info(f" - global_dir: {xnippy_empt._global_dir}")
    logging.info(f" - config_dir: {xnippy_empt._config_dir} -> project's default_dir")
    logging.info(f" - local_dir: {xnippy_empt._local_dir}")
    
    logging.info(' + Create config on local testing folder.')
    xnippy_empt.create_config('local')
    assert xnippy_empt.config_created == 'local', "Create local configuration"
    logging.info(f" - global_dir: {xnippy_empt._global_dir}")
    logging.info(f" - config_dir: {xnippy_empt._config_dir} -> local_dir")
    logging.info(f" - local_dir: {xnippy_empt._local_dir}")
    
    logging.info(' + Delete config on local testing folder.')
    with pytest.warns() as record_1:
        xnippy_empt.delete_config('local', yes=True)
        # expected to have warning, because config is not deleted
        assert len(record_1) == 1, "Warning related to the config file not exists in config directory"
    logging.info(f" - global_dir: {xnippy_empt._global_dir}")
    logging.info(f" - config_dir: {xnippy_empt._config_dir} -> project's default_dir")
    logging.info(f" - local_dir: {xnippy_empt._local_dir}")
    
    logging.info(' + Xnippy initiate with config file.')
    xnippy_expt = xnippy.XnippyManager(**presets['example'])
    assert xnippy_expt.config != default_config, "Example config != default config"
    logging.info(f" - global_dir: {xnippy_expt._global_dir}")
    logging.info(f" - config_dir: {xnippy_expt._config_dir} -> project's default_dir")
    logging.info(f" - local_dir: {xnippy_expt._local_dir}")
    

def test_pluginfetcher(pytest, xnippy, presets):
    logging.info("++ Step2. Xnippy.get_fetcher(plugin) method testing")
    config = xnippy.XnippyManager(**presets['example'])
    
    logging.info(f' + Check installed plugin')
    available = config.avail
    logging.info(f' + List plugins')
    logging.info(f"  -> avail plugins: {available}")
    if len(available):
        plugin = available[0]
        plugin_string = f'{plugin.name}=={str(plugin.version)}'
        logging.info(f' + Installing: {plugin_string}...')
        with pytest.warns() as record:
            config.install(plugin_name=plugin.name, plugin_version=str(plugin.version), yes=True)
            assert len(record) == 1
        logging.info(f' - Avail Remote: {config.avail} because its installed.')
        logging.info(f' - Installed: {config.installed}')
        installed_plugin = config.installed[0]
        logging.info(f" - Activated? {installed_plugin._activated}")
        result = installed_plugin._imported_object(2, 3)
        assert result == (2+3) + (2*3)
        result = installed_plugin._imported_object(4, 5)
        assert result == (4+5) + (4*5)
        logging.info(f' - Imported modules: {list(installed_plugin._include.keys())}')
    logging.info("++ Removing config folder.")
    config.delete_config('local', yes=True)