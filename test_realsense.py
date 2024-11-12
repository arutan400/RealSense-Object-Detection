import pyrealsense2 as rs

def test_realsense():
    ctx = rs.context()
    if len(ctx.devices) == 0:
        print("No device connected")
    else:
        print("Device connected")

if __name__ == "__main__":
    test_realsense()