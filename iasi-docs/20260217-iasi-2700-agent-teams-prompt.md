# iasi-2700 Machine 创建 - Agent Teams 并行执行提示词

## 使用说明

1. 在 Claude Code 中开启新会话
2. 将下方"主协调 Agent 提示词"完整复制给 Claude
3. Claude 会自动创建 Team 并并行调度子 Agent 执行任务

---

## 主协调 Agent 提示词（完整复制此部分给 Claude）

```
请作为 Agent Teams 的主协调者，帮我完成在社区 OpenBMC 中添加 iasi-2700 machine 的任务。

## 前置信息
- 工作目录：/home/iasi/workspace/openbmc
- ASPEED 参考仓库：/home/iasi/workspace/aspeed-openbmc
- 目标 machine：iasi-2700（基于 AST2700 SoC）
- 参考配置：ast2700-default（标准 128MB SPI Flash）

## 你的任务（按顺序执行）

### 第一步：创建目录结构
首先创建以下目录：
- meta-iasi/conf/
- meta-iasi/conf/machine/
- meta-iasi/recipes-bsp/u-boot/
- meta-iasi/recipes-kernel/linux/linux-aspeed/

### 第二步：创建 Agent Team 并并行分配任务

使用 TeamCreate 创建一个名为 "iasi-2700-team" 的团队，然后并行启动 3 个子 Agent：

**重要提示**：
- 每个子 Agent 只负责自己的文件，互不依赖
- 使用并行方式同时启动所有 Agent
- 你必须等待所有 Agent 报告完成后再进行验证
- **不要**在子 Agent 没有返回时自己去做他们的工作

#### 并行启动 Agent 1（Layer 配置专家）
名称：layer-agent
任务：创建 meta-iasi/conf/layer.conf

参考文件：
- /home/iasi/workspace/openbmc/meta-facebook/meta-yosemite5/conf/layer.conf
- /home/iasi/workspace/openbmc/meta-evb/meta-evb-aspeed/meta-evb-ast2600/conf/layer.conf

内容要求：
```bitbake
# We have a conf and classes directory, add to BBPATH
BBPATH .= ":${LAYERDIR}"

# We have recipes-* directories, add to BBFILES
BBFILES += "${LAYERDIR}/recipes-*/*/*.bb \
            ${LAYERDIR}/recipes-*/*/*.bbappend"

BBFILE_COLLECTIONS += "iasi"
BBFILE_PATTERN_iasi = "^${LAYERDIR}/"
BBFILE_PRIORITY_iasi = "10"

LAYERDEPENDS_iasi = "core \
                     openembedded-layer \
                     networking-layer \
                     meta-python \
                     phosphor-layer \
                     aspeed-layer \
                    "

LAYERSERIES_COMPAT_iasi = "scarthgap"
```

#### 并行启动 Agent 2（Machine 配置专家）
名称：machine-agent
任务：创建 meta-iasi/conf/machine/iasi-2700.conf

参考文件：
- /home/iasi/workspace/aspeed-openbmc/meta-aspeed-sdk/meta-ast2700-sdk/conf/machine/ast2700-default.conf
- /home/iasi/workspace/openbmc/meta-evb/meta-evb-aspeed/meta-evb-ast2600/conf/machine/evb-ast2600.conf
- /home/iasi/workspace/openbmc/meta-aspeed/conf/machine/include/ast2700.inc

内容要求：
```bitbake
# iasi-2700 Machine Configuration
# Based on AST2700 SoC with 128MB SPI Flash

# Device Tree Configuration
KERNEL_DEVICETREE = "aspeed/ast2700-evb.dtb"
UBOOT_DEVICETREE = "ast2700-evb"
UBOOT_MACHINE = "evb-ast2700_defconfig"
KBUILD_DEFCONFIG = "aspeed_g7_defconfig"

# Include base configurations
require conf/machine/include/ast2700.inc
include conf/machine/include/obmc-bsp-common.inc

# Secure boot disabled by default
SOCSEC_SIGN_ENABLE = "0"

# Flash layout - 128MB standard configuration
FLASH_SIZE = "131072"
FLASH_UBOOT_OFFSET = "0"
FLASH_UBOOT_ENV_OFFSET = "4096"
FLASH_KERNEL_OFFSET = "4224"
FLASH_ROFS_OFFSET = "13440"
FLASH_RWFS_OFFSET = "98304"
RWFS_SIZE = "33554432"

# Serial console configuration
SERIAL_CONSOLES = "115200;ttyS12"

# Machine features
MACHINE_FEATURES += "\
    obmc-phosphor-fan-mgmt \
    obmc-phosphor-chassis-mgmt \
    obmc-phosphor-flash-mgmt \
    obmc-host-ipmi \
    obmc-host-state-mgmt \
    obmc-chassis-state-mgmt \
    obmc-bmc-state-mgmt \
    "

# Provider configuration
PREFERRED_PROVIDER_virtual/obmc-system-mgmt ?= "packagegroup-obmc-apps"
PREFERRED_PROVIDER_virtual/obmc-host-ipmi-hw ?= "phosphor-ipmi-kcs"
VIRTUAL-RUNTIME_obmc-host-state-manager ?= "x86-power-control"
VIRTUAL-RUNTIME_obmc-chassis-state-manager ?= "x86-power-control"

# MCTP support
include conf/distro/include/mctp.inc
```

#### 并行启动 Agent 3（BSP 配方专家）
名称：bsp-agent
任务：创建以下 3 个文件

文件 1：meta-iasi/recipes-bsp/u-boot/u-boot-aspeed_%.bbappend
```bitbake
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

# iasi-2700 uses standard evb-ast2700 configuration
# Override here if needed
```

文件 2：meta-iasi/recipes-kernel/linux/linux-aspeed_%.bbappend
```bitbake
FILESEXTRAPATHS:prepend := "${THISDIR}/linux-aspeed:"

SRC_URI += "file://iasi-2700.cfg"
```

文件 3：meta-iasi/recipes-kernel/linux/linux-aspeed/iasi-2700.cfg
```
# iasi-2700 specific kernel configurations
# Add specific driver configurations here as needed
# Example:
# CONFIG_I2C_ASPEED=y
# CONFIG_SPI_ASPEED=y
```

### 第三步：等待所有 Agent 完成

**重要**：
- 等待所有 3 个 Agent 都报告任务完成
- 如果某个 Agent 报告错误或未完成，不要代替它完成工作
- 可以通过询问 Agent 状态来确认进度

### 第四步：验证和汇总

当收到所有 Agent 完成报告后，执行以下验证：

1. 列出 meta-iasi 目录结构：`tree meta-iasi/`
2. 验证每个文件是否存在：
   - meta-iasi/conf/layer.conf
   - meta-iasi/conf/machine/iasi-2700.conf
   - meta-iasi/recipes-bsp/u-boot/u-boot-aspeed_%.bbappend
   - meta-iasi/recipes-kernel/linux/linux-aspeed_%.bbappend
   - meta-iasi/recipes-kernel/linux/linux-aspeed/iasi-2700.cfg
3. 验证文件语法（检查是否有明显错误）
4. 输出最终目录结构树
5. 提供构建验证命令：

```bash
# 构建验证命令
cd /home/iasi/workspace/openbmc
source setup iasi-2700
bitbake core-image-minimal
```

## 任务完成标准

- [ ] 目录结构创建完成
- [ ] Team 创建成功
- [ ] 3 个 Agent 全部启动（并行）
- [ ] Agent 1 报告 layer.conf 创建完成
- [ ] Agent 2 报告 iasi-2700.conf 创建完成
- [ ] Agent 3 报告 3 个 BSP 文件创建完成
- [ ] 所有文件验证通过
- [ ] 构建命令已输出

## 注意事项

1. **并行执行**：3 个 Agent 应该同时启动，而不是等待一个完成再启动下一个
2. **不代劳**：作为 Lead Agent，你只负责协调和验证，不要自己创建文件
3. **等待反馈**：必须收到 Agent 的完成确认后才进行验证步骤
```

---

## 备选方案：简化单 Agent 执行

如果 Teams 功能不可用，使用以下简化提示词：

```
请在 /home/iasi/workspace/openbmc 中创建 iasi-2700 machine 配置。

需要创建的文件：

1. meta-iasi/conf/layer.conf
2. meta-iasi/conf/machine/iasi-2700.conf
3. meta-iasi/recipes-bsp/u-boot/u-boot-aspeed_%.bbappend
4. meta-iasi/recipes-kernel/linux/linux-aspeed_%.bbappend
5. meta-iasi/recipes-kernel/linux/linux-aspeed/iasi-2700.cfg

具体内容参考 /home/iasi/workspace/openbmc/iasi-docs/20260217-iasi-2700-agent-teams-prompt.md 中的详细配置。

完成后：
1. 列出创建的所有文件
2. 输出目录结构
3. 提供构建命令：cd /home/iasi/workspace/openbmc && source setup iasi-2700 && bitbake core-image-minimal
```

---

## 参考文件路径速查

| 文件 | 路径 |
|------|------|
| AST2700 基础配置 | /home/iasi/workspace/openbmc/meta-aspeed/conf/machine/include/ast2700.inc |
| AST2600 EVB 参考 | /home/iasi/workspace/openbmc/meta-evb/meta-evb-aspeed/meta-evb-ast2600/conf/machine/evb-ast2600.conf |
| ASPEED ast2700-default | /home/iasi/workspace/aspeed-openbmc/meta-aspeed-sdk/meta-ast2700-sdk/conf/machine/ast2700-default.conf |
| meta-yosemite5 layer.conf | /home/iasi/workspace/openbmc/meta-facebook/meta-yosemite5/conf/layer.conf |
