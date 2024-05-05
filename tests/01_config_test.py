def test_xnippy_init(pytest, xnippy, presets, config):
    with pytest.warns() as record_1:
        # empty preset doesn't have config file: expecting warning == 1
        xnippy_empt = xnippy.Xnippy(**presets['empty'])
    assert len(record_1) == 1, "Warning related to the config file not exists in config directory"
    assert xnippy_empt.config == config, "Check the loaded config is one in the default inside package"
    
    with pytest.warns() as record_2:
        xnippy_expt = xnippy.Xnippy(**presets['example'])
    assert len(record_2) == 0, "No warning"
    assert xnippy_expt.config != config, "Example config != default config"
    
    
    
    # plugins = xnippy.get_fetcher('plugin')
    # assert plugins.is_connected() == True, "Check network is accessible"
