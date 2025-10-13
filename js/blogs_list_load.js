(function () {
    const blogsList = document.getElementById('blogs-list');
    const blogsInfo = []; // 这里存放博客数据
    const template = document.getElementById('blog-card-template');
    // 渲染博客列表
    function renderBlogs() {
        if (!blogsInfo.length) {
            blogItem.querySelector('.blog-list-item-title').textContent = '无法加载博客';
            blogItem.querySelector('.blog-list-item-brief-summary').textContent = '请稍后再试';
            blogItem.querySelector('.blog-list-item-meta').innerHTML = '';
            blogsList.appendChild(blogItem);
            return;
        }
        blogsList.innerHTML = ''; // 清空现有内容
        blogsInfo.forEach(blog => {
            const blogItem = template.content.cloneNode(true);
            blogItem.querySelector('.blog-list-item-title').textContent = blog.title;
            blogItem.querySelector('.blog-list-item-meta').querySelector('.blog-list-item-date').textContent = blog.date;
            blogItem.querySelector('.blog-list-item-meta').querySelector('.blog-list-item-author').textContent = blog.author;
            blogItem.querySelector('.blog-list-item-brief-summary').textContent = blog.brief_summary;
            blogItem.querySelector('.blog-list-item-link').setAttribute('href', `single_blog.html?blog_id=${blog.id}`);
            blogsList.appendChild(blogItem);
        });
    }

    // 从 JSON 文件加载博客数据
    async function loadBlogsFile() {
        try {
            const response = await fetch('../data/blogs.json');
            if (!response.ok) {
                throw new Error('load blogs response was not ok');
            }
            const data = await response.json();
            blogsInfo.push(...data);
            renderBlogs();
        } catch (error) {
            console.error('Error loading blogs:', error);
        }
    }

    // 初始化
    function init() {
        loadBlogsFile();
    }
    init();
})();