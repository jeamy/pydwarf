
import sys
import os
sys.path.append(os.getcwd())

try:
    from app.services.proto import motor_pb2
    print("ReqMotorRun fields:", list(motor_pb2.ReqMotorRun.DESCRIPTOR.fields_by_name.keys()))
    print("ReqMotorStop fields:", list(motor_pb2.ReqMotorStop.DESCRIPTOR.fields_by_name.keys()))
except Exception as e:
    print(f"Error: {e}")
