# CSS3 核心知识复习笔记（基于学习笔记整理）
## 一、CSS 基础认知
### 核心要点
- **作用**：控制网页视觉表现（样式美化、布局定位、动画交互），与HTML分工：HTML负责结构，CSS负责样式。
- **样式表分类**：
  - 内联样式：写在`style`属性中，仅作用于当前标签，耦合度高（不推荐）。
  - 内部样式：写在`<head>`的`<style>`中，作用于当前页面，适合小型项目。
  - 外部样式：单独`.css`文件，通过`<link>`引入，作用于整个网站，完全分离（推荐）。


## 二、CSS 选择器（核心：选对元素）
### 1. 基础选择器
| 类型         | 语法       | 匹配范围                | 关键特点                          |
|--------------|------------|-------------------------|-----------------------------------|
| 类型选择器   | `div { }`  | 所有指定标签            | 复用性低，易冲突                  |
| 类选择器     | `.class { }` | 含对应class的元素       | 可重复使用（核心，推荐），多类名共存 |
| ID选择器     | `#id { }`  | 唯一含对应id的元素      | 页面唯一，主要配合JS交互          |
| 通配符选择器 | `* { }`    | 所有元素                | 用于全局重置（清除默认边距）      |

### 2. 伪类选择器（`:`，状态/位置特殊元素）
- **状态伪类**：
  - 链接伪类：`a:link`（未访问）、`a:visited`（已访问）、`a:hover`（悬停）、`a:active`（点击），需遵循**LVHA顺序**。
  - 交互伪类：`:hover`（任意元素悬停）、`:focus`（表单元素获焦）。

### 3. 伪元素选择器（`::`，元素特定部分）
| 伪元素        | 作用                  | 关键注意                          |
|---------------|-----------------------|-----------------------------------|
| `::first-line` | 选文本首行            | -                                 |
| `::first-letter` | 选文本首字母          | -                                 |
| `::placeholder` | 选输入框占位符        | -                                 |
| `::before`    | 元素内最前插入虚拟内容 | 需`content`属性（必填，空内容用`""`），默认内联元素 |
| `::after`     | 元素内最后插入虚拟内容 | 同上                              |

### 4. 分组选择器（并集选择器）
- 语法：`选择器1, 选择器2 { 样式 }`，实现多元素共享样式，减少冗余。


## 三、CSS 三大特性（解决样式冲突）
### 1. 继承性
- 可继承：与文字相关（`color`、`font-family`、`line-height`等）。
- 不可继承：盒模型相关（`width`、`margin`、`border`等）。
- 特殊：浏览器默认样式（如`<h1>`加粗、`<a>`下划线）需单独覆盖。

### 2. 层叠性
- 优先级相等时，**后定义的样式覆盖先定义的**（“谁后写，听谁的”）。

### 3. 优先级（权重比拼）
- 权重规则：4位层级值（不进位），顺序：`!important`（最高）> 内联样式(1,0,0,0) > ID选择器(0,1,0,0) > 类/属性/伪类(0,0,1,0) > 标签/伪元素(0,0,0,1) > 通配符/继承(0,0,0,0)。
- 慎用`!important`，破坏优先级逻辑。


## 四、盒子模型（布局核心）
### 1. 组成（从内到外）
- 内容区（content，`width`/`height`控制）→ 内边距（padding）→ 边框（border）→ 外边距（margin）。

### 2. 尺寸计算（`box-sizing`）
| 属性值         | 计算方式                          | 推荐场景                  |
|----------------|-----------------------------------|---------------------------|
| `content-box`  | 实际宽 = width + padding + border | 无需精确控制尺寸          |
| `border-box`   | 实际宽 = width（含padding和border） | 需精确控制尺寸（推荐全局用） |

- 全局设置（推荐）：
  ```css
  * { box-sizing: border-box; margin: 0; padding: 0; }
  ```


## 五、CSS 文本样式
### 1. 字体样式核心属性
| 属性               | 作用                  | 常用值示例                  |
|--------------------|-----------------------|-----------------------------|
| `color`            | 文字颜色              | `#333`、`rgba(255,103,0,0.5)` |
| `font-family`      | 字体                  | `"Microsoft YaHei", sans-serif` |
| `font-size`        | 字号                  | `14px`、`16px`              |
| `font-weight`      | 粗细                  | `400`（正常）、`700`（加粗） |
| `text-decoration`  | 文本装饰              | `none`（去下划线）、`line-through`（删除线） |

### 2. `font` 简写属性
- 语法：`font: font-style font-weight font-size/line-height font-family`（**必须含`font-size`和`font-family`**）。
- 示例：`font: 14px/1.5 "Microsoft YaHei", Arial, sans-serif`。

### 3. 多行文字溢出省略号（WebKit内核）
```css
.multi-ellipsis {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3; /* 显示3行 */
  overflow: hidden;
  text-overflow: ellipsis;
}
```


## 六、CSS 背景与阴影
### 1. 背景属性
- 复合写法（推荐顺序）：`background: 颜色 图片 重复 固定 位置/尺寸`。
- 示例：`background: #f5f5f5 url(banner.jpg) no-repeat fixed center/cover`。

### 2. 背景渐变
- **线性渐变**：`linear-gradient(方向, 颜色1 位置, 颜色2 位置)`。
  - 示例：`linear-gradient(to right, #ff6700, #4ecdc4)`（水平橙到蓝）。
- **文字渐变**：
  ```css
  .text-gradient {
    background: linear-gradient(to right, #ff6700, #4ecdc4);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  ```


## 七、样式初始化（统一浏览器差异）
- **小型项目**：简单重置（通配符清边距、去列表样式、去链接下划线等）。
- **中大型项目**：用`Normalize.css`（保留有用默认样式，兼容性更好），通过`<link>`引入。


## 八、字体图标（优化图标加载）
- **优势**：矢量缩放、样式灵活（改`color`/`font-size`）、减少请求。
- **常用库**：Font Awesome、阿里iconfont、Bootstrap Icons。
- **使用步骤**（以iconfont为例）：下载图标→引入`iconfont.css`→用`<i class="iconfont 图标类名"></i>`调用。


## 九、核心技巧速记
1. 伪元素`::before`/`::after`必写`content`属性，默认内联元素。
2. 链接伪类需按LVHA顺序写（`:link`→`:visited`→`:hover`→`:active`）。
3. 全局盒模型推荐`border-box`，避免尺寸计算问题。
4. 文字渐变需配合`background-clip: text`和透明文字。
5. 多行溢出省略号仅支持WebKit内核，依赖`-webkit-line-clamp`。


