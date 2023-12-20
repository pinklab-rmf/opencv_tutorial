import cv2
import numpy

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class ImgLaplace(Node):
    def __init__(self):
        super().__init__('img_laplace')

        self.declare_parameter('camera_topic', '/camera')
        
        self.declare_parameter('smoothType', 'MedianBlur')
        self.smoothType = self.get_parameter('smoothType').value

        self.declare_parameter('sigma', 3)
        self.sigma = self.get_parameter('sigma').value
        

        self.img_subscriber = self.create_subscription(
            Image,
            '/camera', # 이미지 토픽
            self.image_callback,
            10
        )

        self.img_control = self.create_publisher(Image, '/img_laplace', 10)

        self.cv_bridge = CvBridge()

    def image_callback(self, msg):
        img = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        filter_img = self.filter(img)

        pub_img = self.cv_bridge.cv2_to_imgmsg(filter_img, "bgr8")
        self.img_control.publish(pub_img)

    def filter(self, frame):
        ddepth = cv2.CV_16S

        ksize = (self.sigma*5)|1
        # Removing noise by blurring with a filter
        if self.smoothType == "GAUSSIAN":
            smoothed = cv2.GaussianBlur(frame, (ksize, ksize), self.sigma, self.sigma)
        if self.smoothType == "BLUR":
            smoothed = cv2.blur(frame, (ksize, ksize))
        if self.smoothType == "MedianBlur":
            smoothed = cv2.medianBlur(frame, ksize)

        # Apply Laplace function
        laplace = cv2.Laplacian(smoothed, ddepth, 5)
        # Converting back to uint8
        result = cv2.convertScaleAbs(laplace, (self.sigma+1)*0.25)
        return result


def main():
    rclpy.init()

    node = ImgLaplace()

    rclpy.spin(node)

    node.destroy_node()
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()