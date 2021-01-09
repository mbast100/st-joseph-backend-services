from data.internal_configurations.internal_configurations import InternalConfigurations


class TestInternalConfigurations():

    def test_save_internal_config(self, internal_configuration_new):
        internal_configs = InternalConfigurations(
            params=internal_configuration_new.data)
        assert internal_configs.save

    def test_update_internal_config(self):
        updates = {
            "config": {
                "image": "some_image_address",
                "display": False
            }
        }
        internal_configs = InternalConfigurations(feature="test_feature")
        assert internal_configs.update(updates)

    def test_update_not_missing_feature(self):
        updates = {
            "config": {
                "image": "some_image_address",
                "display": False
            }
        }
        internal_configs = InternalConfigurations()
        assert not internal_configs.update(updates)

    def test_invalid_input_updates(self):
        updates = ["hello"]

        internal_configs = InternalConfigurations()
        assert not internal_configs.update(updates)

    def test_invalid_update(self):
        updates = {
            "config": {
                "image": "some_image_address",
                "display": False
            }
        }

        internal_configs = InternalConfigurations(feature="random23")
        assert not internal_configs.update(updates)

    def test_get_internal_config(self):

        internal_config = InternalConfigurations().all
        assert len(internal_config) > 0

    def test_get_internal_config_by_feature_name(self):

        internal_config = InternalConfigurations().find_by("feature", "test_feature")
        assert len(internal_config) == 1

    def test_get_internal_config_by_feature_name_that_dosent_exist(self):

        internal_config = InternalConfigurations().find_by("feature", "random1")
        assert len(internal_config) == 0
