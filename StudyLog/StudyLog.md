# StudyLog
StudyLog，学习日志，主要记录和学习有关的。

## ai笔记有关
- origin文件夹中是让Copilot完成的复习笔记，有许多幻觉。在看望下面两个文件夹的笔记后，可以稍微看一下。
- full、review文件夹是让豆包完成的详细的学习笔记、复习笔记，内容更为准确。主要就看这两个文件夹中的笔记。

ai完成网页的问题
- 第一章和后面其他章节的标题、按钮样式、页面布局不一样。**已解决**
- “我的练习”模块没有做好。其中的几个功能都不能正常使用。**解决部分，“添加练习”功能未实现**
- 各个css、js文件都是内联的，不能复用。**已解决**
- 网页从vscode中打开会比较卡顿，在浏览器中不会。**目前来看是vscode插件特性，无法解决**


# 知识
## emmet缩写
emmet缩写、各种快捷写法！
:
w100+h100
.className+.className2
ul>li*3


## 杂项
1. 
```css
display: flex;
/* 横向排列，有时带有： */
/* 两端对齐/垂直居中/换行/间距 */
justify-content: space-between;
align-items: center;
flex-wrap: wrap;
gap: 10px;
```
2. 子绝父相

<!-- 详见第三章代码的 29-网格布局-网格填充方式以及图片缩放.html -->
3. 设置圆角后需要隐藏溢出内容
    /* 1. box给了圆角，还需要使用hidden切割掉 */

4. img底部白边解决？
    /* 2. 图片下面有空隙，因为图片是基线对齐的。 */
    /* 修改：block，再根据情况修改w、h为100% */


图片缩放：
fill:   图片完全填充容器，不保持宽高比，可能会变形。
contain:保持宽高比，图片完全显示在容器内，可能会有空白。
cover:  保持宽高比，图片裁剪后完全覆盖容器，可能会被裁剪。
```css
    /* 2. 图片下面有空隙，因为图片是基线对齐的。 */
    /* 修改：block，再根据情况修改w、h为100% */
    .box img {
      display: block;
      width: 100%;
      height: 100%;

      /* 控制图片如何适应容器。fill、contain、cover */
      /* object-fit: contain; */
      object-fit: cover;

      /* 控制图片在容器中的位置。top left。center常与cover搭配使用 */
      object-position: center;
    }
```

5. transition有关
谁变化，谁加transition。比如li:hover，需要给li加transition。


6. 改li中的文字颜色
文字可以直接改，但li中的a也需要拿出来修改，比如：
```css
  /* 第一个li中的文字改成橙色 */
  .service-bd li:first-child,
  .service-bd li:first-child a {
    color: #ff5000;
  }

  .service-bd li a:hover {
    color: #ff5000;
  }
```

7. 第三章练习中的 _18：
```css  
/* 1. */
  /* before是行内元素，设置宽高没用。（之前是改为块级元素） */
  /* 但是加了定位 position: absolute; ，则可以直接给宽度和高度！ */

/* 2.flex布局在一行上时，会压缩，需要使用flex: 0 0 px; */
  .box ul li {
    /* 怎么让图片初步布局成那样的？
    这里使用200px后，还需要对img也设置为100%才行。(让img和li一样大) */
    /* width: 200px; 这样会导致压缩 */
    /* 不拉伸，不收缩，初始200px */
    flex: 0 0 200px;
  }
  .box ul li img {
    width: 100%;
  }
```

8. 
li中a需要设置为块级元素，才能撑满整个li，从而让hover效果生效。

9.  
input中的placeholder颜色设置：（需要使用伪类）
```css
.search input::placeholder {
  font-size: 16px;
  color: pink;
}
```

10. ul>li>a...
   <!-- a包所有的。a不能包li，因为ul后面只应该有li
  a是行内元素。需要转为block，增加高 -->

11. small标签
small标签表示小号字体，一般用于注释、版权信息等。它会使文本变小，但不会改变语义。
变多小？
可以通过CSS设置small标签的字体大小，例如：
```css
small {
  font-size: 12px;
}
```
如果不设置，浏览器会使用默认的小号字体大小，通常比正常文本小一些。
<!-- 自己设置，不然就是默认的80% -->
可能是这样

12. li、a定位疑问 （详情见 第三章练习中的**_16的 StudyLog、li_a.html**）
```css
/* 需要使用 a 来定位，是a的hover，不是li的 */
.shortcut li a:hover {
  color: #5EB69C;
  background-color: #fff;
}
```

## 杂项2
1. 绝对定位与块级元素
对于普通元素（如 <a> 标签），如果要设置宽高，必须显式设置 display: block
对于绝对定位的伪元素，由于position: absolute已经使其表现得像块级元素，所以不需要显式设置 display: block
不过需要注意的是，为了代码的可读性和明确性，即使在绝对定位的情况下，有时也会显式添加 display: block，这样其他开发者能更清楚地理解代码意图。
**在第四章的StudyLog中有更详细的笔记**

## 定位布局问题
要想把一个元素放在某个位置，应该怎么做？更广泛的方案。
这是对“放置”的总结。
<!-- ! -->

## 外接笔记
在第四章的练习中，有一个笔记，记录了章节的一些问题



## 代码片段
（从头开始看太过用时，以后遇见值得记录的再记下来）

### li横向排列
要让li横向排列，可以给ul加上：
```css
ul {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```
### CSS初始化

### 居中
见第二章练习中的 _居中.html

### 文本省略
```css
  /* 单行文本溢出省略 */
  overflow: hidden;
  text-overflow: ellipsis;
  /* white-space: nowrap; */
  /* 多行 */
  -webkit-line-clamp: 2;
  display: -webkit-box;
  -webkit-box-orient: vertical;
```

### 扩散边框效果
```css
/* 使用阴影效果实现扩散边框效果，避免抖动 */
.banner .circleDot li:hover{
  
  box-shadow: 0 0 0 4px rgba(255, 255, 255, .5);
  background-color: #fff;
}
/* 使用outline */
/* .banner .circleDot li:hover {
  outline: 4px solid rgba(255, 255, 255, .5);
  background-color: #fff;
} */
```
outline是什么？
outline是元素的轮廓线，类似于border，但不会占用空间。可以用来突出显示元素，比如在hover时添加outline效果。
怎么用？
```css
.element {
  outline: 2px solid red; /* 设置轮廓线的宽度、样式和颜色 */
}
```
### ul、li常见横向初始化
```css
.box-bd ul {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.box-bd ul li {
  width: 304px;
  height: 404px;
  background-color: #EEF9F4;
  text-align: center;
}
.box-bd ul li a {
  display: block;
  height: 100%;
}
.box-bd ul li img {
  width: 304px;
  height: 304px;
}
```

### 盒子思想
cloHead 盒子中有两个子盒子，左边的h2和右边的cloHead-right盒子。通过flex布局让它们横向排列，并且左右对齐。
cloHead-right 盒子中只有两部分子盒子，左边的ul和右边的a标签。通过flex布局调整它们。

布局：
```html
  <div class="cloHead">
    <h2>服饰</h2>
    <div class="cloHead-right">
      <ul>
        <li><a href="#">热门</a></li>
        <li><a href="#">女装</a></li>
        <li><a href="#">奢侈品</a></li>
        <li><a href="#">裤装</a></li>
        <li><a href="#">衬衫</a></li>
        <li><a href="#">T恤</a></li>
      </ul>
      <a href="#">查看更多 <i class="iconfont icon-arrow-right-bold"></i><a>
    </div>
  </div>
```
调整：
```css
.cloHead {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 102px;
  padding-top: 10px;
  background-color: #fff;
}
.cloHead-right {
  display: flex;
  gap: 65px;
}
```


### Grid 响应式布局（核心实战）
通过 `repeat(auto-fill, minmax(210px, 1fr))` 实现“列数随容器宽度自动调整”，无需媒体查询：
```css
.container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); /* 列宽最小210px，自动填充列数 */
  gap: 16px;
}
```
- **效果**：容器变宽时自动增加列数，变窄时自动减少列数，适配所有屏幕尺寸。

### grid 跨列跨行
```css
  .box .item:first-child {
    /* 1 / 3 1号线到3号线 */
    /* grid-column: 1 / 3;
    grid-row: 1 / 3; */
    /* span 2是跨2个单元格的意思 */
    grid-column: 1 / span 2;
    grid-row: 1 / span 2;
    height: auto;
  }
```

### 多栏布局
```css
    .box {
      column-count: 5;
      column-gap: 20px;
      column-rule: 1px dashed red;
      max-width: 1200px;
      border: 1px solid red;
      margin: 30px auto;
    }

    .box .item {
      height: 150px;
      background-color: pink;
      margin-bottom: 20px;
      /* 不允许盒子被切割 */
      break-inside: avoid-column;
      -webkit-column-break-inside: avoid;
    }
```

### svg描边动画
```css
    .box .scroll svg {
      width: 3858px;
      stroke-dasharray: 3858px;
      stroke-dashoffset: 3858px;
      animation: move 20s linear forwards;
    }
    
    @keyframes move {
      0% {
        stroke-dashoffset: 3858px;
      }

      100% {
        stroke-dashoffset: 0px;
      }
    }
```

###
  /* 添加倒影 */
  -webkit-box-reflect: below 1px linear-gradient(transparent, #0002);

### 点阵
```css
/* background-image: radial-gradient(transparent 1px, #fff 1px); 
- 这是最有趣的部分，创建了一个径向渐变背景：
<!--!从中心开始1像素内是透明色(transparent) 
<!--!从1像素处开始到外面都是白色(#fff)(中间那个点是透明的，向外就是白色)
这种效果创造了一种类似点阵的纹理图案

background-size: 4px 4px; - 将上述背景图案的重复单元设置为4x4像素大小，使点状图案按此规格重复排列

backdrop-filter: saturate(50%) blur(4px); - 这是现代CSS的一个强大特性：
saturate(50%) - 降低背后元素50%的色彩饱和度
blur(4px) - 对元素背后的内容应用4像素的高斯模糊
这使得该元素后面的内容看起来更柔和、朦胧，产生磨砂玻璃般的效果 */
    .navbar2 {
      top: 130px;
      border-bottom: 1px solid #ccc;
      background-image: radial-gradient(transparent 1px, pink 1px);
      background-size: 10px 10px;
      backdrop-filter: saturate(50%) blur(4px);
    }
```



### 动画时间线
```css
      animation: scrollbar 2s linear forwards;
      /* 让动画绑定时间线 */
      animation-timeline: scroll();


      animation: anim 1s linear forwards;
      /* 绑定视图时间线 */
      animation-timeline: view();
```









# 想法
## 网页适配
网页适配、缩放问题。比如，怎么在一半的屏幕上合理显示内容。
网页整体缩放。只改变大小，不改变布局、比例、位置。看上去和原来一样，只是变小了而已。（似乎不太好完成，通过简单的方法）
之前尝试过，一直没有达到我预想中的效果，暂时搁置。
（见 adapt.html。预想即可在vscode中的一半屏幕显示完整网页）

## 脚手架
是什么？似乎后面学到vue就会学到、用到了。

## 笔记有关
除了让ai生成的笔记外，我自己写的笔记有些杂乱了。日志可以按天来写，但是学习笔记我感觉还是应该分开写，每个章节写一个、学到哪里写到哪里，最后再合在一起或者放在一起。

**前面的笔记先不管了，从第六章开始，笔记写在每章当中。之复习的时候后再来全部整理一下吧。**




