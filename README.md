# 🏎️ INC493 Final Project — ROS 2 RC Car with micro-ROS Sensors

Final project for **INC493** (KMUTT): a 1/10-scale **F1TENTH-style RC car** running **ROS 2**,
with a **VESC** motor controller, **Hokuyo LiDAR**, a joystick for manual / autonomous mode,
and **Arduino micro-ROS** nodes streaming IMU and wheel-encoder data.

## 🧩 System Overview

```text
 Joystick ──/joy──┐
                  ├──► f1_test (my_subscriber_node) ──► /commands/motor/speed ──► VESC ──► motor
 Hokuyo ──/scan───┘                                └──► /commands/servo/position ──► steering servo

 Arduino + ICM-20948 IMU ──micro-ROS──► /imu_data, /yaw
 Arduino + wheel encoder ──micro-ROS──► RPM
```

## 📁 Repository Structure

| Path | Description |
|---|---|
| `Rccar_ws/src/f1_test/` | Main driving node: joystick manual mode + LiDAR-based autonomous mode |
| `Rccar_ws/src/combine_pkg/` | Draft launch to start VESC driver + joystick together (`launch/setup.py` is unfinished — has syntax errors) |
| `Arduino/Allnode/` | micro-ROS node: ICM-20948 IMU (DMP) + yaw + encoder RPM in one sketch |
| `Arduino/imu_uros/`, `Arduino/IMU/` | micro-ROS IMU publisher variants |
| `Arduino/encoder*/` | Wheel encoder / RPM sketches |
| `Arduino/libraries/` | Arduino libraries used (micro_ros_arduino, SparkFun ICM-20948, …) |
| `microros_ws/` | micro-ROS setup / agent workspace |

## 🕹️ Driving Modes (`f1_test`)

Controlled with the joystick buttons:

| Button | Mode |
|---|---|
| `buttons[5]` | **Manual** — joystick axes → speed and steering |
| `buttons[4]` | **Auto** — steers and sets speed from the `/scan` ranges (LiDAR-based obstacle / wall avoidance) |
| `buttons[2]` | **Stop** — steering center, motor stop |

Manual mode maps `axes[3]` → servo position (0.15–0.85) and `axes[7]` → motor speed (±1500 ERPM).
In auto mode LiDAR ranges are filtered to 0.09–9.99 m before computing steering and speed.

## 🛠️ Hardware

- RC car chassis (1/10) with **VESC** ESC and steering servo
- **Hokuyo** 2D LiDAR (`urg_node2`)
- **SparkFun ICM-20948** 9-DoF IMU + wheel encoder on Arduino (micro-ROS)
- Gamepad / joystick (`joy_node`)
- Onboard Linux computer with ROS 2

## 🚀 Run

```bash
# 1. micro-ROS agent for the Arduino (adjust the port)
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0

# 2. Car drivers and joystick
cd Rccar_ws && colcon build && source install/setup.bash
ros2 launch vesc_driver vesc_driver_node.launch.py
ros2 launch urg_node2 urg_node2.launch.py
ros2 run joy joy_node

# 3. Driving node
ros2 run f1_test f1_test_lidar
```

> Build the micro-ROS agent first with `microros_ws` — see
> [micro-ROS-and-install_rosHumble](https://github.com/Pakgard007/micro-ROS-and-install_rosHumble).

## 🔗 Related

- [ZED-2i_Lane_Object_Detection_](https://github.com/Pakgard007/ZED-2i_Lane_Object_Detection_) — perception for the full-size vehicle (F1TENTH Korea 2023)
- [micro-ROS-Digipot-Servo-Control-Node](https://github.com/Pakgard007/micro-ROS-Digipot-Servo-Control-Node)
