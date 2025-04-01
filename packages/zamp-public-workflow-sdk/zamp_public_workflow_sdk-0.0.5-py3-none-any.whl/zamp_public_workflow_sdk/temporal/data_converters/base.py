from temporalio.converter import DataConverter, PayloadCodec

class BaseDataConverter:
    converter = DataConverter.default

    @staticmethod
    def add_payload_codec(payload_codec: PayloadCodec):
        BaseDataConverter.converter.add_payload_codec(payload_codec)
        
    @staticmethod
    def get_converter():
        return BaseDataConverter.converter