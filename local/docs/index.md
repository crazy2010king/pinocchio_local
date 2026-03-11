# Pinocchio示例程序文档总览

欢迎来到Pinocchio示例程序文档中心！这里包含了所有示例的详细说明、原理讲解和使用指南。

## 1. 快速导航

### 📐 运动学类示例
| 示例名称 | 功能说明 | 语言 |
|---------|---------|------|
| [overview-simple](examples/kinematics/overview-simple.md) | 简单运动学计算示例 | Python/C++ |
| [overview-urdf](examples/kinematics/overview-urdf.md) | URDF模型加载和运动学计算 | Python/C++ |
| [overview-SE3](examples/kinematics/overview-SE3.md) | SE3变换操作示例 | Python/C++ |
| [overview-lie](examples/kinematics/overview-lie.md) | 李代数运算示例 | Python/C++ |
| [kinematics-derivatives](examples/kinematics/kinematics-derivatives.md) | 运动学导数计算 | Python/C++ |
| [build-reduced-model](examples/kinematics/build-reduced-model.md) | 简化模型构建 | Python/C++ |

### ⚙️ 动力学类示例
| 示例名称 | 功能说明 | 语言 |
|---------|---------|------|
| [inverse-dynamics](examples/dynamics/inverse-dynamics.md) | 逆动力学计算（RNEA） | Python/C++ |
| [forward-dynamics-derivatives](examples/dynamics/forward-dynamics-derivatives.md) | 正动力学导数计算 | Python/C++ |
| [inverse-dynamics-derivatives](examples/dynamics/inverse-dynamics-derivatives.md) | 逆动力学导数计算 | Python/C++ |
| [contact-dynamics](examples/dynamics/contact-dynamics.md) | 接触动力学计算 | Python |
| [contact-cholesky](examples/dynamics/contact-cholesky.md) | 接触动力学Cholesky分解 | Python |

### 💥 碰撞检测类示例
| 示例名称 | 功能说明 | 语言 |
|---------|---------|------|
| [collisions](examples/collision/collisions.md) | 碰撞检测示例 | Python/C++ |
| [collision-with-point-clouds](examples/collision/collision-with-point-clouds.md) | 点云碰撞检测 | Python |
| [geometry-models](examples/collision/geometry-models.md) | 几何模型处理 | Python/C++ |
| [capsule-approximation](examples/collision/capsule-approximation.md) | 胶囊体近似 | Python |

### 🎮 仿真类示例
| 示例名称 | 功能说明 | 语言 |
|---------|---------|------|
| [simulation-pendulum](examples/simulation/simulation-pendulum.md) | 单摆仿真 | Python |
| [simulation-inverted-pendulum](examples/simulation/simulation-inverted-pendulum.md) | 倒立摆仿真 | Python |
| [simulation-contact-dynamics](examples/simulation/simulation-contact-dynamics.md) | 接触动力学仿真 | Python |
| [anymal-simulation](examples/simulation/anymal-simulation.md) | Anymal机器人仿真（无可视化） | Python |
| [cassie-simulation](examples/simulation/cassie-simulation.md) | Cassie机器人仿真（无可视化） | Python |

### 🔢 自动微分类示例
| 示例名称 | 功能说明 | 语言 |
|---------|---------|------|
| [cppad-basic](examples/autodiff/cppad-basic.md) | CppAD自动微分基础 | C++/Python |
| [cppad-kinematics](examples/autodiff/cppad-kinematics.md) | 运动学自动微分 | C++/Python |
| [cppad-dynamics](examples/autodiff/cppad-dynamics.md) | 动力学自动微分 | C++/Python |

## 2. 文档使用说明

### 文档结构
每个示例文档都包含以下部分：
1. **原理概述**：算法原理和理论背景
2. **功能说明**：示例实现的功能和输入输出
3. **依赖要求**：所需依赖库和安装方法
4. **使用方法**：编译和运行说明
5. **代码解析**：关键代码和API调用讲解
6. **运行结果**：运行截图和结果分析
7. **扩展应用**：扩展方向和实际应用案例

### 符号说明
- 📝 注意事项
- ⚠️  警告信息
- 💡 提示和技巧
- 🔗 相关参考链接

## 3. 相关资源

### 官方资源
- [Pinocchio官方网站](https://stack-of-tasks.github.io/pinocchio/)
- [Pinocchio GitHub仓库](https://github.com/stack-of-tasks/pinocchio)
- [Pinocchio API文档](https://gepettoweb.laas.fr/doc/stack-of-tasks/pinocchio/master/doxygen-html/)

### 学习资源
- [刚体动力学教程](https://www.springer.com/gp/book/9780387743141)
- [机器人学导论](https://www.cambridge.org/core/books/introduction-to-robotics/9E7F8E8D6F3A7E4B7D3E2C5A7B8C9D0E)

## 4. 贡献指南
欢迎贡献新的示例和改进文档！请参考[贡献指南](contributing.md)了解详细流程。
