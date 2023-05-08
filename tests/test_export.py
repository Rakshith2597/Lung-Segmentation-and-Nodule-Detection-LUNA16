import unittest
import os
from src.utils.downloader import download_checkpoint
from src.utils.exporter import Exporter
from src.utils.get_config import get_config

def create_export_test_for_stage1():
    class ExportTestStage1(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            cls.config = get_config(action='export', stage=1)
            if not os.path.exists(cls.config['checkpoint']):
                download_checkpoint()
            cls.model_path = cls.config['checkpoint']

        def test_export_onnx(self):
            self.exporter = Exporter(self.config, stage=1)
            self.exporter.export_model_onnx()
            self.assertTrue(os.path.join(os.path.split(self.model_path)[
                            0], self.config.get('model_name_onnx')))

        def test_export_ir(self):
            self.exporter = Exporter(self.config, stage=1)
            model_dir = os.path.split(self.config['checkpoint'])[0]
            if not os.path.exists(os.path.join(model_dir, self.config.get('model_name_onnx'))):
                self.exporter.export_model_onnx()
            self.exporter.export_model_ir()
            name_xml = self.config['model_name'] + '.xml'
            name_bin = self.config['model_name'] + '.bin'
            xml_status = os.path.exists(os.path.join(model_dir, name_xml))
            bin_status = os.path.exists(os.path.join(model_dir, name_bin))
            self.assertTrue(xml_status)
            self.assertTrue(bin_status)

        def test_config(self):
            self.model_path = self.config['checkpoint']
            self.input_shape = self.config['input_shape']
            self.output_dir = os.path.split(self.model_path)[0]
            self.assertTrue(self.output_dir)
            self.assertTrue(self.model_path)
            self.assertListEqual(self.input_shape, [1, 1, 512, 512])
    return ExportTestStage1


def create_export_test_for_stage2():
    class ExportTestStage2(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            cls.config = get_config(action='export', stage=2)
            if not os.path.exists(cls.config['checkpoint']):
                download_checkpoint()
            cls.model_path = cls.config['checkpoint']

        def test_export_onnx(self):
            self.exporter = Exporter(self.config, stage=2)
            self.exporter.export_model_onnx()
            checkpoint = os.path.split(self.config['checkpoint'])[0]
            self.assertTrue(os.path.join(
                checkpoint, self.config.get('model_name_onnx')))

        def test_export_ir(self):
            self.exporter = Exporter(self.config, stage=2)
            self.model_path = os.path.split(self.config['checkpoint'])[0]
            if not os.path.exists(os.path.join(self.model_path, self.config.get('model_name_onnx'))):
                self.exporter.export_model_onnx()
            self.exporter.export_model_ir()
            name_xml = self.config.get('model_name') + '.xml'
            name_bin = self.config.get('model_name') + '.bin'
            xml_status = os.path.exists(
                os.path.join(self.model_path, name_xml))
            bin_status = os.path.exists(
                os.path.join(self.model_path, name_bin))
            self.assertTrue(xml_status)
            self.assertTrue(bin_status)

        def test_config(self):
            self.model_path = self.config['checkpoint']
            self.input_shape = self.config['input_shape']
            self.output_dir = os.path.split(self.model_path)[0]
            self.assertTrue(self.output_dir)
            self.assertTrue(self.model_path)
            self.assertListEqual(self.input_shape, [1, 1, 64, 64])
    return ExportTestStage2


class TestExportStage1(create_export_test_for_stage1()):
    'Test case for stage1'


class TestExportStage2(create_export_test_for_stage2()):
    'Test case for stage2'


if __name__ == '__main__':
    unittest.main()
