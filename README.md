# 伶枫的博客

最简博客系统 —— 通过 GitHub Issues 写博客，Actions 自动构建。

## 🚀 工作原理

1. **写作**：在 [GitHub Issues](../../issues) 写文章（Markdown 格式）
2. **标签**：添加 `blog` 标签才会发布
3. **构建**：Actions 自动抓取 Issues 生成静态页面
4. **部署**：自动发布到 GitHub Pages

## ✍️ 如何写文章

1. 进入 [Issues → New](../../issues/new)
2. 标题作为文章标题
3. 正文使用 Markdown 格式
4. 右侧 Labels 添加 `blog`
5. 可选：添加其他标签作为分类
6. 点击 Submit new issue

等待约 1 分钟，文章自动发布到博客。

## 🏗️ 本地构建（可选）

```bash
# 安装依赖
pip install requests markdown

# 运行构建
python scripts/build.py

# 查看生成的页面
cd dist && python -m http.server 8080
```

## 📁 项目结构

```
.
├── .github/workflows/build.yml  # Actions 工作流
├── scripts/build.py             # 构建脚本
├── templates/                   # HTML 模板
│   ├── index.html              # 首页模板
│   └── post.html               # 文章页模板
├── dist/                        # 生成的静态站点（自动创建）
└── README.md
```

## 🔧 配置

### 1. 创建 blog 标签
访问：https://github.com/ZhiXuanWang/blog/labels
- 创建标签 `blog`

### 2. 配置 GitHub Pages
访问：https://github.com/ZhiXuanWang/blog/settings/pages
- **Source**: Deploy from a branch
- **Branch**: `main` / `docs`
- 点击 Save

### 3. 绑定自定义域名（可选）
1. 创建 `CNAME` 文件写入域名
2. 域名 DNS 添加 CNAME 指向 `ZhiXuanWang.github.io`

## 📝 示例 Issue

```markdown
## 标题

正文内容，支持 **Markdown** 语法。

### 代码示例

```python
print("Hello, World!")
```

- 列表项 1
- 列表项 2

> 引用文本
```

## 🌐 访问博客

- 首页：https://lf.164746.xyz
- GitHub Pages：https://zhixuanwang.github.io/blog/
