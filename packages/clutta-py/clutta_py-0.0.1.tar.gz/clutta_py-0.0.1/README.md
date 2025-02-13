# Clutta-Python SDK

Clutta-Python is the official Python SDK for interacting with Clutta, a platform for observability and monitoring. 
Use this SDK to send pulse data, either individually or in batches, with ease and reliability.

---

## Installation

To add Clutta-Go to your Go project, use the following command:

```python
pip install clutta-py
```

## Features
- **Effortless Integration**: Simple setup with reusable client initialization.
- **Single Pulse Support**: Send individual data points with precision.
- **Batch Processing**: Transmit multiple data points efficiently in one operation.

# Getting Started

## 1. Initialize the Client
   This involves setting up the client once and reusing it across your application. Copy the code below into a new python file or into your preferred location.

   ```python
    import os
    from dotenv import load_dotenv
    from clutta.core import Clutta
    from clutta.pulse import Pulse


    load_dotenv() # To load your API key and other sensitive information from your environment or .env file.

    api_key=os.getenv("API_KEY")

    # Set up your new Clutta client called "test" with your API key
    test=Clutta(api_key)
    test.new_client()
   ```

## 2. Sending a Pulse
   You can then send an individual pulse for targeted updates. Copy and paste the following code inside the same file as above. Remember to replace the placeholder values of the signatureId, chainId etc. with actual values from your Clutta account.

   ```python
    # Create a pulse
    pulse1=Pulse(
        signatureId="unique-signature-id",
        chainId="unique-chain-id",
        correlationId="unique-correlation-id",
        sourceId="your-source",
        userId="your user-id",
        status=1, # Status: 0 for unknown, 1 for success, 2 for failure
        statusDescription="Success"
        )

    # Send the pulse
    test.send_pulse(pulse1)
   ```

## 3. Sending Multiple Pulses
   You can also Ooptimize performance by sending pulses in bulk. Copy and paste the following code as well. Remember to replace placeholder values as needed.

   ```python
    # Create 2 pulses
    pulse2=Pulse(
        signatureId="unique-signature-id",
        chainId="unique-chain-id",
        correlationId="unique-correlation-id",
        sourceId="your-source",
        userId="your user-id",
        status=1, # Status: 0 for unknown, 1 for success, 2 for failure
        statusDescription="Success"
        )
    
    pulse3=Pulse(
        signatureId="unique-signature-id",
        chainId="unique-chain-id",
        correlationId="unique-correlation-id",
        sourceId="your-source",
        userId="your user-id",
        status=1, # Status: 0 for unknown, 1 for success, 2 for failure
        statusDescription="Success"
        )
    
    # Send the pulses in bulk as a list
    test.send_pulses([pulse2,pulse3])
   ```

# License

Clutta-Python is open-source and licensed under the MIT License. Contributions are welcome.


# Support

For technical support, documentation, or to report issues, visit the Clutta Documentation or contact our support team.


# About Clutta

Clutta is redefining observability with cutting-edge tools designed to help organizations monitor, analyze, and optimize their systems. 
Whether you're scaling to millions of users or managing critical infrastructure, Clutta provides the insights you need to excel.



