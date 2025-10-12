(function() { 
    const getQueryParam = (param) => {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }
    const renderMarkdown = async (markdown_file) => {
        const markdownFilePath = `../posts/${markdown_file}`;
        const response = await fetch(markdownFilePath);
        if (!response.ok) {
            throw new Error('Failed to load markdown file');
        }
        const markdown = await response.text();
        const md = window.markdownit();
        return md.render(markdown);
    }

    const renderSingleBlog = async (blog) => {
        const blogContainer = document.getElementById('blog-content');
        document.title = blog.title;
        blogContainer.querySelector('.blog-date').textContent = blog.date;
        blogContainer.querySelector('.blog-author').textContent = blog.author;
        blogContainer.querySelector('#blog-markdown').innerHTML = await renderMarkdown(blog.md_file);
    }  

    async function loadBlog() {
        try {
            const blogsInfo = [];
            const response = await fetch('../data/blogs.json');
            if (!response.ok) {
                throw new Error('load blogs response was not ok');
            }
            const data = await response.json();
            blogsInfo.push(...data);
            const blogId = getQueryParam('blog_id');
            console.log('Find Blog ID:', blogId);
            const blog = blogsInfo.find(b => b.id === blogId);
            if (blog) {
                renderSingleBlog(blog);
            } else {
                console.error('Blog not found');
            }
        } catch (error) {
            console.error('Error loading blogs:', error);
        }
    }

// 主程序
    loadBlog();


})();