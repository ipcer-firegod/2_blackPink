#
## 跟着写过程中的问题
- 大部分的放在有问题的代码头上了，一些不好归位的放在这里：

缩放调整似乎有问题，不知道后面是否会设置

## 关于 `.shortcut li a:hover` 和 `.shortcut li:hover` 的区别
简短结论先说：  
1) `.shortcut li a:hover` 是直接选中并改变链接（a）本身的样式——这是最明确且兼容的做法。  
2) 只写 `li:hover` 只会改变 li 元素的样式，并不会自动改变 a 的样式（除非 a 没有自己颜色设置并从 li 继承 color）。  
3) 如果想在鼠标悬停 li 时改变内部 a 的样式，应写成 `.shortcut li:hover a { … }`。

详细说明（含示例与建议）：

- 选择器意义不同
  - `.shortcut li a:hover`：当鼠标悬停在 a 元素上时，直接改变 a 的样式（最常用、直观、准确）。
  - `.shortcut li:hover`：当鼠标悬停在 li 上时，改变 li 的样式（背景、边框、内边距等），并不会直接改变子元素 a 的样式，除非该子元素的属性是“继承”自父元素且没有被子元素覆盖。

- 关于继承（为什么有时候看起来 `li:hover` 能改变 a）
  - CSS 属性 `color` 是会继承的 —— 如果 `a` 没有自己定义 color，那么 li:hover 设置的 color 会被 a 继承，链接颜色会变。
  - 但在你的代码里，有 `.shortcut li a { color: #fff; }`，a 显式定义了 color，这会覆盖继承，因此即使 `li:hover` 改变了 color，也不会影响已经显式设置 color 的 a。所以在此场景下必须明确选择 a（比如通过 `li:hover a` 或 `a:hover`）来改变颜色。

- 两种常见的正确写法（效果相似但语义不同）
  - 当你希望“鼠标在链接上时变色”：
    ```css
    .shortcut li a { color: #fff; }
    .shortcut li a:hover,
    .shortcut li a:focus { color: #5EB69C; } /* 加上 :focus 支持键盘访问 */
    ```
  - 当你希望“鼠标在 li 任意位置（包括 li 的 padding）悬停时，链接也变色”：
    ```css
    .shortcut li:hover a { color: #5EB69C; }
    .shortcut li:focus-within a { color: #5EB69C; } /* 支持键盘 focus 时也生效 */
    ```
    注意：写成 `.shortcut li:hover a` 比单写 `li:hover` 更明确地改变 a。

- **关于可点击区域与用户体验（实践建议）**
  - 如果想让整个 li 区域都能触发 link 的 hover（更大的命中区），最好把 a 设为块级并填满 li：
    ```css
    .shortcut li a { display: block; padding: 0 12px; height: 52px; line-height: 52px; }
    /* 这样 a 的 hover 区域等同于 li 的可见区域，使用 a:hover 就足够了 */
    ```
  - 同时务必添加键盘可访问样式：
    ```css
    .shortcut li a:focus,
    .shortcut li a:focus-visible { outline: 2px solid #5EB69C; }
    ```

- 关于移动端
  - 移动端没有 hover，需考虑 `:active` 或用 JS 处理交互（或直接用明显的视觉样式避免依赖 hover）。

- 小结 / 推荐做法
  - 核心规则：如果你要改变链接的颜色或文字样式，直接写选择器针对 `a`（`a:hover` 或 `li:hover a`）是最可靠的。  
  - 最佳实践：让 `a` 占满可点击区域（display:block + padding/height），并同时实现 `:hover`、`:focus`/`:focus-visible`、`:active` 的样式，保证鼠标与键盘/触屏用户都有良好体验。