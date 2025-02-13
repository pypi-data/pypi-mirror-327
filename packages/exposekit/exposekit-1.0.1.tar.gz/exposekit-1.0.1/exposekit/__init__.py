from .tunnel import Tunnel, SSHTunnel
from .proxy import get_local_ip, handle_client, setup
"""
$credentials = Get-Content pypi.txt
$username = $credentials[0]
$password = $credentials[1]
twine upload dist/* --username $username --password $password  # or use __token__ with the API key in the password variable
"""