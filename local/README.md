# Pinocchio示例程序集合

本项目是Pinocchio机器人动力学库的示例程序集合，包含了运动学、动力学、碰撞检测、仿真、自动微分等各个功能模块的可运行示例，方便学习和参考。

## 1. 项目介绍

### Pinocchio库简介
Pinocchio是一个高效的机器人动力学库，实现了刚体动力学的各种算法，包括：
- 正逆运动学
- 雅可比计算
- 正逆动力学（RNEA、CRBA、ABA算法）
- 碰撞检测
- 自动微分
- 刚体系统仿真

### 示例集合概述
本示例集合包含约56个可运行的示例，分为以下类别：
- 📐 **运动学类**：正逆运动学、SE3变换、李代数运算等
- ⚙️ **动力学类**：正逆动力学、动力学导数计算、接触动力学等
- 💥 **碰撞检测类**：碰撞检测、距离计算、几何模型处理等
- 🎮 **仿真类**：刚体系统仿真、摆系统仿真、接触仿真等
- 🔢 **自动微分类**：基于CppAD的自动微分功能示例

### 平台环境说明
- 操作系统：Ubuntu 22.04 LTS
- CPU架构：x86_64
- Python版本：3.10+
- Pinocchio版本：2.6.x
- 依赖库：eigen3, hpp-fcl, numpy, scipy, matplotlib等

## 2. 快速开始

### 环境配置指南
#### 依赖安装
```bash
# 安装系统依赖
sudo apt install libeigen3-dev libhpp-fcl-dev liburdfdom-dev

# 安装Python依赖
pip install pin numpy scipy matplotlib
```

### 示例编译方法
#### C++示例编译
```bash
# 进入脚本目录
cd scripts

# 编译所有C++示例
./build_cpp_examples.sh
```

### 一键运行说明
```bash
# 检查依赖是否完整
./scripts/check_dependencies.py

# 运行所有示例
./scripts/run_all_examples.sh

# 运行指定类别的示例
./scripts/run_all_examples.sh --category kinematics

# 运行单个示例
./scripts/run_all_examples.sh --example overview-urdf.py

# 生成测试报告
./scripts/generate_report.py
```

## 3. 目录结构说明

```
local/
├── README.md                # 总览文档
├── docs/                    # 文档目录
│   ├── index.md             # 文档主页
│   ├── examples/            # 各个示例的详细文档
│   └── assets/              # 文档资源
├── examples/                # 示例程序
│   ├── cpp/                 # C++示例
│   └── python/              # Python示例
├── scripts/                 # 工具脚本
├── test_results/            # 测试结果目录
└── config/                  # 配置文件
```

## 4. 开发指南

### 贡献新示例的方法
1. 将示例代码放入对应类别的目录
2. 在`config/examples_config.json`中添加示例配置
3. 编写对应的文档放入`docs/examples/`对应目录
4. 测试示例可以正常运行

### 文档编写规范
- 使用Markdown格式，遵循GFM规范
- 文件名与示例程序名保持一致
- 每个示例文档采用统一的结构
- 关键代码添加注释说明
- 注明对应Pinocchio版本和依赖版本

### 常见问题解答
#### Q: 示例运行失败怎么办？
A: 首先运行`check_dependencies.py`检查依赖是否完整，查看`test_results/logs/`下的日志文件定位错误原因。

#### Q: 如何添加新的依赖？
A: 在`config/examples_config.json`中对应示例的`dependencies`字段添加依赖名称，然后在`check_dependencies.py`中添加依赖检查逻辑。

## 5. 附录

### 依赖版本对照表
| 依赖库 | 最低版本 | 推荐版本 |
|--------|----------|----------|
| Pinocchio | 2.6.0 | 2.6.20 |
| Eigen3 | 3.3.7 | 3.4.0 |
| hpp-fcl | 2.1.0 | 2.3.0 |
| Python | 3.8 | 3.10 |
| numpy | 1.21 | 1.24 |

### API速查表
- 完整API文档：https://gepettoweb.laas.fr/doc/stack-of-tasks/pinocchio/master/doxygen-html/

### 参考文献
- [Pinocchio官方文档](https://stack-of-tasks.github.io/pinocchio/)
- [Pinocchio GitHub仓库](https://github.com/stack-of-tasks/pinocchio)
