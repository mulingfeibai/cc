# AI面试系统 - 项目规范

## 项目描述
一个基于AI的面试辅助系统，帮助用户进行模拟面试、技能评估和面试准备。目前只实现PC端。

## 技术栈
- 前端：Vue3 + TypeScript + Vue Router + Pinia + Element Plus
- 后端：Python + FastAPI + SQLAlchemy
- 数据库：SQLite（开发阶段用，简单免安装）
- AI能力：DeepSeek大模型

## 架构要求
- 前后端分离，前端代码放 frontend/ 文件夹，后端代码放 backend/ 文件夹
- 后端严格分层：router → service → repository

## 版本管理
- 使用Git进行代码版本管理
- 创建 .gitignore 文件，排除 node_modules、__pycache__、.idea、.vscode 等
