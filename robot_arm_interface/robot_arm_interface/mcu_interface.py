#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import serial
import math

class UARTBridge(Node):
    def __init__(self):
        super().__init__('uart_interface_node')
        
        # UART configuration - hardcoded to ttyACM0
        self.port_name = '/dev/ttyACM0'
        self.baud_rate = 115200
        self.serial_port = None
        
        # Joint configuration
        self.joint_names = ["base_joint", "joint2", "joint3", "joint4", "end_effector_joint"]
        self.current_angles = [90.0] * 5  # Default to 90 degrees
        
        # Initialize serial port
        self.init_serial()
        
        # Create subscriber
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10)
        
        self.get_logger().info("UART Bridge Node initialized")

    def init_serial(self):
        """Initialize serial connection to ttyACM0"""
        try:
            self.serial_port = serial.Serial(
                port=self.port_name,
                baudrate=self.baud_rate,
                timeout=1
            )
            self.get_logger().info(f"Connected to {self.port_name} at {self.baud_rate} baud")
        except Exception as e:
            self.get_logger().error(f"Failed to open {self.port_name}: {str(e)}")
            self.serial_port = None

    def joint_state_callback(self, msg):
        """Process incoming joint state messages"""
        # Update current angles from message
        for i, name in enumerate(self.joint_names):
            try:
                idx = msg.name.index(name)
                # Convert from radians to degrees (with 90° offset)
                self.current_angles[i] = (msg.position[idx] * 180.0 / math.pi) + 90
            except ValueError:
                pass  # Joint name not found in message
        
        # Send angles to microcontroller
        self.send_angles()

    def send_angles(self):
        """Send current angles to microcontroller via UART"""
        if not self.serial_port:
            self.get_logger().warn("Serial port not connected")
            return
        
        # Create message: "angle1,angle2,angle3,angle4,angle5\n"
        angle_str = ",".join([str(int(angle)) for angle in self.current_angles]) + "\n"
        try:
            self.serial_port.write(angle_str.encode())
            self.get_logger().info(f"Sent angles: {angle_str.strip()}")
        except Exception as e:
            self.get_logger().error(f"Failed to send angles: {str(e)}")
            # Attempt to reconnect
            self.init_serial()

    def destroy_node(self):
        """Cleanup before shutdown"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    
    node = UARTBridge()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()