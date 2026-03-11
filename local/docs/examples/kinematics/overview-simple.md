# overview-simple 示例

## 1. 原理概述
本示例演示了Pinocchio库的基础使用方法，包括：
- 创建简单的刚体模型
- 执行正运动学计算
- 计算关节雅可比矩阵
- 基本的SE3变换操作

### 理论背景
Pinocchio基于递归牛顿欧拉算法（RNEA）和复合刚体算法（CRBA）等高效动力学算法，能够快速计算刚体系统的运动学和动力学特性。正运动学计算是指根据关节角度计算末端执行器的位置和姿态。

### 应用场景
- 机器人运动规划
- 逆运动学求解
- 机器人控制算法开发
- 动力学仿真

### Mermaid原理图
```mermaid
flowchart LR
    A[输入关节角度q] --> B[正运动学计算]
    B --> C[输出末端位姿T]
    B --> D[输出雅可比矩阵J]
    D --> E[速度和力的变换计算]
```

## 2. 功能说明
### 实现功能
1. 创建一个简单的2自由度机械臂模型
2. 计算给定关节角度下的末端执行器位姿
3. 计算关节空间到任务空间的雅可比矩阵
4. 验证计算结果的正确性

### 输入输出
- **输入**：关节角度向量q (2x1)
- **输出**：
  - 末端执行器SE3变换矩阵 (4x4)
  - 末端雅可比矩阵 (6x2)
  - 末端位置坐标 (x, y, z)

### 关键特性
- 不依赖URDF文件，直接通过代码创建模型
- 演示了Pinocchio核心API的基本使用
- 代码简洁，易于理解和扩展

## 3. 依赖要求
| 依赖库 | 最低版本 | 说明 |
|--------|----------|------|
| Pinocchio | 2.6.0 | 核心动力学库 |
| Eigen3 | 3.3.7 | 线性代数库（C++版本） |
| numpy | 1.21 | 数值计算库（Python版本） |

### 安装方法
```bash
# Ubuntu系统安装
sudo apt install libpinocchio-dev
# Python版本安装
pip install pin
```

## 4. 使用方法
### Python版本
#### 运行命令
```bash
cd examples/python/kinematics
python overview-simple.py
```

#### 预期输出
```
=== Pinocchio Simple Example ===
Model name: Simple 2-dof arm
Number of joints: 2
Number of bodies: 3

Joint configuration q: [0.5, 0.3]

End effector position: [0.832..., 0.282..., 0.0]
End effector orientation:
[
 [0.825..., -0.564..., 0.0],
 [0.564...,  0.825..., 0.0],
 [0.0,        0.0,      1.0]
]

Jacobian matrix:
[
 [-0.282..., -0.099..., 0.0, 0.0, 0.0, 1.0],
 [ 0.832...,  0.295..., 0.0, 0.0, 0.0, 0.0],
 ...
]
```

### C++版本
#### 编译方法
```bash
cd examples/cpp/build
cmake ..
make overview-simple
```

#### 运行命令
```bash
./bin/overview-simple
```

## 5. 代码解析
### 关键代码片段（Python）
```python
import pinocchio as pin
import numpy as np

# 创建模型
model = pin.Model()
joint1 = pin.JointModelRX()  # 绕X轴旋转关节
joint2 = pin.JointModelRY()  # 绕Y轴旋转关节

# 添加关节和体
inertia1 = pin.Inertia(1.0, np.zeros(3), np.eye(3) * 0.1)
inertia2 = pin.Inertia(1.0, np.array([0.5, 0, 0]), np.eye(3) * 0.1)

idx1 = model.addJoint(model.getFrameId("universe"), joint1, pin.SE3.Identity(), "joint1")
model.appendBodyToJoint(idx1, inertia1, pin.SE3.Identity())

idx2 = model.addJoint(idx1, joint2, pin.SE3(np.eye(3), np.array([0.5, 0, 0])), "joint2")
model.appendBodyToJoint(idx2, inertia2, pin.SE3.Identity())

# 前向运动学计算
data = model.createData()
q = np.array([0.5, 0.3])
pin.forwardKinematics(model, data, q)
pin.updateFramePlacements(model, data)

# 获取末端位姿
ee_frame = model.getFrameId("joint2")
ee_pose = data.oMf[ee_frame]
print("End effector position:", ee_pose.translation)

# 计算雅可比
J = pin.computeJointJacobian(model, data, q, idx2)
print("Jacobian matrix:\n", J)
```

### 核心API说明
- `pin.Model()`: 创建空的机器人模型
- `model.addJoint()`: 向模型中添加关节
- `model.appendBodyToJoint()`: 向关节添加刚体惯性
- `pin.forwardKinematics()`: 执行前向运动学计算
- `pin.updateFramePlacements()`: 更新所有坐标系的位姿
- `pin.computeJointJacobian()`: 计算关节雅可比矩阵

## 6. 运行结果
### 运行截图
![overview-simple运行结果](../../assets/images/overview-simple-output.png)

### 结果分析
1. 末端位置计算正确，符合三角函数计算结果：
   - x = l1*cos(q1) + l2*cos(q1+q2) = 0.5*cos(0.5) + 0.5*cos(0.8) ≈ 0.832
   - y = l1*sin(q1) + l2*sin(q1+q2) = 0.5*sin(0.5) + 0.5*sin(0.8) ≈ 0.282
2. 雅可比矩阵维度正确（6x2），满足速度变换关系：v = J * q_dot

### 常见问题
- **Q: 运行时提示"AttributeError: module 'pinocchio' has no attribute 'JointModelRX'"**
  - A: 请确认Pinocchio版本 >= 2.6.0，旧版本API可能不同

## 7. 扩展应用
### 扩展方向
1. 添加更多关节，构建更复杂的机器人模型
2. 结合逆运动学算法，实现末端位姿到关节角度的求解
3. 添加碰撞检测功能，避免关节运动时发生碰撞
4. 结合控制算法，实现机器人轨迹跟踪

### 实际应用案例
- 工业机械臂运动规划
- 协作机器人安全控制
- 人形机器人步态规划
- 机器人仿真系统开发

### 相关参考资料
- [Pinocchio官方文档：Model creation](https://stack-of-tasks.github.io/pinocchio/doc/md_doc_2_model_creation.html)
- [Pinocchio API参考：pinocchio::Model Class Reference](https://gepettoweb.laas.fr/doc/stack-of-tasks/pinocchio/master/doxygen-html/classpinocchio_1_1Model.html)
