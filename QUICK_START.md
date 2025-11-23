# ⚡ 快速上手指南

## 最快5分钟开始使用！

### 📋 准备工作（2分钟）

1. **获取免费API密钥**
   - 访问 https://openweathermap.org/api
   - 点击 "Sign Up" 注册账号
   - 在 "API keys" 标签页复制您的密钥

### 🚀 三种使用方式

---

## 方式一：独立使用（最简单）⭐

**适合：** 快速演示、单页应用

### 步骤：

1. 打开 `weather-widget.html` 文件
2. 找到第253行，替换API密钥：
   ```javascript
   const API_KEY = '粘贴您的密钥到这里';
   ```
3. 双击文件在浏览器中打开
4. 完成！🎉

**无需API密钥？** 组件会使用模拟数据演示，您可以直接打开查看效果！

---

## 方式二：iframe嵌入（推荐）⭐⭐⭐

**适合：** 嵌入现有网站、博客、应用

### 步骤：

1. 将 `weather-widget.html` 上传到您的服务器
2. 在需要显示天气的页面添加：
   ```html
   <iframe 
       src="https://your-domain.com/weather-widget.html" 
       width="450px" 
       height="800px" 
       frameborder="0">
   </iframe>
   ```
3. 完成！

**示例：** 打开 `integration-example.html` 查看效果

---

## 方式三：JS模块集成（开发者推荐）⭐⭐⭐

**适合：** 复杂项目、需要编程控制

### 步骤：

1. 在HTML中添加容器：
   ```html
   <div id="my-weather"></div>
   ```

2. 引入JavaScript：
   ```html
   <script src="weather-widget.js"></script>
   ```

3. 初始化组件：
   ```html
   <script>
       const widget = new WeatherWidget('my-weather', 'YOUR_API_KEY');
       widget.init('Beijing');
   </script>
   ```

4. 完成！

**示例：** 打开 `widget-usage-example.html` 查看效果

---

## 🎨 主要功能

- ✅ **搜索城市** - 输入任意城市名查询天气
- ✅ **自动定位** - 点击📍按钮使用当前位置
- ✅ **单位切换** - 点击温度在°C和°F之间切换
- ✅ **详细数据** - 湿度、风速、气压、能见度等
- ✅ **响应式** - 手机、平板、电脑完美适配

---

## 🔧 常见问题

### Q: 为什么显示"模拟数据"？
**A:** 您还没有配置API密钥。获取并配置后即可显示真实数据。

### Q: 城市搜索不到？
**A:** 
- 确保API密钥已正确配置
- 尝试使用英文城市名（如 "Beijing" 而不是 "北京"）
- 检查网络连接

### Q: 如何修改默认城市？
**A:** 
```javascript
// HTML版本：修改第519行
fetchWeather('Shanghai'); // 改为您想要的城市

// JS模块版本：
widget.init('Shanghai');
```

### Q: 如何修改颜色？
**A:** 在CSS中找到 `background: linear-gradient(...)` 并修改颜色值

### Q: 能否离线使用？
**A:** 组件本身可以离线运行，但获取实时天气数据需要网络连接

---

## 📱 本地测试

如果直接打开HTML文件遇到问题，可以启动本地服务器：

### Python 3:
```bash
python3 -m http.server 8080
```

### Python 2:
```bash
python -m SimpleHTTPServer 8080
```

### Node.js (需要安装 http-server):
```bash
npx http-server -p 8080
```

然后访问：http://localhost:8080/weather-widget.html

---

## 🎯 下一步

- 📖 阅读完整文档：`README.md`
- 🔍 查看集成示例：`integration-example.html`
- 💻 查看JS模块示例：`widget-usage-example.html`
- 🎨 自定义样式和功能

---

## 💡 提示

- **免费API额度充足**：OpenWeatherMap免费版每天可调用1,000,000次
- **不要泄露密钥**：不要将包含API密钥的代码提交到公开仓库
- **响应速度**：首次加载可能需要1-2秒获取数据
- **缓存数据**：OpenWeatherMap数据每10分钟更新一次

---

## 🆘 需要帮助？

- 📧 提交Issue：https://github.com/yourusername/weather-widget/issues
- 📚 官方文档：README.md
- 🌐 API文档：https://openweathermap.org/api

---

**开发时间：** 2025-11-23  
**版本：** v1.0.0  
**许可证：** MIT
