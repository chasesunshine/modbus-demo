from pymodbus.client import ModbusTcpClient, ModbusSerialClient
from pymodbus.exceptions import ModbusException
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from pymodbus.constants import Endian

# modbus工具类
class ModbusClient:
    def __init__(self, connection_type='tcp', **kwargs):
        self.connection_type = connection_type
        self.client = None

        if connection_type == 'tcp' or connection_type == 'ip':
            self.client = ModbusTcpClient(
                host=kwargs.get('host', 'localhost'),
                port=kwargs.get('port', 502),
                timeout=kwargs.get('timeout', 3)
            )
        elif connection_type == 'rtu':
            self.client = ModbusSerialClient(
                method='rtu',
                port=kwargs.get('port', 'COM1'),
                baudrate=kwargs.get('baudrate', 9600),
                stopbits=kwargs.get('stopbits', 1),
                bytesize=kwargs.get('bytesize', 8),
                parity=kwargs.get('parity', 'N'),
                timeout=kwargs.get('timeout', 3)
            )
        elif connection_type == 'ASCII':
            self.client = ModbusSerialClient(
                method='rtu',
                port=kwargs.get('port', 'COM1'),
                baudrate=kwargs.get('baudrate', 9600),
                stopbits=kwargs.get('stopbits', 1),
                bytesize=kwargs.get('bytesize', 8),
                parity=kwargs.get('parity', 'N'),
                timeout=kwargs.get('timeout', 3)
            )

    def connect(self):
        """建立连接"""
        return self.client.connect()

    def disconnect(self):
        """断开连接"""
        self.client.close()

    def read_holding_registers(self, address, count, slave=1):
        """读取保持寄存器"""
        try:
            result = self.client.read_holding_registers(address, count, slave=slave)
            if result.isError():
                return None, str(result)
            return result.registers, None
        except ModbusException as e:
            return None, str(e)

    def read_coils(self, address, count, slave=1):
        """读取线圈状态"""
        try:
            result = self.client.read_coils(address, count, slave=slave)
            if result.isError():
                return None, str(result)
            return result.bits, None
        except ModbusException as e:
            return None, str(e)

    def write_register(self, address, value, slave=1):
        """写入单个寄存器"""
        try:
            result = self.client.write_register(address, value, slave=slave)
            if result.isError():
                return str(result)
            return None
        except ModbusException as e:
            return str(e)

    def read_float(self, address, slave=1):
        """读取浮点数（32位，占用2个寄存器）"""
        try:
            result = self.client.read_holding_registers(address, 2, slave=slave)
            if result.isError():
                return None, str(result)

            decoder = BinaryPayloadDecoder.fromRegisters(
                result.registers,
                byteorder=Endian.BIG,
                wordorder=Endian.BIG
            )
            float_value = decoder.decode_32bit_float()
            return float_value, None
        except ModbusException as e:
            return None, str(e)


# 使用示例
if __name__ == "__main__":
    # TCP 连接示例
    modbus_tcp = ModbusClient(
        connection_type='tcp',
        host='192.168.1.100',
        port=502
    )

    if modbus_tcp.connect():
        registers, error = modbus_tcp.read_holding_registers(0, 10)
        if error:
            print(f"读取错误: {error}")
        else:
            print(f"寄存器值: {registers}")

        modbus_tcp.disconnect()