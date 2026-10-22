# 蜜桃猫 · Peach Cat Pet

一只陪你工作的蜜桃猫：**跑动时收起电脑，处理工作时敲蓝色电脑**。

| 跑步 | 处理工作 | 等待回应 |
| --- | --- | --- |
| ![跑步](previews/running-right.gif) | ![工作](previews/running.gif) | ![等待](previews/waiting.gif) |

提供 9 种状态动画，以及完整 v2 素材中的 16 个视线方向。无需重新生成图片。

v1.0.4 保留原图中两个已选定的走路关键姿势及其头身比例、肚子和腿部轮廓，只补充衔接帧组成八帧循环。移动时不带电脑，工作时继续敲电脑。可查看[关键帧与过渡帧](previews/walking-keyposes.png)。

## 快速安装到 Codex

需要 Python 3.9+，无需 pip、API Key 或额外依赖。适用于支持本地自定义宠物目录的 Codex 客户端。

macOS / Linux：

```bash
git clone https://github.com/HydrogenOxideLoveHydrogenPeroxide/peach-cat-pet.git
cd peach-cat-pet
python3 install.py
```

Windows PowerShell：

```powershell
git clone https://github.com/HydrogenOxideLoveHydrogenPeroxide/peach-cat-pet.git
cd peach-cat-pet
py -3 install.py
```

也可以在 [Releases](https://github.com/HydrogenOxideLoveHydrogenPeroxide/peach-cat-pet/releases/latest) 下载 `peach-cat-v1.0.4.zip`，解压后运行安装脚本。

安装完成后，在支持本地宠物的 Codex 客户端中刷新宠物列表或重启，然后选择 **蜜桃猫 / peach-cat**。脚本只安装文件，不自动更改客户端的当前宠物选择。

安装位置：

```text
${CODEX_HOME:-~/.codex}/pets/peach-cat/
├── pet.json
└── spritesheet.png
```

脚本尊重 `CODEX_HOME`，也支持指定路径：

```bash
python3 install.py --codex-home /path/to/your/codex-home
```

如果已经安装同名宠物，默认停止，避免覆盖。更新时使用：

```bash
python3 install.py --replace
```

旧版本会保存到 Codex home 下的 `pet-backups/peach-cat-时间戳-随机后缀/`。卸载时关闭客户端，手动删除 `pets/peach-cat/` 文件夹即可。

## 不使用安装脚本

把仓库内 `pets/peach-cat/` 文件夹复制到自己的 `${CODEX_HOME:-~/.codex}/pets/` 下。这两个文件就是完整的本地宠物包。

## 在 Pets 插件中导入完整 v2 版

下载 [`assets/peach-cat-v2.png`](assets/peach-cat-v2.png)，在支持自定义宠物导入的 Pets 插件会话中附上图片，并发送：

> 请将这张已经完成的 v2 精灵图导入为名为“蜜桃猫”的新宠物并选用。保留现有画面，不重新绘制。先验证精灵图，再完成上传、创建和选用。

导入会创建你自己账号里的宠物，不依赖发布者的宠物 ID。仅把文件复制到本地目录不会将宠物同步到 Pets 账号。

## 两种素材的区别

| 文件 | 尺寸 | 用途 |
| --- | --- | --- |
| `pets/peach-cat/spritesheet.png` | 1536 × 1872 | 本地 Codex 包，9 行、57 个有效帧 |
| `assets/peach-cat-v2.png` | 1536 × 2288 | 完整 v2，11 行、73 个有效帧，含 16 个视线方向 |

本地安装版保留完整 v2 的前 9 行，采用 OpenAI 公开的本地宠物格式；不把 11 行图片直接放进要求 9 行的客户端。完整 v2 原图也一并提供，供支持它的导入器或自己的项目使用。不要缩放精灵图。

动画状态、帧时长与视线顺序见 [`docs/FORMAT.md`](docs/FORMAT.md) 和 [`assets/atlas.json`](assets/atlas.json)。

## 预览与校验

- [完整动画 GIF](previews/all-states.gif) / [MP4](previews/all-states.mp4)
- [全部状态帧](previews/contact-sheet.png) / [16 个视线方向](previews/look-directions.png)
- `SHA256SUMS` 提供两个精灵图及清单的文件校验值。
- 安装脚本会先校验安装素材，再复制文件。
- 运行安装流程测试：`python3 -m unittest discover -s tests -v`。

图像基于用户提供的蜜桃猫参考，由 AI 辅助制作动画。欢迎下载、分享这个仓库并进行个人本地部署；角色名称与原始角色设计的相关权利归原权利人所有。

## English

Peach Cat runs without a laptop and types on a blue laptop while working. Clone this repository and run `python3 install.py` (`py -3 install.py` on Windows), then refresh a compatible Codex client's pet list and select **peach-cat**. Installation uses `CODEX_HOME` or `~/.codex`, requires Python 3.9+, and has no third-party dependencies. `--replace` backs up an existing installation. The local package uses the 9-row format; `assets/peach-cat-v2.png` retains the complete 11-row / 73-frame version for compatible Pets importers.
