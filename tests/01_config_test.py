import logging

def test_config_empty(pytest, xnippet, presets, default_config):
    logging.info('++ Case 1. Xnippet.__init__ test.')
    logging.info(' + Xnippet initiate without package config file.')
    with pytest.warns() as record:
        xnippet_empty = xnippet.XnippetManager(**presets[0])
        assert len(record) == 1
    assert xnippet_empty.config == default_config
    
    logging.info(' + Create config on local testing folder.')
    xnippet_empty.create_config('local')
    assert xnippet_empty.config_created == 'local', "Create local configuration"
    
def test_config_local(pytest, xnippet, presets):
    logging.info('++ Case 2. Xnippet initiate with local config created.')
    xnippet_local = xnippet.XnippetManager(**presets[0])
    
    logging.info(' + Delete config on local testing folder.')
    with pytest.warns() as record:
        xnippet_local.delete_config('local', yes=True)
        assert len(record) == 1
        
def test_config_examp(xnippet, presets, default_config):
    logging.info("++ Case 3. Xnippet initiate with package's default config file.")
    xnippet_expt = xnippet.XnippetManager(**presets[1])
    assert xnippet_expt.config != default_config, "Example config != default config"
