import socket
import struct
import logging


class TFTPHandler:
    def __init__(self, host, port=69):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(5.0)
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


    def _send_rrq(self, filename):
        """Gửi yêu cầu đọc (RRQ) tới máy chủ TFTP.

        Args:
            filename (str): Tên của file cần đọc.
        """
        logging.debug(f"Sending RRQ for file {filename}")
        # Mã lệnh RRQ là 01, chế độ thường là 'octet' (truyền nhị phân)
        mode = "octet"
        rrq_packet = struct.pack(f"!H{len(filename)+1}s{len(mode)+1}s", 1, filename.encode(), mode.encode())

        # Gửi yêu cầu RRQ tới máy chủ
        self.sock.sendto(rrq_packet, (self.host, self.port))

    def _send_wrq(self, filename):
        """Gửi yêu cầu ghi (WRQ) tới máy chủ TFTP.

        Args:
            filename (str): Tên của file cần ghi.
        """
        # Mã lệnh WRQ là 02, chế độ thường là 'octet' (truyền nhị phân)
        mode = "octet"
        wrq_packet = struct.pack(f"!H{len(filename)+1}s{len(mode)+1}s", 2, filename.encode(), mode.encode())

        # Gửi yêu cầu WRQ tới máy chủ
        self.sock.sendto(wrq_packet, (self.host, self.port))

    def _send_data(self, block_number, data):
        """Gửi gói tin DATA tới máy chủ TFTP.

        Args:
            block_number (int): Số block của gói tin DATA.
            data (bytes): Dữ liệu của gói tin.
        """
        data_packet = struct.pack(f"!HH{len(data)}s", 3, block_number, data)
        self.sock.sendto(data_packet, (self.host, self.port))

    def _recv_ack(self):
        """Nhận gói tin ACK từ máy chủ TFTP.

        Returns:
            tuple: Mã lệnh và số block của gói tin ACK.
        """
        data, _ = self.sock.recvfrom(4096)
        opcode, block_number = struct.unpack('!HH', data[:4])
        return opcode, block_number

    def upload(self, local_file_path, remote_file_name):
        """Tải lên file tới máy chủ TFTP.

        Args:
            local_file_path (str): Đường dẫn file cục bộ cần tải lên.
            remote_file_name (str): Tên file trên máy chủ TFTP.
        """
        # Gửi WRQ
        self._send_wrq(remote_file_name)

        # Chờ ACK cho WRQ
        opcode, block_number = self._recv_ack()
        if opcode != 4 or block_number != 0:
            raise Exception("Không nhận được ACK cho WRQ")

        # Đọc và gửi file
        with open(local_file_path, 'wb') as file:
            block_number = 1
            while True:
                # Nhận gói tin dữ liệu
                received_block, data = self._recv_data()

                # Thêm log để kiểm tra số block
                print(f"Expected block: {block_number}, Received block: {received_block}")

                if received_block != block_number:
                    raise Exception("Số block không khớp")
                
                data = file.read(512)  # Đọc tối đa 512 byte
                self._send_data(block_number, data)

                # Chờ ACK cho gói tin DATA
                opcode, received_block = self._recv_ack()
                if opcode != 4 or received_block != block_number:
                    raise Exception("Không nhận được ACK cho gói tin DATA")

                # Kiểm tra điều kiện kết thúc
                if len(data) < 512:
                    break

                block_number += 1

    def download(self, remote_file_name, local_file_path):
        """Tải xuống file từ máy chủ TFTP.

        Args:
            remote_file_name (str): Tên file trên máy chủ TFTP.
            local_file_path (str): Đường dẫn lưu file cục bộ.
        """
        logging.info(f"Starting download of {remote_file_name} to {local_file_path}")
        # Gửi yêu cầu đọc (RRQ)
        self._send_rrq(remote_file_name)
        
        with open(local_file_path, 'wb') as file:
            block_number = 1
            while True:
                # Nhận gói tin dữ liệu
                received_block, data = self._recv_data()
                print(received_block, block_number)
                # Kiểm tra số block nhận được
                if received_block != block_number:
                    logging.warning(f"Mismatch in block number. Expected: {block_number}, Received: {received_block}")
                    self._send_ack(received_block)
                    continue

                # Ghi dữ liệu vào file cục bộ
                file.write(data)

                # Gửi ACK cho gói tin dữ liệu này
                self._send_ack(received_block)

                # Kiểm tra điều kiện kết thúc (gói tin dữ liệu ngắn hơn 512 byte)
                if len(data) < 512:
                    break

                block_number += 1
                
    def _recv_data(self):
        """Nhận gói tin dữ liệu từ máy chủ TFTP.

        Returns:
            tuple: Số block và dữ liệu nhận được.
        """
        logging.debug("Waiting to receive data packet")
        try:
            data, _ = self.sock.recvfrom(4096)
            if len(data) < 4:
                raise Exception("Gói tin nhận được không hợp lệ")

            opcode, block = struct.unpack('!HH', data[:4])

            if opcode == 3:  # DATA packet
                logging.debug(f"Received DATA packet with block number {block}")
                return block, data[4:]
            elif opcode == 5:  # Error packet
                
                if len(data) >= 5:
                    error_msg = data[4:].decode().strip('\x00')
                else:
                    error_msg = "Unknown error"
                logging.error(f"Received ERROR packet: {error_msg}")
                raise Exception(f"Error from server: {error_msg}")
            else:
                raise Exception(f"Unexpected opcode received: {opcode}")
        except socket.timeout:
            # Xử lý timeout ở đây
            logging.error("Timeout occurred while waiting for a response from the server")
            raise Exception("Timeout khi chờ phản hồi từ máy chủ")

    def _send_ack(self, block_number):
        """Gửi gói tin ACK tới máy chủ TFTP.

        Args:
            block_number (int): Số block của gói tin dữ liệu được xác nhận.
        """
        logging.debug(f"Sending ACK for block number {block_number}")
        ack_packet = struct.pack('!HH', 4, block_number)
        self.sock.sendto(ack_packet, (self.host, self.port))
        
    def close(self):
        self.sock.close()

# Sử dụng TFTPClient
# host = '192.168.64.10'
# client = TFTPHandler(host)
# client.download_file('/srv/tftp/up.pdf', '/Users/haison/Downloads/up.pdf')
# client.close()
