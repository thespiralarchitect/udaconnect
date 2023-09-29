import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:30005")
stub = location_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
msg = location_pb2.LocationMessage(
    person_id=1,
    latitude="123123",
    longitude="123123"
)


response = stub.Create(msg)
