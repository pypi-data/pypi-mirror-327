from dataclasses import asdict
import json
from .exceptions import InitialisationError
from .helpers import ensure_cli, execute_command
from .pulse import Pulse


class Clutta:
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def new_client(self):
        try:           
            if ensure_cli():
                print("Clutta client is initialised!")
        except Exception as e:
            raise InitialisationError(f"An error occurred while creating a new Clutta client: {e}")

    def send_pulse(self, pulse: Pulse):
        payload = {**vars(pulse), "apiKey": self.api_key}
        command = f"clutta send pulse --json '{json.dumps(payload)}'"
        execute_command(command)
    
    def send_pulses(self, pulses):        
        pulses_data = [ {**asdict(pulse), "apiKey": self.api_key} for pulse in pulses]
        command = f"clutta send pulses --json '{json.dumps(pulses_data)}'"
        execute_command(command)

