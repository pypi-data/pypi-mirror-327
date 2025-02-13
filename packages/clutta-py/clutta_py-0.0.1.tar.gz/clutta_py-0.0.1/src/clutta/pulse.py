from dataclasses import dataclass

@dataclass
class Pulse:
    signatureId: str
    chainId: str
    correlationId: str
    sourceId: str
    userId: str
    status: int
    statusDescription: str


    