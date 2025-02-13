import unittest
from unittest.mock import patch, MagicMock
from exposekit.tunnel import Tunnel, SSHTunnel
import subprocess

class TestTunnel(unittest.TestCase):
    @patch('requests.get')
    def test_get_public_ip(self, mock_get):
        mock_get.return_value.json.return_value = {'ip': '123.123.123.123'}
        tunnel = Tunnel(None, 5000)
        ip = tunnel.get_public_ip()
        self.assertEqual(ip, '123.123.123.123')

    @patch('socket.socket')
    def test_host(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance

        tunnel = Tunnel('123.123.123.123', 5000)
        with patch.object(tunnel, 'get_public_ip', return_value='123.123.123.123'):
            tunnel.host('123.123.123.123')

        mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_sock_instance.bind.assert_called_once_with(('123.123.123.123', 5000))
        mock_sock_instance.listen.assert_called_once_with(5)
        mock_sock_instance.accept.assert_called()

class TestSSHTunnel(unittest.TestCase):
    @patch('subprocess.Popen')
    def test_run(self, mock_popen):
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        mock_process.communicate.return_value = (b'Output', b'')
        mock_process.returncode = 0

        ssh_tunnel = SSHTunnel(5000)
        ssh_tunnel.run()

        mock_popen.assert_called_once_with(
            'ssh -R 80:localhost:5000 ssh.localhost.run', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

if __name__ == '__main__':
    unittest.main()
