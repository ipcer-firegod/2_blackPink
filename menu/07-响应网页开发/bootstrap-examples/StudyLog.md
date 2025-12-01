# 以前有关笔记
到现在为止，我所使用过的bs类有：

<!-- layout布局，bootstrap响应式布局的关键  -->
## Layout
--Containers
  <div class="container">
    <div class="row align-items-center justify-content-between">
      <!-- ! 理解：1.首先，默认有1列；2.当>=xl时，一列占2/12，即一行可以又六列 -->
       <!-- 可以删去col-xl-2，则默认为1列 。即一行row中，默认是按照一列来排列的  -->
      <div class="item col-xl-2 col-lg-3">1</div>
      <div class="item col-xl-2 col-lg-3">2</div>
    </div>
  </div>

    <div class="container">
    <div class="row">
      <!-- 分别代表列宽由大屏到小屏的占比：2/12(六列),3/12,4/12,6/12，12/12(一列)是默认存在的 -->
      <!-- ! 0px 576px 768px 992px 1200px <=  xs  sm  md  lg xl  -->
      <div class="item col-xl-1 col-lg-3 col-md-4 col-sm-6">1</div>
      <div class="item col-xl-1 col-lg-3 col-md-4 col-sm-6">2</div>
      <div class="item col-xl-1 col-lg-3 col-md-4 col-sm-6">3</div>
      <div class="item col-xl-1 col-lg-3 col-md-4 col-sm-6">4</div>
      <div class="item col-xl-1 col-lg-3 col-md-4 col-sm-6">5</div>
      <div class="item col-xl-1 col-lg-3 col-md-4 col-sm-6">6</div>
    </div>
    <br>
    <!-- ?容器中如果有两个row，在每一row响应变化时不能合适改变，所以只应该有一个row吗？ -->
    <!-- 我的理解是，行就是行+列了。row中的列盒子会响应变化，一个row中列盒子变化，则会从一行到多行。 -->
  </div>

  
<!-- 在class类中添加的参数： 样式类 -->

## Content
--Typography
  display-4（标题放大）

## Helpers
--Position
  fixed-top

## Utilities
--Background （-color）
  bg-primary bg-info
  bg-light bg-dark
  bg-white bg-black  

--Border
  border
  border-top-0 
  border-white border-dark
  border border-3
  rounded rounded-top （圆角）

--Color
  text-white text-secondary text-body text-light （文字颜色）

--Display
  d-none 
  d-md-block
  d-block
  d-flex 
（仅隐藏在MD上	.d-md-none .d-lg-block；
仅在 MD 上可见	.d-none .d-md-block .d-lg-none
0px 576px 768px 992px 1200px <=  xs  sm  md  lg xl ）

--Flex
  justify-content-center 
  align-items-center

--Position
  position-relative
  (position-absolute top-0 start-0 translate-middle)


--Sizing
  w-100（100%）

--Spacing
  mb-5 mb-lg-4 mx-3
  p-2 py-1 pe-0 

--Text
  text-center text-md-end
  text-nowrap
  
  （字体大小、粗细、斜体）
  fs-6
  fw-bold fw-semibold fw-light
  fst-italic

  lh-1 lh-sm lh-base lh-lg （行高）

  text-decoration-none （链接下划线）


<!-- 在class外添加的参数： 暗色主题 -->

## Customize
--Color modes
  data-bs-theme="dark"


<!-- 单独的组件 card -->

## Components
--Cards （cards有关内容较多，此处暂时只给出初始例子）
<div class="card" style="width: 18rem;">
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">Card title</h5>
    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card’s content.</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>


<!-- 输入框 -->

## Forms
--Input group （类似的，输入框有关内容也比较多，此处例子是Button Addons的第二个）
<div class="input-group mb-3">
  <input type="text" class="form-control" placeholder="Recipient’s username" aria-label="Recipient’s username" aria-describedby="button-addon2">
  <button class="btn btn-outline-secondary" type="button" id="button-addon2">Button</button>
</div>


# 占位