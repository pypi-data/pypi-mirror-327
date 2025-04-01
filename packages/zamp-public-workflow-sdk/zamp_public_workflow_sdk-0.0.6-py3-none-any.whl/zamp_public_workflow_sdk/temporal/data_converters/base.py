from temporalio.converter import DataConverter, PayloadCodec

class BaseDataConverter:
    converter = DataConverter.default

    def add_payload_codec(self, payload_codec: PayloadCodec) -> 'BaseDataConverter':
        self.converter.add_payload_codec(payload_codec)
        return self
        
    def get_converter(self) -> DataConverter:
        return self.converter