"""数据库初始化脚本：预置公司、岗位、题库数据。

在 main.py 启动时自动调用 seed_data()，仅当对应表为空时才插入。
"""
from database import SessionLocal
from models import Company, Job, Question

COMPANIES = [
    {
        "name": "字节跳动",
        "description": "字节跳动是一家全球化的互联网科技公司，旗下产品包括抖音、今日头条等，业务覆盖内容、企业服务、教育等领域。",
        "industry": "互联网/科技",
        "logo_url": "https://example.com/logos/bytedance.png",
    },
    {
        "name": "腾讯",
        "description": "腾讯是中国领先的互联网综合服务提供商，业务涵盖社交、游戏、金融科技、云计算等。",
        "industry": "互联网",
        "logo_url": "https://example.com/logos/tencent.png",
    },
    {
        "name": "阿里巴巴",
        "description": "阿里巴巴集团是全球领先的电子商务与云计算公司，业务包括电商、本地生活、云计算等。",
        "industry": "互联网/电商",
        "logo_url": "https://example.com/logos/alibaba.png",
    },
    {
        "name": "美团",
        "description": "美团是中国领先的生活服务电子商务平台，业务覆盖外卖、到店、酒旅、出行等。",
        "industry": "互联网/本地生活",
        "logo_url": "https://example.com/logos/meituan.png",
    },
    {
        "name": "京东",
        "description": "京东是中国领先的自营式电商企业，业务涵盖零售、物流、金融、科技等。",
        "industry": "互联网/电商/物流",
        "logo_url": "https://example.com/logos/jd.png",
    },
]

JOBS = [
    {
        "company_name": "字节跳动",
        "title": "前端开发工程师",
        "job_type": "前端",
        "requirement": (
            "岗位职责：负责抖音等产品的前端页面开发与性能优化。"
            "任职要求：1. 精通 JavaScript、TypeScript、HTML、CSS；"
            "2. 熟悉 Vue 或 React 框架及其原理；"
            "3. 了解 Webpack、Vite 等构建工具；"
            "4. 熟悉浏览器渲染原理与前端性能优化；"
            "5. 具备良好的沟通能力和团队协作精神。"
        ),
        "salary": "20k-40k",
        "location": "北京",
    },
    {
        "company_name": "字节跳动",
        "title": "后端开发工程师",
        "job_type": "后端",
        "requirement": (
            "岗位职责：负责核心业务系统的后端服务设计与开发。"
            "任职要求：1. 精通 Java 或 Python 语言；"
            "2. 熟悉 Spring 框架、MySQL、Redis；"
            "3. 了解分布式系统、消息队列；"
            "4. 熟悉 Linux 环境与 Git；"
            "5. 有高并发系统开发经验者优先。"
        ),
        "salary": "25k-45k",
        "location": "北京",
    },
    {
        "company_name": "腾讯",
        "title": "算法工程师",
        "job_type": "算法",
        "requirement": (
            "岗位职责：负责推荐/搜索/广告等场景的算法研发。"
            "任职要求：1. 熟悉机器学习、深度学习基础理论；"
            "2. 熟练使用 Python，掌握 TensorFlow 或 PyTorch；"
            "3. 熟悉常见算法与数据结构；"
            "4. 有推荐系统或 NLP 项目经验者优先。"
        ),
        "salary": "30k-60k",
        "location": "深圳",
    },
    {
        "company_name": "腾讯",
        "title": "测试开发工程师",
        "job_type": "测试",
        "requirement": (
            "岗位职责：负责产品测试方案设计与自动化测试建设。"
            "任职要求：1. 熟悉软件测试理论、黑盒与白盒测试方法；"
            "2. 熟练使用 JUnit、Selenium 等测试框架；"
            "3. 掌握 Python 或 Java；"
            "4. 熟悉 Linux 与 SQL；"
            "5. 有自动化测试平台开发经验者优先。"
        ),
        "salary": "20k-40k",
        "location": "深圳",
    },
    {
        "company_name": "阿里巴巴",
        "title": "Java开发工程师",
        "job_type": "后端",
        "requirement": (
            "岗位职责：负责电商核心交易系统的设计与开发。"
            "任职要求：1. 精通 Java，熟悉 JVM 原理与调优；"
            "2. 熟悉 Spring、Spring Cloud 微服务；"
            "3. 熟悉 MySQL、Redis、消息队列；"
            "4. 了解分布式事务与高可用架构；"
            "5. 有大型互联网项目经验者优先。"
        ),
        "salary": "25k-50k",
        "location": "杭州",
    },
    {
        "company_name": "阿里巴巴",
        "title": "前端开发工程师",
        "job_type": "前端",
        "requirement": (
            "岗位职责：负责电商平台前端页面与组件库开发。"
            "任职要求：1. 精通 JavaScript、TypeScript、CSS；"
            "2. 熟悉 Vue 或 React；"
            "3. 了解 Node.js 与前端工程化；"
            "4. 熟悉前端性能优化与浏览器原理；"
            "5. 有跨端开发经验者优先。"
        ),
        "salary": "20k-45k",
        "location": "杭州",
    },
    {
        "company_name": "美团",
        "title": "后端开发工程师",
        "job_type": "后端",
        "requirement": (
            "岗位职责：负责外卖业务后端服务开发与架构优化。"
            "任职要求：1. 精通 Java 或 Python；"
            "2. 熟悉 Spring、MySQL、Redis；"
            "3. 了解微服务、容器化（Docker、Kubernetes）；"
            "4. 熟悉高并发、高可用系统设计；"
            "5. 有分布式系统经验者优先。"
        ),
        "salary": "22k-45k",
        "location": "北京",
    },
    {
        "company_name": "美团",
        "title": "算法工程师",
        "job_type": "算法",
        "requirement": (
            "岗位职责：负责配送调度、推荐等算法研发。"
            "任职要求：1. 熟悉机器学习、运筹优化；"
            "2. 熟练使用 Python 与主流深度学习框架；"
            "3. 熟悉常见算法与数据结构；"
            "4. 有路径规划或推荐系统经验者优先。"
        ),
        "salary": "28k-55k",
        "location": "北京",
    },
    {
        "company_name": "京东",
        "title": "测试开发工程师",
        "job_type": "测试",
        "requirement": (
            "岗位职责：负责电商系统测试与质量保障体系建设。"
            "任职要求：1. 熟悉测试理论、测试用例设计方法；"
            "2. 掌握 Java 或 Python 编写测试脚本；"
            "3. 熟悉接口测试、性能测试工具（如 JMeter）；"
            "4. 熟悉 Linux、SQL；"
            "5. 有持续集成测试经验者优先。"
        ),
        "salary": "18k-35k",
        "location": "北京",
    },
    {
        "company_name": "京东",
        "title": "Java开发工程师",
        "job_type": "后端",
        "requirement": (
            "岗位职责：负责零售与物流系统后端开发。"
            "任职要求：1. 精通 Java，熟悉 JVM；"
            "2. 熟悉 Spring、MyBatis、MySQL、Redis；"
            "3. 了解微服务架构；"
            "4. 熟悉 Linux 与 Git；"
            "5. 有高并发、分布式系统经验者优先。"
        ),
        "salary": "22k-42k",
        "location": "北京",
    },
]

QUESTIONS = [
    # ---------- 公共（5 道） ----------
    {
        "question_type": "选择",
        "category": "公共",
        "title": "HTTP 与 HTTPS 的主要区别是什么？",
        "options": [
            "HTTPS 传输速度更快",
            "HTTPS 在 HTTP 基础上增加了 SSL/TLS 加密层",
            "HTTPS 不需要进行身份认证",
            "HTTP 比 HTTPS 更安全",
        ],
        "answer": "B",
        "analysis": "HTTPS 是在 HTTP 基础上通过 SSL/TLS 协议对数据进行加密传输，确保数据安全性和完整性。",
        "difficulty": "简单",
    },
    {
        "question_type": "选择",
        "category": "公共",
        "title": "关于进程与线程的区别，下列说法正确的是？",
        "options": [
            "线程是资源分配的基本单位，进程是调度的基本单位",
            "进程是资源分配的基本单位，线程是调度的基本单位",
            "进程与线程没有区别",
            "线程之间无法共享内存",
        ],
        "answer": "B",
        "analysis": "进程是操作系统资源分配的基本单位，线程是 CPU 调度的基本单位，同一进程内的线程共享进程的内存空间。",
        "difficulty": "中等",
    },
    {
        "question_type": "简答",
        "category": "公共",
        "title": "请简述你对面向对象编程（OOP）三大特性的理解。",
        "options": None,
        "answer": (
            "面向对象三大特性是封装、继承、多态。封装是把数据和操作数据的方法包装在对象中，隐藏内部细节；"
            "继承是子类复用父类的属性和方法；多态是同一接口对不同对象表现出不同行为，提高代码的可扩展性。"
        ),
        "analysis": "考察对 OOP 基础概念的掌握，答题时需覆盖封装、继承、多态三点并简要说明。",
        "difficulty": "简单",
    },
    {
        "question_type": "简答",
        "category": "公共",
        "title": "请描述一次你解决技术难题的经历，并说明你的排查思路。",
        "options": None,
        "answer": (
            "可从问题现象、定位过程、解决方案、结果验证四个步骤描述。例如：遇到线上接口响应慢，"
            "先通过日志和监控定位瓶颈，再分析是 SQL 慢查询还是代码问题，最终通过加索引和优化查询解决。"
        ),
        "analysis": "重点考察解决问题的结构化思维，建议使用 STAR 法则描述背景、任务、行动、结果。",
        "difficulty": "中等",
    },
    {
        "question_type": "选择",
        "category": "公共",
        "title": "TCP 建立连接需要经过几次握手？",
        "options": ["两次", "三次", "四次", "一次"],
        "answer": "B",
        "analysis": "TCP 建立连接需要三次握手，分别交换 SYN 和 ACK 报文，确保双方收发能力正常。",
        "difficulty": "简单",
    },
    # ---------- Java（5 道） ----------
    {
        "question_type": "选择",
        "category": "Java",
        "title": "Java 中 == 和 equals() 的区别是？",
        "options": [
            "== 比较值，equals 比较引用",
            "== 比较引用，equals 默认比较引用但可被重写用于比较值",
            "两者完全等价",
            "== 只能用于基本类型",
        ],
        "answer": "B",
        "analysis": "== 对于基本类型比较值，对于引用类型比较内存地址；equals 默认比较引用，但 String 等类重写了它以比较内容。",
        "difficulty": "简单",
    },
    {
        "question_type": "选择",
        "category": "Java",
        "title": "HashMap 在 JDK8 中的底层数据结构是？",
        "options": ["数组", "链表", "数组 + 链表 + 红黑树", "二叉树"],
        "answer": "C",
        "analysis": "JDK8 中 HashMap 采用数组 + 链表 + 红黑树，当链表长度超过阈值（8）且数组长度足够时转为红黑树。",
        "difficulty": "中等",
    },
    {
        "question_type": "简答",
        "category": "Java",
        "title": "请简述 JVM 的垃圾回收机制及常见的垃圾回收器。",
        "options": None,
        "answer": (
            "JVM 通过可达性分析判断对象是否存活，回收不可达对象。分代回收将堆分为新生代和老年代，"
            "新生代用 Minor GC、复制算法，老年代用 Major/Full GC、标记整理算法。常见回收器有 Serial、Parallel、CMS、G1 等。"
        ),
        "analysis": "考察 JVM 内存管理和 GC 基础，需提及可达性分析、分代回收及常见回收器。",
        "difficulty": "困难",
    },
    {
        "question_type": "选择",
        "category": "Java",
        "title": "下列关于 String、StringBuilder、StringBuffer 的说法正确的是？",
        "options": [
            "String 是可变的",
            "StringBuilder 是线程安全的",
            "StringBuffer 是线程安全的但性能较低",
            "StringBuilder 和 StringBuffer 都不可变",
        ],
        "answer": "C",
        "analysis": "String 不可变；StringBuilder 非线程安全但性能高；StringBuffer 线程安全（方法加 synchronized）但性能较低。",
        "difficulty": "简单",
    },
    {
        "question_type": "简答",
        "category": "Java",
        "title": "请简述 Java 中实现线程同步的几种方式。",
        "options": None,
        "answer": (
            "可使用 synchronized 关键字（同步方法或同步代码块）、ReentrantLock 显式锁、volatile 保证可见性、"
            "Atomic 原子类以及 CountDownLatch、Semaphore 等并发工具类实现线程同步。"
        ),
        "analysis": "考察多线程并发知识，需列举并简要说明几种同步机制。",
        "difficulty": "中等",
    },
    # ---------- 前端（5 道） ----------
    {
        "question_type": "选择",
        "category": "前端",
        "title": "标准 CSS 盒模型由哪些部分组成？",
        "options": [
            "content、padding、border、margin",
            "仅 content 和 padding",
            "content、border、margin",
            "padding、border、margin",
        ],
        "answer": "A",
        "analysis": "CSS 盒模型由内容（content）、内边距（padding）、边框（border）和外边距（margin）四部分组成。",
        "difficulty": "简单",
    },
    {
        "question_type": "选择",
        "category": "前端",
        "title": "Vue3 响应式系统的核心是基于什么实现的？",
        "options": ["Object.defineProperty", "Proxy", "发布订阅模式", "观察者模式"],
        "answer": "B",
        "analysis": "Vue3 使用 Proxy 实现响应式，相比 Vue2 的 Object.defineProperty 能更好地支持数组和新增属性的响应式。",
        "difficulty": "中等",
    },
    {
        "question_type": "简答",
        "category": "前端",
        "title": "请简述浏览器的事件循环（Event Loop）机制。",
        "options": None,
        "answer": (
            "JS 是单线程的，通过事件循环协调任务执行。同步代码先执行，遇到异步任务（宏任务、微任务）分别入队。"
            "每次宏任务执行完后，会清空所有微任务（如 Promise.then），再进行渲染，然后取下一个宏任务。"
            "宏任务包括 setTimeout、事件回调等，微任务包括 Promise、MutationObserver 等。"
        ),
        "analysis": "考察 JS 运行机制，需说明宏任务与微任务的执行顺序。",
        "difficulty": "困难",
    },
    {
        "question_type": "选择",
        "category": "前端",
        "title": "下列关于 let、const、var 的说法正确的是？",
        "options": [
            "var 具有块级作用域",
            "const 声明的变量可以重新赋值",
            "let 和 const 具有块级作用域",
            "let 声明的变量会提升到全局",
        ],
        "answer": "C",
        "analysis": "let 和 const 具有块级作用域，var 只有函数作用域；const 声明后不可重新赋值。",
        "difficulty": "简单",
    },
    {
        "question_type": "简答",
        "category": "前端",
        "title": "请列举几种前端性能优化的方法。",
        "options": None,
        "answer": (
            "可从资源加载、渲染、网络三方面优化：压缩与合并静态资源、使用 CDN、图片懒加载与 WebP 格式、"
            "代码分割与按需加载、减少重排重绘、使用缓存与 HTTP/2、对首屏进行服务端渲染等。"
        ),
        "analysis": "考察前端性能优化综合能力，回答时尽量分类列举。",
        "difficulty": "中等",
    },
    # ---------- 算法（5 道） ----------
    {
        "question_type": "选择",
        "category": "算法",
        "title": "二分查找的时间复杂度是？",
        "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
        "answer": "B",
        "analysis": "二分查找每次将搜索范围减半，时间复杂度为 O(log n)，要求数据有序。",
        "difficulty": "简单",
    },
    {
        "question_type": "选择",
        "category": "算法",
        "title": "快速排序的平均时间复杂度是？",
        "options": ["O(n)", "O(n log n)", "O(n²)", "O(log n)"],
        "answer": "B",
        "analysis": "快速排序平均时间复杂度为 O(n log n)，最坏情况（已有序且每次选到最值）退化为 O(n²)。",
        "difficulty": "中等",
    },
    {
        "question_type": "简答",
        "category": "算法",
        "title": "请简述动态规划的核心思想及其适用场景。",
        "options": None,
        "answer": (
            "动态规划通过把原问题分解为相互重叠的子问题，保存子问题的解避免重复计算，自底向上求解。"
            "核心要素是最优子结构和状态转移方程。适用于最短路径、背包问题、最长公共子序列等存在重叠子问题和最优子结构的场景。"
        ),
        "analysis": "考察动态规划思想，需说明重叠子问题、最优子结构、状态转移。",
        "difficulty": "中等",
    },
    {
        "question_type": "选择",
        "category": "算法",
        "title": "二叉树的前序遍历顺序是？",
        "options": ["左-根-右", "根-左-右", "左-右-根", "根-右-左"],
        "answer": "B",
        "analysis": "前序遍历顺序为根-左-右；中序为左-根-右；后序为左-右-根。",
        "difficulty": "简单",
    },
    {
        "question_type": "简答",
        "category": "算法",
        "title": "如何判断一个单链表是否存在环？",
        "options": None,
        "answer": (
            "可使用快慢指针法：设置快指针每次走两步、慢指针每次走一步，若二者相遇则说明链表存在环；"
            "若快指针走到末尾（null）则无环。"
        ),
        "analysis": "考察链表与双指针技巧，需说明快慢指针的判断原理。",
        "difficulty": "中等",
    },
    # ---------- 测试（5 道） ----------
    {
        "question_type": "选择",
        "category": "测试",
        "title": "黑盒测试与白盒测试的区别是？",
        "options": [
            "黑盒测试关注内部逻辑，白盒测试关注功能",
            "黑盒测试关注功能不关注内部实现，白盒测试关注内部逻辑结构",
            "两者完全一样",
            "白盒测试不需要了解代码",
        ],
        "answer": "B",
        "analysis": "黑盒测试只关注输入输出与功能表现，不关心内部实现；白盒测试基于代码内部逻辑设计测试用例。",
        "difficulty": "简单",
    },
    {
        "question_type": "选择",
        "category": "测试",
        "title": "以下哪个是 Java 常用的单元测试框架？",
        "options": ["JUnit", "Vue", "Spring Cloud", "Docker"],
        "answer": "A",
        "analysis": "JUnit 是 Java 最常用的单元测试框架，常与 Mockito 等配合使用。",
        "difficulty": "简单",
    },
    {
        "question_type": "简答",
        "category": "测试",
        "title": "请简述你如何为一个登录功能设计测试用例。",
        "options": None,
        "answer": (
            "可覆盖：正常登录（正确账号密码）、异常登录（错误密码、账号不存在、空输入）、"
            "边界（密码长度上下限、特殊字符）、安全（SQL 注入、连续失败锁定）、兼容性（不同浏览器）等维度。"
        ),
        "analysis": "考察测试用例设计能力，回答需覆盖功能、边界、异常、安全等维度。",
        "difficulty": "中等",
    },
    {
        "question_type": "选择",
        "category": "测试",
        "title": "冒烟测试（Smoke Test）的主要目的是？",
        "options": [
            "全面验证所有功能",
            "验证核心功能是否基本可用",
            "测试系统性能",
            "测试界面美观度",
        ],
        "answer": "B",
        "analysis": "冒烟测试是在正式测试前对核心功能进行快速验证，确认系统基本可用后再进行详细测试。",
        "difficulty": "简单",
    },
    {
        "question_type": "简答",
        "category": "测试",
        "title": "请简述自动化测试的优缺点。",
        "options": None,
        "answer": (
            "优点：可重复执行、节省回归测试时间、提高测试效率、覆盖人工难以执行的场景。"
            "缺点：前期编写维护成本高、对 UI 变更敏感、无法完全替代人工探索性测试、存在误报漏报。"
        ),
        "analysis": "考察对自动化测试的理解，需客观说明优点与缺点。",
        "difficulty": "中等",
    },
    # ---------- 产品（5 道） ----------
    {
        "question_type": "选择",
        "category": "产品",
        "title": "PRD（产品需求文档）的主要作用是？",
        "options": [
            "记录代码实现细节",
            "定义产品需求、功能与验收标准，作为团队协作的依据",
            "管理公司财务",
            "招聘员工",
        ],
        "answer": "B",
        "analysis": "PRD 是描述产品需求、功能、交互和验收标准的文档，是产品、设计、开发、测试沟通协作的依据。",
        "difficulty": "简单",
    },
    {
        "question_type": "简答",
        "category": "产品",
        "title": "请简述你做用户调研的常用方法。",
        "options": None,
        "answer": (
            "常用方法包括问卷调查、用户访谈、用户观察、数据分析（埋点/漏斗分析）、可用性测试、竞品分析等。"
            "调研前明确目标与用户画像，调研后归纳需求与痛点。"
        ),
        "analysis": "考察用户研究方法，需列举方法并说明调研流程。",
        "difficulty": "中等",
    },
    {
        "question_type": "选择",
        "category": "产品",
        "title": "MVP（最小可行产品）的含义是？",
        "options": [
            "功能最全的版本",
            "用最小的成本验证核心假设的可行产品",
            "最终正式版",
            "只有界面的原型",
        ],
        "answer": "B",
        "analysis": "MVP 是用最小成本快速开发出具备核心功能的产品，用于验证市场需求和假设，再根据反馈迭代。",
        "difficulty": "简单",
    },
    {
        "question_type": "简答",
        "category": "产品",
        "title": "请简述如何评估需求优先级。",
        "options": None,
        "answer": (
            "可用 KANO 模型、RICE（触达、影响、信心、工作量）评分、四象限法（重要紧急）等方法，"
            "结合用户价值、业务价值、开发成本、紧急程度综合排序，优先做高价值低成本的需求。"
        ),
        "analysis": "考察需求优先级评估方法，需列举具体模型或维度。",
        "difficulty": "中等",
    },
    {
        "question_type": "选择",
        "category": "产品",
        "title": "A/B 测试主要用于？",
        "options": [
            "比较两个版本在同一指标上的表现",
            "修复代码 bug",
            "生成测试报告",
            "部署服务器",
        ],
        "answer": "A",
        "analysis": "A/B 测试将用户随机分为两组，分别展示不同版本，通过数据对比判断哪个版本效果更好。",
        "difficulty": "中等",
    },
]


def seed_data():
    """向空表插入种子数据。"""
    db = SessionLocal()
    try:
        if db.query(Company).count() == 0:
            for c in COMPANIES:
                db.add(Company(**c))
            db.commit()

        if db.query(Job).count() == 0:
            companies = {c.name: c for c in db.query(Company).all()}
            for j in JOBS:
                company = companies[j["company_name"]]
                db.add(
                    Job(
                        company_id=company.id,
                        title=j["title"],
                        job_type=j["job_type"],
                        requirement=j["requirement"],
                        salary=j["salary"],
                        location=j["location"],
                    )
                )
            db.commit()

        if db.query(Question).count() == 0:
            for q in QUESTIONS:
                db.add(
                    Question(
                        question_type=q["question_type"],
                        category=q["category"],
                        title=q["title"],
                        options=q["options"],
                        answer=q["answer"],
                        analysis=q["analysis"],
                        difficulty=q["difficulty"],
                    )
                )
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    from database import init_db

    init_db()
    seed_data()
    print("种子数据初始化完成")
