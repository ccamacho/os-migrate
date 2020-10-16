from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import openstack
import unittest

from ansible_collections.os_migrate.os_migrate.plugins.module_utils \
    import server


def sdk_server():
    return openstack.compute.v2.server.Server(
        addresses={
            'external_network': [
                {'OS-EXT-IPS-MAC:mac_addr': 'fa:16:3e:d7:ae:16',
                 'OS-EXT-IPS:type': 'fixed',
                 'addr': '10.19.2.50',
                 'version': 4},
            ],
        },
        description='test server',
        flavor={
            'original_name': 'm1.small',
        },
        id='uuid-test-server',
        image=dict(id='uuid-test-image'),
        key_name='test-key',
        name='test-server',
        security_groups=[
            dict(name='testing123'),
            dict(name='default'),
        ],
        status='ACTIVE',
    )


def server_refs():
    return {
        'addresses_ids': {
            'uuid-external-network': [
                {'OS-EXT-IPS-MAC:mac_addr': 'fa:16:3e:d7:ae:16',
                 'OS-EXT-IPS:type': 'fixed',
                 'addr': '10.19.2.50',
                 'version': 4},
            ],
        },
        'addresses_refs': {
            'external_network': [
                {'OS-EXT-IPS-MAC:mac_addr': 'fa:16:3e:d7:ae:16',
                 'OS-EXT-IPS:type': 'fixed',
                 'addr': '10.19.2.50',
                 'version': 4},
            ],
        },
        'flavor_id': 'uuid-flavor-m1.small',
        'flavor_ref': {
            'name': 'm1.small',
            'project_name': 'test-project',
            'domain_name': 'Default',
        },
        'image_id': 'uuid-test-image',
        'image_ref': {
            'name': 'test-image',
            'project_name': 'test-project',
            'domain_name': 'Default',
        },
        'security_group_ids': [
            'uuid-secgroup-default',
            'uuid-secgroup-testing123',
        ],
        'security_group_refs': [
            {
                'name': 'default',
                'project_name': 'test-project',
                'domain_name': 'Default',
            },
            {
                'name': 'testing123',
                'project_name': 'test-project',
                'domain_name': 'Default',
            },
        ],
    }


class Server(server.Server):
    def _refs_from_ser(self, conn):
        return server_refs()

    @staticmethod
    def _refs_from_sdk(conn, sdk_res):
        return server_refs()


class TestServer(unittest.TestCase):
    def test_serialize_server(self):
        srv = Server.from_sdk(None, sdk_server())
        params, info = srv.params_and_info()

        self.assertEqual(srv.type(), 'openstack.compute.Server')
        self.assertEqual(params['addresses_refs'], {
            'external_network': [
                {'OS-EXT-IPS-MAC:mac_addr': 'fa:16:3e:d7:ae:16',
                 'OS-EXT-IPS:type': 'fixed',
                 'addr': '10.19.2.50',
                 'version': 4},
            ],
        })
        self.assertEqual(params['description'], 'test server')
        self.assertEqual(params['flavor_ref']['name'], 'm1.small')
        self.assertEqual(info['id'], 'uuid-test-server')
        self.assertEqual(params['key_name'], 'test-key')
        self.assertEqual(params['name'], 'test-server')
        self.assertEqual(params['security_group_refs'][0]['name'], 'default')
        self.assertEqual(params['security_group_refs'][1]['name'], 'testing123')
        self.assertEqual(info['status'], 'ACTIVE')

    def test_block_device_mapping_boot_disk_copy(self):
        srv = Server.from_sdk(None, sdk_server())
        sdk_params = srv.sdk_params(None)

        block_dev_map = [
            {
                'boot_index': -1,
                'delete_on_termination': False,
                'destination_type': 'volume',
                'device_name': 'sdb',
                'source_type': 'volume',
                'uuid': 'uuid-some-volume',
            }
        ]
        srv.update_sdk_params_block_device_mapping(sdk_params, block_dev_map)
        self.assertEqual(sdk_params['block_device_mapping'], [
            {
                'boot_index': 0,
                'delete_on_termination': True,
                'destination_type': 'local',
                'source_type': 'image',
                'uuid': 'uuid-test-image',
            },
            {
                'boot_index': -1,
                'delete_on_termination': False,
                'destination_type': 'volume',
                'device_name': 'sdb',
                'source_type': 'volume',
                'uuid': 'uuid-some-volume',
            }
        ])
        self.assertEqual(sdk_params['image_id'], 'uuid-test-image')

    def test_block_device_mapping_boot_disk_nocopy(self):
        srv = Server.from_sdk(None, sdk_server())
        srv.migration_params()['boot_disk_copy'] = True
        sdk_params = srv.sdk_params(None)

        block_dev_map = [
            {
                'boot_index': 0,
                'delete_on_termination': True,
                'destination_type': 'volume',
                'device_name': 'sda',
                'source_type': 'volume',
                'uuid': 'uuid-boot-volume',
            },
            {
                'boot_index': -1,
                'delete_on_termination': False,
                'destination_type': 'volume',
                'device_name': 'sdb',
                'source_type': 'volume',
                'uuid': 'uuid-some-volume',
            }
        ]
        srv.update_sdk_params_block_device_mapping(sdk_params, block_dev_map)
        self.assertEqual(sdk_params['block_device_mapping'], [
            {
                'boot_index': 0,
                'delete_on_termination': True,
                'destination_type': 'volume',
                'device_name': 'sda',
                'source_type': 'volume',
                'uuid': 'uuid-boot-volume',
            },
            {
                'boot_index': -1,
                'delete_on_termination': False,
                'destination_type': 'volume',
                'device_name': 'sdb',
                'source_type': 'volume',
                'uuid': 'uuid-some-volume',
            }
        ])
        self.assertTrue('image_id' not in sdk_params)
