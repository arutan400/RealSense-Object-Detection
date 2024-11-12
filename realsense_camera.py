import pyrealsense2 as rs
import numpy as np

class RealsenseCamera:
    def __init__(self):
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)  # フレームレートを15に変更
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)  # フレームレートを15に変更

        # Check if a device is connected
        ctx = rs.context()
        devices = ctx.query_devices()
        if len(devices) == 0:
            print("No device connected")
            exit(1)
        else:
            for i, device in enumerate(devices):
                print(f"Device {i}: {device.get_info(rs.camera_info.name)}")

        # Start streaming
        self.pipeline.start(config)

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            return None, None

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        return depth_image, color_image

    def get_frame_stream(self):
        frames = self.pipeline.wait_for_frames(10000)  # 待ち時間を10秒に延長
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            return False, None, None

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        return True, color_image, depth_image

    def release(self):
        self.pipeline.stop()