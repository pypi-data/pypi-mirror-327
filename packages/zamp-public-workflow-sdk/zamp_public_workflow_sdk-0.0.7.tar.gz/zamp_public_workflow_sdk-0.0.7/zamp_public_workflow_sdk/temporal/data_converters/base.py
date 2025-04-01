from temporalio.converter import DataConverter, PayloadCodec
import dataclasses

class BaseDataConverter:
    converter = DataConverter.default

    def add_payload_codec(self, payload_codec: PayloadCodec) -> 'BaseDataConverter':
        self.converter = dataclasses.replace(
            self.converter, payload_codec=payload_codec
        )
        
        return self
        
    def get_converter(self) -> DataConverter:
        return self.converter